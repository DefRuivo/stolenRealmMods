#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SANEAMENTO do dump (TST-5) - valores sujos e campos ausentes.

O QUE ESTE TESTE PRENDE (e por que existe)
------------------------------------------
O censo so consegue ler o dump se os valores couberem na regra: sem `|` (o `FIELD` usa
`[^|]+` - um `|` TRUNCA o campo em silencio), sem quebra de linha (a linha se parte) e
sem surpresa. O mod tem o `EfeitosInfo.Limpa` (e os `Limpa` dos patches) para isso, e o
RD-2F acrescentou o marcador `!erro:<Tipo>`: um campo que EXPLODE sai como marcador no
proprio campo, com a linha (e as seguintes) saindo normalmente - a falha e barulhenta,
nunca um dump truncado em silencio.

ESTE TESTE EXIGE
----------------
  1. O MODELO do `Limpa`: `|`->`/`, aspas->`'`, LF/CR->espaco, vazio/nulo->"" e Trim.
  2. O MODELO do `Valor`: nulo->`-`, string vazia->`-`, array->`[N]` (valor vazio NAO
     e valor inventado).
  3. O FONTE VIVO: o `Limpa` faz as QUATRO trocas + Trim, o `Valor` usa `Limpa`, e o
     marcador `!erro:` e seguro para o parser (sem `|`/aspas/quebra).
  4. A PROVA, no parser real, de que um `|` no valor TRUNCA o campo - o motivo de o
     saneador existir.
  5. Campos AUSENTES: linha sem um campo -> chave ausente (o `.get(chave, "")` do censo
     devolve vazio, nao estoura); a entrada `[Summon]` nao tem `desc=` POR DESENHO.

PROVA DE FOGO
-------------
Isca embutida (cada troca do `Limpa` removida numa copia em memoria -> a checagem
REPROVA) + a prova FISICA no `EfeitosInfo.cs` real (restaurado byte a byte) em
`tools/testes/debugger-prova-de-fogo.log`.

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao executa o C# do mod: o modelo Python espelha a conta e a ESTRUTURA do fonte vivo
prende os dois.
"""
import arcabouco as arc
import regras_debugger as rd

META = {
    "nome": "debugger-saneamento",
    "categoria": "pura",
    "requer": [],
    "descricao": ("Limpa/Valor saneiam '|', aspas, quebra de linha, vazio e nulo; o marcador "
                  "`!erro:` e seguro; um '|' no valor trunca o campo no parser real; campos "
                  "ausentes viram vazio e o Summon nao tem desc (isca embutida)"),
}

CENSO = rd.carrega_censo()

# (entrada, saida esperada do Limpa) - a regra transcrita do EfeitosInfo.cs.
CASOS_LIMPA = (
    ("a|b", "a/b"),
    ('a"b', "a'b"),
    ("a\nb", "a b"),
    ("a\r\nb", "a  b"),
    ("  x  ", "x"),
    ("|", "/"),
    ("", ""),
    (None, ""),
    ("normal", "normal"),
)


def _linha(campos, nome, cat="Status", com_desc=True):
    partes = []
    for k, v in campos.items():
        if k == "desc" and com_desc:
            partes.append('desc="%s"' % v)
        else:
            partes.append("%s=%s" % (k, v))
    return "[Info   :Roguelike Debugger] [%s] '%s' | %s" % (cat, nome, " | ".join(partes))


def corpo():
    # ------------------------------------------------ 1. o MODELO do Limpa
    for entrada, esperado in CASOS_LIMPA:
        arc.igual(rd.limpa(entrada), esperado, "Limpa(%r)" % entrada)

    # ------------------------------------------------ 2. o MODELO do Valor
    arc.igual(rd.valor_do_campo(None), "-", "Valor(nulo)")
    arc.igual(rd.valor_do_campo(""), "-", "Valor(string vazia) - nao inventa valor")
    arc.igual(rd.valor_do_campo("x|y"), "x/y", "Valor passa a string pelo Limpa")
    arc.igual(rd.valor_do_campo(["a", "b", "c"]), "[3]", "Valor de array = [N]")
    arc.igual(rd.valor_do_campo("ok"), "ok", "Valor de string normal")

    # ------------------------------------------------ 3. o FONTE VIVO
    cod_efeitos = rd.le_fonte("efeitos")
    cod_status = rd.le_fonte("status")
    falhas = rd.falhas_do_saneamento(cod_efeitos, cod_status)
    arc.exigir(not falhas,
               "o saneamento do dump regrediu em %d ponto(s):\n  - %s"
               % (len(falhas), "\n  - ".join(falhas)))

    # ------------------------------------------------ 4. o parser real: '|' trunca
    campos_sujos = {"tipo": "Normal", "efeitos": "A|B", "nEfeitosDano": "0",
                    "desc": "linha de teste."}
    linha_suja = _linha(campos_sujos, "Alvo")
    cat, nome, campos, desc, f = rd.confere_linha(CENSO, linha_suja)
    arc.igual(campos.get("efeitos"), "A",
              "com '|' no valor o FIELD tem de TRUNCAR (o motivo do saneador); obtido %r"
              % campos.get("efeitos"))
    arc.exigir(rd.contrato_da_linha(CENSO, linha_suja),
               "o contrato nao acusou o '|' no valor")
    # O MESMO valor JA saneado nao quebra:
    linha_limpa = _linha(dict(campos_sujos, efeitos=rd.limpa("A|B")), "Alvo")
    arc.igual(rd.contrato_da_linha(CENSO, linha_limpa), [], "o valor saneado passa")

    # ------------------------------------------------ 5. campos AUSENTES
    # (a) a linha ANTIGA nao tem os campos do RD-2: a chave fica AUSENTE (o `.get(...,"")`
    #     do censo devolve vazio, nao estoura).
    log = arc.ler_texto("debugger-parser-contrato", "entrada", "log")
    antiga = next((l for l in log.splitlines() if "[Status] 'Conqueror Aura'" in l), None)
    arc.exigir(antiga, "nao achei a linha antiga na fixture versionada")
    _, _, campos_antigos, _, _ = rd.confere_linha(CENSO, antiga)
    for ausente in ("tick", "auraSts", "expr", "danoExpr"):
        arc.exigir(ausente not in campos_antigos,
                   "%r nao e campo do formato antigo - ele nao pode aparecer" % ausente)
        arc.igual(campos_antigos.get(ausente, ""), "",
                  "campo ausente %r tem de virar vazio (nao estoura)" % ausente)

    # (b) a entrada `[Summon]` NAO tem `desc=` por desenho: o DESC devolve None e o
    #     parser tolera (`cat != "Summon"` na contagem de truncadas).
    summon = _linha({"sorteio": "sim", "criaturas": "Raven[]"}, "Nature Summoning I",
                    cat="Summon", com_desc=False)
    cat_s, _, _, desc_s, _ = rd.confere_linha(CENSO, summon)
    arc.igual((cat_s, desc_s), ("Summon", None), "Summon sem desc= (por desenho)")
    arc.exigir('cat != "Summon"' in rd.le_censo_texto(),
               "o censo perdeu a excecao do Summon na contagem de descricao truncada")

    # ------------------------------------------------ 6. ISCAS embutidas (o fonte MORDE)
    iscas = {}
    # (a) o Limpa perde a troca do separador - o defeito classico.
    alvo = '.Replace("|", "/")'
    if cod_efeitos.count(alvo) == 1:
        iscas["sem-barra"] = cod_efeitos.replace(alvo, "")
    # (b) o Limpa perde a troca de aspas.
    alvo = '.Replace("\\"", "\'")'
    if cod_efeitos.count(alvo) == 1:
        iscas["sem-aspas"] = cod_efeitos.replace(alvo, "")
    # (c) o Limpa perde o Trim.
    alvo = ".Replace(\"\\\"\", \"'\").Trim();"
    if cod_efeitos.count(alvo) == 1:
        iscas["sem-trim"] = cod_efeitos.replace(alvo, ".Replace(\"\\\"\", \"'\");")
    # (d) o marcador deixa de ser seguro (ganha um '|').
    alvo = 'return "!erro:" + e.GetType().Name;'
    if cod_status.count(alvo) == 1:
        iscas["marcador-com-barra"] = cod_status.replace(alvo, 'return "!erro|" + e.GetType().Name;')

    arc.exigir(set(iscas) >= {"sem-barra", "sem-aspas", "sem-trim", "marcador-com-barra"},
               "as ancoras do plantio nao acharam o trecho: %s" % sorted(iscas))
    for nome in sorted(iscas):
        cod_e = iscas[nome] if "marcador" not in nome else cod_efeitos
        cod_s = iscas[nome] if "marcador" in nome else cod_status
        f = rd.falhas_do_saneamento(cod_e, cod_s)
        arc.exigir(f, "o defeito plantado '%s' PASSOU pela checagem (ela nao morde)" % nome)

    # Isco do MODELO: um Limpa sem a troca do '|' deixaria o valor sujo passar.
    def limpa_fraco(s):
        return (s or "").replace("\n", " ").replace("\r", " ").replace('"', "'").strip()

    arc.exigir(limpa_fraco("A|B") != rd.limpa("A|B"),
               "a isca do modelo (Limpa sem a troca do '|') nao morde")

    print("saneamento: %d casos de Limpa, 5 de Valor, fonte vivo ok; %d isca(s) do fonte "
          "reprovam pela razao certa; '|' no valor trunca no parser real" % (len(CASOS_LIMPA), len(iscas)))


if __name__ == "__main__":
    arc.main(META, corpo)
