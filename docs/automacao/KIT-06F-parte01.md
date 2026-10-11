# KIT-06F — parte 01: abertura da correcao (nova instancia)

Cartao t_73f0779f, run 641, perfil default. Implementer != reviewer KIT-06R run638.
Origem t_66ff87b5 run633; revisao t_f9f88c18 run638. Data local: 2026-10-09 ~22h UTC-03.
Branch ci-validate-test. Entorno: TEMP/TMP/TMPDIR apontados EXPLICITAMENTE para
scratch/kit/KIT-06F-run641/tmp (o reviewer achou o Temp do sistema; aqui nao se repete).

Objetivo: corrigir a RAIZ dos oito achados F1-F8 do KIT-06R nos DOIS caminhos
(Python controle_acesso.py / C# PonteControleRSTV.cs + harness), sem afrouxar
testes, com prova negativa completa e nova instancia de revisao.

Fontes revisados (revalidados vivos por SHA256 ANTES de editar):
- tools/automacao/runtime/controle_acesso.py 2e21f539...787e2f
- tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs 6bfe3db1...db6bbbf

Orceamento de testes: oraculos do reviewer reproduzidos ANTES da correcao contra
os fontes vivos (Python 14 testes = 10 FAIL/4 OK exit1; C# 12 = 8 FAIL/4 OK exit1),
confirmando os achados de forma independente antes de tocar o produto.
