#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_kit11_executor.py - testes OFFLINE do executor KIT-11F (positivos, falha, cancelamento,
CONTROLES NEGATIVOS, rollback/encerramento e regressoes F1-F9 da revisao independente KIT-11R).

O QUE ESTE ARQUIVO PROVA (e o que NAO prova)
--------------------------------------------
Exercita `executor.executar()` com fontes de estado STUB (nunca o jogo):
  * POSITIVO observacao e positivo ATIVO (autorizacao separada + perfil/save de teste);
  * POSITIVO de encerramento SO do PID proprio; FALHA por TIMEOUT e CANCELAMENTO;
  * CONTROLES NEGATIVOS: versao/tipo/condicao/campo executavel/acao ativa proibida, ativo sem
    autorizacao separada, perfil/save nao verificados, frente ocupada;
  * REGRESSOES F1-F9 (cada achado da revisao KIT-11R tem um teste que o pega): permissao negada
    que nao le, override string que nao vira True, `requer_acao` nao booleano, satisfeito estrito,
    JSON invalido estruturado, timeout obrigatorio/finito, polling limitado ao deadline, frente
    obrigatoria e atomica, PID externo nunca fechado, liveness desconhecida que nao forca,
    cleanup que preserva o veredito, rollback que preserva preexistentes, excecoes de setup/
    rollback que liberam a frente, cancelamento na ultima leitura e CLI com exits honestos;
  * ROLLBACK EXATO (arquivo criado some; arquivo modificado volta byte a byte).
**Stub testa o EXECUTOR; stub NAO prova runtime.** Navegacao real/clique fisico: KIT-14.

Convencao do repositorio: `RESULTADO|<PASSOU|REPROVOU>|<nome>|<detalhe>`, exit 0 = todos PASSOU,
1 = algum REPROVOU, 2 = nao conseguiu rodar.

ISCA (`--isca`) MUTA O FONTE
----------------------------
`--isca` NAO e um `AssertionError` incondicional: ele aplica MUTACOES SELETIVAS por substituicao
textual no fonte do executor, roda a suite contra cada mutante e EXIGE que o teste-regressao
correspondente REPROVE. Mutante que passa verde = a suite e um carimbo para aquele guard -> a
isca REPROVA (exit 1). Assim a isca prova DISCRIMINACAO, nao um defeito plantado a mao.

USO
---
    python tools/automacao/kit11/test_kit11_executor.py
    python tools/automacao/kit11/test_kit11_executor.py --isca
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import traceback
from unittest.mock import patch

AQUI = os.path.dirname(os.path.abspath(__file__))
AUTOMACAO = os.path.dirname(AQUI)
REPO = os.path.dirname(os.path.dirname(AUTOMACAO))       # .../tools/automacao -> repo
sys.path.insert(0, os.path.join(REPO, "tools", "testes"))
import arcabouco as arc  # noqa: E402

CAMINHO_EXECUTOR = os.path.join(AQUI, "executor.py")

META = {
    "nome": "kit11-executor",
    "categoria": "pura",
    "requer": [],
    "descricao": ("executor deterministico KIT-11F: espera menu/tela/condicao com timeout FINITO "
                  "e diagnostico, permissoes tipadas e separadas, frente unica OBRIGATORIA e "
                  "atomica, cancelamento/rollback que preservam o veredito e encerramento so da "
                  "instancia comprovadamente criada; falha fechada em config/desconhecido/versao"),
}

TIMEOUT_CURTO = 0.3          # FINITO: o contrato nao aceita timeout ausente (F3)


def _carregar(caminho=None, fonte_texto=None, nome="kit11_executor"):
    caminho = caminho or CAMINHO_EXECUTOR
    if fonte_texto is None:
        with open(caminho, encoding="utf-8") as fh:
            fonte_texto = fh.read()
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    modulo.__dict__["__file__"] = caminho
    exec(compile(fonte_texto, caminho, "exec"), modulo.__dict__)
    return modulo


EX = _carregar()
ESQ = EX.ESQUEMA_EXECUTOR


# ------------------------------------------------------------------ stubs ------
class FonteStub(object):
    """Fonte de estado de TESTE. Nao toca em jogo: responde do mapa e roda `ao_ler` por chave."""

    def __init__(self, mapa=None, ao_ler=None):
        self.mapa = dict(mapa or {})
        self.ao_ler = ao_ler or (lambda tipo, alvo: None)
        self.chamadas = []

    def ler(self, tipo, alvo):
        chave = "%s:%s" % (tipo, alvo)
        self.chamadas.append(chave)
        self.ao_ler(tipo, alvo)
        valor = self.mapa.get(chave)
        if isinstance(valor, dict):
            return valor
        if valor is True:
            return {"satisfeito": True, "observado": True, "diagnostico": ""}
        return {"satisfeito": False, "observado": valor,
                "diagnostico": "estado '%s' nao satisfeito" % chave}


class FonteSuja(object):
    """Fonte que devolve `satisfeito` NAO booleano: o executor NAO pode promover verde (F2)."""

    def __init__(self, valor):
        self.valor = valor

    def ler(self, tipo, alvo):
        return {"satisfeito": self.valor, "observado": "texto"}


class RelogioFalso(object):
    def __init__(self, passo=0.1):
        self.t = 0.0
        self.passo = passo

    def __call__(self):
        self.t += self.passo
        return self.t


def plano(passos, *, modo="observacao", ativa=False, obs=True, versao=1, esquema=ESQ):
    return {"esquema": esquema, "versao": versao, "modo": modo, "nome": "cenario-teste",
            "autorizacao": {"observacao_autorizada": obs, "ativa_autorizada": ativa},
            "passos": passos}


def passo(nome, tipo="menu", alvo=None, timeout_s=TIMEOUT_CURTO, requer_acao=False, **extra):
    # alvo por DEFAULT casado com MAPA_OK (menu->MainMenu, tela->Inventory).
    padrao = {"menu": "MainMenu", "tela": "Inventory"}.get(tipo, nome)
    p = {"nome": nome, "tipo": tipo, "alvo": alvo if alvo is not None else padrao,
         "timeout_s": timeout_s, "requer_acao": requer_acao}
    p.update(extra)
    return p


MAPA_OK = {
    "menu:MainMenu": True,
    "tela:Inventory": True,
    "condicao:jogo_aberto": True,
    "condicao:perfil_de_teste": {"satisfeito": True, "observado": "perfil-teste"},
    "condicao:save_de_teste": {"satisfeito": True, "observado": "save-teste"},
}


def _tmp(prefixo):
    return tempfile.mkdtemp(prefix=prefixo)


def _atuais(pids):
    return lambda imagem: next(pids)


def _roda_cli(argv):
    """Chama `EX.main` em processo (mesmo modulo, inclusive mutado) e devolve o exit code."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return EX.main(argv)


def _cli_arquivos(tmp, *, obs, passos):
    caminho_plano = os.path.join(tmp, "cli-plano.json")
    caminho_estado = os.path.join(tmp, "cli-estado.json")
    with open(caminho_plano, "w", encoding="utf-8") as fh:
        json.dump(plano(passos, obs=obs), fh)
    with open(caminho_estado, "w", encoding="utf-8") as fh:
        json.dump({"estado": {"menu:MainMenu": True}}, fh)
    return caminho_plano, caminho_estado


# ------------------------------------------------------------------ testes -----
def t_positivo_observacao():
    res = EX.executar(plano([passo("ver-menu"), passo("ver-tela", "tela", "Inventory")]),
                      FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_OBSERVADO, "observacao so observa")
    arc.igual(res["permissoes"]["permite_agir"], False, "observacao NAO concede acao")
    arc.igual(res["estado"], EX.CONCLUIDO, "todos os passos satisfeitos")
    arc.igual([p["estado"] for p in res["passos"]], ["SATISFEITO", "SATISFEITO"], "passos")


def t_positivo_ativo():
    res = EX.executar(plano([passo("ver-menu"),
                             passo("agir", "condicao", "save_de_teste", requer_acao=True)],
                            modo="ativo", ativa=True),
                      FonteStub(MAPA_OK), perfil_de_teste="perfil-teste",
                      save_de_teste="save-teste")
    arc.igual(res["veredito"], EX.VEREDITO_PASSOU, "ativo autorizado + ambiente de teste")
    arc.igual(res["permissoes"]["permite_agir"], True, "acao permitida")
    arc.igual(res["ambiente"]["ok"], True, "perfil/save de teste verificados")


def t_falha_timeout():
    p = passo("espera-impossivel", "condicao", "jogo_aberto", timeout_s=0.3)
    res = EX.executar(plano([p]), FonteStub({}), relogio=RelogioFalso(), dormir=lambda s: None)
    arc.igual(res["estado"], EX.TIMEOUT, "timeout por passo")
    arc.igual(res["veredito"], EX.VEREDITO_FALHOU, "timeout = FALHOU")
    arc.exigir("nao encontrou" in res["passos"][-1]["diagnostico"], "diagnostico do timeout")
    arc.exigir(res["passos"][-1]["tentativas"] > 1, "tentou mais de uma vez")


def t_cancelamento():
    estado = {"cancelar": False}

    def ao_ler(tipo, alvo):
        if alvo == "Inventory":
            estado["cancelar"] = True

    fonte = FonteStub({"menu:MainMenu": True, "tela:Inventory": False}, ao_ler=ao_ler)
    res = EX.executar(plano([passo("ver-menu"), passo("ver-tela", "tela", "Inventory")]),
                      fonte, cancelado=lambda: estado["cancelar"])
    arc.igual(res["veredito"], EX.VEREDITO_CANCELADO, "cancelamento")
    arc.exigir("cancelado" in (res["motivo"] or ""), "motivo nomeia o cancelamento")


def t_neg_versao_incompativel():
    res = EX.executar(plano([passo("ver-menu")], versao=99), FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "versao incompativel falha fechado")
    arc.exigir("versao incompativel" in res["motivo"], "motivo nomeia a versao")
    arc.igual(res["passos"], [], "nao executa passo nenhum")


def t_neg_tipo_e_condicao_desconhecidos():
    res = EX.executar(plano([passo("x", "clicar", "Botao")]), FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "tipo desconhecido falha fechado")
    arc.exigir("tipo desconhecido" in res["motivo"], "motivo nomeia o tipo")

    res = EX.executar(plano([passo("y", "condicao", "condicao_inventada")]), FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "condicao desconhecida falha fechado")
    arc.exigir("condicao desconhecida" in res["motivo"], "motivo nomeia a condicao")


def t_neg_campo_executavel():
    p = passo("x")
    p["argv"] = ["cmd", "/c", "echo oi"]
    res = EX.executar(plano([p]), FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "comando arbitrario falha fechado")
    arc.exigir("campo executavel" in res["motivo"], "motivo nomeia o campo executavel")


def t_neg_acao_ativa_proibida_controle_acesso():
    """F9: a trava dura do controle_acesso e REUSADA, nao apenas citada."""
    for chave in sorted(EX.controle_acesso().ACOES_ATIVAS):
        p = passo("x")
        p[chave] = "nao-pode"
        res = EX.executar(plano([p]), FonteStub(MAPA_OK))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO,
                  "acao ativa %r recusada pelo controle_acesso" % chave)
        arc.exigir("controle de acesso" in res["motivo"] or "acao ativa" in res["motivo"],
                   "motivo nomeia a trava")


def t_neg_ativo_sem_autorizacao_separada():
    res = EX.executar(plano([passo("agir", "condicao", "jogo_aberto", requer_acao=True)],
                            modo="ativo", ativa=False, obs=True),
                      FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "ativo sem autorizacao separada")
    arc.exigir("autorizacao SEPARADA" in res["motivo"] or "ativa_autorizada" in res["motivo"],
               "motivo nomeia a autorizacao separada")
    arc.igual(res["passos"], [], "nao executa passo ativo algum")


def t_neg_perfil_save_de_teste():
    p = passo("agir", "condicao", "save_de_teste", requer_acao=True)
    res = EX.executar(plano([p], modo="ativo", ativa=True), FonteStub(MAPA_OK))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "sem perfil/save declarados falha fechado")

    res = EX.executar(plano([p], modo="ativo", ativa=True), FonteStub(MAPA_OK),
                      perfil_de_teste="perfil-teste", save_de_teste="outro-save")
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "save de teste divergente falha fechado")
    arc.exigir(any("save_de_teste" in m for m in res["diagnostico"]), "diagnostico do save")


def t_neg_frente_unica():
    tmp = _tmp("kit11-frente-")
    try:
        lock = os.path.join(tmp, "frente.lock")
        with open(lock, "w", encoding="utf-8") as fh:
            json.dump({"pid": 4321, "token": "outro"}, fh)
        frente = EX.FrenteUnica(lock, pid=1, vivo=lambda p: True)
        try:
            frente.obter()
            raise arc.Falhou("frente viva deveria RECUSAR")
        except EX.FrenteOcupada:
            pass
        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK),
                          frente=EX.FrenteUnica(lock, pid=1, vivo=lambda p: True))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "frente ocupada falha fechado")
        # pid NAO mensuravel -> tambem RECUSA (fail-closed)
        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK),
                          frente=EX.FrenteUnica(lock, pid=1, vivo=lambda p: None))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "pid nao mensuravel falha fechado")
        # lock morto: pode retomar
        frente = EX.FrenteUnica(lock, pid=1, vivo=lambda p: False)
        info = frente.obter()
        arc.exigir(info["ok"], "lock morto pode ser retomado")
        arc.exigir(frente.liberar(), "libera o proprio lock")
        arc.exigir(not os.path.exists(lock), "lock removido na liberacao")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_neg_frente_obrigatoria():
    """F4: a API NAO pode executar sem frente (frente opcional era o buraco)."""
    res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK))
    arc.exigir(res["frente"] is not None, "execucao sem frente nao pode ser bypassada")
    arc.exigir(res["frente"].get("ok") is True, "a frente padrao foi adquirida e e nossa")


def t_neg_frente_atomica_concorrente():
    """F4: dois chamadores concorrentes NAO podem ganhar o mesmo lock."""
    tmp = _tmp("kit11-race-")
    try:
        alvo = os.path.join(tmp, "front.lock")
        original = os.path.exists
        barreira = threading.Barrier(2)
        sucessos = []
        erros = []

        def exists_sincronizado(caminho):
            valor = original(caminho)
            if str(caminho) == alvo:
                try:
                    barreira.wait(timeout=3)
                except threading.BrokenBarrierError:
                    pass
            return valor

        def adquirir(token):
            try:
                sucessos.append(EX.FrenteUnica(alvo, vivo=lambda _: True, token=token).obter())
            except Exception as erro:                       # noqa: BLE001
                erros.append(type(erro).__name__)

        with patch.object(EX.os.path, "exists", exists_sincronizado):
            threads = [threading.Thread(target=adquirir, args=(str(i),)) for i in range(2)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=5)
        arc.exigir(not any(t.is_alive() for t in threads), "harness de corrida terminou")
        arc.igual(len(sucessos), 1, "dois callers aceitos no mesmo lock (race): %r %r"
                  % (sucessos, erros))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------ F1: permissoes ---------
def t_neg_obs_nao_autorizada_nao_le():
    src = FonteStub(MAPA_OK)
    res = EX.executar(plano([passo("ver-menu")], obs=False), src)
    arc.igual(src.chamadas, [], "observacao negada NAO le a fonte")
    arc.igual(res["veredito"], EX.VEREDITO_NAO_EXERCITADO, "nada executado -> NAO_EXERCITADO")
    arc.igual(res["frente"], None, "observacao negada nem adquire frente")


def t_neg_override_string_nao_vira_true():
    res = EX.executar(plano([passo("ver-menu")], modo="ativo"), FonteStub(MAPA_OK),
                      autorizacao={"observacao_autorizada": True, "ativa_autorizada": "false"},
                      perfil_de_teste="perfil-teste", save_de_teste="save-teste")
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO,
              "override string 'false' NAO pode virar autorizacao (coercao booleana)")


def t_neg_requer_acao_nao_booleano():
    p = plano([passo("agir", "condicao", "jogo_aberto", requer_acao="false")],
              modo="ativo", ativa=True)
    res = EX.executar(p, FonteStub(MAPA_OK), perfil_de_teste="perfil-teste",
                      save_de_teste="save-teste")
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "requer_acao nao booleano recusado")
    arc.igual(res["passos"], [], "nenhum passo executado")


# ------------------------------------------------------ F2: fonte --------------
def t_neg_satisfeito_string_nao_vira_verde():
    res = EX.executar(plano([passo("ver-menu")]), FonteSuja("false"))
    arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "satisfeito nao booleano NAO promove verde")


def t_neg_fonte_arquivo_string_nao_vira_verde():
    tmp = _tmp("kit11-satisfeito-")
    try:
        caminho = os.path.join(tmp, "state.json")
        with open(caminho, "w", encoding="utf-8") as fh:
            fh.write('{"estado":{"menu:MainMenu":{"satisfeito":"false"}}}')
        res = EX.executar(plano([passo("ver-menu")]), EX.FonteDeArquivo(caminho))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO,
                  "satisfeito='false' em arquivo NAO satisfaz")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_neg_json_quebrado_estruturado():
    tmp = _tmp("kit11-json-")
    try:
        caminho = os.path.join(tmp, "state.json")
        with open(caminho, "w", encoding="utf-8") as fh:
            fh.write("{broken")
        res = EX.executar(plano([passo("ver-menu")]), EX.FonteDeArquivo(caminho))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "JSON invalido vira falha ESTRUTURADA")
        arc.exigir(any("ilegivel" in d for d in res["diagnostico"]), "diagnostico do JSON")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------ F3: tempo --------------
def t_neg_timeout_obrigatorio_finito():
    casos = [("ausente", None), ("None", None), ("nan", float("nan")),
             ("inf", float("inf")), ("zero", 0), ("negativo", -1)]
    for rotulo, valor in casos:
        p = plano([passo("ver-menu")])
        if rotulo == "ausente":
            p["passos"][0].pop("timeout_s")
        else:
            p["passos"][0]["timeout_s"] = valor
        res = EX.executar(p, FonteStub(MAPA_OK))
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO,
                  "timeout %s (%r) tem de RECUSAR" % (rotulo, valor))


def t_neg_poll_limitado_ao_deadline():
    dormidas = []
    relogio = [0.0]

    def dormir(segundos):
        dormidas.append(segundos)
        relogio[0] += segundos

    res = EX.executar(plano([passo("sem-menu", "condicao", "jogo_aberto", timeout_s=0.05)]),
                      FonteStub({}), intervalo_s=5.0, dormir=dormir,
                      relogio=lambda: relogio[0])
    arc.igual(res["veredito"], EX.VEREDITO_FALHOU, "poll sem satisfazer vira FALHOU")
    arc.exigir(dormidas and max(dormidas) <= 0.05,
               "sleep tem de ser limitado ao restante do deadline: %r" % dormidas)


# ------------------------------------------------------ F5/F7: encerramento ----
def t_pos_encerra_so_o_pid_proprio():
    chamadas = []
    res = EX.executar(plano([passo("ver-menu")], modo="ativo", ativa=True), FonteStub(MAPA_OK),
                      perfil_de_teste="perfil-teste", save_de_teste="save-teste",
                      imagem="StolenRealm.exe", pids_medir=_atuais(iter([{100}, {100, 200}])),
                      pids_criados=[200], pid_vivo=lambda pid: False,
                      executar_cmd=lambda argv: chamadas.append(argv))
    plano_enc = res["encerramento"]["plano"]
    arc.igual(plano_enc["pids"], [200], "encerra SO o PID que ESTA execucao criou")
    arc.exigir(chamadas and all("200" in " ".join(argv) for argv in chamadas),
               "nenhum comando no PID externo (100)")


def t_neg_pid_externo_nunca_fechado():
    """F5: delta de PIDs NAO e propriedade — PID que nasceu durante a observacao nao morre."""
    chamadas = []
    res = EX.executar(plano([passo("ver-menu")], modo="ativo", ativa=True), FonteStub(MAPA_OK),
                      perfil_de_teste="perfil-teste", save_de_teste="save-teste",
                      imagem="StolenRealm.exe", pids_medir=_atuais(iter([{100}, {100, 200}])),
                      pid_vivo=lambda pid: False, executar_cmd=lambda argv: chamadas.append(argv))
    arc.igual(chamadas, [], "nenhum comando: o executor NAO criou o PID 200")
    arc.igual(res["encerramento"]["plano"]["pids"], [], "plano sem PIDs proprios")


def t_neg_encerramento_sem_autorizacao_de_acao():
    """F5: observacao NAO autorizada ainda fechava a instancia — agora nao fecha nada."""
    chamadas = []
    res = EX.executar(plano([passo("ver-menu")], obs=False), FonteStub(MAPA_OK),
                      imagem="StolenRealm.exe", pids_medir=_atuais(iter([{100}, {100, 200}])),
                      pids_criados=[200], pid_vivo=lambda pid: False,
                      executar_cmd=lambda argv: chamadas.append(argv))
    arc.igual(chamadas, [], "observacao negada nao encerra nada")
    arc.igual(res["veredito"], EX.VEREDITO_NAO_EXERCITADO, "nada executado")


def t_neg_liveness_desconhecida_nao_forca():
    """F5: liveness None NAO escala para taskkill."""
    chamadas = []
    EX.executar(plano([passo("ver-menu")], modo="ativo", ativa=True), FonteStub(MAPA_OK),
                perfil_de_teste="perfil-teste", save_de_teste="save-teste",
                imagem="StolenRealm.exe", pids_medir=_atuais(iter([{100}, {100, 200}])),
                pids_criados=[200], pid_vivo=lambda pid: None,
                executar_cmd=lambda argv: chamadas.append(argv))
    arc.exigir(not any(argv and argv[0] == "taskkill" for argv in chamadas),
               "liveness desconhecida nunca forca: %r" % chamadas)
    arc.igual(chamadas, [], "sem medicao -> nenhum comando")


def t_neg_sem_medicao_recusa_encerramento():
    chamadas = []
    res = EX.executar(plano([passo("ver-menu")], modo="ativo", ativa=True), FonteStub(MAPA_OK),
                      perfil_de_teste="perfil-teste", save_de_teste="save-teste",
                      imagem="StolenRealm.exe", pids_medir=lambda imagem: None,
                      pids_criados=[200], pid_vivo=lambda pid: False,
                      executar_cmd=lambda argv: chamadas.append(argv))
    arc.igual(res["encerramento"]["plano"]["recusado"], True, "sem medicao -> recusa")
    arc.igual(res["encerramento"]["acoes"], [], "recusa nao executa nada")


# ------------------------------------------------------ F6/F7: rollback --------
def t_neg_cleanup_preserva_veredito():
    """F6: o rollback do `finally` NAO pode trocar OBSERVADO/FALHOU/CANCELADO."""
    tmp = _tmp("kit11-cleanup-")
    try:
        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK),
                          area_trabalho=tmp, relativos=["nao_existe.txt"],
                          dir_backup=os.path.join(tmp, "bk"))
        arc.igual(res["veredito"], EX.VEREDITO_OBSERVADO, "cleanup preserva OBSERVADO")
        arc.exigir(EX.ROLLBACK not in res["estados"], "ROLLBACK nao e estado terminal")

        res = EX.executar(plano([passo("sem-menu", "condicao", "jogo_aberto", timeout_s=0.02)]),
                          FonteStub({}), area_trabalho=tmp, relativos=["nao_existe.txt"],
                          dir_backup=os.path.join(tmp, "bk2"))
        arc.igual(res["veredito"], EX.VEREDITO_FALHOU, "cleanup preserva FALHOU (timeout)")

        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK),
                          cancelado=lambda: True, area_trabalho=tmp, relativos=["nao_existe.txt"],
                          dir_backup=os.path.join(tmp, "bk3"))
        arc.igual(res["veredito"], EX.VEREDITO_CANCELADO, "cleanup preserva CANCELADO")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_neg_rollback_preserva_preexistentes():
    """F7: diretorio vazio preexistente e dir_backup do chamador NAO podem ser removidos."""
    tmp = _tmp("kit11-preserva-")
    try:
        vazio = os.path.join(tmp, "empty")
        os.makedirs(vazio)
        backup = os.path.join(tmp, "backup")
        os.makedirs(backup)
        sentinela = os.path.join(backup, "owner.txt")
        with open(sentinela, "w", encoding="utf-8") as fh:
            fh.write("preexistente")
        criado = os.path.join(vazio, "new.txt")

        fonte = FonteStub({"menu:MainMenu": True},
                          ao_ler=lambda *_: open(criado, "w", encoding="utf-8").write("novo"))
        EX.executar(plano([passo("ver-menu")]), fonte, area_trabalho=tmp,
                    relativos=["empty/new.txt"], dir_backup=backup)
        arc.exigir(os.path.isdir(vazio), "diretorio vazio preexistente preservado")
        arc.exigir(not os.path.exists(criado), "arquivo criado nesta execucao removido")
        arc.exigir(os.path.exists(sentinela), "dir_backup do chamador NAO foi apagado")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_rollback_exato():
    tmp = _tmp("kit11-rb-")
    try:
        rel = "CriadoPelaRodada.txt"
        mod = "Modificado.txt"
        with open(os.path.join(tmp, mod), "w", encoding="utf-8") as fh:
            fh.write("ANTES")

        def ao_ler(tipo, alvo):
            with open(os.path.join(tmp, rel), "w", encoding="utf-8") as fh:
                fh.write("novo")
            with open(os.path.join(tmp, mod), "w", encoding="utf-8") as fh:
                fh.write("DEPOIS")

        fonte = FonteStub({"menu:MainMenu": True}, ao_ler=ao_ler)
        res = EX.executar(plano([passo("ver-menu")]), fonte,
                          area_trabalho=tmp, relativos=[rel, mod],
                          dir_backup=os.path.join(tmp, ".bk"))
        rb = res["rollback"]["plano"]
        arc.igual(rb["criados"], [rel], "arquivo criado volta pelo rollback")
        arc.exigir(not os.path.exists(os.path.join(tmp, rel)), "arquivo criado removido")
        with open(os.path.join(tmp, mod), encoding="utf-8") as fh:
            arc.igual(fh.read(), "ANTES", "arquivo modificado restaurado byte a byte")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------ F8: excecoes -----------
def _com_coletor_falso(patch_nome, patch_valor):
    """Devolve um coletor controlado e troca `EX.coletor` para que o executor use ELE."""
    col = EX.coletor()
    antigo_metodo = getattr(col, patch_nome)
    setattr(col, patch_nome, patch_valor)
    antigo_coletor = EX.coletor
    EX.coletor = lambda: col
    return col, antigo_metodo, antigo_coletor


def _restaura_coletor(col, nome, antigo_metodo, antigo_coletor):
    setattr(col, nome, antigo_metodo)
    EX.coletor = antigo_coletor


def t_neg_setup_excecao_libera_frente():
    tmp = _tmp("kit11-setup-")
    lock = os.path.join(tmp, "frente.lock")
    frente = EX.FrenteUnica(lock, vivo=lambda _: True)

    def explode(*_a, **_k):
        raise OSError("sandbox injetou falha no snapshot")

    col, antigo_metodo, antigo_coletor = _com_coletor_falso("snapshot_arquivos", explode)
    try:
        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK), frente=frente,
                          area_trabalho=tmp, relativos=["x.txt"],
                          dir_backup=os.path.join(tmp, "bk"))
        arc.exigir(not os.path.exists(lock), "excecao de setup NAO pode deixar a frente presa")
        arc.igual(res["veredito"], EX.VEREDITO_FECHADO, "excecao de setup vira falha estruturada")
        arc.exigir(res["cleanup_erros"], "erro de setup registrado, nao escondido")
    finally:
        _restaura_coletor(col, "snapshot_arquivos", antigo_metodo, antigo_coletor)
        shutil.rmtree(tmp, ignore_errors=True)


def t_neg_rollback_excecao_libera_frente():
    tmp = _tmp("kit11-rollback-")
    lock = os.path.join(tmp, "frente.lock")
    frente = EX.FrenteUnica(lock, vivo=lambda _: True)
    with open(os.path.join(tmp, "x.txt"), "w", encoding="utf-8") as fh:
        fh.write("antes")

    def explode(*_a, **_k):
        raise OSError("sandbox injetou falha no rollback")

    col, antigo_metodo, antigo_coletor = _com_coletor_falso("executar_rollback", explode)
    try:
        res = EX.executar(plano([passo("ver-menu")]), FonteStub(MAPA_OK), frente=frente,
                          area_trabalho=tmp, relativos=["x.txt"],
                          dir_backup=os.path.join(tmp, "bk"))
        arc.exigir(not os.path.exists(lock),
                   "excecao de rollback NAO pode pular a liberacao da frente")
        arc.igual(res["veredito"], EX.VEREDITO_OBSERVADO,
                  "excecao de rollback nao troca o veredito terminal")
        arc.exigir(any("rollback" in e for e in res["cleanup_erros"]),
                   "erro de rollback registrado")
    finally:
        _restaura_coletor(col, "executar_rollback", antigo_metodo, antigo_coletor)
        shutil.rmtree(tmp, ignore_errors=True)


def t_neg_cancelamento_na_ultima_leitura():
    estado = {"cancelar": False}
    fonte = FonteStub({"menu:MainMenu": True}, ao_ler=lambda *_: estado.update(cancelar=True))
    res = EX.executar(plano([passo("ver-menu")]), fonte, cancelado=lambda: estado["cancelar"])
    arc.igual(res["veredito"], EX.VEREDITO_CANCELADO,
              "cancelamento lido na ultima leitura NAO pode ser ignorado")


# ------------------------------------------------------ F9: CLI/exits ----------
def t_cli_exits_e_saida_em_arquivo():
    """F1/F9: exits honestos (0/1/2) e veredito lido do ARQUIVO, nao da mensagem."""
    tmp = _tmp("kit11-cli-")
    try:
        # (a) observacao negada -> NAO_EXERCITADO / exit 2
        caminho_plano, caminho_estado = _cli_arquivos(tmp, obs=False, passos=[passo("ver-menu")])
        saida = os.path.join(tmp, "r1.json")
        codigo = _roda_cli(["--plano", caminho_plano, "--estado", caminho_estado,
                            "--saida", saida])
        arc.igual(codigo, 2, "observacao negada -> exit 2")
        with open(saida, encoding="utf-8") as fh:
            doc = json.load(fh)
        arc.igual(doc["veredito"], EX.VEREDITO_NAO_EXERCITADO,
                  "veredito lido do arquivo de saida")
        arc.igual(doc["passos"], [], "nada executado")

        # (b) observacao autorizada e satisfeita -> OBSERVADO / exit 0
        caminho_plano, caminho_estado = _cli_arquivos(tmp, obs=True, passos=[passo("ver-menu")])
        codigo = _roda_cli(["--plano", caminho_plano, "--estado", caminho_estado])
        arc.igual(codigo, 0, "observacao satisfeita -> exit 0")

        # (c) timeout -> FALHOU / exit 1
        caminho_plano, caminho_estado = _cli_arquivos(
            tmp, obs=True, passos=[passo("sem-menu", "condicao", "jogo_aberto", timeout_s=0.02)])
        codigo = _roda_cli(["--plano", caminho_plano, "--estado", caminho_estado])
        arc.igual(codigo, 1, "timeout -> exit 1")

        # (d) plano ilegivel -> exit 2 (nada executado)
        ruim = os.path.join(tmp, "ruim.json")
        with open(ruim, "w", encoding="utf-8") as fh:
            fh.write("{nao-json")
        codigo = _roda_cli(["--plano", ruim, "--estado", caminho_estado])
        arc.igual(codigo, 2, "plano ilegivel -> exit 2")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


TESTS = [
    ("positivo-observacao", t_positivo_observacao),
    ("positivo-ativo", t_positivo_ativo),
    ("falha-timeout", t_falha_timeout),
    ("cancelamento", t_cancelamento),
    ("neg-versao-incompativel", t_neg_versao_incompativel),
    ("neg-tipo-condicao-desconhecidos", t_neg_tipo_e_condicao_desconhecidos),
    ("neg-campo-executavel", t_neg_campo_executavel),
    ("neg-acao-ativa-proibida-controle-acesso", t_neg_acao_ativa_proibida_controle_acesso),
    ("neg-ativo-sem-autorizacao-separada", t_neg_ativo_sem_autorizacao_separada),
    ("neg-perfil-save-de-teste", t_neg_perfil_save_de_teste),
    ("neg-frente-unica", t_neg_frente_unica),
    ("neg-frente-obrigatoria", t_neg_frente_obrigatoria),
    ("neg-frente-atomica-concorrente", t_neg_frente_atomica_concorrente),
    ("neg-obs-nao-autorizada-nao-le", t_neg_obs_nao_autorizada_nao_le),
    ("neg-override-string-nao-vira-true", t_neg_override_string_nao_vira_true),
    ("neg-requer-acao-nao-booleano", t_neg_requer_acao_nao_booleano),
    ("neg-satisfeito-string-nao-vira-verde", t_neg_satisfeito_string_nao_vira_verde),
    ("neg-fonte-arquivo-string-nao-vira-verde", t_neg_fonte_arquivo_string_nao_vira_verde),
    ("neg-json-quebrado-estruturado", t_neg_json_quebrado_estruturado),
    ("neg-timeout-obrigatorio-finito", t_neg_timeout_obrigatorio_finito),
    ("neg-poll-limitado-ao-deadline", t_neg_poll_limitado_ao_deadline),
    ("pos-encerra-so-o-proprio", t_pos_encerra_so_o_pid_proprio),
    ("neg-pid-externo-nunca-fechado", t_neg_pid_externo_nunca_fechado),
    ("neg-encerramento-sem-autorizacao-de-acao", t_neg_encerramento_sem_autorizacao_de_acao),
    ("neg-liveness-desconhecida-nao-forca", t_neg_liveness_desconhecida_nao_forca),
    ("neg-sem-medicao-recusa-encerramento", t_neg_sem_medicao_recusa_encerramento),
    ("neg-cleanup-preserva-veredito", t_neg_cleanup_preserva_veredito),
    ("neg-rollback-preserva-preexistentes", t_neg_rollback_preserva_preexistentes),
    ("rollback-exato", t_rollback_exato),
    ("neg-setup-excecao-libera-frente", t_neg_setup_excecao_libera_frente),
    ("neg-rollback-excecao-libera-frente", t_neg_rollback_excecao_libera_frente),
    ("neg-cancelamento-na-ultima-leitura", t_neg_cancelamento_na_ultima_leitura),
    ("cli-exits-e-saida-em-arquivo", t_cli_exits_e_saida_em_arquivo),
]


# ------------------------------------------------------------------ isca -------
# Cada mutacao neutraliza UM guard por substituicao textual no fonte do executor. A suite TEM de
# reprovar o teste indicado: se o mutante passa, a suite e um carimbo para aquele guard.
MUTACOES = [
    ("F1-obs-negada-volta-a-ler",
     "    if not quer_agir and not obs:",
     "    if not quer_agir and not obs and False:",
     "neg-obs-nao-autorizada-nao-le"),
    ("F1-override-string-coercao-booleana",
     '        ativa = _booleano(aut["ativa_autorizada"], "autorizacao.ativa_autorizada")',
     '        ativa = bool(aut["ativa_autorizada"])',
     "neg-override-string-nao-vira-true"),
    ("F1-requer-acao-coercao-booleana",
     '            requer = _booleano(passo["requer_acao"], "passo %r.requer_acao" % nome)',
     '            requer = bool(passo["requer_acao"])',
     "neg-requer-acao-nao-booleano"),
    ("F9-trava-controle-acesso-neutralizada",
     '        ativas = sorted(str(k) for k in passo if str(k).lower() in proibidas)',
     '        ativas = []',
     "neg-acao-ativa-proibida-controle-acesso"),
    ("F3-timeout-ausente-aceito-com-default",
     """    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ConfigInvalida("%s: 'timeout_s' obrigatorio e numerico, veio %r" % (onde, valor))""",
     """    if valor is None:
        return 0.05
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ConfigInvalida("%s: 'timeout_s' obrigatorio e numerico, veio %r" % (onde, valor))""",
     "neg-timeout-obrigatorio-finito"),
    ("F3-sleep-sem-limite-do-deadline",
     "            espera = min(intervalo_s, max(0.0, limite - decorrido))",
     "            espera = intervalo_s",
     "neg-poll-limitado-ao-deadline"),
    ("F2-satisfeito-string-vira-booleano",
     '    satisfeito = _satisfeito_estrito(resposta["satisfeito"], "fonte do passo %r" % passo["nome"])',
     '    satisfeito = bool(resposta["satisfeito"])',
     "neg-satisfeito-string-nao-vira-verde"),
    ("F2-satisfeito-arquivo-string-vira-booleano",
     """            satisfeito = _satisfeito_estrito(valor.get("satisfeito"),
                                             "estado '%s' de %s" % (chave, self.caminho))""",
     """            satisfeito = bool(valor.get("satisfeito"))""",
     "neg-fonte-arquivo-string-nao-vira-verde"),
    ("F2-json-invalido-deixa-de-ser-estruturado",
     """        except Exception as erro:
            raise ConfigInvalida("estado ilegivel em %s: %s: %s"
                                 % (self.caminho, type(erro).__name__, erro))""",
     """        except Exception as erro:
            return {"satisfeito": False, "observado": None,
                    "diagnostico": "estado ilegivel: %s" % erro}""",
     "neg-json-quebrado-estruturado"),
    ("F4-frente-volta-a-ser-opcional",
     """    if frente is None:
        frente = FrenteUnica(caminho_frente_padrao())
    try:
        res["frente"] = frente.obter()""",
     """    try:
        res["frente"] = frente.obter() if frente is not None else None""",
     "neg-frente-obrigatoria"),
    ("F4-lock-sem-O_EXCL",
     "                fd = os.open(self.caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)",
     "                fd = os.open(self.caminho, os.O_CREAT | os.O_WRONLY, 0o600)",
     "neg-frente-atomica-concorrente"),
    ("F5-delta-de-pid-vira-propriedade",
     '                    plano_enc["pids"] = [p for p in plano_enc["pids"] if p in pids_proprios]',
     '                    pass',
     "neg-pid-externo-nunca-fechado"),
    ("F5-liveness-desconhecida-escala-forca",
     '                    if any(medir(p) is None for p in plano_enc["pids"]):',
     '                    if False:',
     "neg-liveness-desconhecida-nao-forca"),
    ("F6-cleanup-volta-a-trocar-o-veredito",
     """                res["rollback"] = {"plano": plano_rb, "acoes": acoes, "residuo": residuo}""",
     """                _muda(ROLLBACK)
                res["rollback"] = {"plano": plano_rb, "acoes": acoes, "residuo": residuo}""",
     "neg-cleanup-preserva-veredito"),
    ("F7-rollback-sem-snapshot_de_dirs",
     "                plano_rb = col.planejar_rollback(before, after, dirs_antes, dirs_depois)",
     "                plano_rb = col.planejar_rollback(before, after)",
     "neg-rollback-preserva-preexistentes"),
    ("F8-liberacao-da-frente-so-sem-erro",
     """        try:
            res["frente_liberada"] = frente.liberar()
        except Exception as erro:
            res["cleanup_erros"].append("liberar frente: %s: %s" % (type(erro).__name__, erro))""",
     """        if not res["cleanup_erros"]:
            try:
                res["frente_liberada"] = frente.liberar()
            except Exception as erro:
                res["cleanup_erros"].append("liberar frente: %s: %s"
                                            % (type(erro).__name__, erro))""",
     "neg-setup-excecao-libera-frente"),
    ("F8-cancelamento-na-ultima-leitura-ignorado",
     """        if cancelado():
            return _cancelado("cancelado pelo chamador durante a ultima leitura")
        if ultimo["satisfeito"]:""",
     """        if ultimo["satisfeito"]:""",
     "neg-cancelamento-na-ultima-leitura"),
    ("F1-cli-NAO_EXERCITADO-com-exit-errado",
     """    if veredito == VEREDITO_NAO_EXERCITADO:
        return 2""",
     """    if veredito == VEREDITO_NAO_EXERCITADO:
        return 1""",
     "cli-exits-e-saida-em-arquivo"),
]


def _roda_testes(testes):
    """Roda uma lista de (nome, fn) e devolve {nome: (passou, detalhe)}."""
    resultado = {}
    for nome, fn in testes:
        try:
            fn()
            resultado[nome] = (True, "ok")
        except arc.Falhou as erro:
            resultado[nome] = (False, str(erro))
        except Exception as erro:                                    # noqa: BLE001
            resultado[nome] = (False, "excecao inesperada: %s: %s" % (type(erro).__name__, erro))
            traceback.print_exc()
    return resultado


def _roda_testes_verboso(testes):
    falhou = 0
    for nome, fn in testes:
        try:
            fn()
            print("RESULTADO|PASSOU|%s|ok" % nome)
        except arc.Falhou as erro:
            falhou += 1
            print("RESULTADO|REPROVOU|%s|%s" % (nome, erro))
        except Exception as erro:                                    # noqa: BLE001
            falhou += 1
            print("RESULTADO|REPROVOU|%s|excecao inesperada: %s: %s"
                  % (nome, type(erro).__name__, erro))
            traceback.print_exc()
    return falhou


def _isca(argv=None):
    """Prova DISCRIMINACAO: cada mutacao tem de ser capturada pelo teste-regressao indicado."""
    global EX
    with open(CAMINHO_EXECUTOR, encoding="utf-8") as fh:
        fonte_original = fh.read()
    falhas = 0
    nao_aplicadas = 0
    for i, (nome, de, para, teste) in enumerate(MUTACOES):
        if de not in fonte_original:
            nao_aplicadas += 1
            falhas += 1
            print("RESULTADO|REPROVOU|isca:%s|ANCORA NAO ENCONTRADA no fonte" % nome)
            continue
        mutante = fonte_original.replace(de, para, 1)
        if mutante == fonte_original:
            nao_aplicadas += 1
            falhas += 1
            print("RESULTADO|REPROVOU|isca:%s|SUBSTITUICAO INEFICAZ" % nome)
            continue
        EX = _carregar(fonte_texto=mutante, nome="kit11_executor_mutante_%d" % i)
        mapa = _roda_testes(TESTS)
        passou, detalhe = mapa.get(teste, (None, "teste inexistente"))
        if passou is False:
            print("RESULTADO|PASSOU|isca:%s|mutante capturado por %s" % (nome, teste))
        else:
            falhas += 1
            print("RESULTADO|REPROVOU|isca:%s|mutante PASSOU VERDE em %s (%s)"
                  % (nome, teste, detalhe))
    EX = _carregar()
    print("=" * 70)
    print("isca: %d mutacao(oes), %d nao aplicada(s), %d falha(s)"
          % (len(MUTACOES), nao_aplicadas, falhas))
    return 1 if falhas else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Testes offline do executor KIT-11F.")
    ap.add_argument("--isca", action="store_true",
                    help="muta o fonte do executor e exige que a suite capture cada mutacao")
    args = ap.parse_args(argv)

    if args.isca:
        return _isca()

    try:
        falhou = _roda_testes_verboso(list(TESTS))
    except Exception:                                                # noqa: BLE001
        traceback.print_exc()
        return 2
    print("=" * 70)
    print("%d teste(s), %d falha(s)" % (len(TESTS), falhou))
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
