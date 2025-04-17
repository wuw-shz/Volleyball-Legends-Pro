@echo off
echo Building Volleyball Legends Pro...

timeout /t 2 /nobreak > nul

echo Cleaning previous builds...
if exist "dist\VolleyballLegendsPro" (
    rmdir /s /q "dist\VolleyballLegendsPro"
    if %ERRORLEVEL% neq 0 (
        echo Warning: Could not clean dist directory. Proceeding anyway...
    )
)

if exist "build\volleyball_legends_pro" (
    rmdir /s /q "build\volleyball_legends_pro"
    if %ERRORLEVEL% neq 0 (
        echo Warning: Could not clean build directory. Proceeding anyway...
    )
)

echo Generating version information...
python generate_version_info.py
if %ERRORLEVEL% neq 0 (
    echo Version generation failed!
    exit /b %ERRORLEVEL%
)

echo Running PyInstaller...
pyinstaller volleyball_legends_pro.spec --noconfirm
if %ERRORLEVEL% neq 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)

echo Build completed successfully!

timeout /t 2 /nobreak > nul

echo Creating release package...
if not exist "releases" mkdir releases
python make_release.py
if %ERRORLEVEL% neq 0 (
    echo Release packaging failed!
    exit /b %ERRORLEVEL%
)

echo Build and release packaging complete!
pause 