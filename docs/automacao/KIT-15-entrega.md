# KIT-15 — ENTREGA (pacote instalável e guia para outros modders)

Cartão `t_10584ca5` · perfil `default` · implementador **run 677** · data 2026-10-10
Workspace `C:/dev/stolen-realm` · **OFFLINE**: sem jogo, sem save, sem perfil do dono, sem deploy,
sem publicação, sem `git add/commit/push`.

Revisão independente precriada: `t_effde07f` (KIT-15R), que é liberada por esta conclusão.
Esta entrega **não** é autoaprovação, aceite humano, prova em jogo ou DoD.

## 1. O que foi entregue

| # | Artefato | Papel |
|---|---|---|
| 1 | `tools/automacao/kit15/manifesto.json` | receita do pacote: componentes, versões, origem da versão, dependências, compatibilidade medida |
| 2 | `tools/automacao/kit15/instalador.py` | instalar/atualizar/remover/rollback/status + backup por transação + rollback automático |
| 3 | `tools/automacao/kit15/descoberta.py` | descoberta/seleção de paths sem usuário fixo (jogo/perfil apenas detectados, nunca escritos) |
| 4 | `tools/automacao/kit15/pacote.py` | staging, manifesto com hashes medidos, zip determinístico, `testzip`, scan |
| 5 | `tools/automacao/kit15/scan.py` | segredos/conteúdo proibido + ausência de DLL proprietária |
| 6 | `tools/automacao/kit15/teste_kit15.py` | suíte offline (18 testes) |
| 7 | `tools/automacao/kit15/contra_prova_kit15.py` | 7 defeitos plantados que **têm** de reprovar |
| 8 | `tools/automacao/kit15/roda_testes_kit15.sh` | runner único com exit 0/1/2 distintos |
| 9 | `tools/automacao/kit15/README.md` · `README.en.md` · `CHANGELOG.md` · `docs/primeiro-uso.md` | documentação PT-BR/EN, primeiro uso, changelog |
| 10 | `scratch/kit/KIT-15-run677/cli/pacote/kit-rstv-0.1.0.zip` | zip/release **candidato local** (42 membros) |
| 11 | `docs/automacao/KIT-15-parte01..04.md` | checkpoints com provas (parte 02 = inventário, 03/04 = execuções) |

Nenhum arquivo de implementação pré-existente foi editado. `git status --short` mostra apenas `??`
para `tools/automacao/kit15/` e `docs/automacao/KIT-15-parte0*.md`.

## 2. Veredito por critério de aceite (prova do autor; revisão independente pendente)

| Critério do cartão | Resultado | Evidência (comando real + exit) |
|---|---|---|
| Instalar/atualizar/remover **com rollback** | **PASSOU** offline | CLI: `instalar` exit0 (41/41 arquivos), `atualizar` exit0 (**1** de 41 reescrito), `rollback` exit0 (`problemas: []`), `remover` exit0 (41 tratados). Arquivo pré-existente voltou **byte a byte** (lido do disco, não da mensagem) |
| Dependências reais e versões consistentes | **PASSOU** | versões lidas do fonte (`KIT04Adapter.SR.csproj` 0.1.0, `KitSdk.csproj` 1.0.0, `VERSAO_EXECUTOR` 1) e declaradas com a origem no manifesto; componentes apontam para os fontes **revisados** (hashes `cad1bcc2…`, `480a9a02…`, `bdd33622…`, `9f2eabdd…` conferem com os pareceres KIT-06F/12F2/08F/13R) |
| Descoberta/seleção de paths sem usuário fixo | **PASSOU** | `test_15` (argumento → ambiente → config do usuário → padrão do repo → HOME), `test_16` (nenhum nome de usuário embutido no código); `descoberta.py --json` real |
| Uso básico sem SDK/Python | **PASSOU com ressalva declarada** | sem SDK .NET, sem rede, sem IA/Hermes/credencial (só Python stdlib). **Sem Python**: modo manual documentado em `docs/primeiro-uso.md` e exercitado por `test_14` (cópia manual + conferência de hashes + remoção). Ferramenta empacotada no zip (`tools/`), o receptor não precisa de SDK para instalar/scan/empacotar |
| README PT-BR e EN, primeiro uso, exemplos, changelog, compatibilidade medida | **PASSOU** | `docs/README.md`, `docs/README.en.md`, `docs/primeiro-uso.md`, `CHANGELOG.md` (tabela de origem revisada por componente); compatibilidade: Python 3.14.7/Windows 11 **MEDIDO**, Unity/BepInEx/ModAPI **NÃO_MEDIDO** nesta rodada (herdado de KIT-02), Linux/macOS NÃO_MEDIDO |
| Zip/release candidato local testado em diretório limpo sem jogo | **PASSOU** | `pacote.py montar` exit0 `PACOTE_LIMPO`, `zip_sha256 126e367b…`, 42 membros, `testzip: null`; instalação **a partir do zip** em destino limpo exit0 e `status` = INSTALADO |
| Scan genérico de segredos/conteúdo e ausência de DLL proprietária | **PASSOU** | `scan.py <zip>` exit0 `LIMPO`; `scan.py tools/automacao/kit15` exit0 `LIMPO`; controles negativos reais: segredo sintético detectado (`test_17`) e `Assembly-CSharp.dll` dentro do zip detectado (`test_18`, `verificar` → ACHADO exit1) |
| Nada de push/tag/GitHub Release/Thunderstore/`publicar:true` | **PASSOU** | nenhum comando de publicação executado; nenhuma ferramenta do pacote implementa publicação; relatório do pacote grava `publicacao: NAO_EXECUTADA (… KIT-G4)` |

## 3. Execuções reais (exit + caminho da evidência)

1. `python tools/automacao/kit15/teste_kit15.py` → `Ran 18 tests in 5.202s` / `OK`, **exit 0**
   (`scratch/kit/KIT-15-run677/log-suite.txt`).
2. `python tools/automacao/kit15/contra_prova_kit15.py --saida scratch/kit/KIT-15-run677/contra`
   → `CONTRA-PROVA|OK|baseline=True|recusados=7/7|falsos-verdes=[]`, **exit 0**
   (`log-contra.txt`, `contra/contra-prova.json`, `contra/log-D*.txt`).
3. `bash tools/automacao/kit15/roda_testes_kit15.sh` → `KIT-15 RESULTADO|VERDE|suite=0 contra-prova=0`,
   **exit 0** (`log-runner.txt`); com `PYTHON=python-inexistente` → **exit 2** (infra ≠ falha lógica).
4. `python tools/automacao/kit15/pacote.py montar --saida …/cli/pacote` → **exit 0**,
   `PACOTE_LIMPO`, 42 membros, `zip_testzip null` (`cli/01-montar.json`).
5. `pacote.py verificar <zip>` → **exit 0** `OK`, `tem_manifesto true`, `scan_total 0`
   (`cli/02-verificar.json`); `scan.py <zip>` → **exit 0** `LIMPO` (`cli/03-scan.json`).
6. CLI do instalador em diretório limpo: `04 instalar` 0 · `05 status` 0 (INSTALADO) ·
   `06 atualizar` 0 (`arquivos_escritos 1` de 41) · `07 rollback` 0 · `08 remover` 0 ·
   `09 instalar <zip>` 0 · `10 status` 0 · `11 remover` 0 (`cli/04..11-*.json`).
7. Travas do repo: `check_segredos.py` **exit 0**, `check_dupes.py` **exit 0**,
   `audita_docs.py` **exit 0** (`gate-*.txt`).

## 4. Artefato local, identidade e hashes

Zip candidato **local** (não publicado):

```
scratch/kit/KIT-15-run677/cli/pacote/kit-rstv-0.1.0.zip
42 membros · 164881 bytes · CRC/testzip OK · zero DLL/pdb/exe
SHA256: 126e367b059562ff248d469201ac325142a3d5342ec84458fb75201bdf5708cb
```

Hashes dos entregáveis (saída bruta em `scratch/kit/KIT-15-run677/hashes-kit15.txt`):

- `instalador.py` `81243659708035c77b68de14eecb6018ffbf5858b2445440701283604e1b9596`
- `pacote.py` `c006c0ff1061ae2117691207cca9e0ad39a7fc5e58e6297e02ec7c8406b964cd`
- `descoberta.py` `10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86`
- `scan.py` `a9fe0bfff406356607a54947174247244f4d6d5d14624b7490bfd53244c11dba`
- `teste_kit15.py` `14e0b537f38ff05d735a5d35d8e22911af8a0395c9f4b60ec45543f6db831019`
- `contra_prova_kit15.py` `c2910ac29213bcb2ea27383a6b8a3b7f29b5349bad7c1d2e4c6cb57c8702b12d`
- `manifesto.json` `37096997a661627e70313056597454cfa721ca0947e3c2b99db9a0e13d5fc0a1`
- `roda_testes_kit15.sh` `6b0657e84c1a22acf4c98eed6103cfc69ff7b92adae2336b5274e7bad44b8a35`
- `README.md` `7c408754d1b9f60f4498cbb9145e060c7c6fd0af14dc97edf16b5cdc43f17240`
- `README.en.md` `225c5e2ca9583797ebb71439cdaa693acebbea98fc0fc7d6dcfa0882e5aaa884`
- `CHANGELOG.md` `be2888fe10d72416b306c8c979889f607df5f5f09a35e7f4c83b5cc41fff7547`
- `docs/primeiro-uso.md` `aa437797ae28a216a5932885401d9696415a29020ba9beab4aabf861d5c032f8`

Componentes empacotados (hashes medidos no inventário, `componentes-hashes.txt`): core (12 arquivos,
`CorePlugin.cs 77e2d1cb…`, `PipelinePassivo.cs 8aec5b8a…`), adapter (`PonteControleRSTV.cs cad1bcc2…`),
recorder (`coletor.py 159ff2aa…`, `observacao_passiva.py 63124b86…`, `controle_acesso.py 379d680f…`),
runner (`executor.py bf03f81b…`), viewer (`visualizador.py bdd33622…`), integração (`integracao.py 480a9a02…`),
sdk (`RegistryV1.cs 9f2eabdd…`, `KitSdk.csproj d81fc947…`).

## 5. Defeitos encontrados durante a implementação (registro honesto)

1. colisão de timestamp no cofre de backups → `remover` devolvia o arquivo errado (corrigido; carimbo
   único por operação, inclusive entre processos);
2. `--componentes` ainda trazia componentes não pedidos (corrigido);
3. `ValueError` escapando da API em componente desconhecido (agora exit 1 com erro legível);
4. `unittest.main(module=None)` não descobria testes (`NO TESTS RAN`, exit 5) → carregamento explícito;
5. **falso verde na contra-prova**: o defeito D7 inicial não tinha efeito (mutava só um dos dois filtros
   de `bin/obj`) e o contador somava o baseline aos "recusados", mascarando o falso verde. Ambos
   corrigidos: D7 passou a mutar os dois pontos e o contador só considera defeitos.

## 6. Lacunas e limites (declarados, não maquiados)

- **NÃO_EXERCITADO**: carregamento do plugin em jogo (BepInEx/Unity lifetime), UI/UX, frames/pixels,
  personagem real, perfil/save do dono, deploy, gates humanos KIT-G1..G4, aceite humano, DoD.
- **NÃO_EXERCITADO**: build C# dentro do pacote — as referências Unity locais do jogo não são
  redistribuídas; o pacote é fonte + ferramenta, não binário.
- **NÃO_MEDIDO nesta rodada**: matriz Unity/BepInEx/biblioteca-de-terceiros (herdada de KIT-02/docs/AMBIENTE.md),
  Linux/macOS.
- **Limite do scan**: cobre padrões conhecidos de credencial e binários por extensão; não promete
  anonimato universal nem detecta segredo ofuscado. Os `.csproj` de exemplo podem referenciar `lib/`
  local quando o receptor compilar (limite já declarado pelo KIT-13).
- O modo manual (sem Python) não tem rollback: se o usuário copiar sobre arquivos próprios, não há
  restauração — documentado no primeiro-uso; rollback exige o instalador.
- Aprovação técnica (por vir) ≠ aceite humano ≠ DoD de mod.

## 7. Próximo passo

`t_effde07f` (KIT-15R) — revisão independente, por instância/autoria separada, deve: conferir os 12
hashes acima contra os arquivos vivos; montar o zip em sandbox **própria** e reabri-lo; exercitar
instalar/atualizar/remover/rollback em diretório limpo (inclusive a partir do zip); tentar refutar o
rollback (interromper/plantar divergência de hash) e o scan (planta de segredo e DLL); conferir que a
suíte dele reproduz RED na cópia com defeito e GREEN na intacta; e registrar PASSOU/FALHOU/
NÃO_EXERCITADO/INDETERMINADO por critério. Não reproduzir apenas este relatório.

Nada foi publicado: push/tag/GitHub Release/Thunderstore/`publicar:true` seguem reservados a KIT-G4.
