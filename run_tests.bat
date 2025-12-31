@echo off
echo ========================================
echo تشغيل اختبارات تطبيق إدارة المهام
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
echo [2/2] تشغيل الاختبارات التلقائية...
echo.
pytest test_app.py -v --tb=short

echo.
echo ========================================
echo انتهى تشغيل الاختبارات
echo ========================================
pause

