#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4/COR-AUT4 — contrato ESTATICO do probe C# e da seguranca do projeto.

Nao executa Unity (nao ha jogo nesta rodada): le os FONTES do probe e cobra os
marcadores que a tarefa exige. E o contrato que a rodada runtime vai exercer.

COR-AUT4:
  A1 — o probe tem de LER a chave `Sessao` do `.cfg` (a sessao da rodada e gerada
       pelo DRIVER; a evidencia sem ela nao pertence a rodada).
  A6 — porta OPT-IN de ida-e-volta (leitura): `DemostrarTooltip` default FALSE,
       `MarcadorIdaEVolta`, chamada REAL de `Tooltip.ShowTooltip` e releitura do
       titulo, com o resultado registrado em `ida_e_volta` (declarado como LEITURA,
       nunca como simulacao do produto).

AUD-1 (`t_6db50f7a`) — AGREGADOS portados do CAP-1 e IDENTIDADE do instrumento:
  * `LeituraAgregados.cs` e um componente ISOLADO (estatico, sem instancia do plugin,
    sem estado mutavel) e SOMENTE LEITURA — o inventario por shader/fonte, as fontes em
    memoria (com `ShaderUtilities.ShaderRef_MobileSDF`) e a lista do que a tela JA
    DESENHOU. O porte e conferido contra o CAP-1 (`scratch/cap1/CapProbe`), que e o
    instrumento historico da medicao.
  * L1 da AUD-1: o JSON do probe passa a carregar a IDENTIDADE do binario —
    `hash_fonte_declarado` (do `.cfg`) e `hash_dll_do_probe` CALCULADO no runtime
    (sha256 do proprio assembly). Nenhum hash de 64 hex pode estar escrito no fonte:
    hash hardcoded seria valor declarado passando por medicao.
  * A COSTURA probe x coletor: todo campo de `coletor.CAMPOS` (o que o driver MEDE) tem
    de ser emitido pelo probe — e os agregados novos sao CONTEXTO de topo, nao campo de
    observacao (`campos_alvo` fora do schema e plano invalido, A2 da AUT-4R2).
  * O rotulo "espelho do criterio do BetterFont" do `criterio_de_efeito` e CONFERIDO
    contra a fonte espelhada (`BetterFont/Plugin.cs`: `TemEfeitoNoMaterial` ->
    `SombraDesenhada`, BF-5) — a sombra so conta quando esta DESENHADA (keyword ligada
    ou offset/dilate != 0), nunca pela cor com alfa. Isca:
    `contra-prova/cp_aut4probe_isca_sombra_por_cor.py`.
"""
import os
import re

import comum as C

META = {
    "nome": "aut4-probe-contrato",
    "categoria": "pura",
    "requer": [],
    "descricao": "probe traz gate de autorizacao, NAO_EXERCITADO, PlayerLoop, ScreenCapture, owners "
                 "Harmony, manifest/rollback, sessao do driver (A1), ida-e-volta opt-in (A6), os "
                 "agregados isolados do CAP-1 (inventario/fontes/textos visiveis) e a identidade do "
                 "fonte/DLL dentro do JSON (L1); csproj SEM deploy",
}

PROBE = os.path.join(C.caminho_probe(), "AUT4ProbePlugin.cs")
CSPROJ = os.path.join(C.caminho_probe(), "AUT4Probe.csproj")


# ---- fidelidade do rotulo "espelho do criterio do BetterFont" (BF-5) ----------
# O `criterio_de_efeito` emitido no JSON e o numero `textos_com_efeito_no_material`
# se APRESENTAM como espelho do criterio do BetterFont. Espelho se confere contra a
# FONTE espelhada (`BetterFont/Plugin.cs`: TemEfeitoNoMaterial -> SombraDesenhada),
# nunca contra a propria afirmacao: foi assim que a redacao herdada do CAP-1 passou a
# mentir — dizia espelhar o mod e media `_UnderlayColor.a`, que o mod NAO olha (a
# sombra INERTE que o shader nao desenha, BF-5/`Plugin.cs:1196-1234`).

BETTERFONT = os.path.join(C.REPO, "BetterFont", "Plugin.cs")
RE_TOKENS_DE_SOMBRA = re.compile(r"\b(UNDERLAY_[A-Z_]+|_Underlay[A-Za-z]+)\b")


def _corpo_da_funcao(texto, assinatura):
    """Corpo (entre as chaves) da funcao cuja assinatura contem `assinatura`.

    Devolve `None` quando nao acha (a ausencia e DEFEITO de quem chama, nao excecao:
    quem chama o teste de fidelidade precisa poder DIZER o que faltou)."""
    inicio = texto.find(assinatura)
    if inicio < 0:
        return None
    abre = texto.find("{", inicio)
    if abre < 0:
        return None
    profundidade = 0
    for i in range(abre, len(texto)):
        if texto[i] == "{":
            profundidade += 1
        elif texto[i] == "}":
            profundidade -= 1
            if profundidade == 0:
                return texto[abre + 1:i]
    return None


def conferir_espelho_da_sombra(texto_agregado, texto_betterfont):
    """Lista de defeitos do ramo da SOMBRA do agregado contra o BetterFont.

    Vazia = o probe realmente espelha `SombraDesenhada` do mod: mesma keyword
    (`UNDERLAY_ON`/`UNDERLAY_INNER`) e mesma geometria (`_UnderlayOffsetX`/
    `_UnderlayOffsetY`/`_UnderlayDilate`) — e a cor `_UnderlayColor` FORA do criterio."""
    corpo_bf = _corpo_da_funcao(texto_betterfont, "bool SombraDesenhada(Material")
    if corpo_bf is None:
        return ["nao achei SombraDesenhada em %s — sem ela nao ha espelho a conferir" % BETTERFONT]
    esperado = sorted(set(RE_TOKENS_DE_SOMBRA.findall(corpo_bf)))

    corpo_efeito = _corpo_da_funcao(texto_agregado, "bool EfeitoNoMaterial(Material")
    if corpo_efeito is None:
        return ["nao achei EfeitoNoMaterial em LeituraAgregados.cs"]

    defeitos = []
    if "SombraDesenhada(" not in corpo_efeito:
        defeitos.append("EfeitoNoMaterial nao delega a sombra a SombraDesenhada (como o "
                        "BetterFont: TemEfeitoNoMaterial -> SombraDesenhada)")
    if "_UnderlayColor" in corpo_efeito:
        defeitos.append("EfeitoNoMaterial le _UnderlayColor: cor com alfa NAO e sombra "
                        "desenhada (sombra INERTE do jogo, BF-5)")

    corpo_sombra = _corpo_da_funcao(texto_agregado, "bool SombraDesenhada(Material")
    if corpo_sombra is None:
        defeitos.append("o agregado nao tem SombraDesenhada: a sombra ficou inline, sem espelho")
    else:
        obtido = sorted(set(RE_TOKENS_DE_SOMBRA.findall(corpo_sombra)))
        if obtido != esperado:
            defeitos.append("o ramo da sombra nao espelha SombraDesenhada do BetterFont: "
                            "esperado %s, obtido %s" % (esperado, obtido))
        if "_UnderlayColor" in corpo_sombra:
            defeitos.append("o ramo da sombra le _UnderlayColor: cor com alfa NAO e sombra "
                            "desenhada (sombra INERTE do jogo, BF-5)")
    return defeitos


def corpo():
    for p in (PROBE, CSPROJ):
        C.arc.exigir(os.path.isfile(p), "fonte do probe ausente: %s" % p)
    cs = open(PROBE, encoding="utf-8").read()
    proj = open(CSPROJ, encoding="utf-8").read()

    # 1. gate de autorizacao com default false
    C.arc.exigir("Autorizado" in cs, "o probe precisa da chave de autorizacao")
    C.arc.exigir("NAO_EXERCITADO" in cs, "sem autorizacao o probe tem de devolver NAO_EXERCITADO")

    # 2. driver independente do Update do plugin destruido
    C.arc.exigir("PlayerLoop" in cs, "o motor tem de ser injetado no PlayerLoop (nao depender do Update do plugin)")

    # 3. leitura do objeto vivo: TMP + material/cor/geometria/owners
    for marcador in ("TMP_Text", "fontSharedMaterial", "GetWorldCorners", "GetPatchInfo",
                     "IsKeywordEnabled", "_FaceColor", "_OutlineColor"):
        C.arc.exigir(marcador in cs, "leitura do objeto vivo sem o marcador %r" % marcador)

    # 4. PNG pela API do Unity (nao print de desktop)
    C.arc.exigir("ScreenCapture.CaptureScreenshot" in cs, "o PNG tem de sair pela API do Unity")

    # 5. espera de ESTADO + timeout/orcamento (nao sleep cego)
    C.arc.exigir("Orcamento" in cs or "budget" in cs.lower(), "o probe precisa de teto de tempo")
    C.arc.exigir("GetParsedText" in cs, "a espera de estado usa texto renderizado de verdade")

    # 6. manifest + rollback (arquivos que o probe cria)
    C.arc.exigir("manifest" in cs.lower(), "o probe precisa montar o manifest dos artefatos")
    C.arc.exigir("rollback" in cs.lower() or "restaur" in cs.lower(),
                 "o probe precisa declarar o que criou, para o rollback exato")

    # 7. sem deploy: o csproj do probe NAO pode ter alvo DeployToBepInEx
    C.arc.exigir("DeployToBepInEx" not in proj, "csproj do probe com alvo de deploy — proibido")
    C.arc.exigir("netstandard2.1" in proj, "TargetFramework esperado netstandard2.1")

    # 8. guarda de null do CLR (ReferenceEquals), NUNCA o `==` da Unity.
    #    O GameObject do plugin e DESTRUIDO na 1a cena => "fake null": `i == null`
    #    responde True e o gancho/motor fica MUDO (achado A3 da AUT-4R). O driver
    #    do PlayerLoop segue como caminho principal (nao depende da instancia).
    C.arc.exigir("ReferenceEquals" in cs,
                 "gancho/motor tem de usar ReferenceEquals (null do CLR), nao o == fake-null da Unity")
    C.arc.exigir("(i == null)" not in cs and "(i != null)" not in cs,
                 "guarda fake-null (operador == da Unity sobre a instancia) ainda presente no probe")
    C.arc.exigir("PlayerLoop" in cs and "SetPlayerLoop" in cs,
                 "o driver principal no PlayerLoop tem de ser preservado")

    # 9. A1: a sessao e do DRIVER (lida do .cfg), nao um carimbo inventado do probe
    C.arc.exigir('Config.Bind("Geral", "Sessao"' in cs,
                 "A1: o probe tem de LER a chave 'Sessao' do cfg (sessao da rodada, do driver)")
    C.arc.exigir("_sessaoCfg" in cs and 'DateTime.Now.ToString' in cs,
                 "A1: a sessao do cfg tem de VENCER o carimbo local (fallback declarado)")

    # 10. A6: porta opt-in de ida-e-volta — LEITURA, default FALSE
    C.arc.exigir('Config.Bind("Geral", "DemostrarTooltip", false' in cs,
                 "A6: 'DemostrarTooltip' tem de existir com default FALSE (opt-in)")
    C.arc.exigir('Config.Bind("Geral", "MarcadorIdaEVolta"' in cs,
                 "A6: o marcador da ida-e-volta tem de ser configuravel")
    C.arc.exigir("ShowTooltip" in cs and "ChamarShowTooltip" in cs,
                 "A6: a ida-e-volta tem de chamar o HANDLER REAL Tooltip.ShowTooltip")
    C.arc.exigir('ida_e_volta' in cs and '"conferiu"' in cs,
                 "A6: o resultado da ida-e-volta tem de ser registrado por observacao de rodada")
    C.arc.exigir("LEITURA" in cs and "ida-e-volta" in cs,
                 "A6: a porta tem de estar DECLARADA como leitura (nao como simulacao do produto)")
    C.arc.exigir("if (_demostrar.Value)" in cs,
                 "A6: a porta so pode agir quando o cfg autoriza (opt-in de verdade)")

    # 11. AUD-1: AGREGADOS do CAP-1, portados para um COMPONENTE ISOLADO.
    # O leitor por objeto sozinho nao ve o TODO: falta o inventario por shader/fonte, as
    # fontes em memoria (com o shader de REFERENCIA do proprio TMP) e o que a tela JA
    # desenhou. Sao esses tres agregados que fecham a leitura "por objetos".
    agreg = os.path.join(C.caminho_probe(), "LeituraAgregados.cs")
    C.arc.exigir(os.path.isfile(agreg), "AUD-1: componente isolado ausente: %s" % agreg)
    ag = open(agreg, encoding="utf-8").read()
    for marcador in ("internal static class LeituraAgregados", "internal delegate",
                     "LeitorDeTexto", "Inventario(", "Fontes(", "TextosVisiveis(",
                     "por_shader", "por_fonte", "por_combo_shader_fonte", "amostra_regra",
                     "criterio_de_efeito", "textos_com_efeito_no_material", "Incrementa",
                     "ShaderRef_MobileSDF", "shader_de_referencia_mobile_sdf_do_tmp",
                     "shader_suportado", "GetParsedText", "EfeitoNoMaterial", "TexturaDeEfeito"):
        C.arc.exigir(marcador in ag, "AUD-1: agregado do CAP-1 nao portado — falta %r" % marcador)

    # 11.1 ISOLAMENTO: o componente nao conhece a instancia do plugin nem guarda estado, e
    #      e SOMENTE LEITURA (nenhum setter/keyword/destroy no material que ele le).
    C.arc.exigir("Instancia" not in ag,
                 "AUD-1: o componente agregado nao pode depender da instancia do plugin (isolamento)")
    for proibido in ("EnableKeyword(", "DisableKeyword(", "SetColor(", "SetFloat(",
                     "SetTexture(", "SetVector(", "SetDirty(", "Destroy(", ".text ="):
        C.arc.exigir(proibido not in ag,
                     "AUD-1: escrita no jogo dentro do agregado (%r) — o componente e leitura apenas" % proibido)

    # 11.3 FIDELIDADE DO ROTULO "espelho": `criterio_de_efeito` (e o numero
    #      `textos_com_efeito_no_material`) se apresentam como espelho do criterio do
    #      BetterFont — entao o criterio do probe e MEDIDO contra a fonte do mod, nao
    #      apenas afirmado. (Achado da revisao da tarefa: a redacao herdada do CAP-1
    #      dizia espelhar `TemEfeitoNoMaterial` e media `_UnderlayColor.a`, que o mod
    #      nao olha — sombra INERTE, BF-5.)
    C.arc.exigir(os.path.isfile(BETTERFONT),
                 "fidelidade: fonte espelhada ausente em %s — sem ela o rotulo 'espelho do "
                 "criterio do BetterFont' nao pode ser conferido" % BETTERFONT)
    with open(BETTERFONT, encoding="utf-8") as fh:
        fonte_betterfont = fh.read()
    defeitos_espelho = conferir_espelho_da_sombra(ag, fonte_betterfont)
    C.arc.exigir(not defeitos_espelho,
                 "fidelidade: o criterio de EFEITO nao espelha o BetterFont que ele nomeia — %s"
                 % "; ".join(defeitos_espelho))

    # 11.2 o probe USA os tres agregados (a fase de leitura) e os declara no JSON de topo.
    for chamada in ("LeituraAgregados.Inventario(", "LeituraAgregados.Fontes()",
                    "LeituraAgregados.TextosVisiveis("):
        C.arc.exigir(chamada in cs, "AUD-1: o probe nao chama %s na fase de leitura" % chamada)
    for chave in ('_res["inventario"]', '_res["fontes"]', '_res["textos_visiveis"]'):
        C.arc.exigir(chave in cs, "AUD-1: o probe nao emite %s no JSON" % chave)

    # 12. L1 da AUD-1: IDENTIDADE do binario DENTRO do JSON do instrumento.
    ident = os.path.join(C.caminho_probe(), "IdentidadeDoProbe.cs")
    C.arc.exigir(os.path.isfile(ident), "L1: componente de identidade ausente: %s" % ident)
    idn = open(ident, encoding="utf-8").read()
    for marcador in ("SHA256", "ComputeHash", "Assembly", "hash_dll_do_probe",
                     "hash_fonte_declarado", "bytes_dll_do_probe", "erro"):
        C.arc.exigir(marcador in idn, "L1: identidade do instrumento sem %r" % marcador)
    C.arc.exigir('_res["identidade"] = IdentidadeDoProbe.Identidade(_hashFonte.Value)' in cs,
                 "L1: o JSON do probe tem de carregar o bloco 'identidade' (hash do fonte e da DLL)")
    C.arc.exigir("provar_atualidade" not in cs,
                 "L1: a conferencia do hash e do DRIVER (o probe declara, nao se autoconfere)")

    # 12.1 nenhum hash de 64 hex pode estar ESCRITO no fonte: hash hardcoded e declaracao
    #      posando de medicao. A identidade tem de sair do sha256 do arquivo carregado.
    for nome, texto in (("AUT4ProbePlugin.cs", cs), ("IdentidadeDoProbe.cs", idn)):
        C.arc.exigir(not re.search(r"[0-9a-fA-F]{64}", texto),
                     "L1: hash de 64 hex HARDCODED em %s — valor declarado passando por medicao" % nome)

    # 13. COSTURA probe x coletor: todo campo que o DRIVER mede tem de ser emitido pelo
    #     probe (campo medido e nao emitido seria lacuna silenciosa).
    col = C.coletor()
    nao_emitidos = [c for c in col.CAMPOS if ('"%s"' % c) not in cs]
    C.arc.exigir(not nao_emitidos,
                 "costura: o coletor mede campo que o probe nao emite: %s" % nao_emitidos)

    # 13.1 os agregados novos sao CONTEXTO de topo, NAO campo de observacao: nao podem
    #      entrar no schema de `campos_alvo` (A2: alvo fora do schema => plano invalido).
    for chave in ("inventario", "fontes", "textos_visiveis", "identidade", "marcos"):
        C.arc.exigir(chave not in col.CAMPOS_TODOS,
                     "costura: %r virou campo de observacao — agregado de topo nao e alvo medivel" % chave)


if __name__ == "__main__":
    C.arc.main(META, corpo)
