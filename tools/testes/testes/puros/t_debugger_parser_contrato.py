#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRATO DO PARSER do censo (TST-5) - o teste de regressao mais valioso do mod.

O QUE ESTE TESTE PRENDE (e por que existe)
------------------------------------------
O `tools/census.py` le o dump de boot do RoguelikeDebugger com TRES regexes (`LINE`,
`FIELD`, `DESC`). O dump e uma linha de texto com campos `chave=valor` separados por
`" | "` e o `desc=` por ULTIMO. **Um campo novo no dump pode quebrar o censo em
silencio**: o `FIELD` usa `[^|]+` (um `|` DENTRO de um valor TRUNCA o campo sem erro) e
o `DESC` e ancorado no fim da linha (um campo depois do `desc=` faz a descricao sumir).
O mod CRESCE o dump o tempo todo (`efTipos`, `tick`, `auraSts`... entraram no fonte e
ainda nao estao no log); este teste e a trava que impede o crescimento de virar
truncagem muda.

O QUE ELE EXIGE
---------------
  1. A linha no formato ATUAL (o que o `ActionStatusInventoryPatch.cs` emite HOJE,
     campo a campo LIDO do fonte, nao digitado) casa as tres regexes e o `desc` sai
     inteiro.
  2. A linha no formato ANTIGO (a do log VERSIONADO, `tools/fixtures/shrines-exemplo.log`)
     continua legivel - regressao nos dois sentidos.
  3. `desc=` e o ULTIMO campo emitido; nenhum valor tem `|` nem quebra de linha.
  4. As chaves que o censo LE para `Status` estao TODAS entre as emitidas (senao a
     coluna vira vazia em silencio).
  5. Um campo renomeado no dump vira campo VAZIO no censo - e a isca prova que a
     checagem morde.

PROVA DE FOGO
-------------
Ha uma isca EMBUTIDA por defeito (planta o defeito numa copia em memoria da linha ou
do fonte e exige que a checagem REPROVE pela razao certa). A prova FISICA (defeito
plantado no `tools/census.py` real, teste rodado, arquivo restaurado byte a byte com
sha256) esta em `tools/testes/debugger-prova-de-fogo.log`.

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao roda o `parse()` do censo inteiro (ele ESCREVE os CSVs de `docs/cobertura/`; este
teste so exercita as regexes, que sao a fronteira do contrato). Nao executa o C# do
mod: a ligacao entre a linha do teste e o dump real e o log VERSIONADO e a leitura
ESTRUTURAL do fonte que a emite.
"""
import arcabouco as arc
import regras_debugger as rd

META = {
    "nome": "debugger-parser-contrato",
    "categoria": "pura",
    "requer": [],
    "descricao": ("o censo (tools/census.py) le a linha no formato ATUAL (lido do fonte) "
                  "e no ANTIGO (log versionado); `desc=` e o ultimo campo, nenhum valor "
                  "tem '|' nem quebra de linha, e um campo renomeado vira vazio (isca)"),
}

CENSO = rd.carrega_censo()

# As chaves que o censo LE para a categoria Status (as do header de `CATS["Status"]`
# que sao dado do dump; `nome`/`classe`/`descricao`/`status` nao sao `chave=valor`).
CHAVES_STATUS = ("tipo", "raridade", "efeitos", "efeitosDano", "nEfeitosDano")

FIXTURE_LOG = "debugger-parser-contrato"   # -> <nome>.entrada.log (procedencia no arquivo)
NOME_NO_LOG = "Conqueror Aura"

# Valores do formato ATUAL. Emitidos pelo fonte (RD-2): os campos novos entram ANTES
# do `desc=`. O `efeitos` carrega ASPAS de proposito (`Target["ShrineEffectBonus"]`) -
# e assim no log real, e o parser TOLERA (so `|` e quebra de linha quebram).
VALORES_ATUAL = {
    "tipo": "Normal",
    "raridade": "Common",
    "efeitos": 'DamageReduction:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100))),',
    "efeitosDano": "",
    "nEfeitosDano": "0",
    "aura": "nao", "raio": "3", "auraAli": "nao", "auraIni": "nao",
    "modelo": "-", "beneficio": "Buff", "dur": "3", "maxStk": "100",
    "nEfeitosTot": "2", "efTipos": "0:GeneralEffect{Action=10 * Level}; 1:CharacterVariableEffectInfo{Amount=20}",
    "nAttrEf": "1", "attrTipos": "0:CharacterEffectInfo{CharacterAttribute=DamageReduction}",
    "nTrig": "0", "trigEf": "",
    "expr": 'Mathf.Round(5 * (1 + (Source["ShrineEffectBonus"] / 100)))', "danoExpr": "",
    "refAcao": "", "refStatus": "", "tick": "-", "auraSts": "-",
    "desc": "Reduces Damage taken by [0]%.",
}


def _linha(campos, nome, cat="Status"):
    """Monta a linha do dump; o `desc=` sai ENTRE ASPAS (como no log real)."""
    partes = ['%s="%s"' % (k, v) if k == "desc" else "%s=%s" % (k, v)
              for k, v in campos.items()]
    return "[Info   :Roguelike Debugger] [%s] '%s' | %s" % (cat, nome, " | ".join(partes))


def _linha_atual(emitidos):
    campos = {k: VALORES_ATUAL.get(k, "-") for k in emitidos}
    return _linha(campos, "Guardian Aura")


def _linha_antiga():
    """A linha do FORMATO ANTIGO, lida da fixture versionada (procedencia no arquivo)."""
    texto = arc.ler_texto(FIXTURE_LOG, "entrada", "log")
    arc.exigir("PROCEDENCIA" in texto and "shrines-exemplo.log" in texto,
               "a fixture %s.entrada.log perdeu a declaracao de PROCEDENCIA" % FIXTURE_LOG)
    for linha in texto.splitlines():
        if "[Status] '%s'" % NOME_NO_LOG in linha:
            return linha
    raise arc.Falhou("nao achei `[Status] '%s'` na fixture %s.entrada.log"
                     % (NOME_NO_LOG, FIXTURE_LOG))


def _ok(censo, linha, emitidos=None):
    return not rd.contrato_da_linha(censo, linha, emitidos)


def _extrai(censo, linha, chave):
    return rd.confere_linha(censo, linha)[2].get(chave)


def corpo():
    emitidos = rd.campos_emitidos(rd.le_fonte("status"), rd.MARCADOR_STATUS)
    atual = _linha_atual(emitidos)
    antiga = _linha_antiga()

    # ------------------------------------------------ 1. formato ATUAL (lido do fonte)
    arc.exigir(emitidos and emitidos[-1] == "desc",
               "o `[Status]` do fonte NAO emite `desc=` por ULTIMO: %r" % (emitidos[-1:] or None))
    arc.igual(rd.contrato_da_linha(CENSO, atual, emitidos), [],
              "a linha no formato ATUAL viola o contrato do censo")
    cat, nome, campos, desc, falhas = rd.confere_linha(CENSO, atual)
    arc.igual((cat, nome, falhas), ("Status", "Guardian Aura", []), "LINE da linha ATUAL")
    arc.igual(desc, VALORES_ATUAL["desc"], "DESC da linha ATUAL")
    arc.igual(campos.get("efeitos"), VALORES_ATUAL["efeitos"],
              "o valor com ASPAS tem de sair inteiro (aspas nao quebram o FIELD)")

    # 2. as chaves que o censo LE para Status estao todas entre as emitidas
    faltando = [k for k in CHAVES_STATUS if k not in emitidos]
    arc.exigir(not faltando,
               "o fonte do `[Status]` deixou de emitir %s - a coluna do censo vira vazia "
               "em SILENCIO" % faltando)

    # ------------------------------------------------ 3. formato ANTIGO (log versionado)
    arc.igual(rd.contrato_da_linha(CENSO, antiga), [],
              "a linha do log ANTIGO (versionado) viola o contrato - a regressao nos dois "
              "sentidos quebrou")
    cat_a, nome_a, campos_a, desc_a, falhas_a = rd.confere_linha(CENSO, antiga)
    arc.igual((cat_a, nome_a, falhas_a), ("Status", NOME_NO_LOG, []), "LINE da linha ANTIGA")
    arc.exigir(desc_a and desc_a.startswith("Critical hit chance"),
               "o DESC da linha antiga nao saiu: %r" % desc_a)
    arc.igual(campos_a.get("nEfeitosDano"), "0", "nEfeitosDano da linha antiga")
    arc.exigir("efeitosDano" in campos_a, "efeitosDano tem de ser extraido da linha antiga")

    # 3b. a AMBIGUIDADE de prefixo do FIELD (`efeitos` x `efeitosRef`, `nEfeitos` x
    #     `nEfeitosRef`): um campo cujo nome COMECA com o de outro nao pode roubar a
    #     leitura - o alternation tem de exigir o `=` (a isca disso e o campo novo com
    #     nome prefixado).
    linha_action = ("[Info   :Roguelike Debugger] [Action] 'Lanca de Fogo' | dano=Fire | "
                    "efeitos=A; B | efeitosRef=C; D | nEfeitos=2 | nEfeitosRef=3 | "
                    "refAcao=R | refStatus= | expr=E1 | danoExpr=E2 | desc=\"faz X.\"")
    arc.igual(rd.contrato_da_linha(CENSO, linha_action), [], "linha de Action no contrato")
    _, _, cam_ac, desc_ac, falhas_ac = rd.confere_linha(CENSO, linha_action)
    arc.igual((falhas_ac, desc_ac), ([], "faz X."), "Action: LINE/DESC")
    arc.igual((cam_ac.get("efeitos"), cam_ac.get("efeitosRef")), ("A; B", "C; D"),
              "o FIELD tem de separar `efeitos` de `efeitosRef`")
    arc.igual((cam_ac.get("nEfeitos"), cam_ac.get("nEfeitosRef")), ("2", "3"),
              "o FIELD tem de separar `nEfeitos` de `nEfeitosRef`")

    # ------------------------------------------------ 4. o contrato MORDE (iscas embutidas)
    # (a) campo DEPOIS do `desc=` -> o DESC perde a descricao.
    depois = atual.replace('desc="%s"' % VALORES_ATUAL["desc"],
                           'desc="%s" | extra=1' % VALORES_ATUAL["desc"])
    arc.exigir(not _ok(CENSO, depois),
               "a isca do campo depois do desc NAO mordeu (o contrato deixaria passar)")
    arc.igual(rd.confere_linha(CENSO, depois)[3], None,
              "com um campo depois do desc, a descricao TEM de sumir (e o defeito)")

    # (b) '|' DENTRO de um valor -> o FIELD trunca o campo em silencio.
    com_barra = atual.replace("efeitos=DamageReduction:Base:", "efeitos=DamageReduction|Base:", 1)
    arc.exigir(not _ok(CENSO, com_barra),
               "a isca do '|' no valor NAO mordeu (o contrato deixaria passar)")
    arc.igual(_extrai(CENSO, com_barra, "efeitos"), "DamageReduction",
              "com '|' no valor, o FIELD trunca o campo (a prova de que '|' quebra)")

    # (c) quebra de linha -> a entrada deixa de ser UMA linha.
    arc.exigir(not _ok(CENSO, atual.replace(" | modelo=", "\n | modelo=")),
               "a isca da quebra de linha NAO mordeu")

    # (d) campo RENOMEADO no dump -> o censo le vazio, sem erro nenhum.
    renomeada = atual.replace("efeitosDano=", "efeitoDano=", 1)
    arc.exigir(_ok(CENSO, renomeada),
               "renomear um campo NAO muda o contrato da linha (as regexes continuam) - "
               "isso e esperado")
    arc.igual(_extrai(CENSO, renomeada, "efeitosDano"), None,
              "campo renomeado TEM de virar chave AUSENTE no censo (o defeito silencioso)")

    # (e) o FONTE reordenado (desc deixa de ser o ultimo) -> a checagem do fonte morde.
    fonte = rd.le_fonte("status")
    alvo = '$"desc=\\"{desc}\\""'
    arc.exigir(fonte.count(alvo) == 1, "ancora do desc no fonte nao e unica: %d" % fonte.count(alvo))
    fonte_reordenada = fonte.replace(alvo, '$"desc=\\"{desc}\\" | extra={tipo}"')
    emitidos_reordenados = rd.campos_emitidos(fonte_reordenada, rd.MARCADOR_STATUS)
    arc.exigir(emitidos_reordenados[-1] == "extra",
               "a isca do fonte reordenado nao pos o campo depois do desc: %r"
               % emitidos_reordenados[-3:])
    arc.exigir(not _ok(CENSO, _linha_atual(emitidos_reordenados), emitidos_reordenados),
               "a isca do fonte reordenado NAO mordeu (desc virou o ultimo de novo?)")

    print("parser do censo: linha ATUAL (%d campos emitidos, desc por ultimo) e ANTIGA (%s) "
          "leem ok; 5 iscas de contrato reprovam pela razao certa"
          % (len(emitidos), NOME_NO_LOG))


if __name__ == "__main__":
    arc.main(META, corpo)
