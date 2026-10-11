# KIT15-D6-CRLF — parte 01: contra-prova discriminante em clone Windows CRLF

Tarefa `t_be4d89d9` (filha de ORG-PRE-DOC `t_d803c318`; o achado foi declarado como ressalva não
bloqueante no §7 da revisão independente daquela frente). Repo `C:/dev/stolen-realm`. Perfil
`default` confirmado por `hermes profile list` em 11/10/2026. Fotografia de 11/10/2026 17:56 -03:00,
HEAD de entrada `26e3fda62bcc01952adcccdbd944f14e60603b7b` (ORG-R2-E1). Um **commit nominal**:
ferramenta + testes + este relatório.

## 1) O que esta frente fez — e o que NÃO fez

**Feito** (só ferramenta de bancada, sem jogo):

1. `tools/automacao/kit15/contra_prova_kit15.py` — `aplicar_defeito` passou a ancorar por **bytes**,
   reescrevendo a âncora no estilo de quebra de linha do arquivo alvo;
2. `tools/automacao/kit15/teste_kit15.py` — 3 testes novos (`TesteContraProva`, `test_19`..`test_21`);
   a suíte passou de 18 para **21 testes**;
3. `tools/automacao/kit15/README.md` — contagem da suíte (18 → 21) e a linha de compatibilidade
   **medida** (a contra-prova vale em checkout LF **e** CRLF);
4. este relatório.

**NÃO feito, registrado honestamente:**

- nenhum código do jogo, nenhum `Release`/`Debug`, nenhum deploy, nenhuma instalação no perfil do
  dono, nenhum `BepInEx`, nenhum push/publicação/tag;
- nenhum arquivo do KIT-15 foi reescrito além dos dois acima; **nenhum skip** foi criado, nenhum
  veredito `MUTACAO-INVALIDA` foi aceito e **nenhum critério foi afrouxado** (o baseline continua
  exigindo o número exato de testes, zero falha, zero erro, zero skip);
- o saneamento documental de ORG-PRE-DOC **não** foi reimplementado e `tools/check_padroes_segredo.py`
  (SEG) **não** foi tocado;
- nenhum documento histórico de `docs/automacao/KIT-15*.md` foi editado: eles são snapshots de runs
  (com hashes medidos daquele momento) e ficam como estão;
- nenhum snapshot do dono e nenhuma alteração manual já existente na árvore de trabalho foram
  tocados: as edições abertas de AUT5 (`tools/automacao/aut5/*`) foram preservadas como estavam.

## 2) Sintoma reproduzido (ANTES da correção)

Contra-prova do KIT-15 é o meta-teste da suíte: planta UM defeito real em cada módulo, roda a suíte
inteira na cópia e exige RED honesto, com o conjunto de falhas **exatamente** o alvo do defeito.

| Árvore | Comando | Resultado medido |
|---|---|---|
| repo vivo (LF) | `python tools/automacao/kit15/contra_prova_kit15.py` | baseline verde · **7/7** recusados · exit 0 |
| clone Windows `core.autocrlf=true` (CRLF, HEAD 26e3fda) | idem | baseline verde · **6/7** · `D6` = `MUTACAO-INVALIDA` · exit 1 |

Saída real do clone (sandbox `C:\tmp\kit15-crlf\out-antes\contra-prova.json`):

```
baseline-intacto                               OK (-)
D1..D5                                         OK
D6-descoberta-ignora-argumento-explicito       MUTACAO-INVALIDA
D7-pacote-verificador-sempre-ok                OK
CONTRA-PROVA|FALHOU|baseline=True|recusados=6/7
```

Ou seja: no clone, a prova de que a suíte **pega** o defeito D6 simplesmente não acontecia — e o
`baseline=True` mascarava isso como "ferramenta quase boa", não como falha de mutação.

## 3) Causa medida

`aplicar_defeito` lia o arquivo com `open(..., newline="")` e comparava a âncora literal declarada na
lista `DEFEITOS`. A âncora do D6 é a **única multiline** do conjunto
(`'    if explicito:\n        return os.path.abspath(explicito), "argumento"'`): as outras seis são de
uma linha só e casam em qualquer estilo. Medido por contagem de bytes:

| Arquivo | repo vivo | clone CRLF |
|---|---:|---:|
| `descoberta.py` — CRLF / LF puro | 0 / 215 | 215 / 0 |

Logo, no clone, `dados.count(<âncora com \n>)` = **0** → `texto alvo aparece 0 vezes (esperado 1)` →
`MUTACAO-INVALIDA`. A leitura correta do resultado é: **a ferramenta de prova perdia poder
discriminante fora do checkout LF do autor.**

## 4) Correção

`contra_prova_kit15.py`:

- `estilo_de_quebra(dados)` — com bytes crus, devolve `"\r\n"` (só CRLF), `"\n"` (só LF) ou `None`
  (arquivo misto/vazio). Misto **não** é adivinhado: a mutação é recusada com motivo explícito;
- `_no_estilo(ancora, estilo)` — reescreve a âncora declarada com `"\n"` no estilo do arquivo alvo;
- `aplicar_defeito` — lê em `rb`, conta e substitui **bytes**, grava em `wb`. Só o trecho ancorado
  muda: nenhuma quebra de linha fora do alvo é convertida, nenhum byte é normalizado;
- `TESTS_ESPERADOS = 21` substitui o `18` literal do check de baseline (a suíte cresceu com testes
  novos e o número continua **exato**: suíte truncada não vira verde);
- `MODULOS` passou a incluir `contra_prova_kit15.py`, porque a suíte roda dentro da sandbox e o
  `TesteContraProva` importa a própria ferramenta.

`teste_kit15.py` — `TesteContraProva`, com arquivos **sintéticos** próprios (não o módulo vivo, para
continuar válido mesmo quando o defeito D6 está aplicado na sandbox):

- `test_19_ancora_multiline_casa_em_lf_e_em_crlf` — a mesma âncora multiline aplica em LF **e** em
  CRLF, e o resultado é byte a byte o esperado (estilo de quebra intacto);
- `test_20_ancora_ausente_ou_ambigua_e_recusada_sem_tocar_bytes` — 0 ocorrências e 2 ocorrências são
  recusadas com motivo, **sem escrever** no arquivo;
- `test_21_quebras_mistas_nao_sao_adivinhadas` — arquivo misto é recusa explícita.

## 5) Provas medidas (DEPOIS)

| Prova | Comando | Resultado |
|---|---|---|
| suíte no repo vivo | `python tools/automacao/kit15/teste_kit15.py` | `Ran 21 tests` · **OK** · exit 0 |
| contra-prova no repo vivo (LF) | `python tools/automacao/kit15/contra_prova_kit15.py` | baseline verde · **7/7** · exit 0 |
| contra-prova em clone CRLF | idem, no clone `core.autocrlf=true` | baseline verde · **7/7** · exit 0 |
| runner completo no clone CRLF | `bash tools/automacao/kit15/roda_testes_kit15.sh` | `KIT-15 RESULTADO|VERDE|suite=0 contra-prova=0` |
| mutação do D6 no clone CRLF | `resultado-D6.json` | falhas = `['__main__.TesteDescoberta.test_15_descoberta_sem_usuario_fixo']` — **só** o alvo, 0 erro, 0 skip, exit 1 |

Integridade de bytes do mutante (nada além do trecho ancorado mudou):

| Árvore | `descoberta.py` original → mutante | CRLF original → mutante | LF puro original → mutante |
|---|---|---|---|
| LF | 8059 → 8055 bytes | 0 → 0 | 215 → 215 |
| CRLF | 8274 → 8270 bytes | 215 → 215 | 0 → 0 |

A diferença de 4 bytes é exatamente `if explicito:` → `if False:`; a âncora trocada aparece no mutante
com o **mesmo** estilo de quebra do arquivo, e o resto do arquivo é idêntico (o primeiro byte
divergente cai dentro da âncora).

## 6) Controle negativo do PRÓPRIO teste (a regressão não pode voltar em silêncio)

Só afirmar "7/7 nos dois" não prova que o teste novo pega a regressão. Foi injetada, numa cópia
CRLF, a implementação **antiga** de `aplicar_defeito` (âncora só LF) e rodado `TesteContraProva`:

| Rodada (clone CRLF, `descoberta.py` 215 CRLF / 0 LF puro) | tests | reprovados |
|---|---:|---|
| implementação CORRIGIDA | 3 | `[]` |
| implementação ANTIGA injetada | 3 | `test_19_ancora_multiline_casa_em_lf_e_em_crlf`, `test_21_quebras_mistas_nao_sao_adivinhadas` |
| veredito | — | `META-CONTROLE|OK` (exit 0) |

## 7) Limites declarados

- Nada aqui foi exercitado **dentro do jogo**: não abre BepInEx, não compila C#, não usa rede, não
  toca o perfil do dono; é bancada Python stdlib. Um segundo host e Linux/macOS continuam
  **NÃO medidos**.
- `README.en.md` e `CHANGELOG.md` do KIT-15 **não são versionados** (regra `*.md` do `.gitignore`, sem
  exceção nominal no índice): as contagens neles (18 → 21) e a entrada de `Corrigido` sobre este
  achado foram ajustadas **no disco**, fora do commit. Fica registrado para não parecer descuido nem
  mudança invisível de entrega.
- O número de testes (21) é conferido pelo baseline da contra-prova; quem acrescentar teste ao KIT-15
  tem de atualizar `TESTS_ESPERADOS` no mesmo commit.
- Arquivos alterados neste commit e seus SHA-256 de disco:

| Arquivo | bytes | sha256 |
|---|---:|---|
| `tools/automacao/kit15/contra_prova_kit15.py` | 13287 | `7b4ad894122d7ec187bb8ce183a9989ad70b94ffcacc3bdfbe08be4dfee09b34` |
| `tools/automacao/kit15/teste_kit15.py` | 26346 | `5077e5eb836b1e4867d8048a866ab816101aa6a39e15c596222c4ebd922a99ed` |
| `tools/automacao/kit15/README.md` | 7074 | `1c907e1b7a655480e5b9598f4da26194555044184035fefc4d89987bf8b1e4ad` |

## 8) Como reproduzir

```bash
# 1) repo vivo (LF): suíte + contra-prova + runner
python tools/automacao/kit15/teste_kit15.py
python tools/automacao/kit15/contra_prova_kit15.py
bash   tools/automacao/kit15/roda_testes_kit15.sh

# 2) clone Windows CRLF (o caso que falhava)
git -c core.autocrlf=true clone <repo> clona-crlf
cd clona-crlf
python -c "d=open('tools/automacao/kit15/descoberta.py','rb').read(); print(d.count(b'\r\n'), d.count(b'\n')-d.count(b'\r\n'))"
bash tools/automacao/kit15/roda_testes_kit15.sh      # esperado: VERDE, 7/7, exit 0

# 3) resultado estruturado de cada defeito (o que a contra-prova lê)
cat <sandbox>/resultado-D6.json
```
