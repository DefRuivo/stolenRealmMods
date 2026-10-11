# KIT-G2 — REVISAO INDEPENDENTE (gate humano)

> Cartao `t_f19310d3` (KIT-G2) · revisor `default` **run 696** (lente round-1: ARTIFACT)
> \u2260 implementador `default` **run 695**. Data: 2026-10-10 ~12:3x BRT.
> Veredito: **APROVADO**. Natureza: gate humano (registra autorizacao + pre-registro);
> **nao** e aceite da rodada, **nao** e aprovacao tecnica e **nao** e publicacao do DoD.

## 1. Escopo revisado

Deliveravel de gate: `docs/automacao/KIT-G2-entrega.md` + partes
`KIT-G2-parte01/02/03.md`. Objeto: registrar a autorizacao do dono para a sessao MVP
isolada (perfil/save descartavel) e o pre-registro (acoes/cenarios, baseline/controle
negativo, congelamento, limites de performance) antes de o KIT-14 executar runtime.

## 2. Criterios de aceite x evidencia (medida pelo revisor, run 696)

| criterio do cartao | evidencia independente | veredito |
|---|---|---|
| Dono autoriza (build/pacote, perfil descartavel, observacao, navegacao, encerramento), escopo separado da sessao pessoal | Fonte registrada: comentario `default` 09/10 18:19 ("autorizo") + unblock 10/10 12:18; escopo B1\u2013B6 delimitado em parte01 §2 | PASSOU |
| Nao e autorizacao de publicacao | parte01 §3 / entrega §8 declaram explicitamente que publicacao\u2192KIT-G4 | PASSOU |
| Congelar artefatos durante a coleta | parte02 §5 (sha256 antes/durante/depois + `Sessao`/`HashFonte`) | PASSOU |
| Registrar acoes/cenarios pre-registrados | parte02 §3.1\u20133.4 (marco RSTV; cenarios Runner `RSTV-*`; coleta AUT-4 C0\u2013C7; controle negativo) | PASSOU |
| Registrar baseline/controle negativo | parte02 §4 (C0 isolado, fixtures negativas, `--detectar`, baseline do dono, medicao com/sem recorder) | PASSOU |
| Registrar limites de performance antes da rodada | parte03 §1 + §1.1: numero-limite = LACUNA DECLARADA (nenhum numero acordado no repo); metodo de medicao registrado, sem inventar numero | PASSOU |
| Sem aprovacao explicita, KIT-14 nao executa runtime | entrega §8 / parte01 §0 | PASSOU |
| Nada instalado/aberto/salvo/publicado nesta frente | procs do jogo vazio; `runtime-iso` ausente; nada staged | PASSOU |

## 3. Provas de estado reproduzidas pelo revisor (comandos reais)

```
date '+%Y-%m-%d %H:%M:%S %z'  -> 2026-10-10 12:30:49 -0300

sha256sum (conferido, 5 de 5 batem com entrega §7 / parte02 §2):
  AUT4Probe.dll        72928ffa4a84d79dd9a8fadce9f78bd438d1f991a0c100afb30f7bf7da561a5c  OK
  coletor.py           159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d  OK
  cenarios/rstv.py     f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7  OK
  tooltips_shrines.py  65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  OK
  lib/Assembly-CSharp.dll 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a  OK

sha256sum dos entregaveis (batem com metadata do handoff):
  KIT-G2-parte01.md  0371f10a668d79b6cfd6273fdf5e42b5fb3749c91960299d1c329fefa294c145  OK
  KIT-G2-parte02.md  3cf1c3adfb243c0cd55315c8bac11d279a93049007698d1ad34742d9422df251  OK
  KIT-G2-parte03.md  6f203071509c272ef9a37ac46bb6bd6c1394d45957a567a010702c8b0b86f6a5  OK
  KIT-G2-entrega.md  072bdf46d211c4e11e07245f8ce92bf1e3c924f56529da4b44219790e0cf7ff8  OK

Get-Process 'Stolen*'                        -> vazio (jogo do DONO FECHADO)
bash scratch/kit/front-unica.sh check        -> "lock disponivel", OK (exit 0)
ls scratch/kit/runtime-iso                   -> No such file or directory (sem residuo)
perfil do dono .../Default/BepInEx/plugins   -> sem AUT4Probe (probe ausente)
travas do repo:
  check_segredos.py          exit 0
  check_padroes_segredo.py   exit 0
  check_dupes.py             exit 0
  audita_docs.py             exit 0
git rev-parse HEAD           -> d82894ebe95d97f26b7989a848372c691dcb8ef6 (== metadata)
git diff --cached --name-only -> vazio (nada staged; sem `git add -A`)
git ls-files docs/automacao/KIT-G2-*.md -> vazio (arquivos novos/untracked)
mtime dos entregaveis: 12:26:25 / 12:27:06 / 12:27:38 / 12:28:50 (dentro da janela do run 695)
```

## 4. Ressalvas (nao bloqueantes)

- **Contagem de plugins do perfil do dono**: o entregavel declara "10 plugins"; o revisor
  mediu **11 diretorios** em `plugins/`, dos quais 2 sem DLL no topo
  (`HybridSR-Roguelike_Scaling`, `biblioteca-de-terceiros`). A afirmacao
  **material** (perfil do dono **sem `AUT4Probe`**) esta **confirmada** por `find -iname '*AUT4*'`
  (vazio). Divergencia de contagem e de rotulagem, sem efeito no escopo do gate.
- **Limite de performance**: segue como LACUNA declarada (sem numero acordado). O gate nao
  inventa numero \u2014 correto conforme a regra; o dono pode fixar o limiar antes do KIT-14.
- **Janela em relogio (B6)**: limite minimo implicito, declarado para refutacao \u2014 aceito.

## 5. Nao exercitado (declarado, nao e OK)

Runtime em jogo (leitura viva, PNG em jogo, owners vivos, navegacao por handler real,
ida-e-volta, rollback/encerramento em jogo) e build/deploy C#: **NAO_EXERCITADOS** \u2014 sao
objeto do **KIT-14** `t_a1f38855`, que este gate **libera**, nao executa.

## 6. Veredito

**APROVADO.** Os criterios de aceite do gate estao satisfeitos e as provas de estado
reproduzem independentemente. O veredito **nao** e aceite da rodada, **nao** e aprovacao
tecnica do produto e **nao** e publicacao do DoD. Ao fechar, libera **KIT-14** `t_a1f38855`.
