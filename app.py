import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# تصميم يدعم العربية ويمنع تداخل الحروف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    [data-testid="sidebarNavView"] { display: none; }
    .stTable { direction: RTL; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # محاولة قراءة البيانات
    try:
        df = conn.read(spreadsheet=URL, worksheet="khatma")
    except:
        df = pd.DataFrame()

    # خطوة ذكية: إذا كان الجدول فارغاً أو الأعمدة غير صحيحة، ننشئ أعمدة جديدة
    if df.empty or 'Name' not in df.columns:
        df = pd.DataFrame(columns=['Name', 'Part'])
        # تحديث الشيت بالعناوين الصحيحة فوراً
        conn.update(spreadsheet=URL, worksheet="khatma", data=df)

    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("my_form", clear_on_submit=True):
        name = st.text_input("اسمك:")
        part = st.number_input("وصلت للجزء رقم:", min_value=1, max_value=30, step=1)
        submit = st.form_submit_button("تحديث الإنجاز")
        
        if submit and name:
            # إضافة السطر الجديد
            new_entry = pd.DataFrame([{"Name": name, "Part": part}])
            df = pd.concat([df, new_entry], ignore_index=True)
            
            # رفع البيانات للشيت
            conn.update(spreadsheet=URL, worksheet="khatma", data=df)
            st.success(f"تم التسجيل بنجاح يا {name}!")
            st.balloons()
            st.rerun()

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    if not df.empty:
        # عرض الجدول بشكل مبسط وجميل
        st.dataframe(df[['Name', 'Part']], use_container_width=True, hide_index=True)
    else:
        st.info("الجدول فارغ حالياً، كن أول من يسجل إنجازه!")

except Exception as e:
    st.error("جاري تهيئة الاتصال... يرجى تحديث الصفحة بعد ثوانٍ.")
