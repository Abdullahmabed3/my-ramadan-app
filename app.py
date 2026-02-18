import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات تجعل التطبيق يبدو احترافياً على الموبايل
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# كود سحري لإصلاح شكل الحروف والعربية ومنع التداخل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    /* إخفاء القائمة الجانبية افتراضياً لتوسيع المساحة */
    [data-testid="sidebarNavView"] { display: none; }
    .stTable { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

try:
    # الاتصال بقاعدة البيانات
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # محاولة القراءة
    df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit", worksheet="khatma")

        if submit and name:
            # إضافة البيانات الجديدة
            new_data = pd.DataFrame([{"Name": name, "Part": part}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="khatma", data=updated_df)
            st.success("تم التحديث بنجاح!")
            st.rerun()

    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    st.table(df)

except Exception as e:
    st.error("⚠️ خطأ في الاتصال بملف جوجل شيت")
    st.info("تأكد من عمل 'Share' للملف بوضع 'Editor' والتأكد من الرابط في Secrets.")
    # بيانات وهمية حتى لا تظل الصفحة فارغة
    st.table(pd.DataFrame({"الاسم": ["مثال"], "الجزء": [1]}))
