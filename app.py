import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# تحسين الخط والتصميم للعربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    [data-testid="sidebarNavView"] { display: none; }
    .stDataFrame { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    # الاتصال بجوجل شيت
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL, worksheet="khatma")
    
    # التأكد من جاهزية الجدول
    if df is None or df.empty:
        df = pd.DataFrame(columns=['Name', 'Part'])

    # نموذج تسجيل البيانات
    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("add_record", clear_on_submit=True):
        u_name = st.text_input("اسمك الكريم:")
        u_part = st.number_input("الجزء الذي وصلته:", min_value=1, max_value=30, step=1)
        if st.form_submit_button("تحديث إنجازي"):
            if u_name:
                # إضافة السطر الجديد
                new_data = pd.DataFrame([{"Name": u_name, "Part": u_part}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                # رفع للبيانات
                conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
                st.success(f"تقبل الله منك يا {u_name}!")
                st.balloons()
                st.rerun()
            else:
                st.warning("يرجى كتابة الاسم")

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    # عرض الجدول بشكل أنيق
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.info("بانتظار تسجيل أول اسم في القائمة...")
    # زر طوارئ لإنشاء الأعمدة إذا اختفت
    if st.button("تهيئة الجدول لأول مرة"):
        init_df = pd.DataFrame(columns=['Name', 'Part'])
        conn.update(spreadsheet=URL, worksheet="khatma", data=init_df)
        st.rerun()
