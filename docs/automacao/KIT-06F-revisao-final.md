# KIT-06F — REVISAO INDEPENDENTE (rodada 2) — APROVADO

Cartao `t_73f0779f`. Revisor **run652** (perfil default), instancia distinta do
implementador **run650** e do autor **run641**, e distinta tambem do revisor da
rodada 1 (**run645**) e do revisor de origem (**run638**). Nenhum arquivo de
implementacao foi editado por esta revisao.

Lente da rodada (skill sdlc-review): **Execution** — a rodada 1 (`changes_requested`)
pediu a correcao do F6 no caminho ANINHADO; aqui o trabalho foi **executado por
mim**, com defeito REAL plantado pelo revisor, em vez de re-ler o resumo.

Tudo em sandbox proprio: `scratch/kit/KIT-06R-run652/` (TMP/TEMP/TMPDIR
apontados para `scratch/kit/KIT-06R-run652/tmp`).

## 1. Fontes entregues conferem (SHA256 medidos por mim)

```
379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457  tools/automacao/runtime/controle_acesso.py
cad1bcc26cf10d4d754e8e96c076fc39c6dd13ca05486dbe73581e0163cc9084  tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs
e864ac9dbf86dba3403986b8bd6d5adfc43f9caf80a5f0672a927df1a9aebe81  tools/automacao/runtime/harness-controle/Program.cs
375edb6f28c1de10b2346ebc3aab248abc2f5be36caf9771e9b0eaff32e2b1fa  tools/automacao/kit06/teste_controle_acesso.py
d4a2cbb77313e3d63ceb7fb41869cc006e4eaa16375d53e27d77287321a7fbc4  tools/automacao/kit06/contra_prova_kit06.py
```
Batem byte a byte com `KIT-06F-entrega.md` e `scratch/kit/KIT-06F-run650/verificacao-final.json`.

Fontes do revisor preservados e reusados **verbatim** (nao uma linha alterada):
- oraculo Python: `scratch/kit/KIT-06R-run638/test_revisao_kit06.py`
  sha256 `68d6283d2222260ca4792db7f84e5a2254d4d1ef8fb35b8d66d4aaa9b5b5cc7a`
- oraculo C#: `scratch/kit/KIT-06R-run638/harness-reviewer/Program.cs`
  sha256 `1035cd9e8213a95436138cbabd3225225d1bc07ea7ab172629d34ddf913cd341`
- probe F6 aninhado: `scratch/kit/KIT-06R-run645/probe_f6_aninhado.py` e `cs-probe/`

## 2. Correcao pedida na rodada 1 (F6 aninhado) — CONFIRMADA por execucao

**Codigo (lido, nao inferido):** `_coleta_documento` aplica `_copia_profunda` a
`resumo`/`eventos`/`degradacoes`/`rejeitados`/`lacunas`/`capturas`
(`controle_acesso.py:522-532`) e a `trilha_controle` (`:576`); o helper e recursivo
(`:162-176`). No C#, `ColetaDocumento` usa `CopiaValor(...)` em
`Resumo()`/`Eventos()`/`Degradacoes()` (`PonteControleRSTV.cs:457,464-465`) com o
helper recursivo em `:635-657`.

**Probe do revisor, verbatim, contra o fonte VIVO:**
```
python probe_f6_aninhado.py                  -> campos limpos=6 contaminados=0, exit0
```
**Discriminacao (defeito REAL plantado por MIM, nao pelo autor):** reverti a copia
profunda em uma copia do fonte vivo (`mutpy/`, `resumo=dict(resumo)`,
`eventos=[dict(e) for e in eventos]`) — e o MESMO probe reprova:
```
python probe_mutpy.py -> contaminados=4, "PROPAGACAO INTERNA DETECTADA", exit1
```
**C# (defeito plantado por mim: `b["eventos"] = eventos`):**
```
probes/live  (vivo)    -> contaminados=0, exit0
probes/mut   (plantado) -> contaminados=2, exit1
```
O probe C# do revisor (run645 `cs-probe/Program.cs`, verbatim) tambem passa no vivo.
Contra o "antes" gerado pelo proprio autor (`KIT-06F-run650/antes-prefix`) o probe
Python reprova com os mesmos 4 campos contaminados — consistente com a rodada 1.

## 3. Oraculos do revisor (run638) — A/B independente

Copiei os fontes vivos e os fontes ANTIGOS do run638 para sandboxes proprios:
```
oraculo Python vs VIVOS  : Ran 14 tests - OK              exit0
oraculo Python vs ANTES  : Ran 14 tests - FAILED (10)     exit1
oraculo C#     vs VIVOS  : 12 OK / 0 FAIL                 exit0
oraculo C#     vs ANTES  : 4 OK / 8 FAIL                   exit1
```
Cobre F1 (config vazia / config inteiramente rejeitada), F2 (F7 liga-desliga,
RETOMAR despachado), F3 (indicador parado, sem pipeline != observando), F4 (export
retem o evento que anuncia), F5 (falha de IO nao propaga + sentinela preservada),
F6 plano (janela=None limpa) e os positivos de trava (modo passivo, guards, tetos).

## 4. Provas proprias adicionais (alem do oraculo)

`probe_f4f5_revisor.py` (script meu, `src` proprio):
```
F5 nenhuma excecao propagada         OK
F5 exportar() == None                OK
F5 nenhum evento de sucesso EXPORTAR OK   (trilha nao registra sucesso em falha de IO)
F5 degradacao export_falha_io        OK
F5 sentinela preservada              OK   ('SENTINELA-INTOCADA', nao truncada)
F4 coleta.eventos nao vazio          OK (1)
F4 evento com id/dados/quadro        OK
F4 id retido presente                OK
F4 correlacao sessao_controle/coleta OK
F4 lacunas_honestas presente         OK
F4 export gravado + disco com o id   OK
                                        exit0
```

## 5. Suite, contra-prova, cobertura e runner

```
suite do autor (46 testes)                : Ran 46 tests OK                 exit0
contra-prova por regra                    : iscas 38, falhas 0              exit0
runner roda_testes_kit06.sh (PYTHON=python): VEREDITO VERDE, autoteste 9/9   exit0
```
Medicao de cobertura **propria** (`mede_cobertura_revisor.py`, leitura por AST dos
metodos `test_*` e do dict `MUTACOES` do contra-prova — nao reusa o `mede_iscas.py`
do autor):
```
{testes_na_suite: 46, mutacoes_declaradas: 38, uniao_declarada: 46,
 sem_prova_negativa: [], nomes_fantasma: [], cobertura_completa: true}   exit0
```

## 6. F7 (falso verde do harness) — refeito com defeito REAL plantado por mim

Plantei `ConsomeInput false->true` em uma copia do adapter e compilei os dois
harnesses contra ela:
```
harness NOVO (e864ac9d) + defeito, NORMAL
         -> 45 OK / 1 FALHA, "guard_sem_foco.sem_consumo_input", exit1
harness NOVO (e864ac9d) + defeito, --defeito guard
         -> "FALSO VERDE / conjunto != declarado; falhas EXTRAS: guard_sem_foco.sem_consumo_input", exit1
harness VELHO (600503b3, run633) + defeito, --defeito guard
         -> 39 OK / 5 FALHA, "VERDE do controle negativo", exit0   <== FALSO VERDE
```
Harness vivo sem defeito (execucao direta do projeto real):
```
normal               : 46 OK / 0 FALHA                                   exit0
--defeito guard      : 43 OK / 3 FALHA, "conjunto EXATO de 3"            exit0
--defeito ataque     : 44 OK / 2 FALHA, "conjunto EXATO de 2"            exit0
--defeito inventado  : "defeito NAO suportado"                           exit2
argumento desconhecido: uso                                            exit2
```

## 7. Build isolado, pre-flight de deploy e perfil do dono

```
mkdir -p run652/build; cp Directory.Build.props + lib + tools
dotnet build <copia>/KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false
        -> 0 Erro(s), 65 Aviso(s), exit0; DLL em bin/Release da COPIA
pre-flight (projeto sintetico, so prova a condicao de deploy):
        -p:DeployToBepInEx=true    -> DEPLOY=true,  sentinela=escrita, exit0
        (omitido, padrao)          -> DEPLOY=false, sentinela=ausente, exit0
        -p:DeployToBepInEx=false   -> DEPLOY=false, sentinela=ausente, exit0
perfil do dono (plugins+scripts) antes/depois do MEU build: hash IDENTICO
```
Nada foi instalado, aberto ou publicado por esta revisao.

## 8. Veredito por item

- **F1 OK** (oraculo py: `config_vazia`, `config_totalmente_rejeitada`; nada liga binding por default).
- **F2 OK** (F7 alterna de verdade e pausa o pipeline no 2o toque; RETOMAR despacha com efeito).
- **F3 OK** (indicador "parado" sem coleta; sem pipeline => `sem_pipeline`, nao "observando").
- **F4 OK** (export retem evento com id/dados/quadro, degradacoes, correlacao e lacunas honestas — oraculo + probe proprio).
- **F5 OK** (falha-segura: None, degradacao, nenhum evento de sucesso, sentinela intocada).
- **F6 OK — CORRIGIDO E COMPROVADO, plano E aninhado, Python e C#** (secao 2).
- **F7 OK** (conjunto EXATO de falhas; nome nao suportado/extra/ausente recusam; falso verde do harness antigo demonstrado, secao 6).
- **F8 OK em efeito** (o descritor nao chama a integracao de efetiva nem o pacote de compartilhavel; `export_bruto_local=True`; nenhum exportador reprovado adotado; nenhuma sanitizacao duplicada) — **com ressalva nao bloqueante** na secao 9.

## 9. Ressalvas NAO bloqueantes (roteamento, nao correcao desta rodada)

1. **Texto de status do contrato KIT-07 desatualizado.** `contrato_kit07()`
   (`controle_acesso.py:684-685`) e a doc `KIT-06F-parte05.md:32` dizem
   "KIT-07R REPROVADO, correcao KIT-07F **em andamento**". `KIT-07F` (t_a7318a33)
   foi **concluido e aprovado as 22:14:17** — ou seja, 20 min antes do handoff
   da rodada 650 e antes do proprio parecer da rodada 1. A clausula "em andamento"
   ja nao vale. O nucleo do F8 (nao afirmar integracao/pacote compartilhavel)
   continua honesto e conservador; recomenda-se atualizar o texto (e a assercao do
   teste `test_contrato_kit07_declarado_honesto`) quando do consumo pelo KIT-15.
2. **Deriva de ambiente durante a revisao.** Ao rodar
   `python tools/automacao/runtime/roda_testes_runtime.py` obtive **VERMELHO
   (exit1)** — o unico reprovado foi `t_aut4_controle_isolado.py`, que acusa
   mudanca no perfil REAL do dono. A causa foi externa a esta tarefa: o processo
   **"Stolen Realm" foi aberto pelo dono as 22:41:02** (Game open, `LogOutput.log`
   cresceu de 0 para ~1,2 MB; cfgs reescritos 22:41:09-22:41:11). Nenhum codigo do
   KIT-06 escreve no perfil. A rodada 650 mediu a mesma suite **VERDE 16/16 as
   22:33**, antes da abertura do jogo. Nao tratei o jogo (limite explicito), nao o
   fechei nem interagi com ele.

## 10. Limites declarados

- UI real, overlay, input do engine, runtime/pixels/foco: **NAO_EXERCITADO**
  (KIT-G2). `PonteControleRSTV` nao e chamada por `SRAdapterPlugin.Update`;
  a compilacao nao prova acesso em jogo.
- Nenhum commit/add/push, deploy, instalacao, jogo/save/foco, publicacao,
  `Assembly-CSharp.dll`, Bard ou gameplay por esta revisao.
- Esta aprovacao **nao** e aceite humano nem DoD; ela libera apenas o gate
  `t_73f0779f -> t_10584ca5` (KIT-15).

## 11. Veredito

**APROVADO.** A correcao pedida na rodada 1 (F6 aninhado) esta completa nos dois
caminhos e foi demonstrada **reprovando antes e discriminando depois** com defeito
plantado pelo proprio revisor; os sete itens ja reconferidos OK seguem OK por
execucao propria; nenhuma regressao observada. Ressalvas da secao 9 sao de
roteamento e nao bloqueiam.
