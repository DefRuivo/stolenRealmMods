# KIT-15 — parte 04: provas de CLI ponta a ponta e hashes

Sessão: worker run 677 (default) · 2026-10-10 · repo `C:/dev/stolen-realm` · escopo OFFLINE.
Provas em `scratch/kit/KIT-15-run677/` (bancada; nada instalado no perfil do dono, jogo fechado).

## 1. Zip candidato local

```
python tools/automacao/kit15/pacote.py montar --saida scratch/kit/KIT-15-run677/cli/pacote
```
exit **0** · `01-montar.json`:

- `veredito`: **PACOTE_LIMPO**
- `zip`: `scratch/kit/KIT-15-run677/cli/pacote/kit-rstv-0.1.0.zip`
- `zip_sha256`: `126e367b059562ff248d469201ac325142a3d5342ec84458fb75201bdf5708cb`
- `zip_bytes`: 164881 · `zip_membros`: **42** · `zip_testzip`: `null` (íntegro)
- `scan_total`: **0** · `publicacao`: "NAO_EXECUTADA (push/tag/GitHub Release/Thunderstore pertencem a KIT-G4)"

Verificação independente do mesmo arquivo (exit 0):

```
python tools/automacao/kit15/pacote.py verificar <zip>   -> {"veredito": "OK", "tem_manifesto": true, "scan_total": 0}
python tools/automacao/kit15/scan.py <zip>              -> {"veredito": "LIMPO", "total": 0}
```

## 2. Ciclo completo pela CLI (cada passo = processo novo, exit real)

Pré-condição plantada de propósito: `destino/components/core/Json.cs` **já existia** com
conteúdo do "modder" antes de instalar (para provar restauração byte a byte).

| # | comando | exit | efeito observado |
|---|---|---|---|
| 04 | `instalador.py instalar --pacote <staging> --destino <D>` | 0 | `arquivos_escritos` 41 / 41, `versao` 0.1.0, `destino_origem` argumento |
| 05 | `instalador.py status --destino <D>` | 0 | `estado` **INSTALADO**, 41 arquivos, `faltando` [] , `divergentes` [] |
| 06 | `instalador.py atualizar` após alterar **1** fonte no pacote | 0 | `arquivos_escritos` **1** de 41 — só o divergente foi reescrito |
| 07 | `instalador.py rollback --destino <D>` | 0 | `operacao_revertida` instalar, `problemas` [] |
| 08 | `instalador.py remover --destino <D>` | 0 | 41 arquivos tratados, `problemas` [] |
| 09 | `instalador.py instalar --pacote <ZIP> --destino <D2>` | 0 | instalação a partir do **zip** (não só da pasta), 41/41 |
| 10 | `instalador.py status --destino <D2>` | 0 | INSTALADO, 41 arquivos, sem faltando/divergentes |
| 11 | `instalador.py remover --destino <D2>` | 0 | 41 arquivos tratados, `problemas` [] |

Prova do "restaura byte a byte" (lida do disco depois do `remover`, não da mensagem de sucesso):

```
$ cat <D>/components/core/Json.cs
// arquivo do modder que ja existia ANTES do kit
```

Runner único com as três saídas distintas:

```
bash tools/automacao/kit15/roda_testes_kit15.sh                  -> exit 0  (KIT-15 RESULTADO|VERDE|suite=0 contra-prova=0)
PYTHON=python-inexistente bash tools/automacao/kit15/roda_testes_kit15.sh -> exit 2 (ERRO KIT-15: interpretador nao encontrado)
```

Saída verde (runner): `Ran 18 tests in 4.929s` / `OK` e
`CONTRA-PROVA|OK|baseline=True|recusados=7/7|falsos-verdes=[]`.
Logs: `scratch/kit/KIT-15-run677/log-runner.txt`, `log-suite.txt`, `log-contra.txt`,
`cli/01..11-*.json`.

## 3. Travas do repositório e scan dirigido

| gate | comando | exit |
|---|---|---|
| segredos/padrões | `python tools/check_segredos.py` | 0 |
| duplicatas | `python tools/check_dupes.py` | 0 |
| documentação | `python tools/audita_docs.py` | 0 |
| scan dirigido das fontes novas | `python tools/automacao/kit15/scan.py tools/automacao/kit15 --json` | 0 · `{"achados": [], "veredito": "LIMPO"}` |

## 4. Hashes dos entregáveis (sha256sum, saída bruta em `scratch/kit/KIT-15-run677/hashes-kit15.txt`)

```
c2910ac29213bcb2ea27383a6b8a3b7f29b5349bad7c1d2e4c6cb57c8702b12d  tools/automacao/kit15/contra_prova_kit15.py
10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86  tools/automacao/kit15/descoberta.py
81243659708035c77b68de14eecb6018ffbf5858b2445440701283604e1b9596  tools/automacao/kit15/instalador.py
c006c0ff1061ae2117691207cca9e0ad39a7fc5e58e6297e02ec7c8406b964cd  tools/automacao/kit15/pacote.py
a9fe0bfff406356607a54947174247244f4d6d5d14624b7490bfd53244c11dba  tools/automacao/kit15/scan.py
14e0b537f38ff05d735a5d35d8e22911af8a0395c9f4b60ec45543f6db831019  tools/automacao/kit15/teste_kit15.py
37096997a661627e70313056597454cfa721ca0947e3c2b99db9a0e13d5fc0a1  tools/automacao/kit15/manifesto.json
6b0657e84c1a22acf4c98eed6103cfc69ff7b92adae2336b5274e7bad44b8a35  tools/automacao/kit15/roda_testes_kit15.sh
be2888fe10d72416b306c8c979889f607df5f5f09a35e7f4c83b5cc41fff7547  tools/automacao/kit15/CHANGELOG.md
225c5e2ca9583797ebb71439cdaa693acebbea98fc0fc7d6dcfa0882e5aaa884  tools/automacao/kit15/README.en.md
7c408754d1b9f60f4498cbb9145e060c7c6fd0af14dc97edf16b5cdc43f17240  tools/automacao/kit15/README.md
aa437797ae28a216a5932885401d9696415a29020ba9beab4aabf861d5c032f8  tools/automacao/kit15/docs/primeiro-uso.md
```

`git status --short tools/automacao/kit15 docs/automacao/KIT-15-parte0*.md` = apenas `??`
(arquivos NOVOS). Nenhum arquivo vivo foi modificado nesta frente.

## 5. Lacunas declaradas nesta rodada

- **NÃO_EXERCITADO**: carregamento em jogo, BepInEx/Unity runtime, UI/UX, perfil/save do dono,
  deploy, publicação, build C# do pacote (as referências Unity do jogo não são redistribuídas).
- **NÃO_MEDIDO**: Linux/macOS; versões Unity/BepInEx/ModAPI são herdadas de KIT-02/docs/AMBIENTE.md.
- O scan cobre padrões de credencial e binários por nome/extensão; não promete anonimato universal
  nem detecção de segredo ofuscado.
