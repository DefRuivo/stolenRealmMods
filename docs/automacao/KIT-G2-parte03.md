# KIT-G2 — parte03: limites de performance (origem) e provas de estado do gate

> Complementa `KIT-G2-parte01.md` e `-parte02.md`. Saidas reais abaixo (comando + resultado),
> executadas em 2026-10-10 ~12:26–12:27 BRT, apenas **leitura** — nada instalado, aberto,
> encerrado ou publicado.

## 1. Limites de performance: o que existe e o que e LACUNA

O cartao exige "limites de performance antes da rodada". Procura no repositorio
(`docs/automacao/**`, `tools/automacao/**`) por limite/teto/FPS/desempenho/impacto:

- **Nao existe numero-limite acordado pelo dono** para FPS/tempo de quadro/memoria/disco.
  Toda mencao a "desempenho" nos docs esta como **NAO_EXERCITADO** (ex.: `KIT-05F-entrega.md`,
  `KIT-06R-revisao.md`, `AUT-4R-revisao.md`), nunca como limiar numerico.
- Portanto **nao ha numero a declarar** — declarar um seria "inventar numeros", proibido pela
  regra do proprio cartao ("limites acordados, nao numeros inventados"). Isto e **LACUNA
  DECLARADA**, nao um OK.

### 1.1 Metodo de medicao a registrar ANTES da rodada (sem numero inventado)

1. **Mesmo cenario, dois modos**: medir com o recorder e sem o recorder (baseline), no
   **mesmo** cenario e janela — separa efeito do instrumento do efeito do jogo.
2. **Metricas**: FPS / tempo de quadro (media e p95), memoria residente do processo do jogo,
   bytes escritos em disco pelo instrumento por rodada.
3. **Fonte**: contadores do processo do jogo (Windows) + tempos declarados no JSON do probe;
   registrar o **raw**, nao o resumo.
4. **Limiar**: a definir pelo dono/operador **antes** de julgar; o relatorio reporta observado
   x limiar acordado. Sem limiar acordado, o resultado sai **NAO_EXERCITADO/INDETERMINADO**,
   nunca "OK por omissao".
5. **Proibido**: OCR/coordenada como prova primaria; deduzir performance de fixture.

> Ponto explicito para refutacao/aceite: se o dono ja tem um numero-limite em mente, ele
> entra aqui antes da rodada; caso contrario o resultado de performance sera declarado
> NAO_EXERCITADO no KIT-14.

## 2. Provas de estado (comandos reais e resultado)

```
$ date '+%Y-%m-%d %H:%M:%S %z'
2026-10-10 12:26:30 -0300

$ bash scratch/kit/front-unica.sh check
[2026-10-10 12:27:27] [default] Pode executar: lock disponivel
OK          (exit 0)

$ (processos do jogo)
nenhum processo 'Stolen*' ativo      -> jogo do DONO FECHADO

$ ls scratch/kit/runtime-iso
No such file or directory            -> area isolada residual ausente (rollback anterior exato)

$ sha256sum tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll \
            tools/automacao/runtime/coletor.py \
            tools/automacao/cenarios/rstv.py \
            tools/automacao/cenarios/tooltips_shrines.py \
            lib/Assembly-CSharp.dll
72928ffa... AUT4Probe.dll
159ff2aa... coletor.py
f8d0aad1... rstv.py
65c0f3b2... tooltips_shrines.py
8bb4a7c5... lib/Assembly-CSharp.dll   (DLL do JOGO, intacta)

$ ls %APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins
BetterCombatText BetterFont BetterStats BetterTooltips CapProbe
HybridSR-Roguelike_Scaling RoguelikeClassesMod RoguelikeDebugger
RoguelikeSkillTreeVisualizer ScriptEngine
(sem 'AUT4Probe')                     -> perfil do dono limpo do instrumento
```

Leitura dos resultados (sinal, nao mensagem): o jogo esta fechado; a frente esta livre; a area
isolada anterior nao existe; a DLL do jogo tem o hash declarado; o perfil do dono nao carrega
o probe. **Nada foi escrito no perfil do dono, nenhum build/deploy/instalacao foi executado
nesta rodada de gate.**

## 3. Pre-condicoes do KIT-14 que este gate fixa

- Dependencia logica **KIT-15R fechada** (10/10 03:47) e correcao **KIT-15F aprovada** (run691);
  o pacote kit-rstv 0.1.0 identificado esta disponivel para a rodada.
- Autorizacao do dono registrada (parte01 §1), escopo B1–B6 (parte01 §2).
- Baseline/controle negativo e congelamento pre-registrados (parte02 §4/§5).
- Limites de performance: **LACUNA** — metodo registrado (§1.1), sem numero acordado.
