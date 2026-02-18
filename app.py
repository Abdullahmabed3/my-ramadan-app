import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الموبايل
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# تحسين الخطوط والعربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    [data-testid="sidebarNavView"] { display: none; }
    .stTable { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت الخاص بك مباشرة
url = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, worksheet="khatma")

    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("my_form"):
        name = st.text_input("اسمك:")
        part = st.number_input("وصلت للجزء رقم:", min_value=1, max_value=30)
        submit = st.form_submit_button("تحديث الإنجاز")
        
        if submit and name:
            new_entry = pd.DataFrame([{"Name": name, "Part": part}])
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(spreadsheet=url, worksheet="khatma", data=updated_df)
            st.success(f"تم التسجيل بنجاح يا {name}!")
            st.rerun()

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    if not df.empty:
        st.table(df)
    else:
        st.info("لا توجد بيانات مسجلة بعد. كن أول من يسجل!")

except Exception as e:
    st.error("⚠️ فشل الاتصال التلقائي.")
    st.info("تأكد أن الملف في جوجل شيت يحتوي على أعمدة Name و Part في الصف الأول.")
