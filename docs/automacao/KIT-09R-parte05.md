# KIT-09R — parte 05: encaminhamento e proteção da cadeia

Correção criada por ferramenta nativa: t_01f65801, KIT-09F: Corrigir falsos OK, adaptador normalizado e cobertura dos cenarios RSTV. Retorno real ok=true/status=todo/gated_by=t_0564b789. Escopo autocontido F1–F7, aceites e provas existentes, artefato-primeiro e revisão independente obrigatória no MESMO cartão via kanban_request_review (sem revisão duplicada). Perfil default único confirmado; correção cabe a nova instância, não ao revisor run637.

Vínculos adicionados por kanban_link, todos retornaram ok=true:
- t_01f65801 -> t_bbad760d (KIT-10)
- t_01f65801 -> t_f2129aea (KIT-11)
- t_01f65801 -> t_adc1fbfa (KIT-13)
- t_01f65801 -> t_a1f38855 (KIT-14)

A flag gated=false no retorno não é a prova da dependência resultante: é necessário conferir os links persistidos antes de encerrar o parecer. Concluir KIT-09R significa parecer entregue REPROVADO, não pacote aprovado; novos gates evitam liberação da entrega reprovada. Nenhuma política/modelo/cron/prioridade foi alterada.

Fronteira test_rstv.py permanece vermelha; ainda não corrigida. Relatório do autor atribui ao filtro de owners; leitura independente do filtro e teste real confirmaram o tipo do bloqueio. Este problema é externo ao kit09.py e não pode ser mascarado removendo o filtro do KIT-R0F.

Limites permanecem: nenhuma build/dll nova, nenhum acesso ao perfil/save/jogo, nenhum aceite humano/publicação. Resultados próprios já guardados e escopo vivo tools preservado em manifesto (456 arquivos, zero alterado/removido na medição anterior).
