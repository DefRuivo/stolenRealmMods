# KIT-14 — checkpoint 20 / run702

## Pós-processamento real e falha do harness preservada
fechar_coleta.py exit 1 por AssertionError ao comparar listas JSON da baseline com tuplas retornadas por tree_snapshot._percorrer. Não indica drift real: reconferência dirigida no terminal, normalizando representação (tupla/lista apenas), mostrou 53/53, 111/111, 5/5 iguais. Preservarei resultado-pos-coleta.json inicial com equal=false e gravarei reconferência em arquivo novo, não maquiar falha.

## Exits efetivos
- Detector sobre objetos reais: CONFIRMADA/exit 0 (critério somente campos básicos lidos).
- 'Controle ausente personagem' também CONFIRMADA/exit 0: hipótese do harness inválida. Campo personagem é contexto lido {tem_personagem_selecionado:false, personagem:null}, não campo totalmente ausente. Não contar esse controle como negativo validado nem como prova de personagem presente.
- Controle adulterado rotulado fixture: exit 2; não confirma runtime.
- Viewer KIT08: exit 2, 21 NAO_EXERCITADO, aprovação ausente; relatorio.html produzido, 37578 bytes, SHA256 41820fd6c5b7f1cad9889336789c8daa8ff74fca9499f9e57d40e6773921a8c6. Report incompleto não vira verde.
- Exportador KIT07: exit 0, pacote sanitizado local, sem upload. Readback do manifest ainda pendente.
- Registro export readonly exit 0; SHA256 atual == snapshot da rodada: 31bb4e1f0530c749817c207d6843b07a2e9e0726c0e703b40d1bc705def0bd7b.

## Preservação adicional
Probe original imutável; BepInEx isolado removido. coletor/rstv/DLL jogo iguais aos hashes congelados. Sem nova abertura/navegação. Próximo bloco: controle negativo correto contra expectativa explícita, integridade de export e relatório final de cobertura/bloqueio específico.
