# المبادئ البرمجية وأنماط التصميم المطبقة

## المبادئ البرمجية (Software Engineering Principles)

### 1. مبدأ المسؤولية الواحدة (Single Responsibility Principle - SRP)
**الموقع في الكود:** `app.py` - كلاس `TaskManager`

**الوصف:**
- كلاس `TaskManager` مسؤول فقط عن إدارة المهام (CRUD operations)
- كلاس `Config` مسؤول فقط عن إعدادات التطبيق
- كلاس `TaskFactory` مسؤول فقط عن إنشاء المهام
- كلاس `TaskObserver` وملحقاته مسؤولة فقط عن الإشعارات

**مثال من الكود:**
```python
class TaskManager:
    def add_task(self, title, description, priority='medium', due_date=None):
        """Add a new task - Single Responsibility"""
        task = TaskFactory.create_task(title, description, priority, due_date)
        self.tasks.append(task)
        self._save_tasks()
        return task
```

### 2. مبدأ DRY (Don't Repeat Yourself)
**الموقع في الكود:** `app.py` - دوال الحفظ والتحميل

**الوصف:**
- استخدام دوال `_load_tasks()` و `_save_tasks()` لتجنب تكرار كود القراءة والكتابة
- استخدام `TaskFactory` لتجنب تكرار كود إنشاء المهام
- استخدام `get_next_id()` كدالة مشتركة لتوليد المعرفات

**مثال من الكود:**
```python
def _save_tasks(self):
    """Save tasks to JSON file - DRY Principle"""
    with open(self.config.get_data_file(), 'w', encoding='utf-8') as f:
        json.dump(self.tasks, f, indent=2, ensure_ascii=False)
```

### 3. مبدأ KISS (Keep It Simple, Stupid)
**الموقع في الكود:** جميع الملفات

**الوصف:**
- بنية بسيطة وواضحة للتطبيق
- استخدام JSON للتخزين بدلاً من قاعدة بيانات معقدة
- واجهة برمجية RESTful بسيطة
- كود سهل القراءة والفهم

**مثال من الكود:**
```python
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks API - Simple and Clear"""
    tasks = task_manager.get_all_tasks()
    return jsonify(tasks)
```

### 4. مبدأ Open/Closed Principle (OCP)
**الموقع في الكود:** `app.py` - Observer Pattern

**الوصف:**
- يمكن إضافة أنواع جديدة من المراقبين (Observers) دون تعديل الكود الأساسي
- يمكن إضافة أنواع جديدة من المهام عبر Factory Pattern

**مثال من الكود:**
```python
class TaskObserver:
    def update(self, task, event_type):
        pass

class EmailNotifier(TaskObserver):
    def update(self, task, event_type):
        print(f"[Email] Task '{task['title']}' - Event: {event_type}")

# يمكن إضافة مراقب جديد دون تعديل TaskManager
class SMSNotifier(TaskObserver):
    def update(self, task, event_type):
        print(f"[SMS] Task '{task['title']}' - Event: {event_type}")
```

### 5. مبدأ Dependency Inversion Principle (DIP)
**الموقع في الكود:** `app.py` - استخدام Config و Factory

**الوصف:**
- `TaskManager` يعتمد على `Config` و `TaskFactory` كواجهات مجردة
- يمكن استبدال التخزين (JSON) بتخزين آخر دون تغيير الكود الأساسي

## أنماط التصميم (Design Patterns)

### 1. نمط Singleton (الوحدانية)
**الموقع في الكود:** `app.py` - كلاس `Config`

**الوصف:**
- يضمن وجود instance واحد فقط من `Config` في التطبيق
- يوفر نقطة وصول مركزية للإعدادات

**الكود:**
```python
class Config:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Config._initialized:
            self.data_file = 'tasks.json'
            self.max_tasks = 1000
            Config._initialized = True
```

**الفوائد:**
- ضمان وجود نسخة واحدة من الإعدادات
- توفير الذاكرة
- نقطة وصول موحدة

### 2. نمط Factory (المصنع)
**الموقع في الكود:** `app.py` - كلاس `TaskFactory`

**الوصف:**
- يوفر طريقة موحدة لإنشاء كائنات المهام
- يخفي تفاصيل إنشاء المهام عن الكود المستخدم

**الكود:**
```python
class TaskFactory:
    @staticmethod
    def create_task(title, description, priority='medium', due_date=None):
        return {
            'id': TaskManager.get_next_id(),
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'pending',
            'due_date': due_date,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
```

**الفوائد:**
- فصل منطق الإنشاء عن الكود المستخدم
- سهولة إضافة أنواع جديدة من المهام
- كود أكثر تنظيماً

### 3. نمط Observer (المراقب)
**الموقع في الكود:** `app.py` - كلاس `TaskObserver` وملحقاته

**الوصف:**
- يسمح لكائنات متعددة بالاستماع إلى تغييرات المهام
- عند حدوث حدث (إنشاء، تحديث، حذف)، يتم إشعار جميع المراقبين

**الكود:**
```python
class TaskObserver:
    def update(self, task, event_type):
        pass

class EmailNotifier(TaskObserver):
    def update(self, task, event_type):
        print(f"[Email] Task '{task['title']}' - Event: {event_type}")

class LogNotifier(TaskObserver):
    def update(self, task, event_type):
        print(f"[Log] Task '{task['title']}' - Event: {event_type}")

# في TaskManager
def _notify_observers(self, task, event_type):
    """Notify all observers"""
    for observer in self._observers:
        observer.update(task, event_type)
```

**الفوائد:**
- فصل الكود المراقب عن الكود المراقَب
- إمكانية إضافة مراقبين جدد بسهولة
- مرونة عالية في التوسع

## ملخص التطبيق

### المبادئ المطبقة:
1. ✅ **Single Responsibility Principle (SRP)**
2. ✅ **DRY (Don't Repeat Yourself)**
3. ✅ **KISS (Keep It Simple, Stupid)**
4. ✅ **Open/Closed Principle (OCP)**
5. ✅ **Dependency Inversion Principle (DIP)**

### أنماط التصميم المطبقة:
1. ✅ **Singleton Pattern**
2. ✅ **Factory Pattern**
3. ✅ **Observer Pattern**

### الميزات:
- تطبيق ويب لإدارة المهام
- واجهة برمجية RESTful كاملة
- تخزين البيانات في JSON
- نظام إشعارات قابل للتوسع
- اختبارات شاملة (50 اختبار تلقائي)

