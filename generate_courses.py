#!/usr/bin/env python3
"""
Script to generate 50 sample courses in CSV format for manual testing.
"""

import csv
import os
from datetime import datetime

def generate_50_courses():
    """Generate 50 sample courses"""

    courses = [
        {"id": 7, "title": "قواعد البيانات", "description": "تعلم تصميم وإدارة قواعد البيانات", "instructor": "د. سارة حسن", "credits": 3},
        {"id": 8, "title": "شبكات الحاسوب", "description": "أساسيات الشبكات والاتصالات", "instructor": "د. علي محمود", "credits": 4},
        {"id": 9, "title": "أمن المعلومات", "description": "مبادئ الأمان الرقمي والتشفير", "instructor": "د. لينا أحمد", "credits": 3},
        {"id": 10, "title": "تطوير الويب", "description": "بناء تطبيقات الويب الحديثة", "instructor": "د. كريم عبدالله", "credits": 4},
        {"id": 11, "title": "تعلم الآلة", "description": "خوارزميات التعلم الآلي والذكاء الاصطناعي", "instructor": "د. نورا سالم", "credits": 5},
        {"id": 12, "title": "تحليل البيانات", "description": "أدوات وتقنيات تحليل البيانات الكبيرة", "instructor": "د. يوسف محمد", "credits": 3},
        {"id": 13, "title": "هندسة البرمجيات", "description": "منهجيات تطوير البرمجيات", "instructor": "د. منى علي", "credits": 4},
        {"id": 14, "title": "أنظمة التشغيل", "description": "مبادئ أنظمة التشغيل والنواة", "instructor": "د. حسن محمود", "credits": 3},
        {"id": 15, "title": "لغات البرمجة", "description": "مقارنة بين لغات البرمجة المختلفة", "instructor": "د. فاطمة أحمد", "credits": 3},
        {"id": 16, "title": "تصميم واجهات المستخدم", "description": "تصميم تجارب المستخدم الجيدة", "instructor": "د. ليلى سالم", "credits": 2},
        {"id": 17, "title": "إدارة المشاريع", "description": "إدارة مشاريع تطوير البرمجيات", "instructor": "د. عمر حسن", "credits": 3},
        {"id": 18, "title": "الرياضيات المتقطعة", "description": "مفاهيم رياضية لعلوم الحاسوب", "instructor": "د. سارة محمد", "credits": 4},
        {"id": 19, "title": "هياكل البيانات", "description": "هياكل البيانات والخوارزميات", "instructor": "د. أحمد علي", "credits": 4},
        {"id": 20, "title": "تطوير الألعاب", "description": "برمجة ألعاب الفيديو", "instructor": "د. نور حسن", "credits": 3},
        {"id": 21, "title": "الحوسبة السحابية", "description": "خدمات الحوسبة السحابية و AWS", "instructor": "د. كريم سالم", "credits": 3},
        {"id": 22, "title": "إنترنت الأشياء", "description": "تطوير أجهزة IoT والاتصال", "instructor": "د. لينا محمود", "credits": 4},
        {"id": 23, "title": "الواقع الافتراضي", "description": "تطوير تطبيقات VR و AR", "instructor": "د. يوسف أحمد", "credits": 3},
        {"id": 24, "title": "البلوكشين", "description": "تقنية البلوكشين والعملات الرقمية", "instructor": "د. منى سالم", "credits": 3},
        {"id": 25, "title": "تحليل الأداء", "description": "قياس وتحسين أداء البرامج", "instructor": "د. حسن علي", "credits": 2},
        {"id": 26, "title": "البرمجة الوظيفية", "description": "مبادئ البرمجة الوظيفية", "instructor": "د. فاطمة محمد", "credits": 3},
        {"id": 27, "title": "معالجة الصور", "description": "معالجة وتحليل الصور الرقمية", "instructor": "د. ليلى حسن", "credits": 4},
        {"id": 28, "title": "تعلم العمق", "description": "شبكات التعلم العميق", "instructor": "د. عمر سالم", "credits": 5},
        {"id": 29, "title": "أخلاقيات الذكاء الاصطناعي", "description": "الجوانب الأخلاقية للذكاء الاصطناعي", "instructor": "د. سارة أحمد", "credits": 2},
        {"id": 30, "title": "تطوير التطبيقات المحمولة", "description": "برمجة تطبيقات Android و iOS", "instructor": "د. أحمد محمود", "credits": 4},
        {"id": 31, "title": "إدارة الجودة", "description": "ضمان جودة البرمجيات", "instructor": "د. نور علي", "credits": 3},
        {"id": 32, "title": "الأتمتة والسكريبت", "description": "أتمتة المهام باستخدام السكريبت", "instructor": "د. كريم حسن", "credits": 2},
        {"id": 33, "title": "الأمان السيبراني", "description": "حماية الأنظمة من الهجمات السيبرانية", "instructor": "د. لينا سالم", "credits": 4},
        {"id": 34, "title": "تصميم قواعد البيانات", "description": "تصميم قواعد البيانات المتقدمة", "instructor": "د. يوسف محمد", "credits": 3},
        {"id": 35, "title": "البرمجة الموازية", "description": "البرمجة المتعددة الخيوط", "instructor": "د. منى أحمد", "credits": 4},
        {"id": 36, "title": "تحليل النظم", "description": "تحليل وتصميم الأنظمة", "instructor": "د. حسن سالم", "credits": 3},
        {"id": 37, "title": "اللغويات الحاسوبية", "description": "معالجة اللغات الطبيعية", "instructor": "د. فاطمة علي", "credits": 3},
        {"id": 38, "title": "الروبوتات", "description": "برمجة الروبوتات والأتمتة", "instructor": "د. ليلى محمود", "credits": 4},
        {"id": 39, "title": "إدارة الشبكات", "description": "إدارة وصيانة شبكات الحاسوب", "instructor": "د. عمر أحمد", "credits": 3},
        {"id": 40, "title": "الواقع المعزز", "description": "تطوير تطبيقات الواقع المعزز", "instructor": "د. سارة سالم", "credits": 3},
        {"id": 41, "title": "البيانات الكبيرة", "description": "إدارة وتحليل البيانات الكبيرة", "instructor": "د. أحمد حسن", "credits": 4},
        {"id": 42, "title": "الأنظمة الموزعة", "description": "مبادئ الأنظمة الموزعة", "instructor": "د. نور محمود", "credits": 4},
        {"id": 43, "title": "البرمجة السحابية", "description": "تطوير التطبيقات السحابية", "instructor": "د. كريم أحمد", "credits": 3},
        {"id": 44, "title": "الأمان في الويب", "description": "أمان تطبيقات الويب", "instructor": "د. لينا علي", "credits": 3},
        {"id": 45, "title": "معالجة الإشارات", "description": "معالجة الإشارات الرقمية", "instructor": "د. يوسف سالم", "credits": 4},
        {"id": 46, "title": "الذكاء الاصطناعي الأخلاقي", "description": "الجوانب الأخلاقية في الذكاء الاصطناعي", "instructor": "د. منى محمد", "credits": 2},
        {"id": 47, "title": "تطوير API", "description": "تصميم وتطوير واجهات برمجة التطبيقات", "instructor": "د. حسن أحمد", "credits": 3},
        {"id": 48, "title": "البرمجة الكائنية", "description": "مبادئ البرمجة كائنية التوجه", "instructor": "د. فاطمة سالم", "credits": 3},
        {"id": 49, "title": "إدارة الإصدارات", "description": "استخدام Git وأنظمة إدارة الإصدارات", "instructor": "د. ليلى أحمد", "credits": 2},
        {"id": 50, "title": "التصميم المتجاوب", "description": "تصميم مواقع متجاوبة", "instructor": "د. عمر محمد", "credits": 3},
        {"id": 51, "title": "تحليل الأعمال", "description": "تحليل متطلبات الأعمال", "instructor": "د. سارة حسن", "credits": 3},
        {"id": 52, "title": "البرمجة الآمنة", "description": "كتابة كود آمن من الثغرات", "instructor": "د. أحمد علي", "credits": 4},
        {"id": 53, "title": "الذكاء التجاري", "description": "تطبيقات الذكاء الاصطناعي في الأعمال", "instructor": "د. نور سالم", "credits": 3},
        {"id": 54, "title": "إدارة الخدمات", "description": "إدارة خدمات تكنولوجيا المعلومات", "instructor": "د. كريم محمود", "credits": 3},
        {"id": 55, "title": "الواقع الافتراضي التعليمي", "description": "استخدام VR في التعليم", "instructor": "د. لينا أحمد", "credits": 2},
        {"id": 56, "title": "الأتمتة الذكية", "description": "الأتمتة باستخدام الذكاء الاصطناعي", "instructor": "د. يوسف حسن", "credits": 4}
    ]

    # Generate timestamps
    base_time = datetime.now().isoformat()

    # Write to courses_backup.csv (append mode)
    with open('courses_backup.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for course in courses:
            writer.writerow([
                course['id'],
                course['title'],
                course['description'],
                course['instructor'],
                course['credits'],
                base_time,
                base_time
            ])

    print("تم إضافة 50 دورة تدريبية إلى ملف courses_backup.csv")

if __name__ == "__main__":
    generate_50_courses()