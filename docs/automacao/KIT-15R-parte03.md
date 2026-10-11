# KIT-15R — parte 03: identidade real e sandbox

Comando real: python scratch/kit/KIT-15R-run678/setup_review.py (exit 0). Sandbox própria scratch/kit/KIT-15R-run678/sandbox; 535 arquivos vivos de tools (tracked e untracked), copiados byte a byte; COPY_HASH_MISMATCH []. Excluídos .git, bin/obj/cache/ambientes, binários e .env; nenhum remote/perfil/credencial copiado. Inventário completo: scratch/kit/KIT-15R-run678/inventory-before.json.

12 hashes vivos KIT-15 coincidem com os valores do handoff do autor. Destaques: instalador 81243659708035c77b68de14eecb6018ffbf5858b2445440701283604e1b9596; pacote c006c0ff1061ae2117691207cca9e0ad39a7fc5e58e6297e02ec7c8406b964cd; descoberta 10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86. Python --version medido: 3.14.7.

## C5 ACHADO preliminar — ZIP não é idêntico ao fonte vivo
ZIP do autor: SHA256 126e367b059562ff248d469201ac325142a3d5342ec84458fb75201bdf5708cb, 164881 bytes, 42 membros, CRC null, zero DLL. Comparação independente de TODOS os 41 payloads com origem viva: source_mismatch ["tools/descoberta.py"]. Evidência: scratch/kit/KIT-15R-run678/author-zip-identity.json. Próximo bloco irá medir ambos os hashes e diff para explicar a diferença; não presumir que hash do ZIP valida conteúdo correto.

## Temporários
Primeiro comando export medido revelou TMP/TEMP ainda no Temp do sistema (expansão na mesma instrução export), TMPDIR correto. Nenhum teste ainda executado. Corrigir ambiente antes da suíte com atribuições explícitas e medição; não afirmar isolamento por intenção.

C1/C2/C3/C4/C6/C8 ainda INDETERMINADO/NAO_EXERCITADO; nada compilado, instalado no dono ou publicado.
