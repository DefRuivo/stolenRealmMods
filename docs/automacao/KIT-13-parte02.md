# KIT-13 — checkpoint 02 (run661)

Contexto lido: docs/SUPERVISAO.md (regras pertinentes), docs/PROCESSO-REVISAO.md; contratos vivos CorePlugin.cs, ICoreEvento.cs, KIT04Core.csproj e executor.py. Nenhuma alteração nesses arquivos.

Decisões de escopo:
- SDK C# netstandard2.1 sem Unity/BepInEx/jogo no núcleo; API v1 para eventos, leitores e validadores registrados explicitamente pelo host. Código de extensão é confiável (não sandbox); pacote declarativo não carrega código nem nomes de módulos.
- Exemplo de mod C# independente, sem ProjectReference ao SDK. Adaptador opcional separado; harness console offline comprova o efeito da lógica, não carregamento BepInEx/em jogo.
- Pacotes JSON estritos separados da autorização do host; allowlist só de esperas observacionais menu/tela/condicao, traduzidas para executor KIT-11. Não haverá shell, clique, loader de extensão ou autorização dentro do pacote.
- Ponte KIT04 separada, por polling explícito/host; não editar Core, não assumir ordem de carga. API não promete suporte universal Unity/IL2CPP.
- Revisão precriada t_596ee4f5 confirmada em todo, depende desta implementação. Fechamento da fase com kanban_complete libera a revisão; não duplicar same-card review.

Lacuna de descoberta: leitura de runtime/IComponentReader.cs retornou File not found; interface real fica em runtime/KIT04Core (já inventariada). Não repetir caminho errado.

Próximo bloco: ler interfaces/harness/preflight existentes, preparar sandbox e testes seletivos; novas entregas apenas em kit13 e documentos KIT-13.
