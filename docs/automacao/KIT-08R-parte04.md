# KIT-08R — parte 04: refutação seletiva e efeito resultante

Execução `python review_controls.py` em scratch/kit/KIT-08R-run648 por subprocess com timeout120: harness exit0 (discriminador), NÃO significa produto aprovado.

Outputs reais:
- 10/10 controles positivos do reviewer mostrados reprovando sob mutação de uma cópia isolada do módulo. Cada processo `python -m unittest -v test_review_kit08.Positive.<alvo>`: `Ran 1 tests`, FAIL EXATAMENTE alvo esperado, exit1, ERROR0, SKIP0. Escape, CSP, fixture, falha técnica, separação humana, stale, referência, contexto igual/diferente, reuso KIT09. Logs em controls/mutant-*.log; módulo vivo intacto.
- 24/24 falhas da suíte própria novamente executadas individualmente no módulo original: Ran1, FAIL1 exato, exit1, ERROR0, SKIP0. Logs controls/negative-*.log.
- Quatro casos adicionais: Ran4, FAILED(failures=4), zero ERROR/skip. SEM aprovação e aprovação {} são VIGENTE; aprovação fixture com hashes iguais é VIGENTE; sessão OLD do caso vs S1 do contexto ainda PASSOU. extra.log.

Efeito JSON real salvo em observed-effects.json:
- fixture_comparison: estado=OK, baseline=PASSOU, candidata=PASSOU, regressoes=[] apesar de ambos docs rotulados fixture.
- lost_runtime: estado=OK, PASSOU -> INDETERMINADO, regressao=false.
- removed: estado=OK, PASSOU -> (ausente), regressao=false.
- encoded_path: `%2e%2e/private.png` accepted=true; urljoin cria file:///sandbox/package/%2e%2e/private.png; unquote produz /sandbox/package/../private.png. Viola confinamento lexical no pacote quando decodificado. Browser real e carregamento do arquivo NÃO exercitados; não alego exfiltração nem execução de JS.
- without_approval_vigente=true.

Limite dos quatro testes de path: aceitação encoded-traversal confirma guarda insuficiente; drive codificado e query/fragment são formas não validadas como filepath, mas seu efeito específico no browser é INDETERMINADO. Não confundir esses dois casos com exploração provada.

Autoria/roteamento: hermes profile list retornou somente default; não inventarei assignee. Correção deve ir a NOVA instância de implementação nesse perfil existente, com review de outra instância; esta revisão não fará correção. Filhos atuais inspecionados: t_0a434c97 KIT-12 e t_10584ca5 KIT-15 precisam também aguardar correção/conferência KIT-08F para não consumir parecer REPROVADO como aprovação.
