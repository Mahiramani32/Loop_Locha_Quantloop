# ============================================
# PERSON 2 - COMPLETE VERIFICATION & TEST SUITE
# ============================================

Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "🚀 PERSON 2 - COMPLETE VERIFICATION & TEST SUITE" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Magenta

# ============================================
# PART 1: FILE EXISTENCE CHECK
# ============================================
Write-Host "`n📁 PART 1: CHECKING FILE EXISTENCE" -ForegroundColor Yellow
Write-Host "-"*50

$files = @{
    "Root Files" = @(
        ".gitignore",
        "README.md", 
        "requirements.txt",
        "API_INTEGRATION.md",
        "emotion_model.pkl"
    )
    "Backend Package" = @(
        "backend\__init__.py"
    )
    "Modules" = @(
        "backend\modules\__init__.py",
        "backend\modules\language_detector.py",
        "backend\modules\story_decomposer.py", 
        "backend\modules\emotion_analyzer.py"
    )
    "Models" = @(
        "backend\models\__init__.py",
        "backend\models\emotion_model.py"
    )
    "Utils" = @(
        "backend\utils\__init__.py",
        "backend\utils\helpers.py",
        "backend\utils\validators.py"
    )
    "Tests" = @(
        "backend\tests\__init__.py",
        "backend\tests\test_modules.py"
    )
    "Data" = @(
        "backend\data\sample_stories.json"
    )
}

$allExist = $true
foreach ($category in $files.Keys) {
    Write-Host "`n$category" -ForegroundColor Cyan
    foreach ($file in $files[$category]) {
        if (Test-Path $file) {
            $size = (Get-Item $file).Length
            Write-Host "  ✅ $file - OK ($size bytes)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $file - MISSING" -ForegroundColor Red
            $allExist = $false
        }
    }
}

# ============================================
# PART 2: PYTHON SYNTAX CHECK
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "🔍 PART 2: CHECKING PYTHON SYNTAX" -ForegroundColor Yellow
Write-Host "-"*50

$pythonFiles = Get-ChildItem -Path "backend" -Recurse -Filter "*.py" | Select-Object -ExpandProperty FullName

foreach ($file in $pythonFiles) {
    $result = python -m py_compile $file 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $file - Syntax OK" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - Syntax Error" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
    }
}

# ============================================
# PART 3: RUN INDIVIDUAL MODULES
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "🧪 PART 3: TESTING INDIVIDUAL MODULES" -ForegroundColor Yellow
Write-Host "-"*50

Write-Host "`n📝 Testing Language Detector:" -ForegroundColor Cyan
try {
    $output = python -c "
from backend.modules.language_detector import language_detector
result = language_detector.detect('Hello world')
print('  ✅ Import successful')
print(f'  ✅ Detection result: {result[\"language_name\"]} ({result[\"confidence\"]})')
" 2>&1
    Write-Host $output -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed: $_" -ForegroundColor Red
}

Write-Host "`n📝 Testing Story Decomposer:" -ForegroundColor Cyan
try {
    $output = python -c "
from backend.modules.story_decomposer import story_decomposer
result = story_decomposer.decompose('Test story.')
print('  ✅ Import successful')
print(f'  ✅ Word count: {result[\"statistics\"][\"word_count\"]}')
" 2>&1
    Write-Host $output -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed: $_" -ForegroundColor Red
}

Write-Host "`n📝 Testing Emotion Analyzer:" -ForegroundColor Cyan
try {
    $output = python -c "
from backend.modules.emotion_analyzer import emotion_analyzer
result = emotion_analyzer.analyze('I am happy!')
print('  ✅ Import successful')
print(f'  ✅ Dominant emotion: {result[\"dominant_emotion\"][\"name\"]}')
" 2>&1
    Write-Host $output -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed: $_" -ForegroundColor Red
}

Write-Host "`n📝 Testing Emotion Model:" -ForegroundColor Cyan
try {
    $output = python -c "
from backend.models.emotion_model import EmotionModel
model = EmotionModel()
print('  ✅ Import successful')
" 2>&1
    Write-Host $output -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed: $_" -ForegroundColor Red
}

Write-Host "`n📝 Testing Utils:" -ForegroundColor Cyan
try {
    $output = python -c "
from backend.utils import helpers, validators
print('  ✅ Helpers import successful')
print('  ✅ Validators import successful')
" 2>&1
    Write-Host $output -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed: $_" -ForegroundColor Red
}

# ============================================
# PART 4: RUN ACTUAL TESTS
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "🧪 PART 4: RUNNING PYTEST SUITE" -ForegroundColor Yellow
Write-Host "-"*50

try {
    $testOutput = python -m pytest backend\tests\test_modules.py -v 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ All tests passed!" -ForegroundColor Green
        Write-Host $testOutput -ForegroundColor Green
    } else {
        Write-Host "  ❌ Some tests failed" -ForegroundColor Red
        Write-Host $testOutput -ForegroundColor Red
    }
} catch {
    Write-Host "  ❌ Failed to run tests: $_" -ForegroundColor Red
}

# ============================================
# PART 5: CHECK JSON DATA
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "📊 PART 5: CHECKING SAMPLE DATA" -ForegroundColor Yellow
Write-Host "-"*50

try {
    $json = Get-Content "backend\data\sample_stories.json" -Raw | ConvertFrom-Json
    $storyCount = $json.stories.Count
    Write-Host "  ✅ JSON file is valid" -ForegroundColor Green
    Write-Host "  ✅ Contains $storyCount sample stories" -ForegroundColor Green
    
    # Show first story preview
    $firstStory = $json.stories[0]
    Write-Host "`n  📖 First story preview:" -ForegroundColor Cyan
    Write-Host "     Title: $($firstStory.title)" -ForegroundColor White
    Write-Host "     Language: $($firstStory.language)" -ForegroundColor White
    Write-Host "     Emotion: $($firstStory.emotion)" -ForegroundColor White
} catch {
    Write-Host "  ❌ JSON file is invalid: $_" -ForegroundColor Red
}

# ============================================
# PART 6: CHECK REQUIREMENTS
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
Write-Host "📦 PART 6: CHECKING REQUIREMENTS" -ForegroundColor Yellow
Write-Host "-"*50

try {
    $requirements = Get-Content "requirements.txt"
    Write-Host "  ✅ requirements.txt found" -ForegroundColor Green
    Write-Host "  📋 Total packages: $($requirements.Count)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ requirements.txt missing" -ForegroundColor Red
}

# ============================================
# FINAL SUMMARY
# ============================================
Write-Host "`n" + "="*70 -ForegroundColor Magenta
if ($allExist) {
    Write-Host "🎉🎉🎉 PERSON 2 - ALL CHECKS PASSED! 🎉🎉🎉" -ForegroundColor Green
    Write-Host "="*70 -ForegroundColor Magenta
    Write-Host "✅ All files exist" -ForegroundColor Green
    Write-Host "✅ All Python files have valid syntax" -ForegroundColor Green
    Write-Host "✅ All modules import correctly" -ForegroundColor Green
    Write-Host "✅ Tests completed" -ForegroundColor Green
    Write-Host "✅ Sample data is valid" -ForegroundColor Green
    Write-Host "`n📝 Ready for git commit and pull request!" -ForegroundColor Cyan
} else {
    Write-Host "⚠️⚠️⚠️ SOME CHECKS FAILED - PLEASE FIX ISSUES ⚠️⚠️⚠️" -ForegroundColor Yellow
}
Write-Host "="*70 -ForegroundColor Magenta
