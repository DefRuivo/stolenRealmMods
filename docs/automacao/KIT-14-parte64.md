# KIT-14 — run1471 — auditoria real e números exploratórios

Comando python scratch/kit/KIT-14-run1471/audit.py executado exit0. Escopo verde é APENAS carregamento/config/snapshot/restauração das três rodadas; task_accepted=false. Leitura independente das árvores atuais contra snapshot imediato do último boot:115 dados/53 perfil/5 outro jogo idênticos por bytes+SHA256, zero novos/removidos/alterados.

Avaliador canônico tools/automacao/cenarios/rstv.py executado com zero observações de janela RSTV (não passar textos de Select Party como RSTV):7 capacidades NAO_EXERCITADO. Predicate de cadeia completa permanece negativo; exit real do gate específico ainda será exercitado separadamente.

Janela comum de Select Party ociosa, tentativas3000..3600:
- ON: frame1112->1312, realtime33.111->38.445s,200 frames/5.334s,37.495313 FPS médios no intervalo,26.670ms/frame médios.
- OFF: frame1157->1357, realtime32.039->37.372s,200 frames/5.333s,37.502344 FPS,26.665ms/frame.
São cálculos sobre endpoints reais,21 marcadores por intervalo, não p95 nem amostras completas por frame. Zero eventos passivos; sem causalidade de overhead/aceite de performance.

Picos WorkingSet64 no boot inteiro (inclui loading): ON2136485888 bytes; OFF2138525696. PrivateMemorySize64:ON3299631104/OFF3282313216. Amostras27/22, durações de boot64.547443/52.932820s; não confundir esses picos com janela pareada.

Artefatos probe persistidos:ON3216251 bytes/OFF3209309; isso NÃO é I/O total do disco ou só recorder. Recorder ON1 evento inicializacao/passivo0; OFF0 eventos. Logs das três rodadas: zero assinaturas Error/Fatal e exceções nomeadas procuradas; advertências nativas Convex Mesh e DontDestroyOnLoad1 cada. Padrões exatos em verification.json; não dizer Player.log totalmente limpo.

PNG ON inspecionado: Select Party, personagem descartável Peyton Lv1, party vazia, sem Skills/janela/loading. Novo bloco finalizará contra-provas e relatório/handoff sem aceitar critérios ausentes.
