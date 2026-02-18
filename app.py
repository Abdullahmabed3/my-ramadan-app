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
    .stSuccess { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# رابط الشيت الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    # الاتصال بجوجل شيت
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL, worksheet="khatma")
    
    # التأكد من جاهزية الأعمدة (إذا كان الملف فارغاً تماماً)
    if df is None or df.empty or 'Name' not in df.columns:
        df = pd.DataFrame(columns=['Name', 'Part'])

    # نموذج تسجيل البيانات
    st.subheader("📖 سجل إنجازك اليوم")
    with st.form("add_record", clear_on_submit=True):
        u_name = st.text_input("اسمك الكريم:")
        u_part = st.number_input("الجزء الذي وصلته:", min_value=1, max_value=30, step=1)
        submit_btn = st.form_submit_button("تحديث إنجازي")
        
        if submit_btn:
            if u_name:
                # إضافة السطر الجديد
                new_data = pd.DataFrame([{"Name": u_name, "Part": u_part}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                # رفع البيانات للشيت
                conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
                st.success(f"تقبل الله منك يا {u_name}!")
                st.balloons()
                st.rerun()
            else:
                st.warning("يرجى كتابة الاسم أولاً")

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    # عرض الجدول بشكل أنيق
    if not df.empty and 'Name' in df.columns:
        st.dataframe(df[['Name', 'Part']], use_container_width=True, hide_index=True)
    else:
        st.info("القائمة فارغة، كن أول من يسجل!")

except Exception as e:
    st.warning("⚠️ التطبيق يحتاج لتهيئة سريعة للاتصال.")
    if st.button("اضغط هنا لتفعيل الجدول الآن"):
        try:
            # إنشاء جدول تجريبي لفتح القناة بين التطبيق والشيت
            init_df = pd.DataFrame([["بداية الخير", 1]], columns=['Name', 'Part'])
            conn.update(spreadsheet=URL, worksheet="khatma", data=init_df)
            st.success("تم التفعيل بنجاح! الصفحة ستحدث الآن.")
            st.rerun()
        except Exception as err:
            st.error(f"تأكد من حفظ إعدادات Editor في جوجل شيت.")
