# dev.ps1

# ---- Resolve .env path properly ----
$rawEnvPath = Join-Path $PSScriptRoot "..\.env"

try {
    $envPath = (Resolve-Path $rawEnvPath).Path
} catch {
    $envPath = $null
}

# ---- Load .env ----
if ($envPath) {
    $lines = Get-Content $envPath -Encoding UTF8

    foreach ($lineRaw in $lines) {
        $line = $lineRaw.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) { continue }
        if (-not $line.Contains("=")) { continue }

        $key, $value = $line.Split("=", 2)
        $key = $key.Trim()
        $value = $value.Trim()

        # strip quotes
        if ($value.StartsWith('"') -and $value.EndsWith('"')) {
            $value = $value.Substring(1, $value.Length - 2)
        }
        if ($value.StartsWith("'") -and $value.EndsWith("'")) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        Set-Item -Path "env:$key" -Value $value
    }
}

# ---- Effective values ----
$APP_HOST = $env:HOST
$APP_PORT = $env:PORT

if (-not $APP_HOST) { $APP_HOST = "127.0.0.1" }
if (-not $APP_PORT) { $APP_PORT = "1488" }

# ---- Minimal log ----
Write-Host "[dev.ps1] HOST=$APP_HOST PORT=$APP_PORT"

# ---- Start server ----
uvicorn app.main:app `
  --reload `
  --host $APP_HOST `
  --port $APP_PORT `
  --log-level warning `
  --no-access-log
