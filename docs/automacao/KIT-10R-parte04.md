# KIT-10R — run663 — parte04: sandbox e primeiros achados

## Identidade e isolamento — PASSOU

Comando real `python scratch/kit/KIT-10R-run663/prepare_sandbox.py`, exit 0:
`FILES 1156 COPY_HASH_MATCH 1156`, `NO_GIT True NO_DLL True`.
Sandbox própria: C:/dev/stolen-realm/scratch/kit/KIT-10R-run663/sandbox.
Manifesto completo: scratch/kit/KIT-10R-run663/manifest.json. Cópia dirigida de fontes/dados/docs tracked e untracked, sem .git, binários, credenciais/perfil; não é réplica para build C# (build NÃO_EXERCITADO).

SHA256 confrontados com handoff vigente, iguais:
- kit10_cenarios.py: 8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092
- test_kit10_cenarios.py: 6cc5003e0d9facd42cf967b2da480216243b6d902376f5fc20d9c49d9e8db6e2
- prova_red_kit10_guardas2.py: aa9f232b78b0e4cda8ca6de63bcda417cb1b5c79b635ad6235151177c834c6ff
Reusos: CIC-4 65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199; AUT-7 49cd80b641bff189f822ca28d89a6c9f659ccf845092a47f468ee82c518cc975; regras_shrine 1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562; regras_debugger 9e1cdd00b142a8b28aa0f06e8a129229a37702c381e30627054d223f6d1e30e7.

## Execução própria — FALHOU (10 falsos OK)

`python scratch/kit/KIT-10R-run663/test_review_kit10.py` redirecionado a review-output.txt; exit capturado 1. unittest: `Ran 45 tests in 0.668s`, `FAILED (failures=10)`, zero errors, zero skipped. Driver shell apenas extraiu resumo e saiu 0; NÃO confundir com exit 1 real do teste.
Prova de efeito: review-results.json contém cada critério retornado e observação/evidência. Constantes e expectativas próprias; não importa corpo/testes do autor. Cadeia rotulada runtime é SIMULAÇÃO OFFLINE para exercitar o avaliador, não prova do jogo/DLL. DLL declarada é explicitamente simulada; fonte SHA é o real da cópia.

Achados preliminares a reconferir:
- F8: fonte_bonus/dano_observado/contrib_observada = string JSON válida `NaN` produz OK/prova_runtime=True (três casos). Comparador abs(NaN)>limiar não pega defeito.
- F9: Worship recebe contagem ausente ou zero, item fracionário 2.9, aura inventada ou somente uma instância e ainda declara OK/dobro preservado (cinco casos). Defaults/coerções/vacuidade escondem medição não feita.
- F10: Debugger desc com pipe ou log misto com linha dump não reconhecida produz OK/prova_runtime=True (dois casos). Contrato sem truncamento incompleto.

Controles positivos A/B/C/D e guardas antigas, fonte/dano/contrib errados, dobro removido, boot, identidade errada e evidência alterada passaram os asserts próprios; consolidar contagem e negativos seletivos após provas RED.

## Cobertura BetterStats — pendência

AUT-7 linhas 1078–1097 sempre declara base/final NAO_EXERCITADO ou INDETERMINADO; nem campos extras resolvem. KIT-10 só delega. Avaliar se aceite de completar campos foi cumprido sem substituir runtime real por fixture; lacuna nunca verde.
