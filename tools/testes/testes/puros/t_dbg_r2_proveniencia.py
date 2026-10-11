#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O CARIMBO DE PROVENIENCIA do dump do RoguelikeDebugger (DBG-R2, cartao t_3b7c681b).

O QUE ESTE TESTE GARANTE
------------------------
1. **O verificador reprova dump sem proveniencia.** O caso negativo obrigatorio do cartao: um dump
   no formato ANTIGO (o `LogOutput.log` de verdade, sem o bloco `DBG-PROV-V1`) tem de sair
   REPROVADO (exit 1). Prova vermelho->verde: as fixture `dbg-r2-sem-proveniencia.entrada.log`
   vem do formato que o mod usava antes deste cartao.
2. **Os quatro vereditos.** COMPLETO (0) / TRUNCADO (2) / REPROVADO (1) para os dumps versionados,
   exercitando o verificador REAL (`tools/verifica_proveniencia_debugger.py`) - importado do arquivo,
   nao uma copia digitada.
3. **O contrato dos dois lados.** Todo campo que o verificador EXIGE tem de existir no C# vivo
   (`RoguelikeDebugger/Proveniencia.cs`), e a marca do formato (`MARCA`) tem de ser a MESMA nos dois.
   Se alguem tirar um campo do C# ou renomear a marca, isto fica vermelho.
4. **A ordem de emissao e' a decisao do cartao**: `Proveniencia.Cabecalho()` sai ANTES de
   `AplicarPatches()` (identidade gravada antes de qualquer gancho), e o rodape vem de
   `Application.quitting`.
5. **Nada de gancho existente foi reescrito**: os 10 `Patches/*.cs`, o `EfeitosInfo.cs` e o
   `.csproj` batem com o sha256 medido ANTES da implementacao. O `.csproj` intocado tambem prova que
   **nenhuma referencia a API** entrou (a identidade da API e' lida por reflexao).
6. **13 iscas** no positivo (remover campo, encurtar hash, trocar veredito, alvo divergente...): cada
   uma tem de reprovar pelo motivo certo - e o positivo ORIGINAL tem de continuar COMPLETO depois
   (nenhuma isca mexe na fixture, so' no texto em memoria).

O QUE NAO ESTA PROVADO AQUI
---------------------------
Runtime: o plugin nunca foi carregado no jogo nesta rodada (NAO_EXERCITADO). O teste cobre formato,
contrato, ordem estatica e as fontes intocadas - nao a aplicacao real dos ganchos.
"""
import json
import os
import re
import shutil
import tempfile

import regras_proveniencia as reg

import arcabouco as arc

META = {
    "nome": "dbg-r2-proveniencia",
    "categoria": "pura",
    "requer": [],
    "descricao": ("DBG-R2: o carimbo DBG-PROV-V1 (verificador reprova dump sem proveniencia; "
                  "COMPLETO/TRUNCADO/REPROVADO por fixture; contrato campo-a-campo com o C#; "
                  "cabecalho antes dos ganchos; ganchos existentes com sha256 intacto)"),
}

COMPLETO, TRUNCADO, REPROVADO = 0, 2, 1


def _temp(temporario, nome, texto):
    caminho = os.path.join(temporario, nome)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    return caminho


def _troca(texto, de, para, quantas=1):
    arc.exigir(de in texto, "isca invalida: nao achei %r no dump de teste" % de)
    return texto.replace(de, para, quantas)


def corpo():
    temporario = tempfile.mkdtemp(prefix="dbg-r2-")
    try:
        # ---------------------------------------------------------------- 1. marca
        marca = reg.marca()
        arc.igual(marca, "DBG-PROV-V1", "marca do formato lida do verificador")
        arc.exigir('internal const string Marca = "%s"' % marca in reg.fonte("proveniencia"),
                   "o C# nao declara `Marca = %r` - o verificador e o plugin divergiram de marca" % marca)
        arc.exigir("[Proveniencia]" in reg.fonte("proveniencia"),
                   "o C# nao emite o aparelho `[Proveniencia]` que o verificador procura")

        # ------------------------------------------------- 2. contrato dos dois lados
        faltando = reg.faltando_no_cs()
        arc.exigir(not faltando,
                   "o verificador exige campo que o C# nao emite: %s" % ", ".join(faltando))
        exigidos = reg.campos_exigidos()
        total_campos = sum(len(v) for v in exigidos.values())
        arc.exigir(total_campos >= 18,
                   "os campos exigidos encolheram para %d: o contrato do carimbo foi reduzido"
                   % total_campos)

        # ------------------------------------------------------------ 3. as fixtures
        esperados = reg.fixtures_do_cartao()
        for caso, veredito_esperado in sorted(esperados.items()):
            caminho = reg.fixture(caso)
            veredito, motivos, avisos, notas, _ = reg.verificar(caminho, reg.alvo_do_repo())
            arc.igual(veredito, veredito_esperado,
                      "%s tem de sair %s (saiu %s%s)"
                      % (caso, reg.nome_do_veredito(veredito_esperado),
                         reg.nome_do_veredito(veredito),
                         ("; motivos: " + " / ".join(motivos)) if motivos else ""))

        # o caso negativo obrigatorio, com o motivo EXATO: sem cabecalho.
        _, motivos, _, _, campos = reg.verificar(reg.fixture("dbg-r2-sem-proveniencia"),
                                                 reg.alvo_do_repo())
        arc.exigir(any("sem cabecalho de proveniencia" in m for m in motivos),
                   "o dump sem proveniencia reprovou, mas NAO pelo motivo de cabecalho ausente: %s"
                   % motivos)
        arc.igual(campos, {}, "sem cabecalho nao ha campo nenhum a interpretar")

        # o positivo: COMPLETO, com a identidade lida da API e o dump fechado.
        _, motivos, avisos, notas, campos = reg.verificar(reg.fixture("dbg-r2-proveniencia"),
                                                          reg.alvo_do_repo())
        arc.exigir(not motivos and not avisos, "o dump completo acusou %s / %s" % (motivos, avisos))
        arc.igual(campos["inicio"]["identidade"], "api", "identidade do dump completo")
        arc.igual(campos["inicio"]["alvoConforme"], "sim", "gate da API no dump completo")
        arc.igual(campos["inicio"]["sha256Alvo"], campos["alvo"]["assemblyCSharpSha256"],
                  "sha256 do alvo: carimbo x api/docs/target-game.json")
        arc.igual(campos["estado"]["ganchosOk"], "14/14", "contagem de ganchos do dump completo")
        arc.igual(campos["fim"]["estadoDump"], "FECHADO", "estado final do dump completo")
        arc.exigir(any("modoLeitura=ativo" in n for n in notas),
                   "faltou a NOTA de passividade no dump completo (a matriz Flame esta' aplicada)")

        # --------------------------------------------------------- 4. ordem estatica
        plugin = reg.fonte("plugin")
        pos_cabecalho = plugin.find("Proveniencia.Cabecalho()")
        pos_patches = plugin.find("AplicarPatches()")
        arc.exigir(pos_cabecalho > 0 and pos_patches > 0,
                   "Plugin.cs nao chama Proveniencia.Cabecalho()/AplicarPatches()")
        arc.exigir(pos_cabecalho < pos_patches,
                   "o carimbo tem de sair ANTES dos ganchos (cabecalho@%d, patches@%d)"
                   % (pos_cabecalho, pos_patches))
        arc.exigir("Application.quitting += AoFechar;" in plugin,
                   "Plugin.cs nao assina Application.quitting: sem rodape o dump fica sempre truncado")
        arc.exigir("Proveniencia.Fim(" in plugin and "Proveniencia.Estado(" in plugin,
                   "Plugin.cs nao fecha nem declara o estado do dump")

        # -------------------------------------------- 5. ganchos existentes intocados
        medidos = reg.hashes_intocados()
        divergentes = [rel for rel, valor in reg.INTOCADOS.items() if medidos[rel] != valor]
        arc.exigir(not divergentes,
                   "fonte que NAO podia mudar neste cartao mudou: %s" % ", ".join(divergentes))
        csproj = reg.fonte("csproj")
        alcance = re.findall(r"RealmApi|Gumatos|com\.gumatos\.realmapi", csproj)
        arc.exigir(not alcance,
                   "o .csproj passou a referenciar a API (%s): a dependencia tem de ser OPCIONAL" % alcance)
        arc.exigir('"Gumatos.RealmApi.ApiIdentity"' in reg.fonte("proveniencia"),
                   "o C# nao procura a API pelo nome do tipo: a leitura por reflexao saiu do lugar")

        # ------------------------------------------------------------- 6. as iscas
        positivo = reg.ler_fixture("dbg-r2-proveniencia")
        sha_antes = reg.sha256(reg.fixture("dbg-r2-proveniencia"))
        linha_inicio = [l for l in positivo.splitlines() if "DBG-PROV-V1 inicio" in l][0]
        linha_estado = [l for l in positivo.splitlines() if "DBG-PROV-V1 estado" in l][0]

        iscas = [
            ("sem-cabecalho", positivo.replace(linha_inicio + "\n", ""), REPROVADO),
            ("sem-estado", positivo.replace(linha_estado + "\n", ""), REPROVADO),
            ("sem-rodape", "\n".join(l for l in positivo.splitlines()
                                     if "DBG-PROV-V1 fim" not in l) + "\n", TRUNCADO),
            ("estado-parcial", _troca(positivo, "estadoDump=ABERTO", "estadoDump=PARCIAL"), TRUNCADO),
            ("sha-curto", _troca(positivo, "sha256Alvo=8bb4a7c5", "sha256Alvo=8bb4a7c"), REPROVADO),
            ("sha-ausente", _troca(positivo, " | sha256Alvo=8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a", ""), REPROVADO),
            ("build-desconhecido", _troca(positivo, "buildSteam=25240684", "buildSteam=desconhecido"), TRUNCADO),
            ("alvo-divergente", _troca(positivo, "alvoConforme=sim", "alvoConforme=nao"), REPROVADO),
            ("contagem-incoerente", _troca(positivo, "ganchosOk=14/14", "ganchosOk=13/14"), REPROVADO),
            ("api-desligada", _troca(positivo, "apiEnableHooks=sim", "apiEnableHooks=nao"), REPROVADO),
            ("rodape-sem-motivo", _troca(positivo, "motivo=saida-do-jogo", "motivo="), REPROVADO),
            ("modo-invalido", _troca(positivo, "modoLeitura=ativo", "modoLeitura=talvez"), REPROVADO),
            ("estado-invalido", _troca(positivo, "estadoDump=INICIADO", "estadoDump=COMEÇOU"), REPROVADO),
        ]
        for nome, texto, veredito_esperado in iscas:
            caminho = _temp(temporario, "isca-%s.log" % nome, texto)
            veredito, motivos, avisos, _, _ = reg.verificar(caminho, reg.alvo_do_repo())
            arc.igual(veredito, veredito_esperado,
                      "isca %s tinha de sair %s e saiu %s (%s)"
                      % (nome, reg.nome_do_veredito(veredito_esperado),
                         reg.nome_do_veredito(veredito), motivos or avisos))

        # o positivo ORIGINAL nao foi tocado pelas iscas (so' o texto em memoria mudou).
        arc.igual(reg.sha256(reg.fixture("dbg-r2-proveniencia")), sha_antes,
                  "a fixture do positivo mudou de hash: alguma isca escreveu no repositorio")

        # -------------------------------------------- 7. divergencia com --alvo
        alvo = json.load(open(reg.alvo_do_repo(), encoding="utf-8"))
        for campo, valor in (("assemblyCSharpSha256", "0" * 64),
                             ("gameVersion", "9.9.9"),
                             ("steamBuildId", "99999999")):
            adulterado = dict(alvo)
            adulterado[campo] = valor
            caminho_alvo = _temp(temporario, "alvo-%s.json" % campo, json.dumps(adulterado))
            veredito = reg.veredito(reg.fixture("dbg-r2-proveniencia"), caminho_alvo)
            arc.igual(veredito, REPROVADO,
                      "alvo adulterado em %s tinha de reprovar o dump completo" % campo)

        print("proveniencia DBG-R2: %d fixtures pelos vereditos certos, %d campos exigidos presentes "
              "no C#, cabecalho antes dos ganchos, %d fontes intocadas e %d iscas reprovando "
              "(nenhuma fixture alterada)"
              % (len(esperados), total_campos, len(reg.INTOCADOS), len(iscas)))
    finally:
        shutil.rmtree(temporario, ignore_errors=True)


if __name__ == "__main__":
    arc.main(META, corpo)
