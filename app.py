import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", initial_sidebar_state="collapsed")

# تصميم يدعم العربية
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
    # الاتصال المباشر
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL, worksheet="khatma")
    
    # التأكد من وجود الأعمدة
    if df.empty or 'Name' not in df.columns:
        df = pd.DataFrame(columns=['Name', 'Part'])

    # نموذج التسجيل
    with st.form("my_form", clear_on_submit=True):
        name = st.text_input("الاسم:")
        part = st.number_input("الجزء الحالي:", min_value=1, max_value=30, step=1)
        submit = st.form_submit_button("تحديث إنجازي")
        
        if submit and name:
            new_row = pd.DataFrame([{"Name": name, "Part": part}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
            st.success(f"تم التسجيل يا {name}!")
            st.rerun()

    st.divider()
    st.subheader("🏆 لوحة الإنجاز")
    # عرض الجدول
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("يرجى التأكد من كتابة Name و Part في أول صف في Google Sheets")
    # عرض جدول فارغ لكي لا تتوقف الصفحة
    st.table(pd.DataFrame(columns=['Name', 'Part']))
