# KIT-14 — run1524 — checkpoint 79

Causa adicional de lacuna no avaliador lida da saída REAL: única observação RSTV excluída das sete capacidades por owners=[com.gumatos.aut4probe], sem owner do mod sob teste. Motivo literal em verification.json/canonical_rstv: "sem owner do mod sob teste (owners=com.gumatos.aut4probe)". O probe usa OwnersDosFunils() e atribui esse conjunto genérico a cada TMP_Text (AUT4ProbePlugin.cs:699,718,749,1016); o filtro canônico em cenarios/rstv.py:281..283 rejeita. Não remover owner nem reescrever o GUID no payload para forçar aceite; extensão deve provar procedência do alvo atual a partir de estado/métodos vivos reais, com controle sem produto.

Manifest exportado lido: quatro entradas, dois JSON sanitizados e dois PNG não sanitizados automaticamente; HTML excluído por formato_binario_desconhecido. PNGs mostram somente os personagens descartáveis vistos, sem promessa de sanitização automática. JSONs equivalentes semanticamente apesar da reserialização; próxima conferência é hash/tamanho exato contra manifest.

KANBAN.md contém seção run1498 histórica; adicionar seção run1524 sem sobrescrever. Seguimento corretivo deve ficar separado desta coleta e da revisão integral KIT14R, sem repetir correção F3 já aprovada nem criar revisão integral duplicada. Modos, modelos e prioridades existentes não serão alterados.
