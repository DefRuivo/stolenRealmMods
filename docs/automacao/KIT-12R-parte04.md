# KIT-12R — parte 04: primeira refutação própria (não concluir ainda)

Suite própria: `PYTHONDONTWRITEBYTECODE=1 python .../test_review_kit12.py`, executada via subprocess com saída preservada em review-suite.txt. Processo dos testes exit 1 (wrapper terminal exit 0 apenas grava evidência). Resultado literal `Ran 17 tests in 8.776s`, `FAILED (failures=6)`; 11 testes passaram, sem erro/skip. Sandbox própria, nenhuma modificação de produto vivo.

## Hipóteses agora reproduzidas

- F1R: config explicitamente requerida inexistente deixa APROVADO_OFFLINE/exit0; identidade contém configs_ausentes e config_sha=null. Reprovação em test_missing_required_config_never_green.
- F2R: dependência de relatório ausente OU exceção de montagem deixa APROVADO_OFFLINE/exit0, relatorio.disponivel=false. Dois testes reprovados. Não confundir com F3/F4 anteriores (que são fail-closed).
- F3R: --probe-dll explicitamente inexistente com alias de coleta coerente deixa APROVADO_OFFLINE/exit0, dll_probe_sha=null, origem=probe-ilegivel. Ausência não é verde; falta lacuna nomeada.
- F4R: envelope observacoes=7 causa TypeError em carregar_coleta, não lacuna técnica estruturada. Teste converte exceção em FAIL, não ERROR; CLI real será reconferida.
- F5R: critério OK com os nove campos executáveis mantém todos em resultado.criterios (montar_fila sanitiza só critérios que geraram item). Outros três estados foram sanitizados no mesmo teste. Não há prova de execução arbitrária; o achado é quebra do contrato de saneamento/transporte de campos.

Controles positivos usam injeção de avaliador OFFLINE em costura verdadeira e evidência arquivo real da sandbox. Nunca se apresentam como prova de runtime. Ainda será gerado JSON dos efeitos e controles negativos por mutação seletiva dos 11 testes verdes, sem usar relatórios antigos como prova.

Documentos de revisões anteriores pesquisados: dívida F3 = normalização de REPROVADO incoerente e F4 = --verificar sem --config causa falso INVALIDADO (fail-closed). Não correspondem a config solicitada ausente, probe explicitamente ilegível ou relatório indisponível aprovados aqui.

C1/C3/C4: ACHADO/FALHOU provisório nas fronteiras acima. C2 e C5 positivos permanecem PASSOU nos casos medidos. Parecer global final e rota de correção pendentes de confirmação dos efeitos, contra-provas, travas e preservação.
