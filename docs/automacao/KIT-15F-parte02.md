# KIT-15F — correção da instalação/rollback/integridade/pacote (parte 02)

Cartão: t_d83f3ef6. Data: 10/10/2026.
Instância implementadora: `default` — run686 (implementação dos 12 grupos) e run687 (retomada da
mesma instância implementadora). Nenhuma das duas é o revisor `default/run678` nem `default/run685`.
Parecer de origem: `docs/automacao/KIT-15R-revisao.md` (REPROVADO).

Esta parte cobre: (a) o fechamento dos últimos achados que ainda dependiam de correção de
documentação — F9 (link/README) e F8/F9 (garantias medidas × não medidas) —; (b) as provas
re-executadas na árvore viva corrigida; (c) o controle negativo próprio de F11.

## 1. O que foi corrigido (mapa achado → mudança)

Fonte viva corrigida: `tools/automacao/kit15/` (mais os componentes de `tools/automacao/runtime`
que são empacotados). Nada de `Assembly-CSharp.dll`, Bard, gameplay, perfil do dono, publicação.

| Achado | Correção (viva) |
|---|---|
| F1 | ZIP regerado do zero a partir das fontes congeladas; conferência **membro a membro** contra a origem viva (`scratch/kit/KIT-15F-run687/verify_f1.py`). |
| F2 | `instalador.py`: `validar_manifesto` / `_validar_arquivos` / `validar_recibo` — schema, tipos, obrigatórios, hash declarado e **fechamento exato**; arquivo extra não declarado recusa a instalação; recibo vazio/`garbage` não vira `INSTALADO`. |
| F3 | Transação registrada **antes** da cópia; falha de I/O em cópia/backup/recibo reverte e não deixa payload sem journal/recibo. |
| F4 | Ação reversa da remoção passa a restaurar o estado anterior completo; lido de volta; CLI exercitado. |
| F5 | Propriedade explícita (`origem`/`criado`/`preexistente`): preexistente idêntico não é apagado; atualização mantém dono dos arquivos presentes; reseleção não deixa órfãos. |
| F6 | `remover` falha fechado com backup original corrompido **ou ausente**; identidade do original persistida e validada antes de restaurar. |
| F7 | `pacote.py verificar` **sem** `--json` (a forma usada nos guias) imprime o relatório e devolve exit correto — fim do `KeyError zip_membros`. |
| F8 | `teste_kit15.py`, `pacote.py montar/verificar` e `roda_testes_kit15.sh` rodam na árvore **extraída**, sem repositório do autor e sem `KIT15_RAIZ`. |
| F9 | Closures reais fechados (Runner→recorder, Viewer, Integração com os 4 módulos, `ProjectReference` do Adapter resolvendo em `components/core`). Link da documentação corrigido (ver §2). |
| F10 | `scan.py`: padrões aceitam a forma JSON (aspas antes do separador) sem imprimir o segredo; `bin/`/`obj/`/`__pycache__`/`.git` **não** são podados na varredura; entrada ilegível vira achado `erro-io` (exit 2), nunca `LIMPO`. |
| F11 | `contra_prova_kit15.py` lê o **resultado estruturado** (`KIT15_RESULT`) escrito pela suíte e exige: `tests >= 1`, zero ERROR, zero skip, conjunto de falhas **exatamente** o alvo do defeito, exit 1. Quem desvia vira `FALSO-VERDE`/`SEM-EFEITO`/`ALVO-DIVERGENTE`/`MUTACAO-INVALIDA`. |
| F12 | Confinamento: `_dentro`/`validar_rel`/`caminho_seguro`/`validar_id` recusam `..`, absoluto, drive e UNC em id de componente, caminhos do manifesto, do recibo, de backup e de transação — **antes** de qualquer efeito. |

`descoberta.py` ficou **byte a byte igual** à fonte viva já conhecida do revisor
(sha256 `10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86`); o defeito de F1 era o
ZIP entregue ter uma cópia velha desse arquivo, não o arquivo vivo.

## 2. Documentação (F9/F10 — o que o parecer pediu por escrito)

- **Link quebrado**: dentro do pacote, `README.md`/`README.en.md` viram `docs/README.md` e
  `docs/README.en.md`, ficando **ao lado** de `docs/primeiro-uso.md`. O link `docs/primeiro-uso.md`
  apontava para `docs/docs/primeiro-uso.md` (inexistente). Passou a apontar para o irmão
  `primeiro-uso.md`, com nota explicando os dois layouts (pacote × repositório do autor).
- **Garantias exageradas**: a seção de garantias do instalador passou a declarar que são garantias
  **medidas** pela suíte offline (18 testes) e pelos oráculos de revisão (27 + 3), com as novas
  garantias que de fato existem (confinamento de caminhos, rollback de I/O, falha fechada do
  `remover`). A frase absoluta "arquivo local que não pertence ao manifesto **nunca** é apagado nem
  sobrescrito" virou a garantia testada "arquivo local que não pertence ao **recibo** é preservado".
- **Scan**: a descrição passou a dizer o que ele realmente cobre (segredo em JSON sem imprimir o
  valor, `.dll`/`.exe`/`.pdb` em **qualquer** caminho inclusive dentro do zip e em `bin/`, entrada
  ilegível = erro de I/O com exit 2), no lugar da promessa anterior que omitia `bin/` e tratava
  ilegível como limpo.
- **"Sem deixar rastro"**: o título do passo de desinstalação deixou de prometer ausência de rastro;
  o guia agora diz o que `remover` faz e que backup corrompido/ausente faz o comando **parar** com
  erro em vez de restaurar lixo.
- **Medido × não medido**: nova seção nos dois READMEs e em `primeiro-uso.md` separando
  explicitamente o que foi medido (Windows 11 + Python 3.14 stdlib, árvore extraída, zip, runner de
  shell sob Git Bash/MSYS) do que **não** foi (Linux/macOS, WSL bash, compilar C#/.NET, runtime no
  jogo, segundo host).
- **Exemplos de SDK**: `primeiro-uso.md` deixou de prometer "exemplo de cenário" (o pacote não traz
  cenário nem `pertinencia.json`) e aponta para o projeto do próprio SDK (`KitSdk.csproj` +
  `RegistryV1.cs`).

## 3. Decisão de escopo registrada para a revisão

O oráculo P1 (imutável) exige que o recibo tenha **exatamente 41 arquivos** e F2 exige fechamento
exato manifesto↔pacote. Portanto **não** é possível acrescentar membros de payload (exemplos,
contrato, schema novo) sem quebrar o oráculo imutável. A correção de F9 foi feita **fechando os
closures reais** e tornando os componentes autossuficientes, sem alterar a composição do pacote.

## 4. Provas desta retomada (todas em `scratch/kit/KIT-15F-run687/`)

| Prova | Comando | Resultado |
|---|---|---|
| Oráculo de revisão (imutável) | `test_review_kit15.py` (cópia byte a byte) | **27/27 OK**, exit 0 |
| Oráculo extra (imutável) | `test_extra_kit15.py` | **3/3 OK**, exit 0 |
| Suíte do autor | `tools/teste_kit15.py` | **18/18 OK**, exit 0 |
| Contra-prova | `contra_prova_kit15.py` | **7/7 recusados**, exit 0 |
| F11 negativo (isca própria) | `f11-bait/` + `f11-bait-out/contra-prova.json` | **FALSO-VERDE ×7, veredito FALHOU**, exit 1 |
| F1 identidade do ZIP | `verify_f1.py` | 42 membros, 41 payload, **0 divergentes**, `membros_identicos_a_origem_viva=true` |

Oráculos preservados com os hashes do revisor:
`test_review_kit15.py` = `1efb6c18…6a449`; `test_extra_kit15.py` = `e68eb481…9d56`.

Pacote candidato: `scratch/kit/KIT-15F-run687/pacote-proprio/kit-rstv-0.1.0.zip`
sha256 `f1f927fd12eb7314ace62d92b2e550db2c22d7e7143068699a8f9a9341a959bc`, 174455 bytes,
42 membros (41 payload + manifesto gerado), `scan_total=0`, `veredito PACOTE_LIMPO`.

## 5. Condição de ambiente honesta (o que o revisor precisa reproduzir)

No Windows, `subprocess.run(["bash", ...])` resolve o executável pela ordem do `CreateProcess`
(diretório do processo → diretório atual → `System32` → `PATH`). Nesta máquina existe
`C:\Windows\System32\bash.exe` (WSL), que tem precedência sobre o `PATH` e **não enxerga** caminhos
`C:\...` — com ele o teste de shell de F8 devolve 127 por motivo de ambiente, não do produto.

Com um bash que entende caminhos do Windows (Git for Windows/MSYS) o mesmo script, no mesmo layout
extraído, devolve 0 (`18 testes OK` + contra-prova 7/7). A prova acima foi rodada com o bash MSYS
resolvível pelo diretório de trabalho do processo (`scratch/kit/KIT-15F-run687/shim/`), que é o mesmo
arranjo já registrado em `scratch/kit/KIT-15F-run686/f8-shell/resultado.json`
(`oracle_form_rc=127` com WSL × `msys_bash_form_rc=0` com MSYS).

## 6. Limites declarados

Não exercitado nesta correção: runtime no jogo, build/deploy C#, segundo host, Linux/macOS,
publicação (KIT-G4). Nenhum push, tag, Release ou Thunderstore. Nenhuma instalação no perfil do dono,
nenhuma abertura/fechamento de jogo, nenhum save.
