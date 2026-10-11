# KIT-07 — Exportar evidências com privacidade e retenção (parte 01)

Data: 2026-10-09
Cartão: t_c364710f (implementação; revisão independente em t_96d0c463)
Dependência lógica: KIT-05R (t_467952ea) — CONCLUÍDA/APROVADA.

## Objetivo
Produzir um pacote compartilhável de ocorrências (JSON + PNG + logs selecionados,
manifest/hash e diagnóstico) sem segredos nem dados pessoais desnecessários.

## Itens a cobrir (checklist de aceite do cartão)
1. Exportador online/offline: monta pacote JSON+PNG+logs selecionados.
2. Manifest com hash (sha256) de cada arquivo incluído + diagnóstico.
3. Exclusão obrigatória de saves e assemblies proprietários.
4. Sanitização de texto/logs por PADRÕES GENÉRICOS (sem lista fixa de valores):
   - redação de chaves/segredos genéricos (api keys, tokens, senhas, PAT, cookies, bearer/JWT).
   - minimização de nomes/caminhos pessoais (user home, e-mail, nome de usuário).
5. Aviso explícito sobre screenshots (podem conter nomes/chat): revisão/exclusão
   manual antes de exportar; NUNCA prometer sanitização automática perfeita.
6. Sem upload por padrão (nenhuma chamada de rede no caminho de exportação).
7. Limites de disco (tamanho máximo do pacote / por arquivo) e exclusão segura
   (delete de arquivos temporários; nunca apagar originais do usuário).
8. Testes com credenciais FICTÍCIAS, provando que nenhum valor nem PREFIXO do
   valor vaza em stdout, stderr, JSON do manifest ou relatório.

## Status
- [ ] Inventário de arquivos vivos (tools/automacao, scratch/kit, docs/automacao/KIT-05*)
- [ ] Desenho do módulo exportador + sanitizador
- [ ] Implementação
- [ ] Testes (RED mostrado antes de GREEN)
- [ ] Controle negativo / defeito plantado
- [ ] Entrega final + hashes

## Notas
Artefato incremental: cada bloco vira KIT-07-parteNN.md; entrega final em KIT-07-entrega.md.
