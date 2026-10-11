# KIT-15 — parte 03: implementação e primeiras provas reais

Sessão: worker run 677 (default) · 2026-10-10 · repo `C:/dev/stolen-realm`
Escopo offline: nada instalado no perfil do dono, jogo não aberto, nada publicado, sem git add/commit/push.

## 1. Arquivos criados (novos; nenhum arquivo vivo editado)

| caminho | bytes | sha256 |
|---|---|---|
| tools/automacao/kit15/manifesto.json | 4836 | (ver parte 04) |
| tools/automacao/kit15/descoberta.py | ~7,8k | (ver parte 04) |
| tools/automacao/kit15/instalador.py | ~20k | (ver parte 04) |
| tools/automacao/kit15/pacote.py | ~10,7k | (ver parte 04) |
| tools/automacao/kit15/scan.py | 5834 | (ver parte 04) |
| tools/automacao/kit15/teste_kit15.py | ~17,8k | (ver parte 04) |
| tools/automacao/kit15/contra_prova_kit15.py | ~9k | (ver parte 04) |
| tools/automacao/kit15/roda_testes_kit15.sh | 1873 | (ver parte 04) |
| tools/automacao/kit15/README.md | 4876 | (ver parte 04) |
| tools/automacao/kit15/README.en.md | 4717 | (ver parte 04) |
| tools/automacao/kit15/CHANGELOG.md | 2008 | (ver parte 04) |
| tools/automacao/kit15/docs/primeiro-uso.md | 5700 | (ver parte 04) |

Hashes completos medidos com `sha256sum` ficam em
`scratch/kit/KIT-15-run677/hashes-kit15.txt` (parte 04 registra a saída bruta).

## 2. Prova 1 — suíte do autor: VERDE

Comando (saída bruta em `scratch/kit/KIT-15-run677/log-suite.txt`):

```
python tools/automacao/kit15/teste_kit15.py
```

Saída real (exit **0**):

```
Ran 18 tests in 5.202s
OK
```

18 testes cobrindo: manifesto/versões, zip candidato limpo, `testzip`, ausência de DLL
proprietária no zip, instalar com hashes lidos de volta, manifesto do pacote == instalado,
preservação de arquivo local alheio, `atualizar` reescrevendo **só** o arquivo divergente
(mtime dos demais intocado), `rollback` devolvendo bytes originais, `remover` restaurando o
arquivo pré-existente byte a byte, falhas de `remover`/`rollback` sem recibo/transação,
guard de hash divergente com rollback automático, seleção de componentes, **modo manual sem
Python**, descoberta de paths sem usuário fixo (com config do usuário), ausência de nome de
usuário embutido no código e scan com controle negativo (segredo sintético e DLL plantados).

### Defeitos encontrados e corrigidos durante a implementação (registro honesto)

1. **Colisão de timestamp no cofre de backups** — instalar e remover no mesmo segundo
   compartilhavam a pasta `backups/<ts>` e o backup original era sobrescrito pelo arquivo do kit;
   o `remover` devolvia o arquivo errado (detectado por `test_10`). Corrigido com timestamp
   único por operação (contador) e ordenação das transações por mtime.
2. **Seleção explícita de componentes** — `--componentes core` ainda trazia os demais
   obrigatórios; agora seleção explícita instala exatamente o pedido (+ ferramenta/docs).
3. **`ValueError` escapando da API** — componente desconhecido derrubava `instalar()` em vez de
   devolver exit 1 com erro legível.
4. **`unittest.main(module=None)` não descobria nenhum teste** (`NO TESTS RAN`, exit 5) — o
   carregamento passou a ser explícito por módulo, com exit 0/1/2 distintos.

## 3. Prova 2 — contra-prova dos defeitos plantados: VERDE

Comando (saída bruta em `scratch/kit/KIT-15-run677/log-contra.txt`):

```
python tools/automacao/kit15/contra_prova_kit15.py --saida scratch/kit/KIT-15-run677/contra
```

Saída real (exit **0**):

```
  baseline-intacto                               OK (-)
  D1-instalador-sem-conferencia-de-hash          OK (test_12_hash_divergente_apos_escrita_dispara_rollback)
  D2-instalador-reescreve-tudo                   OK (test_08_atualizar_muda_so_o_arquivo_divergente)
  D3-instalador-nao-guarda-original              OK (test_10_remover_restaura_estado_anterior)
  D4-scan-sem-bloqueio-de-binario                OK (test_17_scan_controle_negativo_e_limpo)
  D5-scan-sem-deteccao-de-segredo                OK (test_17_scan_controle_negativo_e_limpo)
  D6-descoberta-ignora-argumento-explicito       OK (test_15_descoberta_sem_usuario_fixo)
  D7-pacote-empacota-bin-obj                     OK (test_03_zip_sem_dll_proprietaria_nem_perfil)
CONTRA-PROVA|OK|baseline=True|recusados=7/7|falsos-verdes=[]|sandbox=...
```

Cada defeito é aplicado em **cópia sandbox própria** (o repo vivo não é editado) e o RED só
conta se a saída tiver `Ran N tests` (a suíte rodou de verdade) com exit 1. Logs por defeito em
`scratch/kit/KIT-15-run677/contra/log-D*.txt`; resumo JSON em
`scratch/kit/KIT-15-run677/contra/contra-prova.json`.

### Regras de honestidade dessa contra-prova

- defeito cujo texto não é encontrado 1× vira `MUTACAO-INVALIDA` (nunca aprovado);
- defeito sem efeito vira `SEM-EFEITO` (falso verde) e **reprova** a contra-prova — foi o que
  aconteceu na primeira execução: o defeito D7 inicial mutava só o filtro de diretórios do
  `pacote.py`, mas o segundo filtro (por parte do caminho) ainda bloqueava `bin/`, então o
  defeito **não tinha efeito**. Corrigi o D7 para mutar os dois pontos (defeito efetivo) em vez
  de aceitar o falso verde;
- o contador de recusados exclui o baseline (bug de contagem corrigido: antes o baseline
  "OK" era somado aos defeitos recusados, mascarando um defeito sem efeito).

## 4. Estado até aqui

- [x] Inventário dos fontes (parte 02)
- [x] Manifesto com versões e origem de cada versão
- [x] Instalador com instalar/atualizar/remover/rollback/status + rollback automático
- [x] Descoberta de paths sem usuário fixo (+ config do usuário)
- [x] Pacote/zip candidato + `testzip` + scan
- [x] README PT-BR/EN, primeiro uso, changelog
- [x] Suíte 18/18 verde e contra-prova 7/7
- [ ] CLI ponta a ponta em diretório limpo (instalar/atualizar/remover/rollback reais)
- [ ] Runner único `roda_testes_kit15.sh` com exit 0/1/2
- [ ] Zip final + verificação do zip publicado-localmente + hashes na entrega
- [ ] Entrega final

Próximas provas continuam offline. Publicação permanece bloqueada (KIT-G4).
