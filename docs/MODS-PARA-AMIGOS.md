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
bash tools/pack-for-friends.sh BetterTexts BetterFont
```

### O que entra no pacote

| Mod | Entra? | Por quê |
|---|---|---|
| `BetterTexts` | ✅ | textos e tooltips mais claros |
| `BetterStats` | ✅ | atributos como `base (total)` |
| `BetterFont` | ✅ | fonte serifada (Times New Roman) |
| `RoguelikeDebugger` | ❌ | é ferramenta de desenvolvimento — despeja **milhares** de linhas no log; só serve pra nós |
| `RoguelikeQoL` | ❌ | o HUD foi desabilitado por decisão de projeto (`AtivarHUD=false`) |
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
        ├── BetterTexts/BetterTexts.dll
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
[Info   :Better Texts] Better Texts carregado.
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
  BepInEx, usadas só para compilar. Todo mod referencia `..\lib\` — nenhum mod
  depende da pasta de outro mod (isso foi corrigido em 29/09: `BetterStats` e
  `BetterFont` apontavam para `..\RoguelikeQoL\lib\`).
- Cada mod é um projeto independente, com `DeployToBepInEx` próprio no `.csproj`
  (copia a DLL para o perfil local depois do build).
- Depois de compilar, a DLL de cada mod fica em
  `<Mod>\bin\Debug\netstandard2.1\<Mod>.dll` — é essa que o script empacota.
