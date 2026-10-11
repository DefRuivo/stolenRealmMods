# KIT-14 — run699: builds executadas; primeiro harness vermelho preservado

## Execução real

`python scratch/kit/KIT-14-run699/test_qualificar.py` — exit 1; `Ran 7 tests`, 2 failures + 2 errors + 0 skip. qualification.log e offline-result.json preservam o resultado, sem apresentá-lo como verde.

- Guarda positiva de deploy exit0; XML sem opt-in plantado exit1.
- AUT4Probe e KIT04Adapter.SR (inclui Core) compilaram na sandbox com DeployToBepInEx=false e USERPROFILE/APPDATA/LOCALAPPDATA redirecionados no ambiente e MSBuild; preflight real antes de cada build exit0.
- AUT4Probe: 0 erros, 1 aviso; SHA256 679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57, 56320 bytes.
- Adapter/Core: 0 erros, 65 avisos; Adapter SHA256 ab2da7587436b9457d152b110ef50014567d430747f85794678e0ab08456f3b0, 31744 bytes.
- Avisos (nullable e System.Net.Http) não ocultados; logs brutos individuais no diretório logs/.
- Fonte vivo 1343 arquivos e 3 árvores pessoais (53/111/5 arquivos) reconferidos byte a byte, sem divergência. Nenhuma DLL carregada em jogo.

## Falha do harness e discrepância de pacote

O CLl montar retornou exit0 e `veredito=PACOTE_LIMPO`, como o fonte pacote.py:270 realmente define; o harness cobrou equivocadamente `OK` (veredito da operação verificar), portanto reprovou antes de extrair. Os failures/errors seguintes são cascata dessa precondição ausente, não quatro defeitos independentes do produto.

Não alterar o produto nem seus critérios. Corrigir somente o harness após confronto com stdout e código; reusar builds e pacote já feitos, sem repetir o trabalho pronto, e guardar execução original.

Montagem inicial tem 39 membros/38 payload, enquanto a revisão KIT-15F declarou 42/41. A cópia inicial preservou tracked/untracked, mas arquivos ignorados necessários ao pacote podem ter ficado fora. Investigar por manifesto e fonte vivo antes de usar esse candidato como pacote entregue; não afirmar identidade com KIT-15F até confronto completo. Este é um achado de preparo a resolver, não aprovação.

Runtime/save descartável/UI/desempenho continuam NAO_EXERCITADO. Não pedir novos limiares nem inferir isolamento do save pessoal.
