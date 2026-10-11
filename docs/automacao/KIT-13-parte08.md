# KIT-13 — checkpoint 08 (run661)

README de uso completo escrito (sem Hermes/IA/credenciais, API, instalação NÃO autorizada, desfazer, limites por jogo/Mono/IL2CPP). CorePluginBinding novo faz facade REAL dos métodos públicos lidos no Core: RegistrarEvento/ObterEventos/EstaHabilitado; não supõe cast para ICoreEvento, não limpa auditoria. Dependências de compilação da ponte separadas, mod segue independente.

Hardening antes da prova final: timeout inteiro gigantesco poderia estourar math.isfinite; comparar teto ANTES da conversão evita OverflowError, e test_timeouts agora inclui 10**400. Guards de ModuleSpec/loader explícitos, aviso de tipo só no input deliberadamente inválido anotado no teste. Nada em engine/travas compartilhadas alterado.

Próximo bloco: repetir sandbox final com fontes atuais, rodar mutações cs/py/extra; depois scanners dirigidos e pacote de fonte sem DLL proprietária. Mantidos logs anteriores, não sobrescritos.
