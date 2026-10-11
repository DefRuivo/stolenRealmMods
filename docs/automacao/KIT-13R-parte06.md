# KIT-13R — audit final real exit1 por deriva EXTERNA, não ocultada

Comando: python scratch/kit/KIT-13R-run664/audit_final.py → exit1.

Resultados reais antes do exit1:
- Source manifest autor27/27 SHA iguais, sandbox207/207 iguais, DLLs iniciais20/20 iguais, Assembly-CSharp intacta, sem .git na sandbox.
- ZIP fonte44 entradas/102589B SHA256 8b85276e39b196279f8cae8c2120b40a656c965da821b806605db37c43e5efcf e evidência252/242635B SHA256 058696f2b7978dd63b37c045506b473f4fea223e77c97ff24b481fb557085a74: CRC OK, bytes de cada membro iguais aos respectivos arquivos, zero DLL/MZ/.git/perfil/credencial.
- Fonte ZIP EXTRAÍDA em cópia nova, sem lib/ do dono: preflighttrue1/false0,2 builds Standalone/Harness exit0, Standalone/Harness runtime offline exit0 e CLI menu/skills exit0 com JSON runtime_exercitado=false. Distribuição básica executável sem instalar/deploy/game refs para os componentes puros. Plugins/ponte continuam exigindo referências locais NÃO distribuídas, limite declarado.
- Travas check_segredos/check_dupes/audita_docs exit0 com logs reais em audit-logs.
- Motores reais scanners em727 textos (fontes/docs/logs/manifestos e membros não binários dos ZIPs): zero hits padrão/genérico. Controle sintético em MEMÓRIA detectado por ambos, sem gravar/imprimir valor.
- Mutations results.json lidos: autor14py+17cs+2extra e reviewer14py+13cs; todos0->1->0 e SHA restaurado, bad=[].

CAUSA do exit1: baseline vivo divergiu apenas em tools/automacao/kit10/kit10_cenarios.py. É outro cartão/frente; não foi editado por esta revisão nem compõe KIT13, que usa KIT11/controle_acesso/coletor/Core. Não alegar que os207 vivos permaneceram iguais. Copy_changed=[] e27 fontesKIT13 iguais demonstram sandbox preservada e escopo revisado idêntico. Confirmar hashes de compartilhados e ausência de importKIT10 no próximo bloco antes de classificar como deriva externa não bloqueante.

O script exit1 e seu JSON foram preservados, não alterados para apagar obstáculo. Nova abordagem final: readback dirigido de identidade do escopo/dependências, mantendo a deriva externa explícita. Não precisa repetir extração nem build, já exercitados e logs existentes. Nenhum produto/jogo/perfil alterado pelo reviewer.
