# Removes Founder on Windows: only the skill folders our installer marked as ours. Nothing you made with it is ever touched.
$ErrorActionPreference = "Stop"
$Commands = @("board", "competitors", "consumer", "pricing", "offer", "cfo", "marketing", "brand", "ops", "launch", "plan")   # written by scripts/sync.py from skill.json
$removed = 0
foreach ($base in "founder", "bmac-founder") {
  foreach ($name in @($base) + @($Commands | ForEach-Object { "$base-$_" })) {
    $dir = Join-Path $HOME ".claude\skills\$name"
    if (-not (Test-Path -LiteralPath $dir)) { continue }
    if (Test-Path -LiteralPath (Join-Path $dir ".founder-install")) {
      Remove-Item -Recurse -Force -LiteralPath $dir; $removed++
    } else {
      Write-Output "Left $dir alone: Founder did not install it."
    }
  }
}
if ($removed -gt 0) { Write-Output "Removed Founder ($removed skill folders)." } else { Write-Output "Founder was not installed." }
