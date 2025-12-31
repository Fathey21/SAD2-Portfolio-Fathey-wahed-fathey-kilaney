@echo off
echo ========================================
echo تشغيل تطبيق إدارة المهام
echo ========================================
echo.

echo [1/2] التحقق من تثبيت المكتبات...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo تثبيت المكتبات المطلوبة...
    pip install -r requirements.txt
) else (
    echo المكتبات مثبتة بالفعل ✓
)

echo.
echo [2/2] تشغيل التطبيق...
echo.
echo التطبيق يعمل على: http://localhost:5000
echo اضغط Ctrl+C لإيقاف التطبيق
echo.
python app.py

pause

