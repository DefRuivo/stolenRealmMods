# kit-rstv — pacote instalável (KIT-15)

Distribuição **local** do kit de teste/observação de mods de **Stolen Realm**.
Core + Adapter + Recorder são obrigatórios; Runner, Viewer, Integração e SDK são opcionais.

> Este pacote **não publica nada**. Push, tag, GitHub Release, Thunderstore e `publicar:true`
> pertencem a KIT-G4 e não são executados por nenhuma ferramenta daqui.
> Nada aqui abre o jogo, instala no perfil do dono, mexe em save ou usa rede.

## Para quem não programa

O passo a passo em PT-BR tem estes caminhos, conforme o layout:

- **Repositório de origem:** `tools/automacao/kit15/docs/primeiro-uso.md`
  (caminho relativo a este README: `docs/primeiro-uso.md`).
- **Pacote extraído:** `docs/primeiro-uso.md`, **ao lado** de `docs/README.md`.

Este README é copiado sem alteração para o pacote. Os caminhos são apresentados
como texto para não oferecer um link relativo que só funcione em um dos layouts.
Resumo: você precisa de **Python 3** (só a biblioteca padrão) para instalar/atualizar/remover/scan;
se `python` não estiver disponível, existe o **modo manual** (extrair o zip e apagar a pasta),
também descrito lá. Compilar C# é **opcional** e só para quem for usar Core/Adapter em jogo.

## O que tem dentro

| Componente | Obrigatório | Linguagem | Papel |
|---|---|---|---|
| `core` | sim | C# | esquema, serialização, eventos e validação |
| `adapter` | sim | C# | hooks/leitura do Stolen Realm e tradução para o Core |
| `recorder` | sim | Python | observação passiva, trava de acesso e coleta/rollback |
| `runner` | não | Python | execução determinística de cenários conhecidos |
| `viewer` | não | Python | relatório HTML estático dos resultados |
| `integracao` | não | Python | ciclo alteração → evidência → correção → revalidação |
| `sdk` | não | C# | API versionada (`Gumatos.KitSdk.V1`) para extensões de mod |

Versão do pacote: **0.1.0** (candidato local). Cada componente tem a sua própria versão,
lida do `.csproj` ou do código, e registrada em `kit-rstv.manifest.json`.

## Instalar / atualizar / remover / rollback (offline)

Da pasta extraída do pacote (onde está `kit-rstv.manifest.json`):

```bash
python tools/instalador.py instalar  --pacote . --destino C:/kit-rstv
python tools/instalador.py atualizar --pacote . --destino C:/kit-rstv
python tools/instalador.py status    --destino C:/kit-rstv
python tools/instalador.py rollback  --destino C:/kit-rstv
python tools/instalador.py remover   --destino C:/kit-rstv
```

Sem `--destino`, o destino é **descoberto** (sem usuário fixo em lugar nenhum):
`--destino` → variável `KIT_RSTV_HOME` → arquivo de configuração do usuário →
`<raiz do repo>/dist/kit-rstv` (quando o layout do repo existe) → `<HOME do usuário>/kit-rstv`.
Para ver o que foi resolvido:

```bash
python tools/descoberta.py --json
python tools/descoberta.py --destino-sugerido
```

### Garantias do instalador

Garantias **medidas** pela suíte offline deste pacote (`tools/teste_kit15.py`, 21 testes) e pelos
oráculos de revisão KIT-15R (27 + 3 testes):

- toda escrita é conferida por **hash lido de volta**; divergência dispara **rollback automático** e exit 1;
- cada transação fica registrada em `<destino>/.kit-rstv-transacoes/<ts>.json` e pode ser revertida;
- bytes anteriores ficam em `<destino>/.kit-rstv-backups/<ts>/`;
- `atualizar` reescreve **somente** arquivo cujo hash difere (arquivo idêntico não é tocado);
- `remover` devolve o arquivo que já existia **byte a byte** e apaga apenas o que o recibo declara como criado pelo kit;
- arquivo local que não pertence ao recibo é preservado (há teste explicitamente para isso);
- caminhos de origem/destino/backup/recibo são confinados à raiz do destino: manifesto ou recibo com
  `..`/absoluto/drive/UNC é recusado **antes** de qualquer efeito;
- falha de I/O no meio da cópia reverte a transação e não deixa payload sem recibo/journal;
- backup de original corrompido ou ausente faz `remover` **falhar fechado** (não sobrescreve o destino);
- exit code sempre distingue: `0` ok · `1` falha lógica (hash/estado/entrada) · `2` erro de infraestrutura.

Estas garantias valem para o uso offline descrito aqui. Elas **não** foram medidas dentro do jogo
(ver "Limites declarados" e "Compatibilidade").

## Gerar o zip candidato e conferir

```bash
python tools/pacote.py montar --saida scratch/kit/KIT-15-minha-rodada
python tools/pacote.py verificar <caminho>/kit-rstv-0.1.0.zip
python tools/scan.py <caminho>/kit-rstv-0.1.0.zip --json
```

O `pacote.py` monta o staging, escreve `kit-rstv.manifest.json` com hashes **medidos**,
gera o zip determinístico, roda `testzip` e o scan. O relatório sai em
`<saida>/pacote-relatorio.json` com `veredito`, `zip_sha256`, `zip_membros` e `scan_achados`.

O `scan.py` reprova: credencial/chave privada/token em texto — inclusive quando aparecem em JSON,
sem imprimir o segredo —, qualquer `.dll`/`.pdb`/`.exe` **em qualquer caminho** (inclusive dentro do
zip e em pastas como `bin/`) e ainda `.git/`, `__pycache__/`, `obj/` e logs. Entrada ilegível **não**
vira "limpo": ela é reportada como erro de I/O e o exit é `2` (infraestrutura).

## Testes (offline, sem jogo)

```bash
python tools/teste_kit15.py                # suite: 21 testes
python tools/contra_prova_kit15.py         # defeitos plantados TEM de reprovar (RED)
bash  tools/roda_testes_kit15.sh           # suite + contra-prova + exit 0/1/2
```

## Dependências

- **Uso básico** (instalar/atualizar/remover/rollback/scan/zip): Python 3 stdlib.
  Sem rede, sem conta, sem credencial, sem IA, sem Hermes, sem SDK .NET.
- **Uso avançado** (compilar Core/Adapter/exemplos): .NET SDK 6+ e as referências Unity
  locais do jogo (`lib/`), que **não** são redistribuídas neste pacote.

## Limites declarados

- Runtime em jogo (BepInEx carregando o plugin, UI/UX, pixels, personagem) é **NÃO_EXERCITADO** aqui:
  exige gate humano e rodada autorizada.
- O pacote é uma distribuição **local**; publicação é KIT-G4.
- Aprovação técnica não é aceite humano nem DoD.

## Compatibilidade — medido × não medido

**Medido nesta entrega:** Windows 11 + Python 3.14 (somente biblioteca padrão); a suíte do pacote e a
contra-prova rodando na árvore **extraída**, sem o repositório do autor e sem variáveis do autor; a
geração e a verificação do zip; o runner de shell `tools/roda_testes_kit15.sh` sob **bash do Git for
Windows (MSYS)**; a contra-prova discriminando os 7 defeitos em checkout **LF** e em checkout
**CRLF** (clone Windows com `core.autocrlf=true`).

**NÃO medido:** Linux/macOS e outros shells; o `bash` do WSL (não enxerga caminhos `C:\...` — o runner
precisa de um bash que entenda caminhos do Windows); compilar Core/Adapter/SDK (exige .NET SDK 6+ e as
referências Unity do jogo, que não são redistribuídas); carregar o plugin no jogo; um segundo host.
