# EV-R1 — parte 01: escopo e origem verificável

Tarefa: t_48d68679. Trabalho exclusivamente offline, sem iniciar jogo, sem instalar plugin e sem publicação.

## Origem confirmada

- Assembly instalado: `E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll`.
- SHA-256 medido: `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`.
- Cópia de referência existente: `C:/dev/stolen-realm/lib/Assembly-CSharp.dll` (7.712.768 bytes; equivalência ainda NÃO_EXERCITADA).
- Extrator reutilizável localizado: `C:/dev/stolen-realm/scratch/rv28/dump_fortunes.py` (leitura pendente).
- Referência de índice: `C:/dev/stolen-realm/docs/cobertura/DUMP-PASSIVAS-REVISAO.md`, 961 linhas. O documento é um recorte de skills, não uma prova da cobertura de eventos.
- Ferramentas detectadas: `ilspycmd` em `C:/Users/Pichau/.dotnet/tools`; Python 3.14.7. `importlib.util.find_spec('UnityPy')` retornou `None` no Python padrão.

## Limites e preservação

`git -C C:/dev/stolen-realm status --short` mostrou alterações preexistentes de outros trabalhos. Nenhum desses arquivos será reescrito. Novos artefatos serão produzidos neste workspace em `docs/automacao/` e `docs/cobertura/EV-R1/`, em partes numeradas e sem sobrescrita.

Não há contagem total de eventos verificada ainda. Ausência em censos não será tratada como ausência nos assets. Nomes, textos e recompensas só serão incluídos a partir do assembly instalado ou dos assets serializados instalados. Valores não encontrados terão `null` e motivo explícito.

## Reprodução do diagnóstico

Executado no workspace: `python -c "from pathlib import Path; import importlib.util,hashlib; a=Path('E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll'); print(importlib.util.find_spec('UnityPy')); print(hashlib.sha256(a.read_bytes()).hexdigest())"`.

Cobertura, resolução de referências e validação de schema: NÃO_EXERCITADO nesta etapa inicial; os resultados serão registrados em novas partes.
