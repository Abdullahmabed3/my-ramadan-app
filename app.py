import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

# تصميم الأقسام (Tabs) بشكل أنيق
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #262730; border-radius: 10px; color: white; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 رمضان في سوهاج")
st.write("أهلاً بك في تطبيقك الرمضاني المتكامل")

# إنشاء الأقسام
tab1, tab2, tab3, tab4 = st.tabs(["📖 الختمة", "✅ تحدي اليوم", "🤲 الأدعية", "🕌 إمساكية"])

# --- القسم الأول: متابعة الختمة (التسجيل داخلي) ---
with tab1:
    st.subheader("📖 سجل ختمتك مع أصحابك")
    
    URL = "https://docs.google.com/spreadsheets/d/1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4/edit"
    
    try:
        # اتصال مباشر مع تصفير الذاكرة لضمان التحديث اللحظي
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL, worksheet="khatma", ttl=0)
        
        # نموذج الإدخال داخل التطبيق
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                u_name = st.text_input("الاسم:")
            with col2:
                u_part = st.number_input("الجزء:", min_value=1, max_value=30, step=1)
            
            submit = st.form_submit_button("إرسال الإنجاز داخل التطبيق")
            
            if submit and u_name:
                new_data = pd.DataFrame([{"Name": u_name, "Part": u_part}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(spreadsheet=URL, worksheet="khatma", data=updated_df)
                st.success(f"تم تسجيل إنجازك يا {u_name} بنجاح!")
                st.balloons()
                st.rerun()

        st.divider()
        st.write("📊 لوحة الإنجاز الحالية:")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.warning("حدث اتصال بالقاعدة.. تأكد أنك لم تغير اسم الورقة من 'khatma'")

# --- بقية الأقسام (تحدي، أدعية، إمساكية) ---
with tab2:
    st.subheader("✅ تحدي الطاعات اليومي")
    st.checkbox("صلوات الجماعة")
    st.checkbox("السنن الرواتب")
    st.checkbox("أذكار المساء")

with tab3:
    st.subheader("🤲 مساحة الأدعية المشتركة")
    st.text_area("اكتب دعاءً:")
    st.button("انشر الدعاء")

with tab4:
    st.subheader("🕌 مواعيد الصلاة - سوهاج")
    st.info("الفجر: 04:45 | المغرب: 06:10 (تقديري)")
