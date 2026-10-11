# KIT-06 — parte 02: módulo do plano de controle + suíte verde

Cartão `t_66ff87b5` · run 633 · 2026-10-09.

## 1. Produzido neste bloco

| Arquivo | O quê |
|---|---|
| `tools/automacao/runtime/controle_acesso.py` | Plano de controle offline: atalhos configuráveis, guards, observar/pausar/marcar/exportar, indicador, trava de modo ativo, contrato KIT-07 |
| `tools/automacao/kit06/teste_controle_acesso.py` | Suíte `unittest` (35 testes) da lógica acima |

## 2. Execução real (autor e offline)

```
$ cd /c/dev/stolen-realm
$ python tools/automacao/kit06/teste_controle_acesso.py
 ...
 Ran 35 tests in 0.030s

 OK
EXIT=0
```

## 3. Decisões de projeto (e por quê)

- **Guards de contexto** (`chat_aberto`/`digitando`/`remapeando`/`foco_no_jogo`):
  um atalho do instrumento **não dispara** com chat aberto, digitação ativa ou
  UI de remapeamento; e **não** com o jogo sem foco — porque **nunca forçamos
  foco** (`foco_forcado` é travado em 0). Cada bloqueio gera degradação
  explícita (`guard_chat`/`guard_remapeamento`/`guard_sem_foco`).
- **Trava dura de modo ativo**: `ACOES_ATIVAS` e `habilitar_modo_ativo()` existem
  só para a recusa ser **explícita e testável**; ligar observação só entra em
  `modo="passivo"`. Pedir modo ativo incrementa `modo_ativo_pedidos` e devolve
  `None` com degradação `modo_ativo_proibido`.
- **Sem encerrar sessão do dono**: `parar_observacao` só para de coletar
  (`encerrou_sessao` travado em `False`).
- **Sem conflito com input**: `consome_input=False` — o plano apenas **lê** o
  estado das teclas; não suprime nem reenvia input.
- **Marcação manual**: exige observação ativa; **permitida em pausa** (o humano
  anota o que viu) e grava `pausado_no_momento`, janela e severidade.
- **Export sem IA**: `exportar()` grava JSON local (pasta padrão
  `scratch/kit/KIT-06/export/`), com `runtime=NAO_EXERCITADO`; nada de Hermes,
  credencial ou rede.
- **KIT-07**: `contrato_kit07()` declara o esquema `KIT-07/export/1`
  (`status_kit07=NAO_IMPLEMENTADO`) — contrato declarado, **sem acoplamento**.

## 4. Integração verificada com o KIT-05F

Testes `TestIntegracaoKit05F` ligam o plano de controle ao
`observacao_passiva.ObservacaoPassiva` **real**: pausar pelo atalho pausa o
pipeline (e o pipeline passa a barrar registro, conforme F2 do KIT-05F) e o
**indicador lê `eventos_total`** do pipeline.

## 5. Próximo bloco

- Ponte C# de atalhos (offline, sem Unity no núcleo) + harness.
- Contra-prova adversarial (defeitos plantados) + runner `roda_testes_kit06.sh`.

## 6. Progresso

- [x] parte01 (inventário + checklist)
- [x] parte02 (módulo + suíte 35/35 verde)
