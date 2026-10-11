# KIT-14 — run704 / checkpoint 27: Cloud comprovada em configuração e capacidade limitada

Comando readonly terminal exit0 encontrou em C:/Program Files (x86)/Steam/userdata/37602317/7/remote/sharedconfig.vdf, bloco específico 1330000, cloudenabled=0. Confirmação independente em configuração do relato do operador: Steam Cloud específica desligada. localconfig mantém histórico synchronized; não interpretar esse histórico como toggle ligado. Nenhuma configuração Steam editada.

Driver AUT4 conferido por inteiro (AUT4ProbePlugin.cs 842–867): procura apenas botão ativo com rótulo contendo Skills, chama onClick.Invoke e registra procura/achou/clique. Não navega menu nem cria personagem. Ausência de Skills deve ficar AUSENTE/NAO_EXERCITADO, não sucesso.

Recorder passivo identificado: CorePlugin + SRAdapterPlugin/PontePassivaRSTV existentes. Opt-ins habilitado e passivoHabilitado default false; Adapter usa Update do plugin, sem driver PlayerLoop no bloco conferido. Isso é risco de ciclo de vida a medir, não conclusão runtime antecipada.

Próximo experimento autorizado: ambiente de dados novo e vazio (não selecionar/copiar personagem pessoal), profile descartável, AUT4 Navegar=true/sem escrita de tooltip; comparar condições identificadas e registrar se driver realmente encontra alvo. Produto não será remendado para verde. Qualquer etapa dependente de clique OS/menu/criação manual entra em runbook residual.

Leitura de AdapterSR.cs por nome presumido retornou ausente; nomes reais são SRAdapterPlugin.cs/PontePassivaRSTV.cs e foram usados. Não repetir a leitura inválida.
