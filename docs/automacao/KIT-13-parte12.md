# KIT-13 — checkpoint 12 (run661)

Verificação complementar inicialmente FALHOU/exit1: verify_handoff.py detectou candidato de entropia em KIT-13-parte11.md, linha7. Localização/tamanho foram extraídos sem imprimir valor sensível. Era o rótulo SHA256 colado ao hash do pacote (70 caracteres), não credencial; o próprio texto recém-escrito estava tipograficamente incorreto.

Correção local mínima por patch: separar rótulo de seu valor (`SHA256: `), preservando exatamente os64 caracteres do hash do ZIP. Nenhum detector/lista de isenções/threshold foi alterado. Isso também é prova de que o scanner dirigido dispara quando há candidato, não uma alegação de zero sem exercício.

Índice final legível agora em docs/automacao/KIT-13-entrega-final.md; entrega inicial preservada. Fontes/SDK/pacote fonte continuam com hashes do manifesto e provas verdes. Próximo comando repetirá a verificação complementar real; até então não alegar handoff verde. A etapa que falhou não chegou a criar o ZIP de evidências, então não há sobrescrita de pacote anterior.
