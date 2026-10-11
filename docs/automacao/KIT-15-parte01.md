# KIT-15 — Preparar pacote instalável e guia para outros modders (parte 01: esqueleto)

Data: 2026-10-10 (sessão do worker, run 677)
Cartão: t_10584ca5 — KIT-15, perfil default, workspace `C:/dev/stolen-realm`
Escopo: OFFLINE. Sem jogo, sem instalação, sem deploy, sem publicação, sem git push/tag.

## Objetivo

Preparar distribuição simples **local** do kit:

- pacote **Core + Adapter + Recorder** (obrigatório do kit);
- **Viewer** e **Runner** opcionais;
- documentação para **não programadores** (README PT-BR e EN, primeiro uso, exemplos SDK/cenários, changelog, compatibilidade medida);
- instalador com **instalar/atualizar/remover com rollback**, dependências reais, versões consistentes;
- descoberta/seleção de paths sem usuário fixo, sem exigir SDK/Python para uso básico (empacotar a ferramenta quando necessário);
- **zip/release candidato local** testado em diretórios limpos, sem jogo;
- scan genérico de segredos/conteúdo e ausência de DLL proprietária.

Fora do escopo desta frente (pertencem a KIT-G4): push, tag, GitHub Release, Thunderstore, publicar:true.

## Itens a cobrir (checklist de aceite)

1. Inventário dos fontes vivos dos componentes (Core, Adapter, Recorder, Viewer, Runner) — paths e hashes.
2. Manifesto de pacote: nome, versão, componentes, dependências reais, compatibilidade medida.
3. Instalador offline com `instalar` / `atualizar` / `remover` e **rollback** (backup + restauração verificada).
4. Descoberta/seleção de paths sem usuário fixo (variáveis, argumento CLI, auto-descoberta), sem exigir SDK.
5. Empacotamento da ferramenta quando o uso básico não puder exigir Python/SDK.
6. README PT-BR + README EN, guia de primeiro uso, exemplos SDK/cenário, changelog.
7. Geração de zip/release candidato local.
8. Teste em diretórios limpos (sandbox), sem jogo.
9. Scan de segredos/conteúdo; ausência de DLL proprietária do jogo.
10. Prova de execução real (exit codes, paths, hashes) registrada neste artefato.
11. Bloqueio explícito dos atos de publicação (KIT-G4) — declarado, não executado.

## Regras seguidas

- Build/testes em cópia isolada; `-p:DeployToBepInEx=false` quando houver build C#.
- Nada de instalar no perfil do dono, abrir/fechar jogo, carregar save, publicar.
- Evidência com sessão, caminho, comando, exit code e hash.
- PASSOU / FALHOU / NÃO_EXERCITADO / INDETERMINADO distintos.
- Artefato incremental: este arquivo é a parte 01; blocos seguintes em `KIT-15-parteNN.md`; entrega final em `KIT-15-entrega.md`.

## Estado

- [x] Esqueleto criado (este arquivo)
- [ ] Inventário dos fontes
- [ ] Manifesto de pacote
- [ ] Instalador com rollback
- [ ] Descoberta de paths / empacotamento
- [ ] READMEs + changelog
- [ ] Zip candidato + teste em diretório limpo
- [ ] Scan de segredos / DLL proprietária
- [ ] Entrega final
