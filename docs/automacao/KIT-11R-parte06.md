# KIT-11R — parte 06: travas e gate de correção criado

Comando real: python -c subprocess.run para check_segredos.py, check_padroes_segredo.py, check_dupes.py e audita_docs.py, timeout60 por subprocesso.
Resultado: check_segredos exit0 (393 bytes log); check_padroes_segredo exit0 (269 bytes); check_dupes exit0 (96 bytes); audita_docs exit0 (12040 bytes). Logs individuais e guards.json em scratch/kit/KIT-11R-run653. São travas sobre versionados: não aprovam arquivos KIT11 untracked. Leitura das duas travas de segredos confirma git ls-files como escopo; varredura dirigida extra ainda será registrada.
Build/versões/pacote de mod/execução runtime e preflight C# NAO_EXERCITADO: não houve mudança C#, não necessário à revisão Python. Não rodar suite runtime que toca perfil real só para repetir um verde upstream; módulos reusados foram exercitados com efeitos isolados.

## Correção nativa
Criado t_2a38d1d3 — KIT-11F: Corrigir permissões, frente única, encerramento e rollback (F1–F9), assignee default em NOVA instância implementadora, pai t_79c1525f. tool retornou status todo/gated_by=t_79c1525f. Corpo inclui nove grupos, hashes,36 testes próprios,12 mutações, restrições offline e review independente no mesmo cartão. Ainda não executado por este reviewer.
Chamadas kanban_link retornaram ok:true:
- t_2a38d1d3 -> t_0a434c97 KIT-12;
- t_2a38d1d3 -> t_adc1fbfa KIT-13;
- t_2a38d1d3 -> t_a1f38855 KIT-14.
Não inferir efeito só do ok: leitura de volta dessas dependências será registrada antes de afirmar gate verificado.

F1 permissões e coerções; F2 fonte inválida; F3 limites de tempo; F4 frente não atômica/opcional; F5 encerramento sem ownership/autorização e fallback na dúvida; F6 perda do resultado terminal; F7 rollback destrutivo; F8 cleanup excepcional/cancelamento; F9 cobertura/provas e documentação inexata. Concluir esta revisão significa entregar REPROVADO, não aprovação do KIT-11, runtime humano ou DoD.
