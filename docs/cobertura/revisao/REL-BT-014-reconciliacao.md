# REL-BT-014 — reconciliação do changelog/escopo da 0.1.4 (PREPARAÇÃO LOCAL)

Cartão: `t_3941b8ce` (revisão independente: `t_1b5dd4d9`). Gate de publicação: **PUB-1**
(`t_e083bd4f`, bloqueado). **Nada publicado, nada empurrado, perfil do dono intacto, sem pacote novo.**

## 0. Estado de partida (verificado)

| fato | prova |
|---|---|
| Baseline publicada: **BetterTooltips 0.1.3** | `release/mods.json` (`publicado_em` 2026-10-03T22:48:02Z) e API fresca `GET /api/experimental/package/DefRuivo_StolenRealmMods/BetterTooltips/` → `latest = 0.1.3` |
| Local: **0.1.4** nos 4 lugares (csproj = manifest = Plugin.cs = README) | `python tools/check_versoes.py` → **exit 0** |
| A 0.1.4 local NÃO é publicável ainda | ver §4 (semântica do número de Decay/Flame em aberto + changelog contraditório) |

## 1. Matriz de claims — fonte × aceite × pendência

Cada linha é uma afirmação **pública** (description / README / CHANGELOG) ou uma decisão de código,
com a fonte, o aceite e o que continua pendente.

| # | claim / comportamento | onde | fonte | aceite | pendência |
|---|---|---|---|---|---|
| C1 | A nota de Armor sai do feed de combate e fica só no corpo da tooltip (BUG-34) | CHANGELOG 0.1.4; código `LocalizePatch.cs` (flag de contexto de feed) | código + log | **ACEITO pelo dono 05/10 e 06/10** (`t_9e2d83f8`) | — (preservar; não reabrir sem regressão nova) |
| C2 | O número exibido das auras de PERIGO é avaliado **sem** o fator (`Source = null` + constante sem fator) — RV-30 | `ShrineAuraPatch.cs`; regra pura `tools/testes/regras_rv30.py` | código (decompilado l.41935 / l.34381-34383) | **não é decisão**: é o desenho atual do código | **RV-49 ABERTO** — com ou sem o fator é decisão de medição em jogo |
| C3 | "o dobro registrado em jogo era **defeito do próprio mod**" | README (Verification) e CHANGELOG (0.1.4 / RV-48 / 0.1.0) | **REFUTADO**: dono confirmou o dobro CORRETO + evidência `t_d02f9212`/RV-49 (06/10) | dono | — (corrigido: §2) |
| C4 | "as auras de perigo escalam pelo bônus do **shrine**, não o seu" | README (Verification) e CHANGELOG (0.1.4 / RV-48) | **REFUTADO**: no caminho do DANO o `Source` da ação é o personagem que **TEM a aura** (`UseTriggerSource = 0`) | — | corrigido; a **evidência** fica no código (`ShrineAuraPatch` docstring) e em `docs/cobertura/revisao/RV-19-shrines.md` §4.2.1/§4.5 |
| C5 | "não existe perk de jogador `Worship` (`worship` = 0 ocorrências no código)" | README (Shrine auras / Verification) e CHANGELOG (RV-48, 0.1.0) | **zero ocorrência no código/censo NÃO prova ausência no asset** | dono (dobro correto) | corrigido para "**não encontrado no código/dados lidos**" (§2) |
| C6 | O número da cura do Sustenance não pode mais derrubar a tooltip (RV-28) | CHANGELOG 0.1.4; `LocalizePatch.cs` | código (guarda de existência do atributo) | aceite RV-28 registrado (06/10) | — |
| C7 | Os ganchos leem argumentos **pelo nome** (TRV-1) | CHANGELOG 0.1.4; fonte | código; `python tools/check_patches.py` → **exit 0** | — | — |
| C8 | A linha `Your active shrine auras:` usa o **personagem sob o cursor** (RV-50), exceto no tooltip do shrine (aí o selecionado) | `ShrineAuraPatch.cs` (`Receptor`) | código | — | **RV-50a..g ABERTO** — conferência visual em jogo (KANBAN.md) |
| C9 | description: "shrine aura numbers **with your real bonus**" | `manifest.json` | imprecisa (o número de Decay/Flame não inclui o fator) | — | corrigida (§2) |

**Leitura da matriz:** só o item C1 tem aceite humano fechado. C2/C8 são comportamento atual do código
com decisão/conferência **em aberto** (RV-49, RV-50). C3/C4/C5 eram **afirmações falsas** na
documentação pública — o defeito que este cartão corrige. C6/C7 são código com aceite/verde.

## 2. Diff de textos (edições preservando o trabalho do dono)

Arquivos e hashes (sha256) **depois** da edição:

```
2d90523fece12951273339174ca3046f459abd95214dd6d8d076768bfe0a3c71  BetterTooltips/README.md      (*)
c5bbe90d228b2c940ebba5953a69affdb25bc6d14bca98a6ca680f7e13f23b64  BetterTooltips/CHANGELOG.md   (*)  (após a tradução o hash foi `ab98530d…`; o valor final é este, depois do ajuste de wrap do §8)
6ed2db6c50c109654f1f7d11a33ecf6a266284a6f2921fa988710b43301a2a9a  BetterTooltips/manifest.json
9f6db23a0541ee08c01001b5a39984f63813a41d5d904cd483cd4bda1a7212dc  BetterTooltips/BetterTooltips.csproj   (não tocado por este cartão)
f5e328ceb808d741d772402eecf3736f48678c4e7c30fc449751f63d2821ee66  BetterTooltips/Plugin.cs                (não tocado por este cartão)
```

`(*)` = re-medido depois das correções do REL-BT-014R (07/10, §8): o `README.md` teve o bullet A3
reformulado e o `CHANGELOG.md` passou **inteiro** para o inglês. Hashes de 07/10, **antes** dessas
correções, ficam no comentário REL-BT-014R do cartão `t_1b5dd4d9` e no veredito
`scratch/rel-bt-014r-revisao.md` (README `344c8954…`, CHANGELOG `77fea1b1…`). sha256 do arquivo como
ele está no disco (CRLF, a convenção do working tree deste repo).

Diff completo: `scratch/rel-bt-014-diff-textos.diff` — regenerado em 07/10 pelo REL-BT-014R;
499 linhas, `git diff HEAD` dos 3 arquivos, sha256 `470a773a1d4eb4cbed36a42292a6a66633f9ba258a3d34402e212fa83e50cbb4`.

O que mudou:

1. **`manifest.json` — `description`**: "including shrine aura numbers with your real bonus" →
   "plus shrine aura values for the character in focus". (190 caracteres, ≤ 250; JSON válido.)
2. **`README.md` — "Shrine auras"**: diz explicitamente que as duas auras de **perigo** (Decay/Flame)
   **não** são multiplicadas pelo bônus nesta versão (remete à *Verification*).
3. **`README.md` — "Verification"**: reescrita. Separa (a) **evidência** (o dobro é correto — o motor
   o produz; o `Source` da ação é quem tem a aura), (b) o **rótulo** errado (o "perk `Worship`"), (c) a
   **decisão pendente** (RV-49 — com ou sem o fator no número exibido). Remove a afirmação de ausência
   por zero ocorrências.
4. **`README.md` — resumo PT-BR**: "auras de shrine de **buff** … ; as duas de **perigo** seguem sem o
   fator — pendência aberta (RV-49)".
5. **`CHANGELOG.md` — seção 0.1.4**: reescrita em **inglês acessível** (acompanha o README público), com
   o bullet de BUG-34 mantido como registro, o bullet de RV-30 reescrito (desenho do código × decisão
   aberta) e um bloco **"NOT A FACT — kept on the record"** com as três afirmações falsas (C3/C4/C5).
   O AVISO de que **BUG-34 tem aceite** foi acrescentado.
   **07/10 (REL-BT-014R, §8):** o CHANGELOG **inteiro** passou para o inglês (as seções históricas foram
   **traduzidas**, não reescritas: os mesmos fatos, literais, números e marcadores `⚠`, apenas em inglês).
6. **`CHANGELOG.md` — seção RV-48**: recebeu um marcador `⚠ CORRIGIDA em 07/10` no topo (o corpo fica
   como **histórico**, sem ser reescrito).
7. **`CHANGELOG.md` — seção "Números dinâmicos de shrine" (0.1.0)**: recebeu marcador `⚠ Historico com
   correcao`.

**Edições do dono preservadas:** o texto histórico do changelog **não** foi reescrito — só marcado; a
linha `- **Version:** 0.1.4` do README ficou intacta (a trava `check_versoes.py` segue verde).

## 3. Escopo — o que a 0.1.4 leva (código atual × aceite)

| item | no código agora | aceite | pode sair como FATO? |
|---|---|---|---|
| BUG-34 (Armor fora do feed) | sim (`LocalizePatch`) | **sim** (dono 05–06/10) | sim |
| RV-28 (Sustenance blindado) | sim | sim (06/10) | sim |
| TRV-1 (ganchos por nome) | sim | — (verde por teste) | sim |
| RV-30 correção (número de perigo sem o fator) | sim | **não** — RV-49 aberto | **não** como "correção certa"; só como "desenho atual, decisão aberta" |
| RV-48/TX-1 (texto de `Worship`) | sim (texto) | **não** — rótulo fabricado; dobro correto | **não**; só como "não encontrado no código/dados lidos" |

## 4. Roteiro do gate residual (o que falta para a 0.1.4 ser publicável)

Nada disto é executável por agente (é olho humano no jogo e decisão do dono):

1. **G1 — RV-49 (medição em jogo).** Protocolo em `docs/CONFERENCIA-DONO-06-10.md` §4.1: Decay com
   `Horn of Devotion` (+100) e sem; Flame com +100 e sem — anotar o número da linha × o dano na tela.
   **Fecha:** a decisão "com ou sem o fator". Então: registrar no `KANBAN.md` (RV-49) **e** ajustar
   `tools/testes/regras_rv30.py` **junto** (a regra cobra o desenho atual). **Não fechar RV-49 por
   texto** — é medição.
2. **G2 — RV-50a..g (conferência visual da linha `Your active shrine auras:`).**
3. **G3 — conferência visual do RV-33** (`docs/CONFERENCIA-RV33-DECAY-FLAME.md`).
4. **G4 — se G1 mudar o número:** refazer o pacote (a DLL muda) e a conferência visual da linha.
5. **G5 — aceite humano exato da build** + pipeline (PUB-1). Enquanto G1/G2/G3 não fecharem,
   **não empacotar como publicável**.

## 5. Pacote / hashes

**Não foi empacotado pacote novo.** A semântica afeta o pacote (o changelog está contraditório e a
decisão do número de Decay/Flame está aberta), então a 0.1.4 **não** sai como publicável.

O pacote que existia — `dist/gumatos-BetterTooltips-0.1.4.zip`
(163337 bytes, sha256 `fbc4c5fde8342a752f0990227d19284bb64b75a5f47f5ba2517290bb18a90a4b`, de 07/10
02:02) — **ficou STALE**: `README.md`, `CHANGELOG.md` e `manifest.json` mudaram depois dele, e o zip é
cópia congelada. **Não reutilizar**: qualquer envio tem de repacotar a partir do fonte já corrigido.

Prova (o texto DENTRO do zip × o texto no disco, CRLF normalizado nos dois lados — `IGUAL=False` nos
três; re-medido em 07/10 **depois** das correções do §8):

```
manifest.json   zip=562f15b495108a49  disco=16e0c8992a52414c  IGUAL=False
README.md       zip=654946490ea0307c  disco=b9edbcf64a8a3ee2  IGUAL=False
CHANGELOG.md    zip=51afbb10e2474a98  disco=33357349d653db8e  IGUAL=False
```

O veredito não mudou com o §8: continua **STALE** (e agora também por causa das correções). A DLL DENTRO
do zip — 184320 bytes, sha256 `914154812a2fd44202b191651122ef183303530aa476bd419b690af8526c846f` — é
**byte-idêntica** à `BetterTooltips/bin/Release/netstandard2.1/BetterTooltips.dll`; o literal `0.1.4`
aparece 3× no assembly. Como o §8 só mexeu em texto, a DLL do pacote segue em dia e **não** precisa de
rebuild — o que falta é **repacotar** (G4).

## 6. Travas (executadas nesta rodada)

Re-executadas em 07/10 na rodada do §8 (mesmo exit code antes e depois das correções). O **vermelho é
pré-existente e de outras frentes** — nenhuma pendência é deste cartão.

| trava | resultado |
|---|---|
| `python tools/check_versoes.py` | **exit 0** — os 6 mods batem nos 4 lugares |
| `python tools/testes/roda_testes.py --puros` | **VERDE, exit 0** — 93 rodaram / 93 passaram / 0 reprovaram (1 de `jogo` excluído de propósito) |
| `python tools/check_dupes.py` | **exit 0** |
| `python tools/check_fix_keys.py` | **exit 0** |
| `python tools/check_notas_redundantes.py` | **exit 0** |
| `python tools/check_patches.py` | **exit 0** (2 avisos que não reprovam) |
| `python tools/check_chave_compartilhada.py` | **exit 0** (nenhuma chave nas duas tabelas — o INC-1) |
| `python tools/check_dependencias.py` | **exit 0** (todas as dependências resolvem) |
| `python tools/check_deploy_optin.py` | **exit 0** (7 alvos de deploy, todos sob `Condition`) |
| `python tools/audita_docs.py` | exit 1 com **5** pendências (eram **6**): a contagem do índice de `docs/cobertura/revisao/` foi acertada pela entrada deste relatório. As 5 restantes são **pré-existentes e de outros cartões** (`RV-29` fora do índice, `check_cit.py`/`check_x.py`, dependência do `BetterCombatText`, `ReloadProbe`) — citações de ferramentas de bancada e de caminhos fora do repositório, não versionados. **0** citam o REL-BT-014/BetterTooltips |
| `python tools/checa_citacoes.py` | **exit 1** com **15** pendências, todas **pré-existentes e de outros documentos** (`NULL-1`, `REL-DBG-012-delta-e-pacote`, `docs/automacao/AUT-4*`, `RSTV-27R/28R/29R`). **0** apontam para o REL-BT-014 ou para os textos do BetterTooltips |
| `python tools/check_padroes_segredo.py` | **exit 1 (VERMELHO)** — **6** hits, todos **pré-existentes do commit `d5f4882` (CIC-6)**, nenhum deste cartão: `docs/automacao/AUT-3FR-revisao.md:37` (FORMATO: URL com token embutido), `tools/automacao/offline/testes/t_aut3_segredos.py:32 e :81` (ENTROPIA), `tools/automacao/offline/testes/t_aut3f2_achados.py:44` (ENTROPIA) e `:237`/`:245` (FORMATO: chave PEM). Nada nos arquivos do REL-BT-014. **Não mascarar:** o gate é vermelho e assim fica registrado; corrigir é de outro cartão |

Sem `dotnet build` nesta rodada: a mudança é **só de texto** (`README.md`/`CHANGELOG.md`/`manifest.json`),
nada compila — evita disputar `obj/`/`bin/` com outra frente.

## 7. Limites deste documento

- É **preparação local**. Não é DoD do mod nem aprovação de publicação.
- Não fecha o RV-49 (medição em jogo) nem o RV-50 (conferência visual).
- Não altera fórmula, constante, cor ou código; não altera medida aceita (BUG-34 preservado).
- A seção histórica do CHANGELOG **está em inglês desde 07/10** (REL-BT-014R, §8): as seções históricas
  foram **traduzidas** (mesmos fatos, literais, números e marcadores `⚠`), não reescritas em conteúdo.

## 8. REL-BT-014R (07/10) — correções aplicadas por roteamento do dono

O cartão de revisão `t_1b5dd4d9` devolveu **5 ACHADOs** (A1..A5, ver `scratch/rel-bt-014r-revisao.md`).
O `kanban_request_changes` foi recusado por proveniência de review, e o dono autorizou (07/10) aplicar as
correções **de texto** aqui, sem tocar fórmula/número/perfil e sem invalidar o aceite de BUG-34.

| achado | o que era | o que foi feito |
|---|---|---|
| **A1** | o §2/§7 deste relatório dizia a seção 0.1.4 "em inglês acessível", mas 3 bullets da MESMA seção estavam em PT-BR (`BUG-34`, `RV-28`, `TRV-1`) | os 3 bullets passaram para o inglês; a afirmação do relatório ficou **verdadeira** |
| **A2** | critério do corpo do pai "CHANGELOG INTEIRO em inglês acessível" não cumprido (histórico em PT-BR) | **`CHANGELOG.md` inteiro em inglês**: todas as seções (RV-48, 0.1.3, 0.1.2, MAN-2/REV-47, RV-46, 0.1.1, 0.1.0 + subseções) **traduzidas** — literais de código/chave/log, números, endereços de asset, marcadores `⚠` e a tabela de hashes preservados. Cópia do texto anterior: `scratch/rel-bt-014r/CHANGELOG-antes-da-traducao.md` |
| **A3** | `README.md` "Verification" abria com a asserção proibida em negrito ("There is no player *Worship* perk") | o bullet virou "**The *Worship* label, not the number.** No player perk by that name was **found in the game's code and data we read**" — sem afirmar ausência; o resto do bullet (rastro `T2_Worshiper`, "não é prova") intacto |
| **A4** | o §6 DESTE relatório omitia o gate vermelho e outros (`check_padroes_segredo`, `check_chave_compartilhada`, `check_dependencias`, `check_deploy_optin`) | §6 reescrito com a tabela **completa** (12 travas), incluindo o **VERMELHO** `check_padroes_segredo.py` exit 1 / 6 hits pré-existentes, e `checa_citacoes.py` exit 1 / 15 pendências — nenhuma delas deste cartão |
| **A5** (menor) | a linha `ECONOMY-EXCEPTION` continua no **corpo** de `t_3941b8ce` | **não aplicado**: não há tool de edição de corpo de cartão no conjunto desta sessão (`kanban_*` só muda estado/anexo/comentário). Fica registrado como pendência de board para o dono — não é texto do entregável |

**Não tocado:** `manifest.json` (hash idêntico ao da revisão), `BetterTooltips.csproj`, qualquer `.cs`,
`tools/`, fórmulas, números exibidos, perfil do dono. Sem build, sem instalação, sem pacote novo, sem
push/tag/release/upload.

**Provas desta rodada (re-medidas, não herdadas):**

- `check_versoes.py` **exit 0** depois das edições (0.1.4 nos 4 lugares).
- 12 travas re-executadas: exit codes **idênticos** aos da revisão (§6).
- `roda_testes.py --puros` **VERDE, exit 0** — 93/93.
- Hashes: `README.md` `2d90523f…`, `CHANGELOG.md` `c5bbe90d…`, `manifest.json` `6ed2db6c…` (inalterado).
- Diff regenerado: `scratch/rel-bt-014-diff-textos.diff`, 499 linhas, sha256 `470a773a…`.
- ZIP `dist/gumatos-BetterTooltips-0.1.4.zip` **segue STALE** (`IGUAL=False` nos três textos, §5) — a DLL
  dentro dele é byte-idêntica à `bin/Release` (`9141548…`), então falta **repacotar**, não rebuildar.
- Nenhum resíduo de PT-BR de prosa no CHANGELOG: varredura por ~50 palavras funcionais portuguesas
  devolveu **1** hit, dentro do literal de log `... no-piso=sim|nao` (que é literal de código, preservado).

**O que continua aberto (não é deste cartão):** RV-49 (medição em jogo), RV-50a..g e RV-33 (conferência
visual), re-pacote da 0.1.4 (G4), aceite do dono + pipeline (G5), e a linha do corpo de `t_3941b8ce` (A5).
