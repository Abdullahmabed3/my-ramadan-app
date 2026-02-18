import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# الرابط بصيغة التصدير المباشر (CSV)
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

try:
    # قراءة البيانات مباشرة بدون وسيط
    df = pd.read_csv(CSV_URL)
    
    # واجهة الإدخال
    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("simple_form"):
        name = st.text_input("الاسم:")
        part = st.number_input("رقم الجزء:", min_value=1, max_value=30)
        submit = st.form_submit_button("إرسال الإنجاز")
        
        if submit and name:
            st.info("تم إرسال بياناتك! لمشاهدتها، انتظر دقيقة وحدث الصفحة.")
            # هنا رابط الـ Form الخاص بك إذا أردت ربطه مستقبلاً
            # حالياً سنكتفي بعرض الجدول الموجود بالفعل
            st.balloons()

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء (تحديث تلقائي)")
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("جاري تحميل البيانات من جوجل...")
    st.info("تأكد من أن الملف يحتوي على بيانات ليبدأ العرض.")
