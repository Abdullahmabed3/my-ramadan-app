import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

# 2. لمسات التصميم (العربية RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stTextArea textarea, .stTextInput input { text-align: right; direction: RTL; }
    .dua-card { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-right: 5px solid #ffcc00; margin-bottom: 10px; }
    .chat-card { background-color: #262730; padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 5px solid #00ffa2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المتكامل | سوهاج")

# 3. الروابط والمعرفات
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdD0jIvIAxD7MVu9xypZG_tXESCfF89UVwJB585Tuu7qnBeUQ/viewform?embedded=true"

# إنشاء الاتصال بالجداول
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. الأقسام (Tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📖 الختمة", "✅ التحدي", "🤲 دفتر الأدعية", "💬 الدردشة", "🕌 الإمساكية"])

# --- 1. قسم الختمة ---
with tab1:
    st.components.v1.iframe(FORM_URL, height=500, scrolling=True)
    st.divider()
    if st.button("تحديث لوحة الأصدقاء 🔄"): st.rerun()
    try:
        df_khatma = conn.read(spreadsheet=SHEET_ID, worksheet="khatma")
        st.dataframe(df_khatma.iloc[:, 1:], use_container_width=True, hide_index=True)
    except: st.info("في انتظار أول بطل!")

# --- 2. تحدي الطاعات ---
with tab2:
    st.subheader("✅ مهامك اليومية")
    st.checkbox("الصلوات الخمس في المسجد")
    st.checkbox("ورد القرآن الكريم")
    st.checkbox("صلاة التراويح")

# --- 3. دفتر الأدعية (الحفظ المستمر) ---
with tab3:
    st.subheader("🤲 اكتب دعاءً ليؤمن عليه الجميع")
    with st.form("dua_form", clear_on_submit=True):
        name = st.text_input("اسمك:")
        text = st.text_area("الدعاء:")
        if st.form_submit_button("حفظ في الدفتر ✍️"):
            if name and text:
                old_data = conn.read(spreadsheet=SHEET_ID, worksheet="dua")
                new_row = pd.DataFrame([{"الاسم": name, "الدعاء": text}])
                updated_df = pd.concat([old_data, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_ID, worksheet="dua", data=updated_df)
                st.success("تم تسجيل دعائك!")
                st.rerun()

    st.divider()
    try:
        dua_list = conn.read(spreadsheet=SHEET_ID, worksheet="dua")
        for i, row in dua_list.iloc[::-1].iterrows(): # عرض الأحدث أولاً
            st.markdown(f"<div class='dua-card'><b>{row['الاسم']}</b>: {row['الدعاء']}</div>", unsafe_allow_True=True)
    except: st.write("كن أول من يكتب دعاءً.")

# --- 4. الدردشة والمناقشة ---
with tab4:
    st.subheader("💬 دردشة أصدقاء سوهاج")
    with st.form("chat_form", clear_on_submit=True):
        u_name = st.text_input("الاسم:")
        u_msg = st.text_input("الرسالة:")
        if st.form_submit_button("إرسال 🚀"):
            if u_name and u_msg:
                old_chat = conn.read(spreadsheet=SHEET_ID, worksheet="chat")
                new_chat = pd.DataFrame([{"الاسم": u_name, "الرسالة": u_msg}])
                updated_chat = pd.concat([old_chat, new_chat], ignore_index=True)
                conn.update(spreadsheet=SHEET_ID, worksheet="chat", data=updated_chat)
                st.rerun()
    
    st.divider()
    try:
        chat_data = conn.read(spreadsheet=SHEET_ID, worksheet="chat")
        for i, row in chat_data.iloc[::-1].head(20).iterrows(): # عرض آخر 20 رسالة
            st.markdown(f"<div class='chat-card'><b>{row['الاسم']}</b>: {row['الرسالة']}</div>", unsafe_allow_True=True)
    except: st.write("ابدأ الدردشة الآن!")

# --- 5. الإمساكية ---
with tab5:
    st.info("📍 توقيت سوهاج | الفجر: 04:42 - المغرب: 06:05")
    st.success("رمضان كريم عليكم جميعاً!")
