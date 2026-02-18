import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="رمضان يجمعنا", page_icon="🌙", layout="wide")

# تصميم الألوان والخطوط (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المتكامل")

# إنشاء الأقسام (الألسنة)
tab1, tab2, tab3, tab4 = st.tabs(["📖 متابعة الختمة", "✅ تحدي الطاعات", "🤲 دفتر الأدعية", "🕌 الإمساكية"])

# --- القسم الأول: متابعة الختمة ---
with tab1:
    st.header("سجل ختمتك مع أصدقائك")
    SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    
    try:
        df = pd.read_csv(CSV_URL)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("بانتظار تسجيل البيانات...")
    
    st.link_button("✍️ سجل إنجازك في الشيت هنا", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

# --- القسم الثاني: تحدي الطاعات ---
with tab2:
    st.header("قائمة الطاعات اليومية")
    tasks = ["الصلوات الخمس", "صلاة التراويح", "أذكار الصباح والمساء", "ورد القرآن", "صدقة اليوم"]
    for task in tasks:
        st.checkbox(task)
    st.button("حفظ التقدم")

# --- القسم الثالث: دفتر الأدعية ---
with tab3:
    st.header("مساحة الأدعية المشتركة")
    dua_input = st.text_area("اكتب دعاءً ليؤمن عليه أصدقاؤك:")
    if st.button("نشر الدعاء"):
        st.success("تم النشر (سيتم الحفظ في التحديث القادم)")
    
    st.info("اللهم بلغنا رمضان وأنت راضٍ عنا..")

# --- القسم الرابع: الإمساكية ---
with tab4:
    st.header("مواعيد الصلاة (القاهرة)")
    # يمكنك وضع صورة إمساكية مدينتك هنا أو جدول ثابت
    data = {
        "اليوم": ["1 رمضان", "2 رمضان", "3 رمضان"],
        "الإمساك": ["04:30", "04:29", "04:28"],
        "الفجر": ["04:40", "04:39", "04:38"],
        "المغرب": ["18:05", "18:06", "18:07"]
    }
    st.table(pd.DataFrame(data))

