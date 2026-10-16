# KIT-14 — run1498: diagnóstico dirigido do recorder

Leitura dos .cfg preservados confirma Core habilitado=true e Adapter habilitado=true/passivoHabilitado=true. Binário Adapter atual na árvore principal tem o MESMO SHA256 d1b383c6… do consumido; não há uma simples DLL atual omitida. Código SRAdapterPlugin.cs:158..186 alimenta passivo apenas em Update() do BaseUnityPlugin; carregamento/vínculo no log é sucesso, mas nenhum efeito passivo no resultado do Core. Isto é pista de lifecycle do instrumento, não prova final de causa nem defeito do viewer. Não vou chamar AlimentarPassivo com estados sintéticos e rotular como observação real.

Fonte do probe possui leitor ResultadoFinal do Core, mas busca não encontrou chamada operacional a AlimentarPassivo; comentário não vale execução. Fonte e binário/ponte ainda serão comparados com entregas existentes para evitar cartão duplicado. Não editar Adapter nesta tarefa de qualificação.

Árvore All Trees efetivamente visível no PNG novo; textos JSON do mesmo ciclo contêm apenas rótulo All Trees com render vazio e snapshots nulos. É lacuna de sincronização/alcance da leitura: o PNG final e o inventário TXT não são simultâneos. Não usar componentes de Event Window/Inventory para aprovar RSTV/placeholders/clipping.

Próximo bloco executa controles recorder-off e sem kit com isolamento idêntico; resultado será comparado sem inventar performance pareada ou atividade passiva. Campanha continua exploratória, decisão B aplicada.
