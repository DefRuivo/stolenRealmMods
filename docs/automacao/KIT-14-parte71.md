# KIT-14 — run1498: gates reais, export e dependência corretiva

Pós-processamento real executado exit0 APENAS como conformidade das saídas esperadas:
- Viewer KIT08: exit2,7 NAO_EXERCITADO/aprovação ausente; report.html local gerado com PNG real embutido.
- Gate rstv-full histórico COPIADO BYTE A BYTE: exit1. SHAca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4. Mensagem genérica herdada diz que não viu janela; nesta rodada o PNG a vê, mas físico/tooltip/ciclo não passaram, logo não alterar gate por wording.
- Gate bounded histórico: exit0 (rota/identidade/restauração limitadas).
- Gate recorder passivo sobre saída REAL: exit1 (zero passivo), após eliminar hipótese errada de exigir string positiva que o produto não emite.
- KIT07 export: exit0,4 payloads incluídos/1excluído,3851971 bytes, upload não. HTML ficou excluído pela política (grande/não allowlist), original continua local. Problema registrado em JSON offline pelo coletor, NÃO marcação in-game.
- Probe original SHA inalterado.

Duas suítes novas:6+9 testes verdes. Mutantes: campanha com guarda Cloud anulada exit1/1falha; auditor sempre aceitando recorder exit1/2falhas. Sem skip promovido a verde.

Roteamento do ACHADO (não novo gate humano): criado KIT-14F3 t_26bf5ae7 e revisão independente KIT-14F3R t_59d49835. Perfil registrado default reutilizado em NOVAS instâncias/autorias, não executadas por este coletor; não inventar especialista. Rota gpt-6.1-sol/openai-codex/cap10800 mantém a classe existente. Correção→revisão→retomada KIT14, via link t_59d49835→t_a1f38855 confirmado pela ferramenta. Não usar current→correção, pois geraria ciclo de dependência. Nenhuma revisão duplicada da coleta: KIT14R preexistente continua dependente.

Próximo: readback dos cartões/grafo, export por entrada/SHA/CRC, selo do conjunto congelado e relatório final PARCIAL. Não concluir qualificação ainda falha tecnicamente nem pedir ao dono autorização de teste/limiares já dispensados.
