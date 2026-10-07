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
"""
import os

import comum as C

META = {
    "nome": "aut4-probe-contrato",
    "categoria": "pura",
    "requer": [],
    "descricao": "probe traz gate de autorizacao, NAO_EXERCITADO, PlayerLoop, ScreenCapture, owners "
                 "Harmony, manifest/rollback, sessao do driver (A1) e ida-e-volta opt-in (A6); "
                 "csproj SEM deploy",
}

PROBE = os.path.join(C.caminho_probe(), "AUT4ProbePlugin.cs")
CSPROJ = os.path.join(C.caminho_probe(), "AUT4Probe.csproj")


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


if __name__ == "__main__":
    C.arc.main(META, corpo)
