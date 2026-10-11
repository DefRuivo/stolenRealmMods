# KIT-07 — ENTREGA: exportar evidências com privacidade e retenção

Cartão `t_c364710f` · perfil `default` · **offline** (sem jogo, sem save, sem
instalar/deploy/publicar; sem upload). Revisão independente no cartão-filho
pré-criado **t_96d0c463 (KIT-07R)**.

## 0. Veredito por item do aceite

| Item do aceite | Situação | Prova (execução real) |
|---|---|---|
| Pacote JSON + PNG + logs selecionados | PASSOU | CLI real: `2 incluidos, 3 excluidos, 190 bytes, upload=nao` |
| Manifest/hash + diagnóstico | PASSOU | `sha256` por arquivo conferido por `test_manifest_hash_confere`; `diagnostico` no manifest |
| Excluir saves e assemblies proprietários | PASSOU | `slot1.sav`→`save`, `Assembly-CSharp.dll`→`assembly_proprietario` (demo real) |
| Sanitizar por padrão GENÉRICO (sem valores fixos) | PASSOU | `aut3_lib.sanitiza` (reuso) + `minimizar_pessoal` (forma) |
| Aviso de screenshot + revisão/exclusão antes de exportar | PASSOU | PNG **desligado por padrão** (`png_opt_in`), `--revisar-png`, aviso no `diagnostico.avisos` |
| Sem upload por padrão | PASSOU | fonte sem `socket/urllib/requests/http.client`; `permitir_upload=True` levanta erro |
| Limites de disco | PASSOU | por arquivo (exclui, não trunca) e total (erro) |
| Exclusão segura | PASSOU | só apaga pacote com marcador `.kit07-pacote`; recusa qualquer outra pasta |
| Teste com credencial fictícia sem vazar valor/prefixo | PASSOU | `test_cli_nao_vaza_prefixo` cobre stdout, stderr, manifest, relatório e arquivos empacotados |
| Runtime (pixels/desempenho/interferência) | **NAO_EXERCITADO** | exige rodada autorizada do dono |

## 1. Arquivos entregues (novos; SHA256 medidos por `sha256sum`)

```
c5fc715b083685ec209138d0dc56e0f9dc19abcabd9e430493746d6f2a625382  tools/automacao/kit07/exportador.py
2dc7ea39e0834041f7176969aced4c58a19be200e4c84137289b895f65fb4f51  tools/automacao/kit07/teste_exportador_kit07.py
e4cc31d4a46e224c1287f66ea5dad8ef131d41d24353b3b9ea1a97310605272e  tools/automacao/kit07/contra_prova_kit07.py
26ceff5dcdbeae4715052741f8bce02a48724a952acdb04a85b1ad5a6fd5f17d  tools/automacao/kit07/roda_testes_kit07.sh
```
Nenhum arquivo existente foi modificado por esta frente (`git status` mostra apenas
novos: `tools/automacao/kit07/` e `docs/automacao/KIT-07-parte0*.md`). Sem `git add -A`.

## 2. Execução real (comando + exit + caminho da prova)

`bash tools/automacao/kit07/roda_testes_kit07.sh` → **exit 0**; log em
`scratch/kit/KIT-07/rodada-final.log`:
- suíte do autor: `Ran 14 tests ... OK`;
- contra-prova por defeito: `12/12 RECUSOU` + `CONTROLE_falso_verde|RECUSOU` → VERDE;
- contra-prova por teste (`--individual`): `12/12` alvos reprovando SOZINHOS → VERDE;
- `VEREDITO KIT-07: VERDE (exit 0)`.

Uso real do CLI (evidência em `scratch/kit/KIT-07/demo/`):
```
python tools/automacao/kit07/exportador.py --origem .../ocorrencias --destino .../pacote
KIT-07: 2 incluidos, 3 excluidos, 190 bytes, upload=nao         (exit 0)
eventos.json empacotado:
{"evento":"clique_recebido","token":"<REDACTED>","log":"<USUARIO>/AppData/Local/Stolen Realm/Player.log"}
excluidos: Assembly-CSharp.dll(assembly_proprietario) quadro.png(png_opt_in) saves/slot1.sav(save)
```

Varredura de segredo nos arquivos novos (sandbox git própria, cópia dos scanners
reais `tools/check_segredos.py` e `tools/check_padroes_segredo.py`, 6 arquivos
versionados): ambos **exit 0**, "nenhum padrao de credencial encontrado".

## 3. Travas exercitadas como RED (defeito plantado → reprova)
12 defeitos plantados, cada um com o conjunto EXATO de testes que deviam falhar:
sanitização desligada; save não excluído; assembly não excluído; upload ligado;
png ligado por padrão; png marcado como sanitizado; hash errado; limite por
arquivo ignorado; limite total ignorado; exclusão segura fraca; destino alheio
sobrescrito; binário desconhecido aceito. Controle falso-verde (defeito que
derruba OUTRO teste) **recusado** — o discriminador exige o conjunto exato.

## 4. Achados/lacunas registrados (não escondidos)
1. **Teste de CLI incompleto (corrigido nesta entrega):** a 1ª versão não
   verificava o conteúdo dos arquivos empacotados; uma mutação que desliga a
   sanitização passava. Ampliado para varrer todo arquivo textual do pacote.
2. **Limitação conhecida do sanitizador compartilhado (`aut3_lib.sanitiza`):**
   chave cujo NOME termina em pontuação + dois-pontos (ex.: JSON `"password:"`)
   dribla a 1ª linha — o rótulo casa, a aspa de fechamento da chave vira a aspa
   do valor e o valor real sobrevive. A forma realista (`"password": "..."`) É
   redigida. **Não alterei `aut3_lib` (fora do escopo do KIT-07)**; fica como
   observação para o revisor decidir se vira cartão próprio.
3. **Carregador de teste individual (corrigido):** `loadTestsFromName` precisa de
   `Classe.metodo`; antes rodava 0 testes.

## 5. Limites desta entrega
- Sem jogo/save/deploy/instalação/publicação; nada commitado.
- Runtime, pixels e desempenho: NAO_EXERCITADO.
- Aprovar tecnicamente **não** equivale a aceite humano nem publicação do DoD.

## 6. Passo seguinte
Revisão independente no cartão **t_96d0c463 (KIT-07R)**: refutar vazamento,
segredo em artefato, exclusão indevida e falsa promessa de anonimato; exercitar
controle negativo em sandbox própria.
