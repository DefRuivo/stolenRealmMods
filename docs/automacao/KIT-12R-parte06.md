# KIT-12R — parte 06: efeitos confirmados e contra-provas completas

`PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-12R-run674/record_effects.py`: exit 0 (harness de captura, não aprovação de produto).

Efeitos reais lidos de observed-effects.json e effects/*.json:

- controle seam OFFLINE: APROVADO_OFFLINE/0, report disponível, probe medido, runtime_proof_count=0;
- config solicitada ausente: APROVADO_OFFLINE/0, configs_ausentes não vazio, só review/offline, nenhuma lacuna config;
- relatório ausente/erro IO: APROVADO_OFFLINE/0, report_available=false, nenhuma lacuna relatório;
- probe explicitamente ausente com alias coerente: APROVADO_OFFLINE/0, probe_origin=probe-ilegivel, nenhuma lacuna instrumento;
- critério OK: todos os 9 campos executáveis residuais; REPROVADO/NAO_EXERCITADO/INDETERMINADO: resíduos=[];
- probe medido alterado: INCOMPLETO/2 + lacunas contraditória/incoerente; restaurado: APROVADO_OFFLINE/0;
- CLI REAL sem mock com observacoes=7: exit 1, traceback=true, result_exists=false (effects/malformed-cli.txt);
- avaliador REAL com fixture marcada: INCOMPLETO/2, runtime_proof_count=0.

6 negativos individuais: cada um Ran1, exit1, FAILED(failures=1), sem ERROR/skip (individual-negatives.json). Não são falhas artificiais nem exceções mascaradas como verde.

Controle fixture v2 efetivo: before0 -> mutant1 -> restored0, AssertionError no mutante (fixture-control-v2.json). Mutação promove lacuna a APROVADO_OFFLINE; agora a prova refuta falso verde. A primeira mutação redundante 0->0->0 permanece registrada e não soma como discriminante. Assim os 11 testes próprios verdes têm controle negativo discriminante (10 da primeira rodada + fixture v2).

Travas REAIS do repositório: check_segredos, check_padroes_segredo, check_dupes e audita_docs, todas exit0; logs gate-*.txt e gates.json. Scanners cobrem 874 versionados — untracked ainda serão escaneados com motores vivos em lista explícita. Profiling apenas leitura: `hermes profile list` exit0 mostrou somente profile default; não houve mudança de config/modelos/crons.

Consulta read-only à DB (sem mutação SQL) confirma só cartões KIT-12 e KIT-12R, nenhuma correção KIT-12F existente. Próximo passo: relatório final REPROVADO, preservar bytes, criar correção por nova instância default (único perfil disponível) com reconferência independente e gate adicional KIT-15 antes de concluir parecer. Nenhuma correção será executada pelo revisor674.
