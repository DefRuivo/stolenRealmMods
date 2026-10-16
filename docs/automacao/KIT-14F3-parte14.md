# KIT-14F3 — entrega da implementação para revisão independente

Cartão t_26bf5ae7, autor desta retomada run1519. Revisão preexistente t_59d49835 deve refutar; este documento não concede aceite independente, humano, UI/UX, release ou KIT14 integral.

## Entrega e escopo

Base: C:/dev/stolen-realm/scratch/kit/KIT-14F3-run1519/final.
Fontes candidatas: sandbox/tools/automacao/runtime/KIT04Adapter.SR/{SRAdapterPlugin.cs,SRScreenManager.cs,SRPassiveRuntime.cs}. Não aplicadas aos fontes principais.
DLL candidata: build/candidate/KIT04Adapter.SR.dll, SHA256 010de6a67671f0a2a03654e54aebb3ca7ae64c11d50270c50c73b568e9dc72c9.
DLL mutante produtor desligado: build/mutant/KIT04Adapter.SR.dll, SHA256 42f035340c1fdf44ca482b29a3baf123a74d68e870813f465435c49940ec4032.
Campanha: campaign.py; recibos em cases/*/boot01/result.json; configurações preservadas em preserved/config. Build: build.json, scanner deploy inseguro1/seguro0, candidato0 e mutante0, DeployToBepInEx=false. Resumos reais: candidato75warnings/0erros; mutante77warnings/0erros. Não foi rodada suíte global de mods.

Patch aplicável para futura integração: instrument-crlf.patch. git apply --check neste patch saiu0; NÃO foi aplicado. Primeiro instrument-only.patch foi gerado normalizando EOL e git apply --check reprovou1 em arquivos CRLF; ele permanece como prova histórica, NÃO deve ser usado. Corrigido apenas o artefato de diff, sem alterar candidato/testes/DLL. Não houve commit/push/deploy/publicação.

## Causa medida e correção

Plugin morre na primeira cena: Update0/OnDestroy1, Unity-null=true/CLR-null=false. Motor independente PlayerLoop.PostLateUpdate sobrevive, com três opt-ins, dedup de frame e instalação única, remoção verificada ao sair. Guardas passivas usam referência CLR para não confundir componente destruído com objeto C# ausente.

Além do lifecycle, nomes genéricos de tela não cobriam o produto. O host atual é a aba RstvAllSkillTreesPanel (frozen-tab.cs:25, assembly congelado); RstvSkillTreesWindow é janela alternativa antiga. Observador lê GameObject.Find/activeInHierarchy/GetInstanceID/Time/Input da engine, não cria bools fictícios como prova nem aciona gameplay. Evento alimenta a ponte/pipeline existente; captura é pedido no evento e confirmação por arquivo/hash em quadro posterior.

## Verificação executada

verification.json foi gerado lendo exatamente8 sessões distintas e conferindo configs/inputs/hashes. Casos: mutant1 esperado; on0; off0; absent-flags0; core-off0; adapter-off0; passive-off0; adapter-absent0. Todos drivers0/restaurações conferidas. OFF não instala motor nem produz passivo/arquivos. Asserções OFF aplicadas ao ON reprovam1; falta de evidência devolve2.

ON tem um evento real janela_aberta, frame452, path GUI Manager/Character Menu Manager Window/RstvAllSkillTreesPanel, instance_id -297694; captura frame454, SHA256 d130380c44f831384676b3315a558054f3fef9c22a0ba2cb3249992094d3b515. PNG1920x1080 realmente visto: All Trees/Fire. callbacks670, duplicados0, frames com painel219, transição1/captura1; motor final0. Probe congelado consumiu o passivo real sem recompilar/sincronizar. Pipeline mantém runtime=NAO_EXERCITADO, não rótulo inventado.

Identidades de probe/Core/RSTV são congeladas em cada inputs/result; assembly candidato e mutante decompilados e conferidos (produtor só no candidato). O detector original detect.py é idêntico ao anterior e continua exit1 por exigir o host alternativo não aberto. measure-panel.py é medição SUPLEMENTAR do host atual, com sessão/frame/caminho/arquivo/contagem; não substitui a trava full-rstv. O mesmo medidor foi mostrado reprovando o mutante antes de passar o candidato.

## Preservação e reprodução

Baseline tracked/untracked antes da retomada e agregação final: zero arquivos preexistentes alterados/removidos. Somente docs novas e sandbox/artefatos desta tarefa. Dados pessoais/perfil: production115/profile53/other-game5 iguais nos hashes IMEDIATOS de cada boot; PlayerPrefs restaurados. Cloud app0 permaneceu0 (não inspeção do servidor), jogos próprios fechados graciosamente, sem junction/backup/perfil descartável/lock ao fim. Nenhuma sessão do dono foi fechada.

Para reavaliar SEM abrir jogo: python <base>/measure-panel.py <base>/cases/on/boot01 <saida-NOVA>.json; mesmo comando sobre mutant deve devolver1. Para OFF usar caso correspondente e argumento final off. Não reutilizar saída existente. Para reproduzir runtime ou build, copiar os scripts para raiz NOVA e usar novo session prefix/case-dir; campaign recusa roots existentes e checa preflight. Dependências históricas identificadas: run1498 -> workspace F2 t_ace7f7f2 -> run1471/1442/916 e scripts KIT16/front-unica; não é pacote autônomo redistribuível.

## Lacunas que continuam técnicas

KIT14 integral e gate físico NÃO fecharam. Probe congelado ainda usa host antigo para snapshots/render no handler; texto_renderizado vazio/snapshots nulos não foram corrigidos neste escopo. Tooltip, Runner, controles físicos e performance ativa não exercitados. Não converter isso em pedido ao dono: coleta posterior retoma após revisão do instrumento. RSTV permanece independente do kit e sem alteração de produto.
