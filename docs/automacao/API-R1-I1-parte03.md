# API-R1-I1 — parte 03: o que fica NÃO_EXERCITADO e o que depende do dono

Tarefa `t_f32becd0`. Partes anteriores: `API-R1-I1-parte01.md` (deploy opt-in e provas),
`API-R1-I1-parte02.md` (runbook).

## 1. Declaração de NÃO exercitado (nesta tarefa nada de runtime foi executado)

| item | status | por que está assim / como se sabe |
|---|---|---|
| Abrir o jogo | **NÃO** | limitação explícita do cartão; o processo `Stolen Realm` foi conferido **ausente** antes e depois (`01`, `07`) |
| Carregamento do plugin pelo BepInEx | **NÃO_EXERCITADO** | o plugin nunca foi carregado pelo jogo; só o smoke offline em CLR (`08`) |
| Instalação no perfil `r2modman` | **NÃO_EXERCITADA** | nenhum `DeployToBepInEx=true` sem arena isolada; impressão digital do perfil idêntica em `01`/`04`/`07` (hash `8d615c0a…a436`) |
| `Safety.EnableHooks=true` / leitura do `LogOutput.log` da rodada | **NÃO_EXERCITADO** | runbook §4/§5 escritos, não rodados |
| Disparo dos quatro hooks em jogo | **NÃO_EXERCITADO** | e a base 0.1.0 **não loga disparo** (`RealmApi.Hooks` só instala postfix; `RealmHooks.Observed` sai sem assinante) — provar disparo é frente separada |
| Rollback em jogo | **NÃO_EXERCITADO** | procedimento com caminhos medidos (`§8`), mas nada foi instalado para depois remover |
| Modificação/redistribuição de `Assembly-CSharp.dll` | **NÃO FEITA** | a API é observacional; o hash do arquivo do jogo segue `8bb4a7c5…855a` (`07`) |
| Publicação (Thunderstore) | **NÃO FEITA** | ato separado e explicitamente autorizado |
| Alvo de deploy real | **PROVADO SÓ EM ARENA ISOLADA** | `06`: 3 DLLs copiadas com hashes idênticos aos do build, fora do perfil |

Regra que este cartão assume: `NÃO_EXERCITADO` **não é** verde. O que está verde é só o que tem comando e
saída em `docs/automacao/API-R1-I1-evidencias/`.

## 2. O que só o dono pode decidir/autorizar (pendências desta frente)

1. **Autorizar a rodada de runtime** — sem isso o plugin continua desligado (`Safety.EnableHooks=false`) e
   nada é instalado. O comando de instalação está em `API-R1-runbook-runtime.md` §3.2.
2. **Escolher o formato da rodada**: (a) só boot + leitura do log (barato: prova carga e instalação dos 4
   hooks) ou (b) boot + uma partida curta (mantém os postfixes vivos por mais tempo). O runbook §7 assume
   (a) como mínimo e trata (b) como observação opcional.
3. **Decidir se quer a config pré-criada** em vez de dois boots: o BepInEx cria
   `config/com.gumatos.realmapi.cfg` no primeiro boot; quem preferir pode criar o arquivo à mão antes
   (o conteúdo esperado está no runbook §4) — e então é um boot só.
4. **Janela com o jogo fechado**: a linha de base do perfil (§8.1) só vale com o jogo fechado; com o jogo
   aberto o `LogOutput.log` cresce sozinho e contamina a leitura (mesma ressalva já registrada na frente
   AUT-4).
5. **Frente separada para provar DISPARO dos hooks** (consumidor instrumentado ou contador): decisão de
   escopo, não deste cartão — a base 0.1.0 não observa o disparo pelo log.

## 3. Riscos conhecidos (para a decisão do dono)

- A API 0.1.0 é **observacional**: quatro postfixes, sem cancelar/substituir argumento ou resultado. O risco
  em jogo é de **exceção dentro do postfix**, não de mudança de regra de jogo.
- Se o jogo atualizar de verdade, o gate **recusa** (versão ou hash divergentes ⇒ zero hooks) e escreve a
  linha de recusa com os valores medidos — o runbook §6 diz onde lê-los. Não é falha da rodada: é a trava
  funcionando.
- Se um alvo tiver mudado de assinatura, `HookInstallation.Install` é **tudo-ou-nada** e reporta a exceção
  (`esperado 1 alvo, encontrados N`); a rodada é então `NÃO_EXERCITADO` por falha declarada, não por omissão.
- O rollback de nível 1 (desligar `EnableHooks`) exige **reabrir** o jogo: a config é lida no boot.

## 4. Checklist mínimo para quem revisa este cartão

```bash
cd /c/dev/stolen-realm
python tools/check_deploy_optin.py --raiz api                 # [ ok ] 1 alvo de deploy com opt-in
diff docs/automacao/API-R1-I1-evidencias/01-perfil-antes.txt \
     docs/automacao/API-R1-I1-evidencias/04-perfil-depois.txt # diferencas so no texto dos blocos
grep -cE '  [0-9]+  [0-9]{4}-[0-9]{2}-[0-9]{2} ' \
     docs/automacao/API-R1-I1-evidencias/0{1,4}-perfil-*.txt   # 30 e 30
test -e "/c/Users/Pichau/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins/RealmApi" \
     && echo RESIDUO || echo "perfil limpo (sem RealmApi)"
grep -n "Ran 25 tests; failures: 0" docs/automacao/API-R1-I1-evidencias/08-smoke-e-guarda.txt
```

Achados pré-existentes que **não** são deste cartão (não confundir na revisão): os 3 achados da guarda de
opt-in na raiz do repo, todos em `scratch/kit/KIT-14-*` (`02`) — fixtures de teste negativo de outro ciclo.

## 5. Arquivos tocados por este cartão

| arquivo | tipo |
|---|---|
| `api/Plugin/RealmApi.csproj` | editado (alvo `DeployToBepInEx` opt-in, linhas 19-41) |
| `api/README.md` | editado (seção "Como construir" e lista de NÃO exercitado — coerência com o alvo novo) |
| `docs/automacao/API-R1-runbook-runtime.md` | **novo** |
| `docs/automacao/API-R1-I1-parte01.md` | **novo** |
| `docs/automacao/API-R1-I1-parte02.md` | **novo** |
| `docs/automacao/API-R1-I1-parte03.md` | **novo** (este) |
| `docs/automacao/API-R1-I1-evidencias/01…09` | **novos** (saída bruta de comando) |

Nada fora do repo foi tocado: o jogo e o perfil do r2modman ficaram byte a byte como estavam.

## 6. Nota sobre referência ao mod antigo (LIMITES do cartão)

O módulo não referencia o mod antigo em nome, descrição ou código: a checagem sobre o código e sobre os
documentos `.md` devolve **0 arquivos** (`exit 1`). O literal dos nomes do mod legado é **omitido deste
documento de propósito** (mesma regra do cartão pai); o padrão usado foi o do `leak_check` da API-R1:

```bash
grep -ril -E '<mod-legado-A>|<mod-legado-B>' api/ \
     docs/automacao/API-R1-runbook-runtime.md docs/automacao/API-R1-I1-parte0*.md   # exit 1 = nada
```

As evidências `01`, `04` e `07` são a **listagem crua** de `plugins/` + `config/` do perfil do dono
(caminho, bytes, mtime, sha256) e por isso trazem os nomes de pastas que **já existiam** na instalação dele,
inclusive uma pasta de legado desativada. Isso é a impressão digital do perfil — o insumo do comparativo
antes × depois —, não referência nominal deste módulo; os nomes de terceiros que aparecem ali são
consequência de ler o diretório, e nenhum deles foi criado, alterado ou removido por esta tarefa.
