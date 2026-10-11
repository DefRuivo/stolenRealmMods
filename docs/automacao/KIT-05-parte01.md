# KIT-05 — Observação passiva e captura por eventos (parte 01: esqueleto e orientação)

Cartão: t_e9e569f8 (perfil default, run 629)
Data: 2026-10-09
Workspace: C:\dev\stolen-realm

## OBJETIVO DO CARTÃO
Estender a coleta pontual (AUT-4 / CAP-1) para OBSERVAR uma sessão autorizada
enquanto o humano joga, com primeiro conjunto de eventos RSTV.

## ITENS A COBRIR (checklist vivo)
- [ ] 1. Inventariar infraestrutura viva reutilizável (AUT4Probe, coletor.py,
      cenarios/rstv.py, aut5/aut6/aut7, CIC-1..5) antes de editar qualquer coisa.
- [ ] 2. Definir o primeiro conjunto de eventos RSTV a observar em modo passivo
      (clique recebido, janela aberta/fechada, tooltip, falha clique-sem-janela).
- [ ] 3. Implementar observação PASSIVA (sem clicks/saves/equipamentos/escrita).
- [ ] 4. Deduplicação por mudança, fila limitada, retenção e teto de capturas.
- [ ] 5. Pausa segura e degradação explícita.
- [ ] 6. Relacionar id de evento + dados + quadro da captura após atualização
      visual; NÃO afirmar simultaneidade inexistente.
- [ ] 7. Capturar falha clique-sem-janela com motivo/timeout.
- [ ] 8. Testes offline reais (execução registrada com exit code).
- [ ] 9. Sem captura contínua indiscriminada.
- [ ] 10. Fechamento: entrega final com caminhos e hashes.

## RESTRIÇÕES (do cartão, resumo)
- Offline apenas. Sem runtime, sem abrir/fechar jogo, sem save/perfil do dono.
- Build em cópia isolada com `-p:DeployToBepInEx=false`.
- Não editar Assembly-CSharp.dll, Bard, gameplay; não enfraquecer travas.
- Frente única runtime; sem hot-reload presumido.
- Sem git add -A. Evidência real (exit + caminhos), sem inventar resultados.

## PROGRESSO
- [x] Artefato criado (parte01) — orientação inicial.
- Próximo bloco: inventário da infra viva.
