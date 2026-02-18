import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الموبايل وإخفاء القائمة الجانبية
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# إصلاح التصميم للعربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    [data-testid="sidebarNavView"] { display: none; }
    .stTable { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # قراءة البيانات مع تحديد اسم الورقة
    df = conn.read(spreadsheet=URL, worksheet="khatma")
    
    # تأكد من أن الأعمدة موجودة، وإذا لم تكن، أضفها
    if df.empty or 'Name' not in df.columns:
        df = pd.DataFrame(columns=['Name', 'Part'])

    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("my_form"):
        name = st.text_input("اسمك:")
        part = st.number_input("وصلت للجزء رقم:", min_value=1, max_value=30)
        submit = st.form_submit_button("تحديث الإنجاز")
        
        if submit and name:
            # إنشاء سطر جديد متوافق تماماً مع أعمدة الجدول
            new_entry = pd.DataFrame([{"Name": name, "Part": part}])
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            
            # رفع التحديث لجوجل شيت
            conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
            st.success(f"كفو يا {name}! تم التحديث.")
            st.rerun()

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    # عرض الجدول بشكل نظيف
    st.table(df)

except Exception as e:
    st.error("⚠️ لم نتمكن من عرض الجدول بعد.")
    st.info("تأكد من عدم وجود مسافات زائدة في أسماء الأعمدة في ملف جوجل شيت.")
