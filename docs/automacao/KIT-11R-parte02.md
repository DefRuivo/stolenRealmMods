# KIT-11R — parte 02: identidade viva e reprodução baseline

Reviewer run 653. Sandbox C:/dev/stolen-realm/scratch/kit/KIT-11R-run653; cópia dirigida preservou bytes tracked e untracked do escopo, sem .git/remoto/credenciais/perfil do dono. Nenhum build: módulo Python; deploy não executado.

## Identidade SHA-256 (comando python com hashlib + shutil.copy2; exit 0)
- tools/automacao/kit11/executor.py: 65284edd248d3bf1117529b366d150b7cb8578c0ae03c64fcd7358cdbb75b6e2, 24137 B.
- tools/automacao/kit11/test_kit11_executor.py: 1d72ae071ceea8086c49b7d11523fbda1c908eee7f772e44290d38adbf071a02, 14998 B.
- tools/automacao/runtime/coletor.py: 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d, 104102 B.
- tools/automacao/runtime/controle_acesso.py: 379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457, 34265 B.
- tools/testes/arcabouco.py: 08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb, 12519 B.
Inventário persistido em scratch/kit/KIT-11R-run653/inventory.json. Executor/testes idênticos aos hashes upstream.

## C10 — baseline PASSOU apenas lógica offline
Comando real: python scratch/kit/KIT-11R-run653/tools/automacao/kit11/test_kit11_executor.py
Output: 12 linhas RESULTADO|PASSOU (positivo-observacao, positivo-ativo, falha-timeout, cancelamento, neg-versao-incompativel, neg-tipo-condicao-desconhecidos, neg-campo-executavel, neg-ativo-sem-autorizacao-separada, neg-perfil-save-de-teste, neg-frente-unica, encerra-so-instancia-criada, rollback-exato); 12 teste(s), 0 falha(s); exit 0.
Não prova jogo ou navegação. A isca do autor (test_kit11_executor.py:318-319) lança AssertionError incondicional e não injeta defeito no executor; não será aceita como contraprova de comportamento. As três mutações de fonte declaradas pelo autor exigem reconfirmação independente.

## C11 — reuso INDETERMINADO / discrepância documental
coletor.py realmente importado dinamicamente e tem primitivas já corrigidas para preservar diretórios e verificar estado pós-rollback. controle_acesso.py é citado na documentação mas NÃO é importado/usado pelo executor (leitura completa confirma); autorização foi reimplementada em decidir_permissoes. Conferência final distinguirá reuso efetivo de referência nominal.

## Hipóteses dirigidas (AINDA não vereditos de execução)
- C1/C2/C8: timeout ausente é aceito; NaN/inf passam comparação; satisfeito convertido com bool.
- C3: lock não atômico (exists/read/remove/open w); frente é opcional e CLI não fornece lock.
- C4: shutdown usa delta PID, sem registro de processo criado pelo executor; cleanup pode substituir estado terminal; snapshots/backups antes do try; diretórios existentes não são repassados ao rollback; dir_backup externo removido inteiro.
- C5/C7: override de autorização sem validação; status NAO_EXERCITADO da observação não interrompe executar.

Próximo bloco: testes próprios com efeitos reais exclusivamente em arquivos sandbox; fechamento de processos totalmente capturado por driver falso; nenhuma chamada real ao taskkill/PowerShell/jogo.
