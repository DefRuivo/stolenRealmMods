# LANG-C4 — revisão do dono: só o que muda

## Resumo executivo

- Mudam: 16 IDs — 15 de tag e 1 de formatação. MANTER: 67.
- Variável: 0 propostas. Sentido: 0 propostas. Não há grupos artificiais nem correções linguísticas acrescentadas a este lote.
- Universo conferido: 83 IDs únicos / 85 alertas; 59 tags_quebradas + 26 tags_divergentes, com sobreposição de 2 IDs. Alertas não são a quantidade de mudanças.
- Maior impacto: LANG-00914 (Sully Walker), que substitui uma aparente tag de nome por gold/incr/b. Depois: LANG-07329 (tamanho da assinatura), oito restaurações rainb e uma shake. LANG-07575 acrescenta uma quebra de parágrafo e exige atenção à altura.
- Ordem de leitura: tags por risco/impacto (Sully primeiro, tamanho, efeitos, demais destaques); em seguida formatação. Dentro de cada patamar, ID crescente. Os riscos são documentais/esperados, não resultados de teste visual.
- Status: propostas CORRIGIR do lote já revisado tecnicamente, ainda sem aprovação humana. Este documento não implementa, não publica e não autoriza aplicação.

## Como ler os textos literais

Os blocos JSON guardam a string completa, sem paráfrase e sem reticências. As aspas externas são delimitadores; \n é quebra de linha, \r é retorno de carro e \" é aspas no conteúdo. Para copiar a string, decodifique o JSON; não cole as aspas/escapes como texto. Isso conserva espaços e controles sem depender da renderização Markdown.
ATUAL significa o snapshot da fonte abaixo, não uma leitura do jogo em execução. A chave inglesa é imutável e serve de endereço, não é proposta de tradução. Todos os alvos deste digest são entradas_ptbr[0].Value; não alterar outras entradas, gênero ou chaves por busca parcial de nome.

## Prova e proveniência

- Fonte original: `C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_2a6474ff/LANG-R1-entrega-final.zip`.
- SHA-256 do ZIP fonte: `4d509f13280cd9e210593cfce08420dd8e48a75b4261f9faefee2e6afb6bf161`.
- Membro literal: `entrega02/localizacao-ptbr.json`; origem declarada no dump: `resources.assets`, path_id 2547158, `Localization/LocalizationDataPortugueseBrazil`. Os assets do jogo não foram abertos nem revalidados neste cartão.
- SHA-256 do JSON fonte: `dbc7d03f2ebe1e9b8bda33a22aaf577475eae0bad84c009b8979184e3a1411a2`.
- Propostas copiadas sem reescrita: `C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_a1ccc2dd/LANG-C4-propostas-dados01.json`; SHA-256 `9da8d6efb771eda024189c940a5de8811b2f1e7255fdde6cfa8f354091655ad4`. Pacote de origem: `LANG-C4-propostas-entrega01.zip` do cartão t_a1ccc2dd.
- Conferência executada: json.loads do membro original; índice por id sem normalização; igualdade Python == de chave, en e ptbr_atual com o registro e com entradas_ptbr[indice_entrada][campo]. Repetida nos blocos ATUAL efetivamente renderizados neste digest. PROPOSTO comparado literalmente com proposta_exata do lote revisado.
- Contagem independente: filtragem por tags_quebradas/tags_divergentes em suspeitos.json, nos alertas dos registros originais e em revisao-formatacao.csv; comparação dos multiconjuntos (ID, código), sem duplicar os dois IDs sobrepostos. Resultado esperado e testado: 83 IDs / 85 alertas.
- Os MANTER aparecem somente como número no resumo. Sua relação, chaves e textos foram omitidos. A regra do dono os considera aprovados por padrão; nenhum campo de aprovação foi escrito por este cartão.
- Proteção de ajustes pessoais: se o texto vigente diferir do ATUAL, não sobrescrever; preservar o vigente e reapresentar o ajuste ao dono. Esta entrega apenas recorta propostas existentes, sem inferir autoria ou auditar alterações posteriores ao snapshot.
- Reproduzir a prova: `python tools/preparar_revisao_dono.py --verify-only` a partir deste workspace. Recibo com hashes, contagens e número de linhas: `docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json`.
- NAO_EXERCITADO: runtime, interpretação das tags, substituição dinâmica de variáveis, layout/legibilidade, jogo, deploy, publicação e aprovação humana. Nenhuma correção aplicada; nenhuma fonte alterada.

## Tag — maior risco primeiro

### LANG-00914

Tipo/risco: tag; ALTO — aparente tag introduzida na tradução.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[913] → entradas_ptbr[0].Value`; `id = LANG-00914`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"A robust figure stands by a fireplace, the orange light dancing in her eyes. With a musket resting in her hands and a bear skin rug beneath her boots, she exudes a commanding presence. The sight of the horrifying trophy hanging above the fireplace sends a shiver down your spine - the severed head of the dreaded Pig Butcher.\r <gold><incr><b>Sully Walker, the master hunter</b></incr></gold>, greets you.\n\r\n\"Quite a sight, isn't it?\" she booms, her eyes not leaving you as she gestures to the monstrous head. \"Nothing puts the fear of the wilderness into a man quite like the face of his nightmares, eh?\"\r\n\r\nYou clear your throat, nodding in agreement. The grotesque visage of the Pig Butcher is indeed a horrifying sight to behold.\n\n\"And what about you, wanderer?\" Sully asks, her voice dropping to a conspiratorial whisper. \"What's the most dangerous game you've ever hunted down?\"\n"
```
ATUAL — literal da fonte:
```json
"Uma figura robusta está ao lado de uma lareira, a luz laranja dançando em seus olhos. Com um mosquete repousando em suas mãos e um tapete de pele de urso sob suas botas, ela exala uma presença imponente. A visão do troféu horrível pendurado acima da lareira envia um arrepio pela sua espinha - a cabeça decepada do temido Açougueiro de Porcos.\n<Sully Walker, a mestra caçadora>, cumprimenta você.\n\n\"Bela visão, não é?\" ela diz em alto e bom som, seus olhos não deixando você enquanto ela gesticula para a cabeça monstruosa. \"Nada coloca o medo do selvagem em um homem como o rosto de seus pesadelos, hein?\"\n\nVocê limpa a garganta, concordando com a cabeça. A visão grotesca do Açougueiro de Porcos é de fato um espetáculo horrível de se ver.\n\n\"E você, viajante?\" Sully pergunta, sua voz baixando para um sussurro conspiratório. \"Qual foi a caça mais perigosa que você já perseguiu?\""
```
PROPOSTO — literal da proposta revisada:
```json
"Uma figura robusta está ao lado de uma lareira, a luz laranja dançando em seus olhos. Com um mosquete repousando em suas mãos e um tapete de pele de urso sob suas botas, ela exala uma presença imponente. A visão do troféu horrível pendurado acima da lareira envia um arrepio pela sua espinha - a cabeça decepada do temido Açougueiro de Porcos.\n<gold><incr><b>Sully Walker, a mestra caçadora</b></incr></gold>, cumprimenta você.\n\n\"Bela visão, não é?\" ela diz em alto e bom som, seus olhos não deixando você enquanto ela gesticula para a cabeça monstruosa. \"Nada coloca o medo do selvagem em um homem como o rosto de seus pesadelos, hein?\"\n\nVocê limpa a garganta, concordando com a cabeça. A visão grotesca do Açougueiro de Porcos é de fato um espetáculo horrível de se ver.\n\n\"E você, viajante?\" Sully pergunta, sua voz baixando para um sussurro conspiratório. \"Qual foi a caça mais perigosa que você já perseguiu?\""
```
Motivo: Trocar o delimitador de nome que parece uma tag por gold/incr/b da origem, sem alterar nenhuma palavra, vírgula ou quebra.
Se não corrigir: Tag: permanece a aparente tag <Sully Walker, a mestra caçadora>, sem gold/incr/b; há risco de interpretação indevida do nome e perda do destaque. Não foi demonstrado sumiço em tela; restaurar incr pode aumentar a ocupação horizontal.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte02.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-07329

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[7328] → entradas_ptbr[0].Value`; `id = LANG-07329`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"Thanks for all your support!\n<size=15>-Stolen Realm Team</size>"
```
ATUAL — literal da fonte:
```json
"Obrigado por todo o seu apoio!\n- Equipe Stolen Realm"
```
PROPOSTO — literal da proposta revisada:
```json
"Obrigado por todo o seu apoio!\n<size=15>- Equipe Stolen Realm</size>"
```
Motivo: Restaurar tamanho 15 somente na assinatura; manter a quebra e o espaço depois do hífen.
Se não corrigir: Layout/estilo: a assinatura continua sem size=15 da origem. Não foi demonstrado estouro; a proposta também pode mudar legibilidade/altura e requer verificação visual posterior.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte01.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00716

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[715] → entradas_ptbr[0].Value`; `id = LANG-00716`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>Heroes beware, I do not play fair!"
```
ATUAL — literal da fonte:
```json
"Heróis, cuidado, eu não jogo limpo!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Heróis, cuidado, eu não jogo limpo!"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00717

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[716] → entradas_ptbr[0].Value`; `id = LANG-00717`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>I twisted the Citizens into dark, devilish, Denizens!"
```
ATUAL — literal da fonte:
```json
"Torci os Cidadãos em habitantes escuros e diabólicos!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Torci os Cidadãos em habitantes escuros e diabólicos!"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00719

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[718] → entradas_ptbr[0].Value`; `id = LANG-00719`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>Let's play a game, try not to get Maimed!</rainb>"
```
ATUAL — literal da fonte:
```json
"Vamos jogar um jogo, tente não ser Mutilado!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Vamos jogar um jogo, tente não ser Mutilado!</rainb>"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00720

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[719] → entradas_ptbr[0].Value`; `id = LANG-00720`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>Oh, you're not even trying, would you please just start dying?"
```
ATUAL — literal da fonte:
```json
"Oh, você nem está tentando, poderia por favor começar a morrer?"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Oh, você nem está tentando, poderia por favor começar a morrer?"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00722

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[721] → entradas_ptbr[0].Value`; `id = LANG-00722`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>This Jester's employment, is to kill for enjoyment!</rainb>"
```
ATUAL — literal da fonte:
```json
"Este Bobo tem por ofício matar por diversão!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Este Bobo tem por ofício matar por diversão!</rainb>"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00723

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[722] → entradas_ptbr[0].Value`; `id = LANG-00723`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>Why waste time brawling wtih the Abyss ever calling?"
```
ATUAL — literal da fonte:
```json
"Por que perder tempo brigando com o Abismo sempre a chamar?"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Por que perder tempo brigando com o Abismo sempre a chamar?"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00725

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[724] → entradas_ptbr[0].Value`; `id = LANG-00725`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>With no more health, I've made a fool of myself!</rainb>"
```
ATUAL — literal da fonte:
```json
"Com a saúde esgotada, fiz papel de bobo!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Com a saúde esgotada, fiz papel de bobo!</rainb>"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00727

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[726] → entradas_ptbr[0].Value`; `id = LANG-00727`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<rainb>You're bloodied and bruised, and I am amused!</rainb>"
```
ATUAL — literal da fonte:
```json
"Você está ensanguentado e machucado, e eu estou divertido!"
```
PROPOSTO — literal da proposta revisada:
```json
"<rainb>Você está ensanguentado e machucado, e eu estou divertido!</rainb>"
```
Motivo: Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.
Se não corrigir: Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00766

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[765] → entradas_ptbr[0].Value`; `id = LANG-00766`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<shake>ELEMENTAL OVERLOAD!</shake>"
```
ATUAL — literal da fonte:
```json
"SOBRECARGA ELEMENTAL!"
```
PROPOSTO — literal da proposta revisada:
```json
"<shake>SOBRECARGA ELEMENTAL!</shake>"
```
Motivo: Restaurar o par shake presente na origem, preservando exatamente as palavras e a caixa alta. A ausência do efeito no render não foi demonstrada.
Se não corrigir: Tag/estilo: permanece ausente shake; a marca do efeito da origem não chega ao texto pt-BR. Efeito em tela não exercitado, sem quebra de frase ou variável documentada.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00404

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[403] → entradas_ptbr[0].Value`; `id = LANG-00404`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<b>Damage</b> dealt and taken increased by <b>50</b>%.\n\n<i><color=#808080>\"You have given into your rage!\"</i></color>"
```
ATUAL — literal da fonte:
```json
"Dano causado e recebido aumentado em <b>50</b>%.\n\n<i><color=#808080>\"Você se entregou à sua fúria!\"</i></color>"
```
PROPOSTO — literal da proposta revisada:
```json
"<b>Dano</b> causado e recebido aumentado em <b>50</b>%.\n\n<i><color=#808080>\"Você se entregou à sua fúria!\"</i></color>"
```
Motivo: Restaurar somente o negrito de Dano; o fechamento cruzado </i></color> herdado fica intacto, fora desta proposta.
Se não corrigir: Tag/estilo: Dano continua sem o negrito da origem; nada prova quebra funcional. O alerta herdado de </i></color> não é corrigido por esta mudança.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00497

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[496] → entradas_ptbr[0].Value`; `id = LANG-00497`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<color=#CBB396>Boss Loot Modifier: </color>+100%"
```
ATUAL — literal da fonte:
```json
"Modificador de Saque do Chefe: +100%"
```
PROPOSTO — literal da proposta revisada:
```json
"<color=#CBB396>Modificador de Saque do Chefe: </color>+100%"
```
Motivo: Restaurar a cor somente do rótulo, deixando +100% fora da tag, como na origem.
Se não corrigir: Tag/estilo: o rótulo continua sem a cor #CBB396 da origem; o valor permanece igual. Não há perda de variável demonstrada nem estouro de layout comprovado.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte01.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00504

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[503] → entradas_ptbr[0].Value`; `id = LANG-00504`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<color=#CBB396>Loot Modifier: </color>+[modifier value]%"
```
ATUAL — literal da fonte:
```json
"Modificador de Saque: +[modifier value]%"
```
PROPOSTO — literal da proposta revisada:
```json
"<color=#CBB396>Modificador de Saque: </color>+[modifier value]%"
```
Motivo: Restaurar a cor do rótulo. Preservar literalmente +[modifier value]% fora da tag.
Se não corrigir: Tag/estilo: o rótulo continua sem a cor #CBB396 da origem; o valor permanece igual. Não há perda de variável demonstrada nem estouro de layout comprovado.
Variáveis: Tokens preservados literalmente: ["[modifier value]"]. Substituição/resolução dinâmica NAO_EXERCITADA.
Rastreio: proposta em `LANG-C4-propostas-parte01.md`; ATUAL conferido por igualdade literal com o caminho acima.

### LANG-00713

Tipo/risco: tag; MÉDIO — paridade de estilo, sem defeito visual comprovado.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[712] → entradas_ptbr[0].Value`; `id = LANG-00713`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"<i><color=#808080>You've made a deal with a devil!</i></color> \n\nIncreases experience, item drops, and gold gained by 50%. "
```
ATUAL — literal da fonte:
```json
"Você fez um pacto com o diabo!\n\nAumenta a experiência, a quantidade de itens e ouro obtidos em 50%."
```
PROPOSTO — literal da proposta revisada:
```json
"<i><color=#808080>Você fez um pacto com o diabo!</color></i>\n\nAumenta a experiência, a quantidade de itens e ouro obtidos em 50%."
```
Motivo: Restaurar itálico e cinza na primeira frase, fechando apenas as tags novas em ordem inversa; preservar a redação e as quebras.
Se não corrigir: Tag/estilo: a primeira frase continua sem itálico/cinza da origem; não há erro de sentido ou quebra de frase demonstrados.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte03.md`; ATUAL conferido por igualdade literal com o caminho acima.

## Formatação — separação de parágrafo

### LANG-07575

Tipo/risco: formatação (quebra de parágrafo); MÉDIO — altura/separação de parágrafo.
Endereço exato: `entrega02/localizacao-ptbr.json → registros[7574] → entradas_ptbr[0].Value`; `id = LANG-07575`. Índices são base zero.
Chave literal (lookup exato; não editar):
```json
"The remaining Blood Masks, witnessing the defeat of their leader, succumb to their cowardly nature. They scatter, fleeing into the shadows of the forest. \n<br/>\nAmongst their stolen plunder, you unearth your Father's leather-bound journal. Worn with age, it contains a lifetimes worth of knowledge, gained from his countless adventures across the realm. Memories flood your mind as you recall your final moments with him. \n\nAs you stand there, thumbing through the journal, a pit of worry gnaws at your stomach. Your father would not have parted with this, his life's work, willingly, nor in sound mind.\n<br/>\nIf what the bandit said was true, then the old Mountain King Ironheart might hold clues to your father's disappearance.\n\nThe journey to Ironheart would be a perilous path through the Forgotten Mines, veering into the remnants of a once-glorious dwarven realm. There, amidst the echoes of a bygone era, the dwarf king reigned over a kingdom fractured, its splendor lost to the corridors of time. \n\nThe thought of this distant land and untold tales, stirs within your heart the beginnings of another adventure."
```
ATUAL — literal da fonte:
```json
"Os restantes Máscaras de Sangue, ao testemunharem a derrota de seu líder, sucumbem à sua natureza covarde. Eles se dispersam, fugindo para as sombras da floresta.\nEntre os seus espólios roubados, você desenterra o diário de couro do seu pai. Desgastado pela idade, ele contém uma vida inteira de conhecimento, adquirido em suas incontáveis aventuras pelo reino. Memórias inundam sua mente ao relembrar seus últimos momentos com ele.\n\nEnquanto você está lá, folheando o diário, um nó de preocupação corrói seu estômago. Seu pai não teria se separado disto, o trabalho de sua vida, voluntariamente, nem em sã consciência.\n\nSe o que o bandido disse era verdade, então o velho Rei da Montanha Ironheart pode ter pistas sobre o desaparecimento do seu pai.\n\nA jornada até Ironheart seria um caminho perigoso através das Minas Esquecidas, desviando para os remanescentes de um reino anão outrora glorioso. Lá, entre os ecos de uma era passada, o rei anão reinava sobre um reino fraturado, seu esplendor perdido nos corredores do tempo.\n\nO pensamento dessa terra distante e contos não contados, desperta em seu coração o início de outra aventura."
```
PROPOSTO — literal da proposta revisada:
```json
"Os restantes Máscaras de Sangue, ao testemunharem a derrota de seu líder, sucumbem à sua natureza covarde. Eles se dispersam, fugindo para as sombras da floresta.\n\nEntre os seus espólios roubados, você desenterra o diário de couro do seu pai. Desgastado pela idade, ele contém uma vida inteira de conhecimento, adquirido em suas incontáveis aventuras pelo reino. Memórias inundam sua mente ao relembrar seus últimos momentos com ele.\n\nEnquanto você está lá, folheando o diário, um nó de preocupação corrói seu estômago. Seu pai não teria se separado disto, o trabalho de sua vida, voluntariamente, nem em sã consciência.\n\nSe o que o bandido disse era verdade, então o velho Rei da Montanha Ironheart pode ter pistas sobre o desaparecimento do seu pai.\n\nA jornada até Ironheart seria um caminho perigoso através das Minas Esquecidas, desviando para os remanescentes de um reino anão outrora glorioso. Lá, entre os ecos de uma era passada, o rei anão reinava sobre um reino fraturado, seu esplendor perdido nos corredores do tempo.\n\nO pensamento dessa terra distante e contos não contados, desperta em seu coração o início de outra aventura."
```
Motivo: Acrescentar uma única quebra antes de Entre os seus espólios roubados, separando o parágrafo sobre o diário.
Se não corrigir: Formatação: o início do diário segue separado apenas por uma quebra, não uma linha em branco. Não há perda de palavras; a proposta acrescenta altura e pode afetar a janela, sem medição visual.
Variáveis: Nenhum token de variável detectado pelo conjunto de padrões documentado; não há resolução runtime exercitada.
Rastreio: proposta em `LANG-C4-propostas-parte08.md`; ATUAL conferido por igualdade literal com o caminho acima.

## DECISAO

Marque uma opção por ID. AJUSTAR exige o texto ou instrução exata na segunda linha; nenhum campo vem marcado. A decisão humana é registrada no cartão LANG-C4 (t_ec66f0bb), não inferida deste digest.

LANG-00914: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-07329: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00716: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00717: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00719: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00720: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00722: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00723: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00725: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00727: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00766: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00404: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00497: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00504: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-00713: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
LANG-07575: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR
Ajuste/observação do dono: ____________________________________________________________
