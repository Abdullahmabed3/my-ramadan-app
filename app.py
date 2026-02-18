import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# تحسين التصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    [data-testid="sidebarNavView"] { display: none; }
    .stDataFrame { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت المباشر
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    # إنشاء اتصال جديد مع تعطيل الذاكرة المؤقتة (ttl=0) لضمان قراءة التعديلات الجديدة
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL, worksheet="khatma", ttl=0)
    
    # التأكد من وجود الأعمدة
    if df is None or df.empty or 'Name' not in df.columns:
        df = pd.DataFrame(columns=['Name', 'Part'])

    # نموذج تسجيل البيانات
    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("main_form", clear_on_submit=True):
        u_name = st.text_input("اسمك الكريم:")
        u_part = st.number_input("الجزء الحالي:", min_value=1, max_value=30, step=1)
        if st.form_submit_button("تحديث إنجازي"):
            if u_name:
                new_row = pd.DataFrame([{"Name": u_name, "Part": u_part}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                # رفع البيانات للشيت
                conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
                st.success(f"تقبل الله منك يا {u_name}!")
                st.balloons()
                st.rerun()
            else:
                st.warning("يرجى كتابة الاسم")

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    st.dataframe(df[['Name', 'Part']], use_container_width=True, hide_index=True)

except Exception as e:
    st.info("بانتظار تفعيل الاتصال النهائي...")
    # زر الإصلاح السريع
    if st.button("تفعيل الجدول الآن"):
        try:
            # كتابة الأعمدة الأساسية مباشرة في الشيت
            initial_df = pd.DataFrame(columns=['Name', 'Part'])
            conn.update(spreadsheet=URL, worksheet="khatma", data=initial_df)
            st.success("تم التفعيل! يرجى إعادة تحميل الصفحة.")
            st.rerun()
        except:
            st.error("تأكد من أن رابط جوجل شيت مضبوط على Editor")
