import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان يجمعنا - سوهاج", page_icon="🌙", layout="centered")

# 2. تصميم CSS متطور (خلفية متحركة وتنسيق تابس)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* جعل الخلفية داكنة مع تأثير النجوم */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        color: white;
    }

    /* تأثير النجوم المتحركة */
    body::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        z-index: -1;
        animation: stars 100s linear infinite;
    }

    @keyframes stars {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }

    /* تنسيق الخطوط والاتجاه */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: RTL;
    }

    /* تحويل التابس إلى أزرار ذهبية احترافية */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px 20px;
        color: #e0e0e0;
        border: 1px solid rgba(255, 215, 0, 0.2);
        transition: all 0.4s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #D4AF37 100%) !important;
        color: #1b2735 !important;
        font-weight: bold !important;
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }

    /* تنسيق الجداول لتناسب الوضع الليلي */
    .stTable, div[data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    h1, h2, h3 { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان الرئيسي
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 2.5em; margin-bottom: 0;'>🌙 رمضان في سوهاج</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #D4AF37; font-size: 1.2em;'>أهلاً بك في تطبيقك الرمضاني المتكامل</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 4. الأقسام (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📖 الختمة", "✅ تحدي اليوم", "🤲 الأدعية", "🕌 إمساكية سوهاج"])

# --- القسم الأول: متابعة الختمة ---
with tab1:
    st.markdown("### 📖 سجل ختمتك مع أصحابك")
    SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    
    try:
        df = pd.read_csv(CSV_URL)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("💡 جارِ مزامنة البيانات من الشيت...")
    
    st.link_button("✍️ اضغط هنا لتسجيل إنجازك", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit", use_container_width=True)

# --- القسم الثاني: تحدي الطاعات ---
with tab2:
    st.markdown("### ✅ تحدي الطاعات اليومي")
    col1, col2 = st.columns(2)
    tasks = ["الصلوات الخمس", "صلاة التراويح", "أذكار الصباح", "أذكار المساء", "ورد القرآن", "صدقة اليوم", "صلة رحم"]
    
    for i, task in enumerate(tasks):
        if i % 2 == 0:
            col1.checkbox(task, key=f"tk_{i}")
        else:
            col2.checkbox(task, key=f"tk_{i}")
            
    if st.button("حفظ التقدم ✨", use_container_width=True):
        st.balloons()
        st.toast("تقبل الله طاعتك يا بطل سوهاج! 🌟")

# --- القسم الثالث: دفتر الأدعية ---
with tab3:
    st.markdown("### 🤲 مساحة الدعاء المشتركة")
    with st.container():
        dua_input = st.text_area("أكتب دعاءك ليؤمن عليه الجميع:", placeholder="اللهم انك عفو تحب العفو فاعف عنا...")
        if st.button("نشر الدعاء 🚀", use_container_width=True):
            st.success("تم النشر بنجاح! اللهم استجب.")
    
    st.markdown("> **اللهم بلغنا ليلة القدر واجعلنا فيها من المقبولين**")

# --- القسم الرابع: الإمساكية (سوهاج) ---
with tab4:
    st.markdown("### 🕌 مواعيد الصلاة - محافظة سوهاج")
    
    sohag_times = {
        "اليوم": ["1 رمضان", "2 رمضان", "3 رمضان", "4 رمضان", "5 رمضان"],
        "الفجر": ["04:36", "04:35", "04:34", "04:33", "04:32"],
        "الظهر": ["12:02", "12:02", "12:02", "12:01", "12:01"],
        "المغرب": ["18:03", "18:04", "18:04", "18:05", "18:06"],
        "العشاء": ["19:20", "19:21", "19:21", "19:22", "19:23"]
    }
    
    st.table(pd.DataFrame(sohag_times))
    st.caption("🕒 التوقيتات حسب المركز الرئيسي لمحافظة سوهاج لعام 2026.")

# تذييل الصفحة
st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>رمضان كريم | سوهاج 2026</p>", unsafe_allow_html=True)
