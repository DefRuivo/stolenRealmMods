# KIT-07R — parte 06: efeito medido e roteamento de conserto

`python scratch/kit/KIT-07R-run636/measure_effects.py`, exit 0; observed-effects.json registra apenas booleanos, bytes e hashes, nunca valores/prefixos fictícios.

## Efeitos lidos no disco — FALHOU
F1 prefix_in_manifest=true / prefix_in_physical_names=true.
F2 secret_suffix_in_output=true / valid_json=false.
F3 origin_changed=true (hash e3904d4f820116fc0dd7045e11c2bdb0687b8d5d79510d3ff555791802df1e45 -> 87c309d1bc2c91a96cca16ac974a78579095acdb02828205e4c61d85f9b05a18).
F4 png_on_disk=true / png_in_manifest=false / current_opt_in=false.
F5 hashes_match: manifest.json=false, relatorio.md=false.
F6 foreign_keep_exists_after=false; deleted_files_count=2; foreign_dir_exists_after=false.
F7 budget24/input24/diagnostic24/package_bytes_actual1045; expansão budget6/input6/output7.
F8 exit1 / stderr_has_prefix=true / traceback=true / FileExistsError=true; stderr bruto NÃO persistido.
F9 selected_log_exists=false, exclusion_reasons=[assembly_proprietario].

Autor runner reexecutado diretamente no terminal com tee: exit0, Ran14 OK, 12 mutações e controle falso-verde recusados. Log author-runner-verified.log. Efeito não depende só das mensagens de sucesso.

## Preservação — PASSOU até este checkpoint
Terminal: TOOLS_CHANGED []; LIVE_IDENTITIES_MATCH True. Nenhum fonte do produto alterado; cópia do escopo tracked/untracked byte a byte. Alterações manuais preexistentes não pertencem à revisão. Contagem de tools inicial variou 613→614 entre setup1 e setup2 por arquivo de outra frente; baseline final cobre614 arquivos e nenhum dos preexistentes mudou até conferência. Não atribuir novo arquivo de outra frente ao reviewer.

## Roteamento — em conferência
Perfil único default confirmado por `hermes profile list`, mesmo perfil do implementador original mas execução de correção OBRIGATORIAMENTE em nova instância, distinta do reviewer636. Busca read-only SQLite confirmou inexistência de KIT-07F anterior. Criado t_a7318a33 KIT-07F (F1–F9), parent=t_96d0c463; a ferramenta devolveu todo/gated_by parent. Implementador deve request_review no MESMO cartão, depois revisor independente confirma antes de done. Não criar revisão duplicada.
Chamadas kanban_link adicionaram t_a7318a33 como gate de KIT-08 t_e2107a63 e KIT-15 t_10584ca5. Readback dos cartões/arestas ainda obrigatório antes de afirmar sucesso. Comentário no pai original t_c364710f registrou rejeição sem apagar histórico (comment496); será conferido.

Pequena melhoria só no teste reviewer F7: teto total insuficiente pode recusar com ErroExportacao se não deixar arquivos parciais; não é exigido caber manifest em24 bytes. Comportamento atual permanece FAIL; reexecutar suite final antes do handoff.

Runtime/pixels/performance NAO_EXERCITADO; nenhuma publicação/instalação/build/deploy/save/jogo. Próximo: fechar parecer final e verificar scanner/identidade/board/provas zip em allowlist sem .git, inputs/pacotes vazados ou assemblies.
