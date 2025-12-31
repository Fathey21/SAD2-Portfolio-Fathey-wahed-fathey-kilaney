# تعليمات تشغيل التطبيق

## المشكلة الحالية
Python غير موجود في PATH بسبب Windows App Execution Aliases.

## الحلول

### الحل 1: تثبيت Python (موصى به)
1. افتح المتصفح: https://www.python.org/downloads/
2. حمّل Python 3.11 أو أحدث
3. أثناء التثبيت: ✅ **تأكد من تحديد "Add Python to PATH"**
4. بعد التثبيت، أعد فتح Terminal

### الحل 2: تعطيل Windows App Execution Aliases
1. اضغط `Windows + I` لفتح Settings
2. اذهب إلى: **Apps** → **Advanced app settings** → **App execution aliases**
3. أوقف (Turn OFF) الخيارات التالية:
   - `python.exe`
   - `python3.exe`
4. أعد فتح Terminal

### الحل 3: استخدام ملف Batch
1. انقر نقراً مزدوجاً على ملف `run_app.bat`
2. سيحاول الملف العثور على Python تلقائياً

## بعد حل المشكلة

### الخطوة 1: تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### الخطوة 2: تشغيل التطبيق
```bash

```

### الخطوة 3: فتح المتصفح
افتح: http://localhost:5000

## ملاحظات
- إذا ظهر خطأ "python غير معروف"، جرب `py app.py`
- لإيقاف التطبيق: اضغط `Ctrl + C` في Terminal

