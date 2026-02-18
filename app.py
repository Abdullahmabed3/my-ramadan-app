import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stDataFrame { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# معرف الشيت الخاص بك
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# --- الجزء الأول: عرض البيانات ---
try:
    # قراءة البيانات مباشرة
    df = pd.read_csv(CSV_URL)
    
    st.subheader("📖 سجل إنجازك اليوم")
    
    # --- الجزء الثاني: إرسال البيانات (عبر رابط مباشر لضمان عدم التعليق) ---
    st.info("لتسجيل جزء جديد، اضغط على الزر أدناه ليفتح لك ملف الإنجاز:")
    st.link_button("✍️ اضغط هنا لتسجيل إنجازك", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    
    st.divider()
    
    # --- الجزء الثالث: لوحة الشرف ---
    st.subheader("🏆 لوحة الأصدقاء")
    if not df.empty:
        # عرض الجدول بتنسيق جميل
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("لا توجد بيانات حالياً.")

except Exception as e:
    st.error("جاري الاتصال بقاعدة البيانات...")
