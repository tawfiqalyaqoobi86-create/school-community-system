import sqlite3
import pandas as pd
import os

# تحديد المسار المطلق لقاعدة البيانات
# إذا كان التطبيق يعمل على منصة تدعم المجلدات الدائمة مثل Railway، سيستخدم المسار المخصص
DB_PATH = os.environ.get('PERSISTENT_DB_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'community_relations.db'))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. جدول أولياء الأمور
    c.execute('''CREATE TABLE IF NOT EXISTS parents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        participation_type TEXT,
        expertise TEXT,
        interaction_level TEXT,
        phone TEXT
    )''')
    
    # 2. جدول خطة العمل
    c.execute('''CREATE TABLE IF NOT EXISTS action_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objective TEXT,
        activity TEXT,
        responsibility TEXT,
        timeframe TEXT,
        kpi TEXT,
        status TEXT DEFAULT 'قيد التنفيذ',
        priority TEXT,
        task_type TEXT DEFAULT 'معنوي'
    )''')
    
    # 4. جدول سجل اللقاءات والملاحظات التطويرية
    c.execute('''CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        date DATE,
        attendees_count INTEGER,
        summary TEXT,
        ai_recommendations TEXT
    )''')

    # 5. جدول الفعاليات والأنشطة
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date DATE,
        location TEXT,
        attendees_count INTEGER,
        rating INTEGER
    )''')
    
    # 6. جدول التقارير المحفوظة
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date TEXT,
        report_content TEXT
    )''')
    
    conn.commit()
    conn.close()

def get_connection():
    init_db() # التأكد من وجود الجداول في كل مرة
    return sqlite3.connect(DB_PATH, timeout=20)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
