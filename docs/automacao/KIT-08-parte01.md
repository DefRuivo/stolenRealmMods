# KIT-08 — parte01: esqueleto e plano (visualizador HTML local + comparação de sessões)

Cartão `t_e2107a63` · perfil `default` · **offline** (sem jogo, sem save, sem deploy,
sem publicação, sem servidor/rede). Revisão independente no cartão-filho **t_70608c71**.

## Objetivo (do cartão)

Entregar relatório acessível **fora do jogo, sem servidor, conta ou dependência Hermes**.
Por caso/mod mostrar: esperado/observado, prova, imagem, sessão/build/config e lacunas.
Comparar baseline/candidata só com contextos compatíveis; **fonte alterada invalida
aprovação stale**. Escapar texto recebido, **não executar JS dos logs**; arquivos
exportados **não injetam HTML/script**; referências são locais seguras. Aceite
humano/publicação separados do técnico. Reusar decisão/relatório existentes;
demonstrar exemplo real do coletor quando disponível e fixtures rotuladas.

## Dependências lógicas

KIT-02R (OK) e KIT-07R (REPROVADO) — mas o gate de correção KIT-07F (t_a7318a33)
foi **APROVADO** e liberou explicitamente KIT-08. Registrar essa liberação aqui.

## Itens a cobrir (checklist que virará o aceite)

- [ ] A1. Gerador de relatório HTML **local e autocontido** (um arquivo, sem servidor,
      sem CDN, sem fetch de rede, CSS inline, sem dependência Python externa).
- [ ] A2. Por caso/mod: `esperado`, `observado`, `prova`, `imagem`, `sessao/build/config`,
      `lacunas` — vindos do contrato KIT-09 (`kit09.avaliar_cenarios`).
- [ ] A3. Comparação baseline × candidata **só com contextos compatíveis** (mesma
      sessão/build/config/versão de fonte); contexto incompatível → recusa/INDETERMINADO.
- [ ] A4. **Fonte alterada invalida aprovação stale**: hash de fonte/DLL/config divergente
      → marca a aprovação como STALE e não a reapresenta como válida.
- [ ] A5. **Escapar todo texto recebido** (logs/eventos/nomes): nada de HTML/JS executável;
      prova com payload `<script>`/`onerror=`/`javascript:` vira texto inerte.
- [ ] A6. **Sem execução de JS dos logs**: o HTML gerado não contém `<script>` proveniente
      de dados; CSP meta sem `unsafe-inline` para script; nenhuma referência remota.
- [ ] A7. **Referências locais seguras**: imagens/paths resolvidos dentro do pacote local;
      recusa `javascript:`, `data:` de script e path traversal.
- [ ] A8. **Aceite humano/publicação separados do técnico**: seção de veredito técnico
      distinta de aceite humano/DoD, nunca auto-aprovado.
- [ ] A9. **Reuso** de decisão/relatório existentes (KIT-09, KIT-07, CIC-*): não duplicar
      avaliador; consumir a saída real do coletor/avaliador.
- [ ] A10. **Exemplo real do coletor** quando disponível (tools/automacao/runtime/coletor.py
      e fixtures) + **fixtures rotuladas** (sintética/ausente/velha nunca viram PASSOU).
- [ ] A11. Testes offline reais (pytest/unittest) + **contra-prova** (defeito plantado →
      reprova) mostrada como RED; runner com exit distinguível (0/1/2).
- [ ] A12. Evidência identifica sessão, evento/quadro, versão, hash DLL/fonte/config
      quando pertinente, personagem/contexto, esperado independente, observado, caminhos
      e lacunas; PASSOU/FALHOU/NAO_EXERCITADO/INDETERMINADO distintos.

## Restrições observadas nesta frente

- Não instalar, abrir/fechar jogo, carregar save, navegar, publicar.
- Não editar Assembly-CSharp.dll, Bard, gameplay; não enfraquecer travas.
- Inventariar arquivos vivos antes de editar; preservar alterações manuais.
- Um arquivo HTML entregável de verdade, com execução real registrada (exit + caminho).

## Plano de execução (blocos)

1. Ler contratos vivos: `tools/automacao/cenarios/kit09.py` (campos do critério),
   `tools/automacao/runtime/coletor.py` (formato do coletor) e fixtures.
2. Implementar `tools/automacao/kit08/visualizador.py` (gerador HTML + comparação).
3. Suíte `tools/automacao/kit08/teste_visualizador_kit08.py` (offline) + `contra_prova_kit08.py`.
4. Runner `roda_testes_kit08.sh` (suíte + contra-prova, exit 0/1/2).
5. Gerar exemplo REAL a partir de fixture rotulada e registrar sha256 do HTML.
6. Fechar em `docs/automacao/KIT-08-entrega.md` e pedir revisão (`kanban_request_review`).

**Checkpoint parte01:** esqueleto criado; próximo = ler contratos vivos (passo 1).
