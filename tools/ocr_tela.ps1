# OCR de tela via Windows.Media.Ocr (sem chave de API, local).
# Uso:  powershell -NoProfile -ExecutionPolicy Bypass -File tools/ocr_tela.ps1 <imagem.png> [idioma]
# Saida: uma linha por linha de texto do jogo: "BBOX x y x2 y2 <texto>"
#        (x,y = canto sup.esq; x2,y2 = canto inf.dir) — util para mapear onde esta cada texto.
param(
    [Parameter(Mandatory=$true)][string]$ImgPath,
    [string]$Lang = "en-US"
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Runtime.WindowsRuntime | Out-Null
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
[Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime] | Out-Null

function Await2($op, $rt) {
    $m = $asTaskGeneric.MakeGenericMethod($rt)
    $nt = $m.Invoke($null, @($op))
    $nt.Wait(-1) | Out-Null
    return $nt.Result
}

# caminho nativo Windows (troca '/' por '\' para o StorageFile aceitar)
$path = $ImgPath.Replace('/', '\')
$file = Await2 ([Windows.Storage.StorageFile]::GetFileFromPathAsync($path)) ([Windows.Storage.StorageFile])
$stream = Await2 ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await2 ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bitmap = Await2 ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
Write-Output ("IMG {0}x{1}" -f $bitmap.PixelWidth, $bitmap.PixelHeight)

$eng = $null
try { $eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage((New-Object Windows.Globalization.Language $Lang)) }
catch { Write-Output ("lang err: " + $_.Exception.Message) }
if (-not $eng) { $eng = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
if (-not $eng) { Write-Output "NO_ENGINE"; exit 1 }
Write-Output ("LANG " + $eng.RecognizerLanguage.LanguageTag)

$res = Await2 ($eng.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
Write-Output ("LINES " + $res.Lines.Count)
foreach ($line in $res.Lines) {
    $x = 999999; $y = 999999; $x2 = 0; $y2 = 0
    foreach ($w in $line.Words) {
        $r = $w.BoundingRect
        if ($r.X -lt $x) { $x = $r.X }
        if ($r.Y -lt $y) { $y = $r.Y }
        if (($r.X + $r.Width) -gt $x2) { $x2 = $r.X + $r.Width }
        if (($r.Y + $r.Height) -gt $y2) { $y2 = $r.Y + $r.Height }
    }
    Write-Output ("BBOX`t{0:N0}`t{1:N0}`t{2:N0}`t{3:N0}`t{4}" -f $x, $y, $x2, $y2, $line.Text)
}
