# KIT14G-SEG2-INV — parte02: medição própria do congelamento e gates restantes

Complementa parte01; investigação default/run844, 11/10/2026. Evidência reproduzível: `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_ceda98dd/audit_seg2.py` e `audit-result.json` no mesmo diretório. Execução `python audit_seg2.py`: exit 0, sem boot/build/montagem. O script gera drivers em memória e compila seu Python, **não executa** o driver.

## 1. A afirmação de desaparecimento absoluto é FALSA

Varredura leu nomes de 61.205 arquivos em três raízes: `C:/dev/stolen-realm`, `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces` e `C:/Users/Pichau/AppData/Local/hermes/cache/scratch`. Encontrou **52 cópias de AUT4ProbePlugin.cs, com 7 hashes distintos**, e **53 AUT4Probe.dll, com 14 hashes distintos**; 0 erros de leitura. Excluiu diretórios `.git`, junctions/symlinks; não descompactou arquivos nem pesquisou todos os discos. Não se alegará ausência universal.

O par original foi encontrado junto em:

`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/int_r1_c4_fora/tools/automacao/runtime/AUT4Probe/`

- `AUT4ProbePlugin.cs`: **ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2**, 104.974 bytes.
- `bin/Release/AUT4Probe.dll`: **95069e9cbc5e1e7784f80b34589e54cf19651969cddad86b6a35d9b94c89a865**, 75.776 bytes.
- `obj/Release/AUT4Probe.dll`: mesmo hash original (segunda cópia).

Portanto, “não existe em lugar nenhum” não é conclusão sustentável. Ausência no repo vivo/sandbox é diferente de perda de todas as cópias. `KIT-14-entrega-run721.md:19-20` também registrou este par às 02:24 de 11/10. A cópia em cache é recuperável nesta leitura, mas volátil; **não foi restaurada nem selecionada** pelo investigador.

## 2. O congelamento NOVO está íntegro na bancada

`audit-result.json.preflight`: execução do `scratch/kit/KIT-14G-run712/preflight.py`, exit 0. DLL sandbox bate com 7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee; os cinco arquivos de entrada batem repo × sandbox:

| Entrada | SHA256 |
|---|---|
| AUT4ProbePlugin.cs | beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193 |
| LeituraAgregados.cs | f398543671aeb18091bcf89cb126d0d2ac6c71f5cd52ab1080429bc9a37ec641 |
| IdentidadeDoProbe.cs | c23574f324f7a70ddeb2edb484daf292ebd92fc07eb0304bfbf343e58d27bfa6 |
| Json.cs | ae30a1ac059bcf62067047926c13bf43079b30552073540a2f5654551b6b32c6 |
| AUT4Probe.csproj | 418a559beb424066633bc4aed604cd5c9cef9825c9ef5d4950b84f6f26ba0ff6 |

Fonte atual: 109.397 bytes, 2.012 LF, 0 CRLF. Fonte original: 104.974 bytes, 1.957 LF, 0 CRLF. Não é mera conversão de finais de linha. Ambas têm os três marcadores de SEG2; presença textual não prova equivalência comportamental.

O preparo t_c36c7082 concluiu às **14:48:56** (evento 10407), antes desta investigação. `roda.py:35` já aponta ao novo hash; não é necessário repetir/rebuildar esse preparo cegamente. A frase da receita-congelada:38 sobre o antigo PROBE_SHA “atual” está desatualizada.

## 3. PASSAR pré-flight de hashes não torna os três boots executáveis como estão

`audit-result.json.driver_generation`: `roda714.build('INV-offline-only','sem-passivo','Play;Roguelike;Accept',150,90)` gerou/compilou em memória, mas contém **0 ocorrências** de cada chave `CliqueFisico`, `CliqueFisicoEstavel`, `SilencioAposClique`. Sem a costura de configuração prevista em parte01:107-115, os três labels rodariam o mesmo default: gate OFF/silêncio OFF. O teste não foi executado em jogo.

Outro bloqueio independente: `suporte.production_diff()` ainda compara com `KIT-16-run700/run-real-3/antes.manifest`. Medição própria: **111 antes / 106 agora**, 4 novos, 9 removidos, 8 alterados; equal=false. O driver exige esse gate antes do boot. Não é autorização para reverter o save do dono nem prova de dano da bancada: falta baseline imediato por rodada, sem enfraquecer a proteção. A atribuição histórica a jogo do dono vem dos cartões anteriores; autoria exata de cada diferença não foi estabelecida aqui.

## 4. Save real e cópia: prova positiva nesta coleta

`snapshot-antes.json` **não é JSON**; é manifesto TSV de `tree_snapshot.py`, SHA256 c51394a2ec2647207aa34b8e0ea98a3defade7661ae6d5ffa652e888a61cdca3, 106 arquivos.

`audit-result.json.real_vs_snapshot` e `iso_vs_snapshot`: ambos **106/106, 0 novos/0 removidos/0 alterados, equal=true**, com tamanho e SHA256 por arquivo. Caminho real existente, `is_junction=false`, `is_symlink=false`, `st_reparse_tag=0`; `origem-real` inexistente. Cópia pronta não significa sessão montada: **o real continua no caminho real**.

Leitura de processos: 0 processos Stolen*, 4 r2modman, 9 steam* no instante da coleta; nada foi encerrado. Leitura de configuração app 1330000: `cloudenabled=["0"]` às 14:57:49; isso é configuração local OFF, não inspeção do servidor Cloud. Não houve modificação da Cloud.

## 5. A/B precisa da versão corrigida da evidência

`KIT-14G-parte08.md` é histórico: diz “10 execuções” mas lista 13, e sua conclusão categórica foi rebaixada em `KIT-14G-parte10.md:90-109`. `audit-result.json.run716_ab.total_execucoes=13` e classificação corrigida: **gatilho Accept medido; mecânica NÃO isolada**. O agregado filtrado de Event Log tem n=2 para A/B, vazio para C/D/E; não usar o export cumulativo como se fosse janela.

Os controles C/D/E não iniciaram manualmente uma run; sobreviver no menu não elimina falha do arranque em ambiente isolado. `CliqueFisico=true` continua usando `onClick.Invoke()` (`AUT4ProbePlugin.cs:1198`), não reproduz input/raycast/oclusão completos. Último marco limita a última operação registrada; não identifica sozinho a instrução nativa que falhou. Esses limites devem acompanhar o veredito final.

NAO_EXERCITADO: qualquer boot novo, rebuild, restauração da cópia histórica, clique físico e reprodução do erro de rename — proibidos pelo escopo.
