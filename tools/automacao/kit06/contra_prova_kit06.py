#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contra_prova_kit06.py - KIT-06: contra-prova DURAVEL do plano de controle.

Por que existe
--------------
Todo teste tem de ser MOSTRADO REPROVANDO. Aqui plantamos defeitos REAIS no
modulo (`controle_acesso.py`, numa COPIA temporaria — o original nunca e
tocado) e exigimos que a suite APONTE exatamente o defeito.

Discriminador ESTRITO (licao do achado F9 do KIT-05R): uma isca so conta como
detectada se
  (a) o runner sai com exit 1,
  (b) o conjunto EXATO de testes que falharam e o conjunto DECLARADO,
  (c) o output contem `AssertionError`,
  (d) NAO ha `ERROR:` (falha de setup != deteccao) e NAO ha skip,
  (e) houve execucao real (`Ran N tests`, N > 0).
Se a suite passar com o defeito plantado, a contra-prova REPROVA (falso verde).
Ha ainda um AUTOTESTE adversarial (`--autoteste`) que verifica que o proprio
discriminador recusa saidas enganosas.

COBERTURA (KIT-06F): 38 defeitos plantados, cada um com o conjunto EXATO
declarado de testes que DEVEM reprovar. Cobrem TODOS os testes da suite (nenhum
teste sem prova negativa) — inclusive o contrato revisado (OBSERVAR
liga/desliga, RETOMAR despachado, ownership de coleta, export com evidencia,
falha-segura de IO, snapshots defensivos planos E aninhados, config vazia/gate
KIT-07).

Uso:
    python tools/automacao/kit06/contra_prova_kit06.py
    python tools/automacao/kit06/contra_prova_kit06.py --autoteste
    PYTHON=/caminho/python python tools/automacao/kit06/contra_prova_kit06.py

Exit: 0 = verde; 1 = vermelho; 2 = infraestrutura/layout.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))          # .../kit06
REL_MODULO = os.path.join("tools", "automacao", "runtime", "controle_acesso.py")
REL_PIPELINE = os.path.join("tools", "automacao", "runtime", "observacao_passiva.py")
REL_TESTE = os.path.join("tools", "automacao", "kit06", "teste_controle_acesso.py")


def resolver_layout(inicio=AQUI):
    """Resolve a raiz pelo LAYOUT (nunca por `git rev-parse`)."""
    atual = os.path.abspath(inicio)
    for _ in range(8):
        modulo = os.path.join(atual, REL_MODULO)
        teste = os.path.join(atual, REL_TESTE)
        pipeline = os.path.join(atual, REL_PIPELINE)
        if os.path.isfile(modulo) and os.path.isfile(teste) and os.path.isfile(pipeline):
            return atual, modulo, teste, pipeline
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return None, None, None, None


RAIZ, MODULO, TESTE, PIPELINE = resolver_layout()

# --------------------------------------------------------------------------
# DEFEITOS PLANTADOS: nome -> (substituicoes, testes que DEVEM falhar)
# --------------------------------------------------------------------------
MUTACOES = {
    'guard_chat_removido': (
        [
            ('        if c.get("chat_aberto") or c.get("digitando"):',
             '        if False:'),
        ],
        {'TestRoteiro.test_roteiro_offline_completo', 'TestCorrecoesKit06F.test_F4_export_inclui_evento_degradacao_e_correlacao', 'TestGuards.test_chat_bloqueia_e_degrada', 'TestGuards.test_digitando_bloqueia'}),
    'guard_remapeamento_removido': (
        [
            ('        if c.get("remapeando"):',
             '        if False:'),
        ],
        {'TestGuards.test_remapeando_bloqueia'}),
    'guard_sem_foco_removido': (
        [
            ('        if not c.get("foco_no_jogo"):',
             '        if False:'),
        ],
        {'TestGuards.test_sem_foco_bloqueia_sem_forcar_foco'}),
    'trava_modo_ativo_removida': (
        [
            ('        self.modo_ativo_pedidos += 1\n        self._degrada("modo_ativo_proibido",\n                      detalhe="iniciar/observar nao autoriza modo ativo")\n        return None',
             '        self.modo_ativo_pedidos += 1\n        self.modo = "ativo"\n        return self._evento("modo_ativo")'),
        ],
        {'TestTravaModoAtivo.test_habilitar_modo_ativo_sempre_falha'}),
    'acao_ativa_permitida': (
        [
            ('        if acao in ACOES_ATIVAS:\n            self._degrada("acao_ativa_proibida", detalhe="acao=%s" % acao)\n            return None',
             '        if False:\n            pass'),
        ],
        {'TestTravaModoAtivo.test_executar_acao_ativa_recusada'}),
    'conflito_de_atalho_aceito': (
        [
            ('        if tecla in usadas:\n            problemas.append((acao, "conflito_tecla"))\n            problemas.append((usadas[tecla], "conflito_tecla"))\n            norm.pop(usadas[tecla], None)\n            continue',
             '        if False:\n            pass'),
        ],
        {'TestAtalhos.test_conflito_entre_atalhos_recusado'}),
    'tecla_reservada_aceita': (
        [
            ('        if tecla in reservadas:',
             '        if False:'),
        ],
        {'TestAtalhos.test_carrega_atalhos_de_json', 'TestAtalhos.test_tecla_reservada_recusada', 'TestCorrecoesKit06F.test_F1_mapa_totalmente_rejeitado_nao_reativa'}),
    'marcar_sem_observacao_permitido': (
        [
            ('        if not self._observando:\n            self._degrada("marcar_sem_observacao",\n                          detalhe="marcacao manual exige observacao ativa")\n            return None',
             '        if False:\n            pass'),
        ],
        {'TestMarcacao.test_marcar_exige_observacao'}),
    'export_sem_dados_permitido': (
        [
            ('        if not self._observando and not self._marcacoes:\n            self._degrada("exportar_sem_dados",\n                          detalhe="nada para exportar (sem observacao e sem marcacao)")\n            return None',
             '        if False:\n            pass'),
        ],
        {'TestExport.test_export_sem_dados_recusado'}),
    'foco_forcado_ligado': (
        [
            ('        self.foco_forcado = 0               # trava: nunca muda o foco',
             '        self.foco_forcado = 1'),
        ],
        {'TestExport.test_export_grava_arquivo_local_sem_ia', 'TestGuards.test_sem_foco_bloqueia_sem_forcar_foco'}),
    'encerrou_sessao_ligado': (
        [
            ('        self.encerrou_sessao = False        # trava: nunca encerra a sessao',
             '        self.encerrou_sessao = True'),
        ],
        {'TestObservar.test_parar_nao_encerra_sessao_do_dono', 'TestExport.test_export_grava_arquivo_local_sem_ia'}),
    'indicador_pausado_errado': (
        [
            ('            estado = "pausado"',
             '            estado = "observando"'),
        ],
        {'TestIndicador.test_indicador_transicoes'}),
    'pausa_nao_delega_pipeline': (
        [
            ('        self.pipeline.pausar()\n        self._pausado_por_controle = True\n        return self._evento(PAUSAR, {"pausado": True})',
             '        self._degrada("pausa_ignorada", detalhe="defeito plantado")\n        return self._evento(PAUSAR, {"pausado": True})'),
        ],
        {'TestIntegracaoKit05F.test_pausa_do_controle_pausa_o_pipeline', 'TestMarcacao.test_marcar_durante_pausa_permitido', 'TestCorrecoesKit06F.test_F2_retomar_despachado_tem_efeito', 'TestIndicador.test_indicador_transicoes', 'TestRoteiro.test_roteiro_offline_completo', 'TestObservar.test_pausa_delega_ao_pipeline'}),
    'acao_desconhecida_aceita': (
        [
            ('        if acao not in ACOES_CONHECIDAS:\n            problemas.append((acao, "acao_desconhecida"))\n            continue',
             '        if False:\n            pass'),
        ],
        {'TestAtalhos.test_acao_desconhecida_recusada'}),
    'acao_ativa_aceita': (
        [
            ('        if acao in ACOES_ATIVAS:\n            problemas.append((acao, "acao_ativa_proibida"))\n            continue',
             '        if False:\n            pass'),
        ],
        {'TestAtalhos.test_acao_ativa_proibida'}),
    'tecla_vazia_aceita': (
        [
            ('        if not tecla:\n            problemas.append((acao, "tecla_vazia"))\n            continue',
             '        if False:\n            pass'),
        ],
        {'TestAtalhos.test_tecla_vazia_recusada'}),
    'config_nao_dict_sem_erro': (
        [
            ('    if not isinstance(atalhos, dict):\n        raise ErroControleAcesso("atalhos precisa ser um dicionario acao->tecla")',
             '    if not isinstance(atalhos, dict):\n        return {}, []'),
        ],
        {'TestAtalhos.test_config_nao_dict_levanta'}),
    'consome_input_ligado': (
        [
            ('        self.consome_input = False          # so LE teclas',
             '        self.consome_input = True'),
        ],
        {'TestGuards.test_guards_nao_consomem_input'}),
    'sem_binding_silencioso': (
        [
            ('        acao = self.tecla_para_acao(tecla)\n        if acao is None:\n            self._degrada(MOTIVO_SEM_BINDING, detalhe="tecla=%s" % tecla)\n            return None',
             '        acao = self.tecla_para_acao(tecla)\n        if acao is None:\n            return None'),
        ],
        {'TestGuards.test_tecla_sem_binding_degrada'}),
    'modo_nao_passivo': (
        [
            ('        self.modo = "passivo"          # trava dura: sempre passivo',
             '        self.modo = "ativo"'),
        ],
        {'TestTravaModoAtivo.test_observar_nao_abre_porta_ativa', 'TestObservar.test_iniciar_observacao_modo_passivo'}),
    'observar_nao_alterna': (
        [
            ('        if acao == OBSERVAR:\n            return self.alternar_observacao()',
             '        if acao == OBSERVAR:\n            return self._iniciar_observacao()'),
        ],
        {'TestCorrecoesKit06F.test_F2_parar_sem_terminal_pelo_toggle', 'TestObservar.test_f7_alterna_observacao_liga_desliga'}),
    'pausa_sem_observacao_permitida': (
        [
            ('        if not self._observando:\n            self._degrada("pausar_sem_observacao",\n                          detalhe="nao ha coleta para pausar")\n            return None',
             '        if False:\n            pass'),
        ],
        {'TestObservar.test_pausar_sem_observacao_degrada'}),
    'indicador_eventos_zerado': (
        [
            ('            eventos = int(self.pipeline.resumo().get("eventos_total", 0) or 0)',
             '            eventos = 0'),
        ],
        {'TestCorrecoesKit06F.test_F4_export_inclui_evento_degradacao_e_correlacao', 'TestIntegracaoKit05F.test_indicador_le_eventos_do_pipeline'}),
    'marcacao_sem_janela': (
        [
            ('            "janela": janela if janela is not None\n                      else self._contexto.get("janela"),',
             '            "janela": None,'),
        ],
        {'TestMarcacao.test_marcar_registra_contexto'}),
    'teto_problemas_ignorado': (
        [
            ('        if len(self._marcacoes) >= self.teto_problemas:\n            self._degrada("teto_problemas_atingido",\n                          detalhe="teto_problemas=%d" % self.teto_problemas)\n            return None',
             '        if False:\n            pass'),
        ],
        {'TestMarcacao.test_teto_problemas_respeitado'}),
    'export_caminho_relativo_ignorado': (
        [
            ('        else:\n            if not os.path.isabs(caminho):\n                caminho = os.path.join(pasta, caminho)',
             '        else:\n            if not os.path.isabs(caminho):\n                caminho = os.path.join(pasta, "sempre-default.json")'),
        ],
        {'TestExport.test_export_aceita_caminho_relativo_na_pasta'}),
    'contrato_integracao_mentirosa': (
        [
            ('        "integracao_efetiva": False,',
             '        "integracao_efetiva": True,'),
        ],
        {'TestExport.test_contrato_kit07_declarado_honesto'}),
    'indicador_sem_janela': (
        [
            ('            "janela": self._contexto.get("janela"),\n            "eventos": eventos,',
             '            "janela": None,\n            "eventos": eventos,'),
        ],
        {'TestIndicador.test_indicador_mostra_contexto_e_marcacoes'}),
    'atalhos_vazio_reativa_defaults': (
        [
            ('        if atalhos is None:\n            atalhos = atalhos_padrao()\n        atalhos = dict(atalhos)',
             '        atalhos = dict(atalhos or atalhos_padrao())'),
        ],
        {'TestCorrecoesKit06F.test_F1_mapa_vazio_nao_reativa_defaults', 'TestCorrecoesKit06F.test_F1_mapa_totalmente_rejeitado_nao_reativa'}),
    'retomar_sem_efeito': (
        [
            ('        self.pipeline.retomar()\n        self._pausado_por_controle = False\n        if not self._observando:\n            self._observando = True\n            self.modo = "passivo"\n        return self._evento(RETOMAR, {"pausado": False, "observando": True})',
             '        return self._evento(RETOMAR, {"pausado": False, "observando": True})'),
        ],
        {'TestCorrecoesKit06F.test_F2_retomar_despachado_tem_efeito'}),
    'sem_pipeline_vira_observando': (
        [
            ('        elif self.pipeline is None:\n            estado = "sem_pipeline"',
             '        elif False:\n            estado = "sem_pipeline"'),
        ],
        {'TestCorrecoesKit06F.test_F3_indicador_sem_pipeline_e_lacuna'}),
    'ownership_de_coleta_removida': (
        [
            ('        if self.pipeline is not None and hasattr(self.pipeline, "pausar") \\\n                and not self._pipeline_pausado():\n            self.pipeline.pausar()\n            self._pausado_por_controle = True\n        else:\n            self._pausado_por_controle = self._pipeline_pausado()',
             '        self._pausado_por_controle = self._pipeline_pausado()'),
        ],
        {'TestObservar.test_pausa_delega_ao_pipeline', 'TestCorrecoesKit06F.test_F3_parado_nao_coleta_no_pipeline'}),
    'export_correlacao_vazia': (
        [
            ('            "correlacao": {\n                "sessao_controle": self.id_sessao,\n                "sessao_coleta": sessao_coleta,\n            },',
             '            "correlacao": {\n                "sessao_controle": None,\n                "sessao_coleta": None,\n            },'),
        ],
        {'TestCorrecoesKit06F.test_F4_export_inclui_evento_degradacao_e_correlacao'}),
    'export_falha_io_mascarada': (
        [
            ('        except OSError as exc:\n            self._degrada("export_falha_io",\n                          detalhe="%s: %s" % (type(exc).__name__, exc))\n            return None',
             '        except OSError as exc:\n            self._degrada("export_falha_io",\n                          detalhe="%s: %s" % (type(exc).__name__, exc))\n            return "erro-mascarado"'),
        ],
        {'TestCorrecoesKit06F.test_F5_export_falha_io_sem_propagar'}),
    'janela_none_nao_limpa': (
        [
            ('    def atualizar_contexto(self, janela=_SEM_VALOR, chat_aberto=None,',
             '    def atualizar_contexto(self, janela=None, chat_aberto=None,'),
            ('        if janela is not _SEM_VALOR:\n            self._contexto["janela"] = janela',
             '        if janela is not None:\n            self._contexto["janela"] = janela'),
        ],
        {'TestCorrecoesKit06F.test_F6_janela_none_limpa_e_omitir_mantem'}),
    'marcacoes_por_referencia': (
        [
            ('    def marcacoes(self):\n        return [dict(m) for m in self._marcacoes]',
             '    def marcacoes(self):\n        return list(self._marcacoes)'),
        ],
        {'TestCorrecoesKit06F.test_F6_marcacoes_snapshot_defensivo'}),
    'coleta_aninhado_por_referencia': (
        [
            ('        bloco["eventos"] = _copia_profunda(eventos)',
             '        bloco["eventos"] = eventos'),
        ],
        {'TestCorrecoesKit06F.test_F6_coleta_aninhado_snapshot_defensivo'}),
    'atalhos_padrao_com_problema': (
        [
            ('    return {OBSERVAR: "F7", PAUSAR: "F8", MARCAR_PROBLEMA: "F9",\n            EXPORTAR: "F10"}',
             '    return {OBSERVAR: "F7", PAUSAR: "F8", MARCAR_PROBLEMA: "F9",\n            EXPORTAR: "F10", "voar": "F1"}'),
        ],
        {'TestAtalhos.test_padrao_valido'}),
}



def aplica(origem, subs):
    with open(origem, encoding="utf-8") as fh:
        texto = fh.read()
    for velho, novo in subs:
        if velho not in texto:
            return None, "trecho nao encontrado: %r" % velho[:60]
        texto = texto.replace(velho, novo, 1)
    return texto, None


# --------------------------------------------------------------------------
# Discriminador estrito
# --------------------------------------------------------------------------
RE_FAIL = re.compile(r"^(FAIL|ERROR): \S+ \(([^)]+)\)")
RE_RAN = re.compile(r"^Ran (\d+) tests?", re.M)


def _coleta_saida(saida):
    falhas, erros = set(), set()
    for linha in saida.splitlines():
        m = RE_FAIL.match(linha.strip())
        if not m:
            continue
        partes = m.group(2).split(".")
        nome = ".".join(partes[-2:]) if len(partes) >= 2 else m.group(2)
        (erros if m.group(1) == "ERROR" else falhas).add(nome)
    return falhas, erros


def avaliar(saida, exit_code, esperados):
    """Discriminador estrito. Devolve (ok, motivo)."""
    if exit_code != 1:
        return False, "exit esperado 1, veio %s" % exit_code
    falhas, erros = _coleta_saida(saida)
    if erros:
        return False, "houve ERROR (falha de setup, nao deteccao): %s" % sorted(erros)
    if "skipped" in saida:
        return False, "houve teste pulado/skip"
    if "AssertionError" not in saida:
        return False, "sem AssertionError: nao foi falha de assercao"
    m = RE_RAN.search(saida)
    if not m or int(m.group(1)) < 1:
        return False, "sem execucao real (Ran N tests ausente/zerado)"
    if falhas != set(esperados):
        return False, "conjunto de falhas != declarado: obtido=%s esperado=%s" % (
            sorted(falhas), sorted(esperados))
    return True, "ok"


def roda_isca(nome, subs, esperados, py, pasta):
    """Roda a suite contra o modulo mutado numa COPIA temporaria."""
    mutado, erro = aplica(MODULO, subs)
    if erro:
        return False, "mutacao '%s': %s" % (nome, erro)
    tdir = tempfile.mkdtemp(prefix="isca-kit06-")
    try:
        with open(os.path.join(tdir, "controle_acesso.py"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(mutado)
        shutil.copyfile(PIPELINE, os.path.join(tdir, "observacao_passiva.py"))
        shutil.copyfile(TESTE, os.path.join(tdir, "teste_controle_acesso.py"))
        proc = subprocess.run([py, os.path.join(tdir, "teste_controle_acesso.py")],
                              cwd=tdir, capture_output=True, text=True)
        saida = (proc.stdout or "") + (proc.stderr or "")
        with open(os.path.join(pasta, "isca-%s.log" % nome), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(saida)
        return avaliar(saida, proc.returncode, esperados)
    finally:
        shutil.rmtree(tdir, ignore_errors=True)


# --------------------------------------------------------------------------
# Autoteste adversarial do discriminador
# --------------------------------------------------------------------------
def autoteste(py, pasta):
    """Saidas enganosas que o discriminador TEM de recusar."""
    saida_ok = (
        "test_a (__main__.TestAtalhos.test_a) ... ok\n"
        "FAIL: test_b (__main__.TestAtalhos.test_b)\n"
        "AssertionError: x\n"
        "Ran 2 tests\nFAILED (failures=1)\n")
    probes = [
        ("falha de teste NAO-alvo nao confirma o alvo",
         (saida_ok.replace("test_b", "test_outro"), 1,
          {"TestAtalhos.test_alvo"})),
        ("exit 0 com texto de FAIL nao confirma",
         (saida_ok, 0, {"TestAtalhos.test_b"})),
        ("ERROR de setup nao confirma",
         ("ERROR: test_b (__main__.TestAtalhos.test_b)\n"
          "AssertionError: y\nRan 1 test\nERROR\n", 1,
          {"TestAtalhos.test_b"})),
        ("skip nao confirma",
         ("FAIL: test_b (__main__.TestAtalhos.test_b)\nAssertionError: x\n"
          "Ran 1 test\nFAILED (failures=1, skipped=1)\n", 1,
          {"TestAtalhos.test_b"})),
        ("sem AssertionError nao confirma",
         ("FAIL: test_b (__main__.TestAtalhos.test_b)\n"
          "Ran 1 test\nFAILED (failures=1)\n", 1,
          {"TestAtalhos.test_b"})),
        ("execucao vazia (Ran 0) nao confirma",
         ("FAIL: test_b (__main__.TestAtalhos.test_b)\nAssertionError: x\n"
          "Ran 0 tests\n", 1, {"TestAtalhos.test_b"})),
        ("conjunto parcial (subset) nao confirma",
         (saida_ok, 1, {"TestAtalhos.test_b", "TestAtalhos.test_c"})),
        ("saida limpa (exit 0) nao confirma",
         ("Ran 2 tests\nOK\n", 0, set())),
    ]
    oks = 0
    for rotulo, (saida, code, esp) in probes:
        ok, motivo = avaliar(saida, code, esp)
        recusou = not ok
        print("[%s ] autoteste: %s%s" % ("OK" if recusou else "FALHA", rotulo,
                                         "" if recusou else " -> ACEITOU (%s)" % motivo))
        oks += 1 if recusou else 0
    # e um caso VERDADEIRO tem de ser ACEITO (o discriminador nao pode ser sempre-no)
    ok, motivo = avaliar(saida_ok, 1, {"TestAtalhos.test_b"})
    print("[%s ] autoteste: caso verdadeiro ACEITO%s"
          % ("OK" if ok else "FALHA", "" if ok else " -> %s" % motivo))
    oks += 1 if ok else 0
    return oks, len(probes) + 1


def main(argv):
    py = os.environ.get("PYTHON", sys.executable or "python")
    pasta = os.path.join(RAIZ or ".", "scratch", "kit", "KIT-06", "contra-prova")
    if "--autoteste" in argv:
        if RAIZ is None:
            print("ERRO KIT-06: layout inesperado")
            return 2
        os.makedirs(pasta, exist_ok=True)
        oks, total = autoteste(py, pasta)
        print("=" * 60)
        print(" autoteste do discriminador: %d/%d" % (oks, total))
        return 0 if oks == total else 1

    if RAIZ is None:
        print("ERRO KIT-06: layout inesperado (modulo/suite/pipeline ausente)")
        return 2
    os.makedirs(pasta, exist_ok=True)
    print("=" * 60)
    print(" KIT-06 contra-prova por regra (defeito plantado TEM de reprovar)")
    print("=" * 60)
    falhas = 0
    for nome in sorted(MUTACOES):
        subs, esperados = MUTACOES[nome]
        ok, motivo = roda_isca(nome, subs, esperados, py, pasta)
        print("[%s ] %s%s" % ("OK" if ok else "FALHA", nome,
                              "" if ok else " -> " + motivo))
        falhas += 0 if ok else 1
    print("=" * 60)
    print(" iscas: %d, falhas: %d" % (len(MUTACOES), falhas))
    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
