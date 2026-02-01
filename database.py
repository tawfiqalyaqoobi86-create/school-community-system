import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('community_relations.db')
    c = conn.cursor()
    
    # 1. جدول أولياء الأمور
    c.execute('''CREATE TABLE IF NOT EXISTS parents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        participation_type TEXT, -- دعم تعليمي، مالي، خبرات، تطوع، مبادرات
        interaction_level TEXT, -- مرتفع، متوسط، محدود
        expertise TEXT, -- المجال المهني أو المهارة
        interaction_history TEXT, -- سجل اللقاءات والأنشطة
        last_contact DATE
    )''')
    
    # 2. جدول خطة العمل
    c.execute('''CREATE TABLE IF NOT EXISTS action_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objective TEXT,
        activity TEXT,
        responsibility TEXT,
        timeframe TEXT,
        kpi TEXT,
        status TEXT DEFAULT 'قيد التنفيذ', -- مكتمل، قيد التنفيذ، مؤجل
        priority TEXT -- مرتفع، متوسط، منخفض
    )''')
    
    # 3. جدول المبادرات
    c.execute('''CREATE TABLE IF NOT EXISTS initiatives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT, -- تعليمي، اجتماعي، مهني، صحي، ثقافي
        target_group TEXT,
        impact_score INTEGER, -- 1-10
        outcomes TEXT,
        date DATE
    )''')
    
    # 4. جدول سجل اللقاءات والملاحظات التطويرية (للذكاء الاصطناعي)
    c.execute('''CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        date DATE,
        attendees_count INTEGER,
        summary TEXT,
        ai_recommendations TEXT
    )''')
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('community_relations.db')

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
