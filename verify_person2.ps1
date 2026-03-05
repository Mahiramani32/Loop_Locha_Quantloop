# ============================================
# PERSON 2 - COMPLETE FILE VERIFICATION SCRIPT
# ============================================

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "🔍 VERIFYING PERSON 2 PROJECT STRUCTURE" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

$totalFiles = 0
$missingFiles = @()
$emptyFiles = @()
$smallFiles = @()

function Check-File {
    param($Path, $Description)
    
    $global:totalFiles++
    
    if (Test-Path $Path) {
        $file = Get-Item $Path
        if ($file.Length -eq 0) {
            Write-Host "❌ $Description - EMPTY FILE (0 bytes)" -ForegroundColor Red
            $global:emptyFiles += $Path
        } elseif ($file.Length -lt 50) {
            Write-Host "⚠️ $Description - VERY SMALL ($($file.Length) bytes)" -ForegroundColor Yellow
            $global:smallFiles += $Path
        } else {
            Write-Host "✅ $Description - OK ($($file.Length) bytes)" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ $Description - MISSING" -ForegroundColor Red
        $global:missingFiles += $Path
    }
}

Write-Host "`n📁 ROOT DIRECTORY FILES:" -ForegroundColor Yellow
Check-File -Path ".gitignore" -Description ".gitignore"
Check-File -Path "README.md" -Description "README.md"
Check-File -Path "requirements.txt" -Description "requirements.txt"
Check-File -Path "API_INTEGRATION.md" -Description "API_INTEGRATION.md"
Check-File -Path "emotion_model.pkl" -Description "emotion_model.pkl"

Write-Host "`n📁 BACKEND PACKAGE:" -ForegroundColor Yellow
Check-File -Path "backend\__init__.py" -Description "backend/__init__.py"

Write-Host "`n📁 MODULES DIRECTORY:" -ForegroundColor Yellow
Check-File -Path "backend\modules\__init__.py" -Description "modules/__init__.py"
Check-File -Path "backend\modules\language_detector.py" -Description "language_detector.py"
Check-File -Path "backend\modules\story_decomposer.py" -Description "story_decomposer.py"
Check-File -Path "backend\modules\emotion_analyzer.py" -Description "emotion_analyzer.py"

Write-Host "`n📁 MODELS DIRECTORY:" -ForegroundColor Yellow
Check-File -Path "backend\models\__init__.py" -Description "models/__init__.py"
Check-File -Path "backend\models\emotion_model.py" -Description "emotion_model.py"

Write-Host "`n📁 UTILS DIRECTORY:" -ForegroundColor Yellow
Check-File -Path "backend\utils\__init__.py" -Description "utils/__init__.py"
Check-File -Path "backend\utils\helpers.py" -Description "helpers.py"
Check-File -Path "backend\utils\validators.py" -Description "validators.py"

Write-Host "`n📁 TESTS DIRECTORY:" -ForegroundColor Yellow
Check-File -Path "backend\tests\__init__.py" -Description "tests/__init__.py"
Check-File -Path "backend\tests\test_modules.py" -Description "test_modules.py"

Write-Host "`n📁 DATA DIRECTORY:" -ForegroundColor Yellow
Check-File -Path "backend\data\sample_stories.json" -Description "sample_stories.json"

Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "📊 VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Total files checked: $totalFiles" -ForegroundColor White

if ($missingFiles.Count -eq 0) {
    Write-Host "✅ All required files exist!" -ForegroundColor Green
} else {
    Write-Host "❌ Missing files: $($missingFiles.Count)" -ForegroundColor Red
    $missingFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
}

if ($emptyFiles.Count -eq 0) {
    Write-Host "✅ No empty files found!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Empty files: $($emptyFiles.Count)" -ForegroundColor Yellow
    $emptyFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
}

if ($smallFiles.Count -eq 0) {
    Write-Host "✅ All files have good size!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Very small files (check content): $($smallFiles.Count)" -ForegroundColor Yellow
    $smallFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
}

Write-Host "`n" + "="*60 -ForegroundColor Cyan
if ($missingFiles.Count -eq 0 -and $emptyFiles.Count -eq 0) {
    Write-Host "🎉🎉🎉 PERSON 2 PROJECT IS 100% COMPLETE! 🎉🎉🎉" -ForegroundColor Green
} else {
    Write-Host "⚠️ PROJECT NEEDS ATTENTION - Please fix the issues above" -ForegroundColor Yellow
}
Write-Host "="*60 -ForegroundColor Cyan
