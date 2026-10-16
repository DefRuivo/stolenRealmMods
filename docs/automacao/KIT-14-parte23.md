# KIT-14 — checkpoint parte23 / run703

## Bloqueio de capacidade efetivamente encontrado

Captura computer_use da janela Steam realizada: screenshot %USERPROFILE%/AppData/Local/hermes/cache/images/computer_use_bfbfd5821b2b44b0a6b17804adaaef48.png. Steam está na biblioteca; outro jogo (Abyssus) aparece rodando. Não interagi com ele.

Tentativa única de selecionar Stolen Realm na biblioteca (computer_use click [79,205]) foi recusada pela ferramenta antes de executar: `BLOCKED: computer_use click requires approval but single-query mode (-q) runs without a user present to approve it.` Não repetir nem contornar essa aprovação via outro canal de mouse/teclado. A decisão A do dono existe: o problema é capacidade da sessão headless, não falta de consentimento sobre Cloud.

Alternativa pesquisada: documentação primária Steam Support e Steamworks descreve toggle por jogo nas propriedades. Não fornece nesta pesquisa um método CLI equivalente para desligar/restaurar a Cloud por app. Referências consultadas: Steam Support FAQ 68d2-35ab-09a9-7678 e Steamworks /doc/features/cloud. Não presumir que editar VDF com Steam ativo altere o estado efetivo; não parar Steam, afetar Abyssus ou mudar approvals/config Hermes por conta própria.

## Preparação confirmada, sem runtime

Lido KIT-G2-parte01 integralmente: B1–B6 autoriza perfil descartável, leitura, navegação, encerramento da instância própria; mantém isolamento e proíbe publicação. Lidas entregas KIT-10-final2 e KIT-05F; adapter SRAdapterPlugin lido confirma recorder opt-in e Update de plugin, ainda sem efeito runtime demonstrado nesta rodada.

Próximo bloco permitido: registrar caminho/mtime e estado dirigido da Cloud sem expor config integral; conferir diretório real contra snapshot KIT-16 e finalizar entrega parcial com instrução operacional específica. Não abrir jogo nem navegar com sincronização não desligada.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
