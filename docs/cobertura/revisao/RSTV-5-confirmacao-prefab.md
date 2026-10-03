# RSTV-5 — Confirmação do INDETERMINADO do RSTV-3: o que o X do prefab chama

> Tarefa `t_1a1411d7` (RSTV-5). O RSTV-3 levantou um INDETERMINADO: o `closeButton.onClick` do
> `SkillTreeManager` **não está no C#** (é `UnityEvent` serializado no prefab), e o risco era um
> NRE via `CharacterMenusManager.Instance.CloseSkillTreeMenu()` caso a instância estivesse nula
> durante a run. **Lido o prefab:** o X chama `SkillTreeManager.AcceptSkillChanges(true)` — o
> NRE via `CharacterMenusManager.Instance` está **descartado**.

**Fonte:** instalação viva do jogo — `E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm_Data\resources.assets`
(1.723.507.220 bytes; `resources.assets.resS` 2.651.200.736 bytes). Ferramenta: **UnityPy 1.25.3**
(já presente no ambiente). Nenhum arquivo foi modificado; nenhum AssetRipper foi instalado.

---

## 1. O prefab

Varredura dos `GameObject` de `resources.assets` por nome contendo "skill tree" (sem `(Clone)`/`Item`):

| GameObject | `path_id` | o que é |
|---|---|---|
| **`Skill Tree Window`** | **490739** | **o prefab do `SkillTreeManager`** (a raiz que o `ReferenceLoader` instancia) |
| `Skill Tree Window Roguelike` | 723877 | o prefab do `SkillTreeManagerRoguelike` — **o mod NÃO usa** (ver RSTV-1 §10: o caminho do mod é o ramo CAMPANHA) |

A raiz 490739 tem 5 componentes (`RectTransform` 2520584, `CanvasRenderer` 2462625 e três
`MonoBehaviour`).

## 2. O que o X chama (a prova)

Os `MonoBehaviour` de `resources.assets` **não têm typetree legível** (o `read()` tipado falha com
`ValueError: Expected to read N bytes, but only read 32`) — então a leitura foi feita pelo **RAW**
do objeto, procurando o nome do método do `PersistentCall` do `UnityEvent`. Dois botões do prefab
carregam a string `AcceptSkillChanges`:

| `MonoBehaviour` `path_id` | GameObject | alvo do `PersistentCall` |
|---|---|---|
| 2641390 | `Accept Button` | `SkillTreeManager, Assembly-CSharp` → **`AcceptSkillChanges`** |
| **2763658** | **`Close Button (1)`** ← o X | `SkillTreeManager, Assembly-CSharp` → **`AcceptSkillChanges`** |

Bytes ao redor do nome do método (verbatim do raw):
`'SkillTreeManager, Assembly-CSharp'`, `'AcceptSkillChanges'`, `'UnityEngine.Object, UnityEngine, …'`
(o último é o `m_ObjectArgumentAssemblyTypeName` do `ArgumentCache`).

Lendo o `ArgumentCache` inline (o `m_Arguments` é struct, **não** array — por isso o primeiro
parse contou "0 argumentos" e o segundo acertou):

| botão | `m_Mode` | `m_BoolArgument` (`closeMenu`) | `m_CallState` |
|---|---|---|---|
| `Accept Button` | 6 (`Bool`) | **1 (`true`)** | 2 (`RuntimeOnly`) |
| `Close Button (1)` (o X) | 6 (`Bool`) | **1 (`true`)** | 2 (`RuntimeOnly`) |

**Conclusão:** o X (e o Accept) chamam `SkillTreeManager.AcceptSkillChanges(closeMenu: true)`
(`Assembly-CSharp.decompiled.cs` l.177650) — os dois são a MESMA chamada.

## 3. Por que o NRE via `CharacterMenusManager.Instance` está descartado

A string **`CloseSkillTreeMenu`** — o nome do método que o RSTV-3 suspeitava — tem contagem **0**
em **todos** os assets do jogo:

| arquivo | `CloseSkillTreeMenu` | `CloseSkillTree` | `AcceptSkillChanges` |
|---|---|---|---|
| `resources.assets` | **0** | **0** | 2 |
| `level0` / `level1` / `level2` | 0 | 0 | 0 |
| `sharedassets0/1/2.assets` | 0 | 0 | 0 |

Um `PersistentCall` de `UnityEvent` grava o **nome do método como string** no dado do botão; se o X
chamasse `CharacterMenusManager.CloseSkillTreeMenu()`, essa string existiria no asset. Ela não
existe em lugar nenhum. Logo, **o X nunca toca `CharacterMenusManager.Instance`** — e não há NRE por
instância nula vinda do X. (`CloseSkillTreeMenu` continua existindo no C# e é chamado por outros
caminhos de C# do menu de personagem — isso é do jogo, não do X.)

## 4. O que o mod faz com isso (e por que o caminho já está fechado)

O X -> `AcceptSkillChanges(true)` é **exatamente o método que o mod já intercepta**: o prefixo
Harmony `SkillTreeManagerAcceptSkillChangesPatch` (`Patches.cs` l.134-135, por TIPO e assinatura).
Com `ReadOnlySession.Active`:

1. o prefixo limpa `SkillsToAdd`/`SkillsRemoved` e faz `SkillsOnEnter` = união das skills do alvo
   com as do personagem selecionado pelo jogo (`Patches.cs` l.142-185). Na conta do original
   (l.177672-177682), a lista de remoção fica **vazia** e nada é adicionado -> **zero escrita**;
2. o original roda (`return true`), e como `closeMenu == true` ele fecha a janela
   (`base.gameObject.SetActive(false)`, l.177686-177689);
3. o `SetActive(false)` dispara o `OnDisable` (l.178053), cujo postfix encerra a sessão read-only
   (`Patches.cs` l.411-428).

Ou seja: o X é um caminho **fechado e já coberto** pela higienização existente. Não é preciso patch
novo.

## 5. O que continua INDETERMINADO (para o RSTV-6 confirmar em jogo)

A leitura do asset prova a **ligação** (qual método o X chama), não o **comportamento em runtime**.
Confirmar em jogo (RSTV-6):

- clicar o X com a arvore read-only aberta feche a janela, com no `LogOutput.log` a linha
  `RSTV-2: commit higienizado (read-only, closeMenu=True) — nenhuma escrita no personagem` e, em
  seguida, `RSTV: modo somente leitura encerrado`;
- o `needsAccept` precisa estar `true` (o `Initialize` do jogo o seta, l.177536+); se estiver
  `false`, o `AcceptSkillChanges` sai cedo (l.177652) e **não fecha** — o mod não mexe nesse campo,
  mas o caso é observável no log;
- o mesmo para o `Accept Button` (mesma chamada).

## 6. Como reproduzir

```bash
# 1) a string do método NÃO existe em nenhum asset (o achado negativo)
cd "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data"
grep -a -c CloseSkillTreeMenu resources.assets level0 level1 level2 sharedassets*.assets

# 2) o raw de cada MonoBehaviour e o ArgumentCache (UnityPy 1.25.3)
#    (script de bancada: %LOCALAPPDATA%\hermes\cache\scratch\rstv5_probe5.py e rstv5_probe7.py,
#     scratch e gitignored e pode ser podado — a receita essencial esta acima)
python rstv5_probe5.py   # acha quem carrega 'AcceptSkillChanges' e o GO dono
python rstv5_probe7.py   # le m_Mode/m_BoolArgument/m_CallState dos mb 2641390 e 2763658
```
