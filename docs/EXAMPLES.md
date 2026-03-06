# Check all files one last time

Write-Host "🔍 FINAL CHECK:" -ForegroundColor Cyan

$all_files = @(
"backend/app.py",
"backend/config.py",
"backend/utils/helpers.py",
"backend/utils/validators.py",
"backend/data/sample_stories.json",
"backend/tests/test_api.py",
"final_verify.py",
"requirements.txt",
"Dockerfile",
"docker-compose.yml",
".env",
".gitignore",
"docs/API.md",
"docs/EXAMPLES.md"
)

$count = 0
foreach ($file in $all_files) {
if (Test-Path $file) {
Write-Host "✅ $file" -ForegroundColor Green
$count++
} else {
Write-Host "❌ $file MISSING!" -ForegroundColor Red
}
}

Write-Host "`n📊 TOTAL: $count/14 files present!" -ForegroundColor Yellow
