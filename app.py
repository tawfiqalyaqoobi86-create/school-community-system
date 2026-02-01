import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection, init_db
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مساعد مشرف تنمية العلاقات المجتمعية", layout="wide", initial_sidebar_state="expanded")

# تهيئة قاعدة البيانات
init_db()

# تنسيق CSS مخصص للغة العربية والواجهة الرسمية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1e3a8a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الجانبي
st.sidebar.title("🗂️ القائمة الرئيسية")
menu = st.sidebar.radio(
    "انتقل إلى:",
    ["لوحة التحكم", "قاعدة بيانات أولياء الأمور", "خطة العمل", "إدارة المبادرات", "الذكاء الاصطناعي", "التقارير والإحصائيات"]
)

# --- وظائف مساعدة ---
def load_data(table):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

# --- 1. لوحة التحكم ---
if menu == "لوحة التحكم":
    st.title("📊 لوحة القيادة المجتمعية")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("أولياء الأمور الفاعلين", len(load_data("parents")))
    with col2:
        st.metric("المبادرات المنفذة", len(load_data("initiatives")))
    with col3:
        st.metric("الأهداف المكتملة", len(load_data("action_plan")[load_data("action_plan")['status'] == 'مكتمل']))
    with col4:
        st.metric("متوسط أثر المبادرات", f"{load_data('initiatives')['impact_score'].mean():.1f}/10" if not load_data('initiatives').empty else "0/10")

    st.info("مرحباً بك في نظام المساعد الرقمي. يمكنك البدء بإضافة البيانات في التبويبات الجانبية.")

# --- 2. قاعدة بيانات أولياء الأمور ---
elif menu == "قاعدة بيانات أولياء الأمور":
    st.title("👨‍👩‍👧‍👦 قاعدة بيانات أولياء الأمور الفاعلين")
    
    with st.expander("➕ إضافة ولي أمر جديد"):
        with st.form("parent_form"):
            name = st.text_input("الاسم الكامل")
            p_type = st.selectbox("نوع المشاركة", ["دعم تعليمي", "دعم مالي", "خبرات مهنية", "تطوع", "مبادرات"])
            level = st.select_slider("مستوى التفاعل", options=["محدود", "متوسط", "مرتفع"])
            exp = st.text_input("المجال / الخبرة")
            submitted = st.form_submit_button("حفظ البيانات")
            
            if submitted:
                conn = get_connection()
                conn.execute("INSERT INTO parents (name, participation_type, interaction_level, expertise) VALUES (?, ?, ?, ?)",
                             (name, p_type, level, exp))
                conn.commit()
                conn.close()
                st.success("تم الحفظ بنجاح")

    df_parents = load_data("parents")
    st.dataframe(df_parents, use_container_width=True)

# --- 3. خطة العمل ---
elif menu == "خطة العمل":
    st.title("📅 خطة عمل فريق تنمية العلاقات")
    
    with st.expander("📝 إضافة هدف/نشاط جديد"):
        with st.form("plan_form"):
            obj = st.text_area("الهدف الإجرائي")
            act = st.text_input("النشاط/المبادرة")
            resp = st.text_input("المسؤول")
            time = st.text_input("الجدول الزمني")
            kpi = st.text_input("مؤشر الأداء (KPI)")
            prio = st.selectbox("الأولوية", ["مرتفع", "متوسط", "منخفض"])
            submitted = st.form_submit_button("إضافة للخطة")
            
            if submitted:
                conn = get_connection()
                conn.execute("INSERT INTO action_plan (objective, activity, responsibility, timeframe, kpi, priority) VALUES (?, ?, ?, ?, ?, ?)",
                             (obj, act, resp, time, kpi, prio))
                conn.commit()
                conn.close()
                st.success("تم تحديث الخطة")

    df_plan = load_data("action_plan")
    st.table(df_plan)

# --- 4. إدارة المبادرات ---
elif menu == "إدارة المبادرات":
    st.title("💡 المبادرات المجتمعية")
    
    with st.expander("🚀 توثيق مبادرة جديدة"):
        with st.form("init_form"):
            title = st.text_input("عنوان المبادرة")
            cat = st.selectbox("المجال", ["تعليمي", "اجتماعي", "مهني", "صحي", "ثقافي"])
            target = st.text_input("الفئة المستهدفة")
            score = st.slider("مستوى الأثر المتوقع (1-10)", 1, 10, 5)
            outcomes = st.text_area("المخرجات والنتائج")
            submitted = st.form_submit_button("توثيق المبادرة")
            
            if submitted:
                conn = get_connection()
                conn.execute("INSERT INTO initiatives (title, category, target_group, impact_score, outcomes, date) VALUES (?, ?, ?, ?, ?, ?)",
                             (title, cat, target, score, outcomes, datetime.now().date()))
                conn.commit()
                conn.close()
                st.success("تم توثيق المبادرة بنجاح")

    df_init = load_data("initiatives")
    st.dataframe(df_init, use_container_width=True)

# --- 5. الذكاء الاصطناعي (التبويب الذكي) ---
elif menu == "الذكاء الاصطناعي":
    st.title("🤖 مساعد الذكاء الاصطناعي")
    
    parents = load_data("parents")
    inits = load_data("initiatives")
    
    st.subheader("💡 توصيات ذكية لتطوير الشراكة")
    
    if parents.empty:
        st.warning("يرجى إضافة بيانات أولياء الأمور أولاً للحصول على توصيات.")
    else:
        # منطق ذكي بسيط لمحاكاة الـ AI بناءً على البيانات
        high_interact = len(parents[parents['interaction_level'] == 'مرتفع'])
        total = len(parents)
        engagement_rate = (high_interact / total) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📈 نسبة التفاعل المرتفع: {engagement_rate:.1f}%")
            if engagement_rate < 30:
                st.write("⚠️ **توصية:** اقترح تنظيم 'لقاء قهوة صباحي' غير رسمي لكسر الحاجز مع أولياء الأمور ذوي التفاعل المحدود.")
            else:
                st.write("✅ **توصية:** استثمر في أولياء الأمور الفاعلين لقيادة لجان تطوعية جديدة.")
        
        with col2:
            top_expertise = parents['participation_type'].value_counts().idxmax()
            st.success(f"🌟 القوة الكبرى: {top_expertise}")
            st.write(f"نقترح إطلاق مبادرة في مجال '{top_expertise}' لتعظيم الاستفادة من خبرات المجتمع.")

        st.divider()
        st.subheader("📝 توليد مسودة مبادرة جديدة")
        need = st.text_input("ما هو التحدي الحالي في المدرسة؟ (مثلاً: ضعف القراءة، التنمر)")
        if st.button("توليد مقترح مبادرة"):
            st.write(f"### مقترح مبادرة: 'معاً لنتخطى {need}'")
            st.write(f"**الهدف:** إشراك أولياء الأمور في حل مشكلة {need} عبر ورش عمل تخصصية.")
            st.write("**الأنشطة المقترحة:** لقاءات شهرية + كتيب إرشادي + مسابقة مجتمعية.")

# --- 6. التقارير والإحصائيات ---
elif menu == "التقارير والإحصائيات":
    st.title("📈 التحليلات والتقارير الذكية")
    
    inits = load_data("initiatives")
    if not inits.empty:
        fig = px.pie(inits, names='category', title='توزيع المبادرات حسب المجال', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
        
        fig2 = px.bar(inits, x='title', y='impact_score', color='category', title='مستوى أثر المبادرات المنفذة')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("لا توجد بيانات كافية لعرض الرسوم البيانية.")

    if st.button("📄 توليد تقرير رسمي (PDF/Text)"):
        st.text_area("التقرير الرسمي", f"""
        تقرير دوري: مشرف تنمية العلاقات المجتمعية
        التاريخ: {datetime.now().date()}
        ------------------------------------------
        1. ملخص الإنجاز: تم تنفيذ {len(inits)} مبادرة.
        2. حالة أولياء الأمور: يوجد {len(load_data('parents'))} ولي أمر مسجل.
        3. التوصيات: الاستمرار في تعزيز التواصل الرقمي.
        ------------------------------------------
        يعتمد هذا التقرير آلياً بناءً على قاعدة بيانات النظام.
        """)
