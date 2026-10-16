# KIT-14F3 — build candidato + mutante

Preflight deploy executado ANTES de compilar: fixture XML insegura detectada (exit lógico1); scanner canônico sobre a sandbox exit0. A fixture tem extensão .xml.fixture e nunca é executada pelo MSBuild. Logs e recibo em scratch/kit/KIT-14F3-run1502/build.json.

Dois builds REAIS exit0, ambos com -p:DeployToBepInEx=false e referências selecionadas explicitamente:
- candidato Adapter: 17a2e29c0e99dc6684971c00dfb9e4ddad51e6f9ca74197833ad35e27ec351ed;
- mutante produtor desligado: cecf56e2aa0cccf9ca70cf951a83f0965f96e7f005d7b9913a58108d5c522683.

Novo SRPassiveRuntime.cs observa GameObject.Find/activeInHierarchy/Input/Time da engine no PostLateUpdate; não emite clique. Só instala com três opt-ins, guarda unicidade de marcador, dedup frame e remove delegate ao encerrar. Captura PNG solicitada apenas em janela_aberta e limitada pelo pipeline Core; confirma apenas em frame posterior + arquivo real + hash. JSONs separados preservam o recorder congelado do probe (não há sincronização do probe principal).

Campanha nova campaign.py reutiliza a cadeia de isolamento run1498/F2/1471/1442/916, sem substituir salvaguardas. Inputs congelados, somente Adapter diferente; sessão/saída novas para cada caso. Cauda de observação idêntica de 3s após conclusão do probe nos controles positivo/negativo. Nenhum boot do novo candidato foi promovido a aceite nesta fase.
