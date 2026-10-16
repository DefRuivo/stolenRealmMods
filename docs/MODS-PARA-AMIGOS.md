# Enviar os mods para amigos (sem eles programarem nada)

Este documento cobre **os dois lados**: como você gera o pacote e o que o seu amigo
faz com ele. O amigo não compila, não instala SDK, não abre terminal — ele copia
pastas.

---

## 1. Do seu lado: gerar o pacote

```bash
cd /c/dev/stolen-realm
bash tools/pack-for-friends.sh
```

Saída: **`dist/StolenRealm-Mods-<AAAA-MM-DD>.zip`** (dezenas de KB — dá pra mandar
por WhatsApp, Discord ou e-mail sem drama).

O script, em ordem:

1. Compila cada mod (`dotnet build`) e **aborta** se algum tiver erro de compilação;
2. Monta a estrutura de pastas que o BepInEx espera;
3. Copia o `LEIA-ME.txt` (as instruções do amigo) pra dentro do zip;
4. Zipa com o PowerShell (`Compress-Archive`) — nada extra pra instalar.

Para mandar só alguns mods:

```bash
bash tools/pack-for-friends.sh BetterTooltips BetterFont
```

### O que entra no pacote

| Mod | Entra? | Por quê |
|---|---|---|
| `BetterTooltips` | ✅ | textos e tooltips mais claros |
| `BetterStats` | ✅ | atributos como `base (total)` |
| `BetterFont` | ✅ | fonte serifada (Times New Roman) |
| `BetterCombatText` | ❌ | **não está** na lista padrão do `tools/pack-for-friends.sh` (linha 24, que empacota `BetterTooltips`, `BetterStats` e `BetterFont`) — o pacote dele existe para a Thunderstore, não para o zip dos amigos |
| `RoguelikeDebugger` | ❌ | é ferramenta de desenvolvimento — despeja **milhares** de linhas no log; só serve pra nós |
| `RoguelikeSkillTreeVisualizer` | ❌ | **não está** na lista padrão do `tools/pack-for-friends.sh` — o script empacota `BetterTooltips`, `BetterStats` e `BetterFont` (é a lista do próprio script, linha 24) |
| `ReloadProbe` | ❌ | harness de teste, não é mod |

Dentro do zip **só vão as DLLs compiladas**. As `lib/` (referências do jogo/BepInEx)
ficam de fora: elas só servem pra compilar e não devem ser distribuídas —
a `Assembly-CSharp.dll` é propriedade do jogo.

Estrutura do zip:

```
StolenRealm-Mods/
├── LEIA-ME.txt                     <- instruções para o amigo
└── BepInEx/
    └── plugins/
        ├── BetterTooltips/BetterTooltips.dll
        ├── BetterStats/BetterStats.dll
        └── BetterFont/BetterFont.dll
```

---

## 2. Do lado do amigo: instalar

**Não mande instruções extras** — o `LEIA-ME.txt` dentro do zip já tem tudo,
passo a passo, em dois caminhos:

- **Caminho 1 (recomendado):** instalar o **r2modman**, selecionar o jogo, criar um
  perfil, **Start modded** uma vez (isso instala o BepInEx e cria a pasta), depois
  `Settings → Browse profile folder → BepInEx\plugins` e copiar as pastas dos mods.
- **Caminho 2:** baixar o **BepInEx 5 x64**, extrair na pasta do jogo, abrir/fechar
  o jogo uma vez e copiar as pastas dos mods para `BepInEx\plugins\`.

Só isso. Só mande o zip; o resto está dentro dele.

---

## 3. Como conferir que funcionou (você ou ele)

Abra `...\BepInEx\LogOutput.log` e procure por `carregado.` — deve ter uma linha
por mod:

```
[Info   :Better Tooltips] Better Tooltips carregado.
[Info   :Better Stats] Better Stats carregado.
[Info   :Better Font] Better Font carregado.
```

No jogo: a fonte do menu fica serifada e os tooltips mais claros.

---

## 4. Atualizar depois que você mexer num mod

Rode o script de novo e mande o zip novo — ele **substitui** a DLL antiga por
cima. Nada mais precisa ser feito do lado dele.

---

## 5. Notas técnicas

- `lib/` (na raiz do repositório) é **gitignored**: são cópias das DLLs do jogo e do
  BepInEx, usadas só para compilar. Os três mods do pacote padrão usam essas referências.
  A fonte atual do RSTV também referencia os builds Release da RealmApi em `api/`;
  ele não está no pacote padrão. Os argumentos extras do script não resolvem dependências
  nem assemblies auxiliares: não use esse ZIP de uma DLL por mod para distribuir o RSTV atual
  ou a RealmApi sem resolver o contrato de dependências e os três assemblies da API.
- Cada mod tem `DeployToBepInEx` próprio no `.csproj`, mas a cópia só ocorre com
  `-p:DeployToBepInEx=true`. Build comum e empacotamento não instalam (DEPLOY-2).
- Depois de compilar, a DLL de cada mod fica em
  `<Mod>\bin\Release\netstandard2.1\<Mod>.dll` — é essa que o script empacota
  (**Release** é a configuração padrão). O knob é a variável `CONFIG`:
  `CONFIG=Debug bash tools/pack-for-friends.sh` empacota a build de Debug (o
  `--config Debug` é do outro empacotador, o `tools/pack-thunderstore.py`), mas o
  pacote normal sai de Release. Compile com
  `dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false`: a flag
  mantém o deploy explicitamente desligado; desde DEPLOY-2 esse já é o padrão.
  Só `-p:DeployToBepInEx=true` copia a DLL para o perfil do r2modman.
