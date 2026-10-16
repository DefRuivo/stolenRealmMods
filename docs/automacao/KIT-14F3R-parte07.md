# KIT-14F3R — parte 07: confronto de assembly e fonte da falha

Decompilação do runtime candidato com referências é byte a byte idêntica à decompilação do build novo do revisor (assert passou). O build tem SHA diferente por caminho/metadata, mas corpo emitido corresponde ao entregue. Plugin decompilado resolve a guarda CLR como (object)corePlugin==null, enquanto diagnóstico usa null Unity separadamente. Não trocar a prova por uma leitura equivocada da decompilação sem referências.

Log real ON: instalação1 (:21), OnDestroy frame0/Update0 (:44), host All Trees criado (:67), aba selecionada (:73), remoção motores0/callbacks670 (:77). Causa funcional delimitada: o produtor em Update do plugin destruído não executa; o novo observador executa apesar disso. Não afirmamos a origem interna do Destroy da engine, não exigida para a correção.

Consultadas as quatro partes originais KIT-14-parte67–70; preservam falha ON0, config true, render atrasado e runtime constante, coerentes com a entrega nova. RSTV não foi modificado.

Tentativa adicional de confrontar PlayerPrefs atual: reg export executou e arquivo temporário foi removido após hash, mas o wrapper de regex de recibo falhou (exit1) antes de comparar. Isso NÃO é verde nem divergência no registro; repetir apenas leitura/hash com parser correto. Nenhuma importação/escrita no registro foi feita.
