# KIT-07 — parte 02: inventário de arquivos vivos + desenho

## 1. Inventário (reconhecimento real, `ls`/`grep`)

Infraexistente REUTILIZÁVEL (não duplicar):
- `tools/check_segredos.py` e `tools/check_padroes_segredo.py` — detectores
  GENÉRICOS de credencial (só FORMATOS, nunca valores). Exit 1 se achar.
  **Nunca imprimem prefixo do token.**
- `tools/automacao/offline/aut3_lib.py` — núcleo AUT-3: `sanitiza(texto)`
  (2ª linha de defesa: PEM inteiro, atribuição `password/secret/token/api_key`
  preservando rótulo, prefixos conhecidos → `<REDACTED>`), `sha256_file`,
  `sha256_bytes`, `run_cmd`, `area_trabalho`, veredito `OK/REPROVOU/NAO_EXERCITADO`.
- `tools/automacao/kit05/` — padrão de SUÍTE + CONTRA-PROVA (F7/F9): discriminador
  estrito, controle falso-verde recusado, runner `roda_testes_*.sh` sem `.git`.
- `tools/automacao/runtime/observacao_passiva.py` — pipeline passivo (KIT-05F):
  origem dos "eventos/ocorrências" que o KIT-07 empacota.

Arquivos VIVOS do KIT-07 (a criar):
- `tools/automacao/kit07/exportador.py`
- `tools/automacao/kit07/teste_exportador_kit07.py`
- `tools/automacao/kit07/contra_prova_kit07.py`
- `tools/automacao/kit07/roda_testes_kit07.sh`

## 2. Desenho — `exportador.py`

Responsabilidade: montar um PACOTE compartilhável a partir de um diretório de
ocorrências, sem segredo e sem dado pessoal desnecessário.

Contrato (API pública):
- `PoliticaExportacao` (dataclass): limites e opções —
  `max_total_bytes`, `max_bytes_por_arquivo`, `incluir_png` (default **False** =
  screenshots exigem opt-in após revisão manual), `permitir_upload` (default
  **False**, e o módulo NÃO tem caminho de upload),
  padrões de exclusão.
- `excluivel(caminho)` — verdadeiro para:
  * **saves**: `*.sav`, `*.es3`, dir `saves/`, `*save*.json` de perfil;
  * **assemblies proprietários**: `Assembly-CSharp*.dll`, `*.dll`, `*.pdb`,
    `UnityEngine*`, `BepInEx/`, qualquer binário do jogo (`Mono/`, `Managed/`).
  Exclusão é registrada no diagnóstico (com motivo), nunca silenciosa.
- `sanitizar(texto)` = `aut3_lib.sanitiza(texto)` **+** `minimizar_pessoal(texto)`:
  * caminho de usuário `C:\Users\<nome>` / `/home/<nome>` → `<USUARIO>`;
  * e-mail → `<EMAIL>`; hostname da máquina → `<HOST>`;
  * IP privado → `<IP>`.
  Minimização é por PADRÃO GENÉRICO (regex de forma), sem lista de nomes fixos.
- `montar_pacote(origem, destino, politica)` — copia apenas arquivos permitidos,
  aplicando sanitização a texto (`.json/.log/.txt/.csv/.md`), mantendo PNG como
  cópia BYTE A BYTE (não prometemos sanitizar pixel);
  gera `manifest.json` com `sha256`, `bytes`, `sanitizado` (bool), `motivo_exclusao`
  e um `diagnostico` (contagens: incluídos, excluídos por motivo, truncados,
  avisos). Limites de disco: arquivo acima de `max_bytes_por_arquivo` é EXCLUÍDO
  (não truncado silenciosamente) e total acima de `max_total_bytes` é ERRO.
- `lista_revisao_png(origem)` — lista os PNGs para o humano revisar/excluir ANTES
  de exportar; o relatório carrega o aviso fixo de que screenshot pode conter
  nome/chat e **não** há promessa de sanitização automática de imagem.
- `limpar_temporarios(pacote)` — exclusão segura: apaga SÓ o que o exportador
  criou, identificado por marcador `.kit07-pacote`; recusa apagar qualquer coisa
  fora do pacote e nunca toca na origem.

Garantias anti-vazamento (testadas):
- nenhum `socket`/`urllib`/`requests`/`http` no módulo (sem upload por padrão);
- stdout/stderr/JSON/relatório NÃO contêm valor nem PREFIXO de credencial
  fictícia (teste com token falso montado por concatenação).

## 3. Estratégia de prova
1. Suíte unittest (`teste_exportador_kit07.py`) — RED antes de GREEN; cada teste
   com exit próprio.
2. Contra-prova (`contra_prova_kit07.py`) — defeitos plantados (sanitização
   desligada, exclusão desligada, upload ligado, prefixo vazado) TÊM de reprovar;
   discriminador estrito + controle falso-verde recusado.
3. Runner `.sh` sem `.git` (reusa lição F7 do KIT-05F).

Próximo bloco: implementar `exportador.py`.
