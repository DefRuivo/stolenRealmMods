# Primeiro uso — kit-rstv (para quem não programa)

Este guia assume que você **nunca usou** o kit. São 4 passos: conferir o pacote, escolher onde
instalar, instalar e conferir. No fim, como desfazer.

Tempo: ~5 minutos. Você **não** precisa do jogo aberto, nem de conta, nem de internet.

---

## Passo 0 — o que você precisa

- Um computador Windows (o kit também é Python puro, mas só foi medido em Windows 11 até agora).
- O arquivo `kit-rstv-0.1.0.zip` que alguém te entregou **localmente** (não existe publicação oficial
  deste kit; ele não está na Thunderstore).
- **Python 3** instalado (o modo manual no fim dispensa isso).

Para verificar se o Python existe, abra o terminal (Prompt de Comando) e digite:

```
python --version
```

Se aparecer algo como `Python 3.14.7`, você está pronto. Se der erro, use o **modo manual** no fim.

---

## Passo 1 — extrair e conferir o pacote (sem instalar nada)

1. Crie uma pasta, por exemplo `C:\temp\kit-rstv-pacote`.
2. Clique com o botão direito no zip → **Extrair tudo…** → aponte para essa pasta.
3. Abra o terminal dentro dela (no Explorer: Shift + botão direito → "Abrir janela do PowerShell aqui")
   e rode:

```
python tools\pacote.py verificar kit-rstv-0.1.0.zip
```

O que você deve ver: uma linha começando com `PACOTE|OK|`. Isso significa que o zip está íntegro
e **não contém DLL do jogo nem credencial**. Se aparecer `ACHADO`, não instale: avise quem te passou
o arquivo, porque algo estranho entrou no pacote.

---

## Passo 2 — escolher onde instalar

Nada no kit assume o **seu** nome de usuário. Você decide o destino das três formas abaixo
(a primeira que existir vence):

1. você diz na hora: `--destino C:\kit-rstv`
2. variável de ambiente `KIT_RSTV_HOME`
3. se você não disser nada, o kit cai no padrão: `C:\Users\<seu usuário>\kit-rstv`

Para ver o que ele escolheria **sem** instalar nada:

```
python tools\descoberta.py --json
```

No campo `destino_kit` está o caminho que será usado e em `destino_origem` está o motivo
(`argumento`, `ambiente:KIT_RSTV_HOME`, `config`, `padrao-repo` ou `padrao-home`).
Os campos `jogo` e `perfil_bepinex` podem vir `null`: isso é normal — o uso básico não precisa deles
e o kit **não escreve** no perfil do jogo.

---

## Passo 3 — instalar e conferir

```
python tools\instalador.py instalar --pacote . --destino C:\kit-rstv
python tools\instalador.py status   --destino C:\kit-rstv
```

Esperado: a primeira linha termina em `exit=0` e o `status` mostra `"estado": "INSTALADO"`.
O instalador copia os arquivos, **lê cada um de volta** e compara o hash com o manifesto.
Se qualquer byte sair diferente, ele desfaz tudo sozinho e sai com erro — você não fica com
instalação pela metade.

Dentro de `C:\kit-rstv` você vai encontrar:

```
kit-rstv.manifest.json        ficha do pacote: versões, arquivos, hashes
components\core\...           fontes do Core (C#)
components\adapter\...        fontes do Adapter (C#)
components\recorder\...       observação passiva (Python)
components\runner|viewer|integracao|sdk\...   opcionais
tools\...                     instalador, pacote, scan, testes
docs\...                      README, este guia e o changelog
.kit-rstv-installed.json      recibo: o que está instalado e com que hash
.kit-rstv-backups\...         bytes anteriores (para desfazer)
```

### Atualizar (quando alguém te passa uma versão nova)

```
python tools\instalador.py atualizar --pacote . --destino C:\kit-rstv
```

Só os arquivos que **mudaram de verdade** são reescritos. Arquivo igual não é tocado; arquivo seu
que não pertence ao kit nunca é apagado.

### Desfazer uma atualização

```
python tools\instalador.py rollback --destino C:\kit-rstv
```

Isso volta a última transação (instalação, atualização ou remoção) ao estado imediatamente anterior.

---

## Passo 4 — desinstalar

```
python tools\instalador.py remover --destino C:\kit-rstv
```

- arquivos que o kit criou são apagados;
- arquivos que **já existiam** antes do kit voltam byte a byte, do backup guardado na instalação;
- qualquer arquivo seu que não faz parte do kit continua onde estava.

---

## Modo manual (sem Python)

O pacote é só arquivos de texto: você pode usá-lo sem o instalador.

Instalar à mão:

1. extraia o zip numa pasta nova;
2. copie a pasta `components` para o destino (por exemplo `C:\kit-rstv\components`);
3. copie `tools` e `docs` para o mesmo destino;
4. pronto. Para conferir a integridade sem Python, compare os tamanhos dos arquivos com as colunas
   do `kit-rstv.manifest.json` (cada componente lista `rel`, `sha256` e `bytes`).

Remover à mão: apague a pasta do destino. Como o modo manual não escreve em nenhum outro lugar,
não sobra nada para trás — **desde que você tenha copiado para uma pasta nova**. Se você copiou por
cima de arquivos seus, o modo manual **não** tem como restaurá-los: use o instalador para ter rollback.

---

## Primeiros passos depois de instalar (opcional)

- Ler o contrato do SDK: `docs/README.md` (seção de componentes) e o projeto de exemplo do próprio
  SDK em `components/sdk/` (`KitSdk.csproj` + `RegistryV1.cs`). Este pacote **não** traz cenários de
  exemplo nem JSON de pertinência: Runner, Viewer e Integração são opcionais e dependem de dados que
  você mesmo fornece.
- Rodar os testes offline do próprio kit (não abrem o jogo):

```
python tools\teste_kit15.py
python tools\contra_prova_kit15.py
```

- Gerar um zip candidato a partir da sua cópia:

```
python tools\pacote.py montar --saida C:\temp\minha-rodada
```

## O que este kit NÃO faz

- Não abre, fecha ou modifica o jogo; não instala nada no perfil do BepInEx.
- Não publica em lugar nenhum (Thunderstore, GitHub Release, tag, push).
- Não contém DLL do jogo nem de terceiros.
- Não exige IA, Hermes, conta, assinatura ou internet.

## O que foi medido (e o que não foi)

Medido: Windows 11 + Python 3.14 (só biblioteca padrão), com o pacote **extraído** numa pasta qualquer,
sem o repositório de quem montou o kit. É esse o cenário que os testes cobrem.

Não medido: Linux/macOS; o `bash` do WSL (ele não entende caminhos `C:\...`; para o runner de shell use
o **Git Bash**); compilar o C# (`components/*.csproj` exige .NET SDK 6+ e as referências Unity do jogo,
que não vêm no pacote); e nada dentro do jogo (carregar o plugin, UI, personagem) — isso exige uma
rodada autorizada, com gate humano.

Se o `remover` encontrar um backup corrompido ou ausente, ele **para** em vez de restaurar lixo: nesse
caso o arquivo do destino é preservado e você recebe erro (`exit 1`) para resolver à mão.
