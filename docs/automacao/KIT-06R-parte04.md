# KIT-06R — parte 04: contraexemplos próprios reais

Comando: `python scratch/kit/KIT-06R-run638/test_revisao_kit06.py` (executado por subprocess, output preservado em reviewer-suite.log; resultado extraído em reviewer-suite.json).
Resultado REAL: `Ran 14 tests`, `FAILED (failures=10)`, exit 1; zero ERROR, zero skip. Quatro positivos passaram: guards com efeito, trava ativa, pausa/retoma do pipeline e limites/indicador nominal.

## ACHADOS confirmados (FALHOU)

F1 — Configuração vazia/inteiramente recusada ativa defaults. `{}` virou 4 bindings; config observar=Return foi recusada mas F7 ainda retornou ação observar. Python linha 169, main 600–601. A permissão efetiva difere da configuração aceita.

F2 — Ações declaradas não realizam contrato. Segundo F7 mantém observando=True apesar do módulo documentar liga/desliga; retomar validado em F6 retorna None e pipeline permanece pausado=True. Python 283/299/293; C# despacha mesmas ações, mas falta retomar e toggle.

F3 — Indicador não mede efeito. Estado parado permitiu registrar clique real no pipeline (quadro 1); sem pipeline F7 produz estado observando. Python construtor 178–188 e indicador 443–450; início 305–309. Assim ausência não é explicitada e coleta pode contrariar indicador.

F4 — Export perde a evidência da coleta. Arquivo real anuncia eventos=1 mas não contém id do evento, dados ou pedido de captura. `guard_chat` presente na memória também desaparece no export. Python documento_export 420–438; C# DocumentoExport 362–381.

F5 — Export não é falha-segura: pasta configurada apontando a arquivo-sentinela provoca FileExistsError propagado por F10 (zero ERROR de teste, exceção capturada e asserção reprovada). Python 411–416; C# IO 399–403 sem catch. Não houve escrita no perfil.

## Lacuna de API, não automaticamente ACHADO

Teste de limpar janela com None falhou (InventoryPanel retido). API usa None para manter campo, e pode representar vazio por string vazia; sem contrato explícito de fechamento de janela, esta expectativa é hipótese INDETERMINADO, não contada como bug confirmado. Necessário definir forma clara antes de integração runtime.

## Build refeito por abordagem distinta PASSOU offline

Captura de bytes, arquivo bruto build-raw.stdout + build-raw.stderr; cópia legível cp850 em build.log. Comando dotnet build ...KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false dentro da sandbox: exit 0, 0 Erro(s), 1 Aviso(s) MSB3277 (referência System.Net.Http). Compilação não prova UI/runtime.

Próximas provas: defeitos plantados próprios, equivalência C# e discriminador negativo, export KIT-07 vivo; preservar fonte original e não consertar produto nesta revisão.
