import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المشترك")

# الرابط الخاص بك
URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"

try:
    # استخدام ttl=0 لإجبار النظام على تحديث الصلاحيات فوراً
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL, worksheet="khatma", ttl=0)
    
    # واجهة الإدخال
    with st.form("main_form"):
        name = st.text_input("الاسم:")
        part = st.number_input("الجزء:", min_value=1, max_value=30)
        submit = st.form_submit_button("تسجيل الإنجاز")
        
        if submit and name:
            new_data = pd.DataFrame([{"Name": name, "Part": part}])
            # محاولة التحديث المباشر
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
            st.success("تم التسجيل!")
            st.rerun()

    st.divider()
    st.table(df)

except Exception as e:
    st.error("جاري مزامنة الصلاحيات مع جوجل...")
    st.info("إذا كنت متأكداً من تفعيل Editor، فقط انتظر دقيقة واحدة وحدث الصفحة.")
    # محاولة كتابة أول سطر يدوياً لكسر الجمود
    if st.button("تفعيل الرابط الآن"):
        test_df = pd.DataFrame([{"Name": "بداية", "Part": 0}])
        conn.update(spreadsheet=URL, worksheet="khatma", data=test_df)
        st.rerun()
