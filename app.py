import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان يجمعنا", page_icon="🌙", layout="centered")

# 2. تحسين الـ CSS (التنسيق الجمالي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخط العام والاتجاه */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: RTL;
    }

    /* تنسيق التابس (الألسنة) لتصبح كأزرار أنيقة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 15px;
        gap: 0px;
        padding: 10px 20px;
        color: #2e3b4e;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* تأثير عند الوقوف بالماوس أو الاختيار */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e2e6ea;
        border-color: #1f77b4;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        transform: translateY(-2px);
    }

    /* تنسيق الكروت */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* زر التسجيل */
    .stLinkButton a {
        background: linear-gradient(45deg, #28a745, #218838) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي بشكل جذاب
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🌙 تطبيق رمضان المتكامل</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>خيرُ الأعمال أدومها وإن قلّ</p>", unsafe_allow_html=True)
st.divider()

# 3. إنشاء الأقسام (الألسنة) بأيقونات واضحة
tab1, tab2, tab3, tab4 = st.tabs(["📖 الختمة", "✅ التحدي", "🤲 الأدعية", "🕌 الإمساكية"])

# --- القسم الأول: متابعة الختمة ---
with tab1:
    st.markdown("### 📖 سجل ختمتك مع أصدقائك")
    SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
    CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    
    try:
        df = pd.read_csv(CSV_URL)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("💡 بانتظار تسجيل البيانات من ملف الـ Google Sheets...")
    
    st.link_button("✍️ سجل إنجازك في الشيت هنا", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")

# --- القسم الثاني: تحدي الطاعات ---
with tab2:
    st.markdown("### ✅ قائمة الطاعات اليومية")
    col1, col2 = st.columns(2)
    tasks = ["الصلوات الخمس", "صلاة التراويح", "أذكار الصباح والمساء", "ورد القرآن", "صدقة اليوم", "صلة رحم"]
    
    for i, task in enumerate(tasks):
        if i % 2 == 0:
            col1.checkbox(task, key=task)
        else:
            col2.checkbox(task, key=task)
            
    st.button("حفظ التقدم اليومي", use_container_width=True)

# --- القسم الثالث: دفتر الأدعية ---
with tab3:
    st.markdown("### 🤲 مساحة الأدعية المشتركة")
    with st.container(border=True):
        dua_input = st.text_area("اكتب دعاءً ليؤمن عليه أصدقاؤك:", placeholder="اللهم انك عفو كريم تحب العفو فاعف عنا...")
        if st.button("نشر الدعاء 🚀"):
            st.balloons()
            st.success("تم النشر بنجاح!")
    
    st.info("💡 'ما من مسلم يدعو بدعوة ليس فيها إثم ولا قطيعة رحم إلا أعطاه الله بها إحدى ثلاث...'")

# --- القسم الرابع: الإمساكية ---
with tab4:
    st.markdown("### 🕌 مواعيد الصلاة (القاهرة)")
    data = {
        "اليوم": ["1 رمضان", "2 رمضان", "3 رمضان", "4 رمضان"],
        "الإمساك": ["04:30", "04:29", "04:28", "04:27"],
        "الفجر": ["04:40", "04:39", "04:38", "04:37"],
        "المغرب": ["18:05", "18:06", "18:07", "18:08"]
    }
    st.table(pd.DataFrame(data))

# تذييل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em;'>صنع بكل حب في رمضان ✨</p>", unsafe_allow_html=True)
