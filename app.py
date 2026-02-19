import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. إعدادات الصفحة والتنسيق
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stTextArea textarea, .stTextInput input { text-align: right; direction: RTL; }
    .dua-card { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-right: 5px solid #ffcc00; margin-bottom: 10px; }
    .chat-card { background-color: #262730; padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 5px solid #00ffa2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 رمضان يجمعنا - سوهاج")

# 2. المعرفات والروابط المستقرة (التي لا تسبب أخطاء)
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdD0jIvIAxD7MVu9xypZG_tXESCfF89UVwJB585Tuu7qnBeUQ/viewform?embedded=true"

# روابط القراءة المباشرة (حل مشكلة HTTPError)
KHATMA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=khatma"
DUA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=dua"
CHAT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=chat"

# إنشاء الاتصال للكتابة فقط
conn = st.connection("gsheets", type=GSheetsConnection)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📖 الختمة", "✅ التحدي", "🤲 دفتر الأدعية", "💬 الدردشة", "🕌 الإمساكية"])

# --- قسم الختمة ---
with tab1:
    st.components.v1.iframe(FORM_URL, height=500)
    st.divider()
    if st.button("تحديث اللوحة 🔄", key="ref_khatma"): st.rerun()
    try:
        df = pd.read_csv(KHATMA_URL)
        st.dataframe(df.iloc[:, 1:], use_container_width=True, hide_index=True)
    except: st.info("سجل إنجازك ليظهر هنا.")

# --- قسم الأدعية ---
with tab3:
    st.subheader("🤲 دفتر الأدعية")
    with st.form("dua_form", clear_on_submit=True):
        d_name = st.text_input("اسمك:")
        d_text = st.text_area("الدعاء:")
        if st.form_submit_button("حفظ في الدفتر ✍️"):
            if d_name and d_text:
                # نستخدم الاتصال فقط عند الحاجة للكتابة
                existing = conn.read(spreadsheet=SHEET_ID, worksheet="dua")
                new_row = pd.DataFrame([{"الاسم": d_name, "الدعاء": d_text}])
                updated = pd.concat([existing, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_ID, worksheet="dua", data=updated)
                st.success("تم الحفظ!")
                st.rerun()
    st.divider()
    try:
        # القراءة عبر CSV تضمن عدم ظهور الخطأ الأحمر أبداً
        dua_df = pd.read_csv(DUA_URL)
        for i, row in dua_df.iloc[::-1].iterrows():
            st.markdown(f"<div class='dua-card'><b>{row['الاسم']}</b>: {row['الدعاء']}</div>", unsafe_allow_html=True)
    except: st.write("لا يوجد أدعية حالياً.")

# --- قسم الدردشة ---
with tab4:
    st.subheader("💬 مناقشات الأصدقاء")
    with st.form("chat_form", clear_on_submit=True):
        c_name = st.text_input("اسمك:", key="cname")
        c_msg = st.text_input("الرسالة:")
        if st.form_submit_button("إرسال 🚀"):
            if c_name and c_msg:
                existing_chat = conn.read(spreadsheet=SHEET_ID, worksheet="chat")
                new_msg = pd.DataFrame([{"الاسم": c_name, "الرسالة": c_msg}])
                updated_chat = pd.concat([existing_chat, new_msg], ignore_index=True)
                conn.update(spreadsheet=SHEET_ID, worksheet="chat", data=updated_chat)
                st.rerun()
    st.divider()
    try:
        chat_df = pd.read_csv(CHAT_URL)
        for i, row in chat_df.iloc[::-1].head(20).iterrows():
            st.markdown(f"<div class='chat-card'><b>{row['الاسم']}</b>: {row['الرسالة']}</div>", unsafe_allow_html=True)
    except: st.write("ابدأ الدردشة الآن.")

with tab5:
    st.info("📍 سوهاج | الفجر: 04:42 - المغرب: 06:05")
