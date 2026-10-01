# BetterFont

Mod **BepInEx 5** para **Stolen Realm** que troca a fonte renderizada do jogo por uma **serifada (Times New Roman**, com fallback Georgia / Liberation Serif). **Não altera gameplay.**

- **GUID:** `com.gumatos.betterfont`
- **Versão:** 1.0.1
- **Compatível com:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026).
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

- Substitui a fonte de **todos os textos TMP** do jogo por um asset serifado — inclusive telas que abrem depois do boot (level up, tooltips, menus de configuração).
- **Preserva o estilo** (cor de face, contorno e sombra): antes de trocar a fonte, as propriedades de estilo do material que o texto já usava são transportadas para o material **por componente** da fonte nova. Sem isso a troca apagava cor/contorno/sombra — era o defeito da 1.0.0.
- **Preserva o efeito de material de QUALQUER origem** — inclusive o que **outro mod** tenha aplicado naquele texto (contorno/halo, sombra). O texto continua recebendo a serifa e o efeito que já estava nele é reaplicado no material novo. Se o efeito em uso não puder ser reproduzido com fidelidade (textura de face, glow/bevel, shader incompatível), o texto **não é tocado** — melhor não mexer do que entregar meia cópia.
- Se você preferir o comportamento antigo (texto com material próprio, como os títulos e os números de combate do jogo, fica **100% intocado** e não ganha a serifa), ligue `Estilo/PularTextosEstilizados` — ver Configuração.
- A **fonte original do jogo entra como fallback** do asset serifado: ícones, glifos e símbolos que a Times New Roman não tem continuam renderizando, sem virar quadradinho.
- A varredura roda com **tempo real**, então funciona mesmo com `timeScale = 0` (é o caso dos menus do Stolen Realm, onde coroutines e `InvokeRepeating` nunca disparam).
- O updater é criado de forma **preguiçosa**, na primeira UI viva (gatilho em `OptionsManager.Localize`). Criá-lo no `Awake` do plugin não funciona: o jogo destrói o GameObject na primeira carga de cena.
- **Sem qualquer alteração de gameplay** — só a aparência do texto muda.

## O que ele NÃO faz

- **Não altera gameplay** — não muda valor, dano, regra nem balanceamento.
- **Não modifica nenhum arquivo do jogo** (nem save) e não deixa resíduo ao ser removido.
- **Não traduz nem reescreve texto nenhum** — troca só a **face** da fonte; o conteúdo continua sendo o original do jogo.
- **Não escreve no material compartilhado** de nenhum texto e nem no material de outro mod (só **lê** o material em uso, para copiar o estilo) — a cópia é sempre a instância **por componente**.

## Por que a 1.0.0 quebrava o estilo (e o que mudou na 1.0.1)

Em TextMeshPro, `texto.font = novaFonte` **não troca só o tipo de letra**: o `LoadFontAsset()` do TMP descarta o material em uso e passa a usar o **material do asset novo**. Como a cor de face, o contorno e a sombra do jogo vivem **no material**, a troca de fonte apagava o estilo — o defeito aparecia ao entrar em combate ("quebra o estilo e a coloração das fontes").

Na 1.0.1 a varredura faz, nesta ordem:

1. **Captura** o material em uso (`fontSharedMaterial`) do componente antes de mexer.
2. Se `PularTextosEstilizados = true` (escape, **padrão `false`**), o texto com material próprio **não troca de fonte** — visual original 100% intacto.
3. Senão, troca a fonte e **copia as propriedades de estilo** para o material **por componente** (`fontMaterial` — instância só daquele texto), sempre testando `HasProperty` antes de cada `Set`:
   - cor de face `_FaceColor`, `_FaceDilate`;
   - contorno `_OutlineWidth`, `_OutlineSoftness`, `_OutlineColor` + keyword `OUTLINE_ON`;
   - sombra `_UnderlayColor`, `_UnderlayOffsetX/Y`, `_UnderlayDilate`, `_UnderlaySoftness` + keyword `UNDERLAY_ON`.

Essa cópia é o que faz o **efeito aplicado por outro mod** (ou pelo próprio jogo) sobreviver à troca de fonte: o que estava no material anterior daquele texto é reaplicado no material novo — a mesma regra para qualquer mod, sem um conhecer o outro.

**Não** se copia atlas/textura (`_MainTex`, `_TextureWidth`, `_TextureHeight`, `_GradientScale`, `_ScaleRatio_*`): isso pertence à fonte **nova**. Texturas de face (`_FaceTex`), bevel (`_BumpMap`) e as keywords `GLOW_ON`/`BEVEL_ON` não são transportadas — e quando o efeito em uso depende de um deles (ou de um shader incompatível), o texto **não é tocado** (falha-segura: em dúvida, nada pior que hoje). O log de diagnóstico diz, por texto, o que foi copiado e o que ficou de fora.

## Configuração (`BepInEx\config\com.gumatos.betterfont.cfg`)

| Seção | Chave | Padrão | O que faz |
|---|---|---|---|
| `Estilo` | `PreservarEstilo` | `true` | Copia cor/contorno/sombra do material antigo para o material por componente da fonte nova. |
| `Estilo` | `PularTextosEstilizados` | `false` | `false` (padrão): troca a fonte **também** dos textos com material próprio e **reaplica os efeitos que já estavam nele** — é o que mantém o contorno/sombra aplicado por outro mod. `true`: **escape**, comportamento antigo — não troca a fonte de quem tem material próprio (visual original 100% intacto, sem serifa). |
| `Diagnostico` | `LogDiagnosticoEstilo` | `false` | Loga, no `LogOutput.log`, um bloco por texto tratado: objeto, fonte, material compartilhado, shader, o que foi copiado e o que **não** pôde ser transportado. |

O `.cfg` é lido no boot do jogo: mude os valores e reabra o jogo.

## Convivência com outros mods que estilizam texto

Vale para **qualquer** mod que aplique efeito de material (contorno/halo, sombra) num texto de combate ou de qualquer tela: o BetterFont troca a fonte daquele texto e **reaplica no material novo os efeitos que já estavam no material anterior** — quem aplicou o efeito continua com ele, e o texto também ganha a serifa. Não há ordem obrigatória entre os mods: se o efeito for aplicado **antes**, o BetterFont o transporta; se for aplicado **depois**, o mod do efeito clona o material já serifado e o mantém. Nenhum dos dois precisa conhecer o outro.

Só quando o efeito **não** puder ser reproduzido com fidelidade (textura de face, glow/bevel, shader incompatível) o BetterFont deixa aquele texto intocado — e o `Estilo/PularTextosEstilizados = true` restaura o comportamento antigo para todos eles.

## Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a DLL em `BepInEx\plugins\BetterFont\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `BetterFont` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\BetterFont\BetterFont.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   [Info   :Better Font] Better Font carregado.
   ```

## Como desfazer

Apague a pasta `BepInEx\plugins\BetterFont\` (ou desabilite o pacote no r2modman) e abra o jogo de novo. A fonte original volta no próximo boot — o mod não modifica nenhum arquivo do jogo nem deixa resíduo.

## Compilar do fonte

```powershell
cd BetterFont
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterFont.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
