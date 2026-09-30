<#
.SYNOPSIS
    Empacota um mod do repo no formato Thunderstore / r2modman (Windows/PowerShell).

.DESCRIPTION
    Wrapper FINO: nao reimplementa validacao nem empacotamento - delega tudo para o
    tools/pack-thunderstore.py, que e a fonte unica das regras (semver, descricao <= 250,
    README/CHANGELOG, icon.png 256x256 real, DLL buildada em bin/<Config>/ e a checagem
    de versao unica do PKG-2). Duas listas de regras divergem; uma so nao.

    Passos:
      1. dotnet build <Mod>/<Mod>.csproj -c <Config> -p:DeployToBepInEx=false
         O deploy fica DESLIGADO de proposito: gerar pacote nao pode sobrescrever a DLL
         que esta instalada e em teste no perfil do r2modman.
      2. python tools/pack-thunderstore.py --config <Config> <Mods>
      3. confere que dist/gumatos-<Mod>-<versao>.zip existe (versao lida do manifest.json)

    Para saber o que falta (manifest/README/CHANGELOG/icon/DLL/versao) o script NAO
    duplica a checagem: a mensagem do pack-thunderstore.py ja diz o arquivo exato.

.PARAMETER Mods
    Nome(s) do(s) mod(s) - os mesmos nomes das pastas na raiz. Sem nome, empacota TODOS
    (a lista vem de `pack-thunderstore.py --listar-nomes`, nao de uma lista escrita aqui).

.PARAMETER Config
    Release (padrao) ou Debug. Release e a configuracao que vai para o dist/.

.PARAMETER Listar
    So lista os mods descobertos (delega para `--listar`) e sai.

.PARAMETER GerarIcones
    Cria icon.png 256x256 nos mods que estiverem sem (delega para `--gerar-icones`).

.EXAMPLE
    .\scripts\package.ps1 BetterTooltips

.EXAMPLE
    .\scripts\package.ps1

.EXAMPLE
    .\scripts\package.ps1 -Listar

.NOTES
    Nenhum caminho absoluto da maquina de ninguem: a raiz do repo sai de $PSScriptRoot.
    Saida: dist/gumatos-<Mod>-<versao>.zip com manifest.json, README.md, CHANGELOG.md e
    icon.png na RAIZ do zip + plugins/<Mod>/<Mod>.dll.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]] $Mods,

    [ValidateSet('Release', 'Debug')]
    [string] $Config = 'Release',

    [switch] $Listar,

    [switch] $GerarIcones
)

$ErrorActionPreference = 'Stop'

# --- 1. raiz do repo: este arquivo mora em <raiz>/scripts/ -------------------
$Raiz = Split-Path -Parent $PSScriptRoot
$Packer = Join-Path $Raiz 'tools/pack-thunderstore.py'
if (-not (Test-Path $Packer)) {
    Write-Host "!! nao achei tools/pack-thunderstore.py a partir de $Raiz"
    Write-Host "   (o script tem que ficar em <raiz do repo>/scripts/package.ps1)"
    exit 2
}

# --- 2. python: mesma ordem dos outros scripts do repo (PYTHON, python, python3) --
$Python = $env:PYTHON
if (-not $Python) {
    foreach ($cand in @('python', 'python3')) {
        $cmd = Get-Command $cand -ErrorAction SilentlyContinue
        if ($cmd) { $Python = $cmd.Source; break }
    }
}
if (-not $Python) {
    Write-Host "!! python nao encontrado no PATH (defina PYTHON com o caminho do interpretador)"
    exit 2
}

Write-Host "raiz do repo : $Raiz"
Write-Host "python       : $Python"
Write-Host "empacotador  : tools/pack-thunderstore.py (validacao e zip ficam TODOS nele)"
Write-Host "build        : $Config  (deploy no perfil do r2modman DESLIGADO)"

# --- 3. modo -Listar: nada e compilado nem empacotado -----------------------
if ($Listar) {
    Write-Host ""
    & $Python $Packer --listar
    exit $LASTEXITCODE
}

# --- 4. quais mods: a lista sai do PROPRIO empacotador ----------------------
if ($Mods -and $Mods.Count -gt 0) {
    $Alvos = @($Mods)
} else {
    $Alvos = @(& $Python $Packer --listar-nomes | ForEach-Object { $_.Trim() } | Where-Object { $_ })
}
if ($Alvos.Count -eq 0) {
    Write-Host "!! nenhum mod encontrado no repo (esperava pastas <Mod>/<Mod>.csproj com"
    Write-Host "   o target DeployToBepInEx - ver 'python tools/pack-thunderstore.py --listar')"
    exit 1
}

# Nome errado nao vira erro generico: mostra a lista de verdade, vinda do packer.
$Errados = @($Alvos | Where-Object { -not (Test-Path (Join-Path $Raiz "$_/$_.csproj")) })
if ($Errados.Count -gt 0) {
    Write-Host ""
    Write-Host "!! nao e mod do repo: $($Errados -join ', ')"
    Write-Host "   mods que o empacotador conhece:"
    & $Python $Packer --listar
    exit 2
}

# --- 5. build (Release por padrao, SEM tocar no perfil do r2modman) ---------
Write-Host ""
Write-Host "== 1/2 build $Config ($($Alvos.Count) mod(s)) =="
$Falhas = 0
foreach ($m in $Alvos) {
    $csproj = Join-Path $Raiz "$m/$m.csproj"
    Write-Host ("   [build] {0,-32} {1}" -f $m, "-c $Config -p:DeployToBepInEx=false")
    # -p:DeployToBepInEx=false: o alvo DeployToBepInEx existe nos 6 csproj; sem isto o
    # build de Release sobrescreveria a DLL instalada no perfil.
    & dotnet build $csproj -c $Config -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
    if ($LASTEXITCODE -ne 0) {
        Write-Host ("   [FALHA] {0}: build saiu com codigo {1}" -f $m, $LASTEXITCODE)
        $Falhas++
    }
}
if ($Falhas -gt 0) {
    Write-Host ""
    Write-Host "!! build falhou em $Falhas mod(s) - NADA foi empacotado"
    exit 1
}

# --- 6. empacotar: delegado ao pack-thunderstore.py (PKG-3) ----------------
Write-Host ""
Write-Host "== 2/2 empacotando =="
$Argumentos = @($Packer, '--config', $Config)
if ($GerarIcones) { $Argumentos += '--gerar-icones' }
$Argumentos += $Alvos
& $Python @Argumentos
$rc = $LASTEXITCODE
if ($rc -ne 0) {
    Write-Host ""
    Write-Host "!! o pre-flight recusou (exit $rc) - nenhum pacote quebrado foi gerado."
    Write-Host "   Para versao divergente: python tools/pack-thunderstore.py --sincronizar-versao <Mod>"
    exit $rc
}

# --- 7. conferir o pacote gerado (versao lida do manifest.json) ------------
Write-Host ""
Write-Host "== pacotes em dist/ (versao do manifest.json) =="
$Faltando = 0
foreach ($m in $Alvos) {
    $versao = '?'
    $manifesto = Join-Path $Raiz "$m/manifest.json"
    if (Test-Path $manifesto) {
        $versao = (Get-Content -Raw -Encoding UTF8 $manifesto | ConvertFrom-Json).version_number
    }
    $zip = Join-Path $Raiz "dist/gumatos-$m-$versao.zip"
    if (Test-Path $zip) {
        $kb = [math]::Round((Get-Item $zip).Length / 1KB, 1)
        Write-Host ("   ok  {0,-32} v{1}  dist\{2}  ({3} KB)" -f $m, $versao, (Split-Path -Leaf $zip), $kb)
    } else {
        Write-Host ("   !!  {0,-32} v{1}  sumiu: {2}" -f $m, $versao, $zip)
        $Faltando++
    }
}
if ($Faltando -gt 0) {
    Write-Host "!! $Faltando pacote(s) esperados nao estao em dist/ - confira a saida acima"
    exit 1
}

Write-Host ""
Write-Host "Instalar: r2modman -> aba Online -> 'Install from file' -> escolha o zip."
exit 0
