@echo off
echo ========================================
echo   Task Management App - تشغيل التطبيق
echo ========================================
echo.

REM Try different Python commands
echo جاري البحث عن Python...
echo.

REM Try python command
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo تم العثور على Python!
    echo.
    python app.py
    goto :end
)

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo تم العثور على Python عبر py launcher!
    echo.
    py app.py
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo تم العثور على Python3!
    echo.
    python3 app.py
    goto :end
)

REM If nothing works, show error
echo.
echo ========================================
echo   خطأ: Python غير موجود!
echo ========================================
echo.
echo يرجى تثبيت Python من:
echo https://www.python.org/downloads/
echo.
echo أو تعطيل Windows App Execution Aliases:
echo Settings ^> Apps ^> Advanced app settings ^> App execution aliases
echo.
pause

:end

