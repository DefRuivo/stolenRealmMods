# API-R1 — parte 03: identidade estrutural e correção de medida

Correção da parte 02: o ZIP tem 146.843 bytes, NÃO 146.883. Medido por `Path('scratch/reference.zip').stat().st_size`, saída de `python inspect_identity.py`.

O parser local `inspect_identity.py` percorreu header e tabela de tipos/objetos do serialized file 22. Achou 19 objetos, PlayerSettings (class ID 129) path ID 1, offset 1264, tamanho 892. Dentro desse objeto há uma única string semver length-prefixed: 1.3.1, offset relativo 640 / absoluto 1904. Unity version no header: 2022.3.62f2. Evidência privada: `scratch/player-settings-evidence.json`.

O leitor é restrito a serialized v22 com type tree ausente e rejeita formatos diferentes; não é um parser geral de Unity. A ordem estrutural foi comparada à implementação pública de SerializedFile do projeto AssetStudio, obtida por curl em `scratch/serialized-file-reference.txt`. Sem type tree, o leitor NÃO comprova o nome semântico do campo: documentaremos a string medida no objeto PlayerSettings, sem chamar a leitura de runtime de Application.version. No runtime autorizado, o plugin verificará Application.version e o SHA-256 do assembly antes de instalar hooks.

Alvo explícito da base: Stolen Realm 1.3.1, Steam AppID 1330000, build instalado 25240684, Unity 2022.3.62f2, hash Assembly-CSharp registrado na parte 02. ACF contém UserConfig/BetaKey=public e MountedConfig/BetaKey=open_beta: não inferir que todo usuário da branch pública tenha o mesmo build; a compatibilidade é restrita ao hash.

A documentação oficial de postfix Harmony foi obtida em `scratch/harmony-postfix-reference.html`. Ainda precisamos exercitar o mecanismo com métodos CLR locais; isso não será confundido com chamada Unity/BepInEx.
