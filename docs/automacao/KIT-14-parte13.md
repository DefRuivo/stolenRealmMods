# KIT-14 — checkpoint 13 / run702

## Estado real medido (terminal exit 0, 13:49:53–54 BRT)
- Jogo FECHADO; STOLEN_PROCESS_COUNT=0.
- persistentDataPath é diretório real, não junction; backup real ausente.
- Área scratch/kit/kit16-iso existe com cópia e baseline antiga; não foi limpada nem alterada nesta retomada.
- BepInEx isolado scratch/kit/runtime-iso/BepInEx ausente.
- Frente única livre, front-unica check exit 0.

## Leitura dirigida
KIT-16 prepara copiando o diretório real (linha 213), exporta registro, renomeia e cria junction. Não há isolamento remoto Cloud nesse trecho. AUT-4 tem driver/config já entregues; não vou escrever cfg ad hoc nem duplicar a instrumentação. Observação readonly e PNG em boot/menu podem ser úteis; navegação/escrita de save requer resolver o risco remoto primeiro.

Uma leitura de AdapterPlugin.cs falhou por caminho inexistente; ferramenta apontou SRAdapterPlugin.cs. Correção do lookup no próximo bloco, sem presumir símbolo.

## Limites
Ainda nenhuma instalação/boot/runtime. Estado restored local e lock livre não provam Cloud seguro para save modificado. A coleta de performance segue exploratória; nada foi medido ou estimado.
