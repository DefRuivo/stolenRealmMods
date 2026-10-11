# KIT-06R — parte 05: equivalência C#, defeitos plantados e export vivo

Execução própria: `python scratch/kit/KIT-06R-run638/exercita_adversarios.py`, exit 0 do driver. Logs por comando preservam exit interno (verde do driver não aprova o produto).

## C# fontes reais compilados por LINK

`dotnet run --project scratch/kit/KIT-06R-run638/harness-reviewer/Review.csproj -p:DeployToBepInEx=false`: exit 1, 4 OK / 8 FAIL (reviewer-csharp.log).
Reproduz F2 (F7 toggle e retomar), F3 (parado com registro e sem pipeline observando), F4 (evento+guard ausentes no export), F5 (IOException propagado). Config vazia C# passa: o bypass F1 é específico Python.

F6 adicional — Evidência C# mutável pelo consumidor: `Marcacoes()[0]["descricao"]` alterada fora da ponte modifica a marcação interna e o export seguinte; listas novas compartilham dicionários vivos. PonteControleRSTV.cs:378/474–476. Python devolve dict cópia, C# não. NÃO houve mutação de gameplay; apenas sandbox offline.

F7 adicional — Oráculo C# dá falso verde com falha estranha ao controle. Fonte sandbox mutado ConsomeInput=false->true; normal: 43 OK / 1 FALHA, exit 1. `--defeito guard`: 40 OK / 4 FALHA mas exit 0 (3 esperadas + consumo de input extra). `--defeito inventado`: 43 OK / 1 FALHA, exit 0 com falha não relacionada. Program.cs:38–41 aceita qualquer valor e :63–76 só exige alguma falha. Controle negativo precisa conjunto exato e rejeição de nomes desconhecidos; não esconder falhas extras. Logs harness-defeito-real-input/falso-verde-guard/defeito-desconhecido.log.
Restaurado byte a byte e recompilado: 44 OK/0 FALHA exit 0 (harness-restaurado.log), hash da ponte novamente 6bfe3db1... . Normal original guard=41/3 e ataque=42/2, ambos exit 0, reexecutados.

## Contra-prova dos quatro oráculos próprios positivos

Defeitos reais em arquivos mutado-guard/modo/pausa/limites.py (somente scratch): guard removido; modo ativo indevido; delegação da pausa removida; retenção de degradações removida. Cada oráculo: Ran 1 test, 1 failure, 0 error, 0 skip (exit lógico unittest 1). contra-prova-revisor.json e cp-revisor-*.log. Testes discriminam efeito, não fixture runtime. Fontes vivos intocados.

## KIT-07 disponível mas sem integração do botão

API real exportador.montar_pacote exercitada: export local KIT-06 contém e-mail sintético revisao@example.invalid; consumo manual pelo KIT-07 produz 1 arquivo, e-mail bruto ausente. contrato_kit07 continua NAO_IMPLEMENTADO. integracao-kit07.json registra leitura posterior dos dois arquivos. Isso prova consumo por diretório possível, não integração sem terminal. Export KIT-06 é bruto/local; não chamar compartilhável/sanitizado. Critério integração efetiva: FALHOU/lacuna, a corrigir sem acoplar obrigatoriamente mods. UI/G2/runtime continuam NAO_EXERCITADO.

## Preservação e obstáculos

Comparação independente dos 188 hashes vivos iniciais: DRIFT [] (inclui lib/produto e fontes novos). DLLs build sandbox: Adapter ffe8108296e47661d0daf7f0fc430b3e41d069669fc7353992dd52acd97bcf45; Core b6c0a01a3dba88543439634d10fd0f3abd9a3ef7196f43170bf80ea3a9d50482.
Runner via subprocess bash: exit 2, python não encontrado (não verde). Tentativa terminal agregada para PYTHON explícito bloqueada pelo parser de comandos, exit -1; não alterar política de aprovações. Próxima abordagem simples ou registrar NAO_EXERCITADO.
Perfis reais consultados `hermes profile list`: somente default. Correção deve ir à mesma fila/profile existente, em NOVA instância distinta do reviewer run638, sem inventar especialista/profile/modelo nem editar configuração.
