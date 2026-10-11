# KIT-G1 — Gate de autorização humana para a rodada mínima AUT-4 (parte 01)

> Cartão: `t_49c93c37` · perfil default · run 618 · workspace `C:\dev\stolen-realm` (dir)
> Início: 2026-10-09 18:20 (Hora oficial do Brasil, UTC-03:00). Modelo: deepseek-flash.
> Regra desta frente: **registrar a autorização**; **não** executar a rodada runtime,
> **não** instalar, **não** abrir/encerrar jogo, **não** publicar.

## 1. Objetivo do cartão

Gate **HUMANO** que autoriza a rodada mínima do instrumento AUT-4 em **ambiente isolado**:
instalar o probe **identificado**, iniciar/encerrar a **instância de teste** e **coletar UI**.
Save e navegação **só** se explicitamente incluídos. Marcar **somente esta autorização** —
não aceite nem publicação do DoD.

## 2. Itens a cobrir (checklist do gate)

- [ ] I1. Registro da autorização do dono com data/autoria (fonte: comentário do cartão).
- [ ] I2. Escopo exato autorizado (o que ESTÁ dentro) e o que NÃO está.
- [ ] I3. Perfil declarado da rodada (isolado, fora do perfil do dono).
- [ ] I4. Build declarada (identidade por hash DECLARADO; DLL do probe + fonte + driver).
- [ ] I5. Ações autorizadas (instalar probe identificado; iniciar/encerrar instância de teste; coletar UI).
- [ ] I6. Janela da rodada (quando / por quanto tempo / teto de orçamento).
- [ ] I7. Isolamento e rollback **revisados primeiro** (KIT-03F e KIT-04F aprovados).
- [ ] I8. Frente única e ausência de hot-reload; declaração de reinício se o jogo do dono estiver aberto.
- [ ] I9. Proibições preservadas (publicação, save/navegação sem autorização, Assembly-CSharp, Bard).
- [ ] I10. Dependências lógicas (KIT-03R, KIT-04R) satisfeitas e verificadas contra o board.
- [ ] I11. Fechamento: artefato de entrega + hashes + destravamento do filho AUT-4.

## 3. Base normativa consultada (leitura fria)

- `docs/SUPERVISAO.md` — regras do projeto e DoD (a conferir/registrar).
- `docs/PROCESSO-REVISAO.md` — modelo de revisão independente (a conferir/registrar).
- `docs/automacao/AUT-4-runbook-rodada-autorizada.md` — gates G1–G8, identidade da build,
  cenários C0–C7, critérios de aceite AC1–AC10, lacunas.
- `docs/automacao/AUT-4-preparacao.md` — o que foi construído offline e o que segue NÃO EXERCITADO.
- Handoffs dos pais: `t_0451c587` (KIT-04R), `t_160668bd` (KIT-03F), `t_9670452a` (KIT-03R),
  `t_d5c98d36` (KIT-04F).

## 4. Fatos já verificados

- **Dependências lógicas satisfeitas no board**: os quatro pais do cartão
  (`t_0451c587`, `t_160668bd`, `t_9670452a`, `t_d5c98d36`) estão `completed` e
  `unsatisfied_parents` vazio.
- **KIT-03R → corrigido por KIT-03F (`t_160668bd`)**: veredito APROVADO; isolamento com
  controle negativo (skip não vira verde; `prove-isolation` legítimo exit 0 e negativo exit 1;
  frente única recusa 2º acquire; rollback exato; build `-p:DeployToBepInEx=false` em cópia isolada).
- **KIT-04R → corrigido por KIT-04F (`t_d5c98d36`)**: veredito APROVADO; Core e Adapter compilam
  em cópia isolada (exit 0), 45/45 hashes conferidos, controle negativo 6/6, perfil do dono sem
  KIT04, `Assembly-CSharp.dll` intacta.
- **Autorização do dono registrada no thread do cartão** (09/10/2026, mensagem "autorizo"),
  com escopo fechado ao próprio cartão.

## 5. Pré-condição do AUT-4 (do runbook, §2)

| artefato | sha256 declarado |
|---|---|
| fonte do probe `AUT4Probe/AUT4ProbePlugin.cs` | `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94` |
| DLL do probe `AUT4Probe/bin/Release/AUT4Probe.dll` | `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7` |
| driver `coletor.py` | `adb48dca024120db91b65e28b8842b7f303ca1725359cdaf4deab5530ae1dd46` |
| `lib/Assembly-CSharp.dll` (DLL do JOGO — intocada) | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |

## 6. Próximos passos desta execução

- Conferir os hashes acima **contra o disco** (prova de identidade dos arquivos vivos).
- Localizar e declarar a **raiz isolada** usada (ambiente isolado do KIT) e o procedimento de
  rollback revisado.
- Verificar se o **jogo do dono está aberto** (declarar reinício em vez de interferir).
- Registrar a **janela** da rodada e fechar o artefato de entrega.
