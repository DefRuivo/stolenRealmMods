# KIT-14 — run1442, checkpoint 54

Identidade atual conferida no terminal: AUT4ProbePlugin.cs principal continua com 109397 bytes, SHA256 beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193, sem EsperarInteractable. Não usar esse gate antigo no novo teste.

Lidos os drivers históricos run712/run714, suporte run704 e driver run911. Reutilizar a infraestrutura KIT16 e a frente única, mas não executar diretamente esses drivers: estão presos a identidades/caminhos antigos e a baseline histórica. O driver run911 já demonstra snapshot imediato, fechamento do PID próprio e rollback somente após jogo fechado; seu contrato será a base, não a antiga comparação que poderia rejeitar deriva legítima dos dados.

Nenhuma edição do produto/principal. R2 será consumido de forma identificada em bancada temporária; ponte e alteração manual não serão sincronizadas cegamente. Próximo bloco ainda é preflight e leitura de comandos exatos para a montagem/restauração. A política 13/10 elimina a necessidade de novo orçamento humano de boots, mas não dispensa testes de segurança, Cloud OFF verificada e manutenção de uma única frente.
