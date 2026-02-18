import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

# 2. تحسين المظهر ودعم اللغة العربية (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    iframe { border-radius: 15px; border: 2px solid #ffcc00; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #262730; border-radius: 10px; color: white; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المتكامل | سوهاج")

# 3. الروابط (تم تحديثها بناءً على بياناتك)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdD0jIvIAxD7MVu9xypZG_tXESCfF89UVwJB585Tuu7qnBeUQ/viewform?embedded=true"
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
# رابط القراءة المباشر من ورقة khatma
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=khatma"

# 4. إنشاء الأقسام (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📖 متابعة الختمة", "✅ تحدي اليوم", "🤲 دفتر الأدعية", "🕌 الإمساكية"])

# --- القسم الأول: الختمة ---
with tab1:
    st.subheader("✍️ سجل إنجازك اليوم")
    # عرض نموذج جوجل للإدخال من داخل التطبيق
    st.components.v1.iframe(FORM_URL, height=550, scrolling=True)
    
    st.divider()
    st.subheader("🏆 لوحة شرف الأصدقاء")
    
    if st.button("تحديث البيانات 🔄"):
        st.cache_data.clear()
        st.rerun()

    try:
        # قراءة البيانات مباشرة من ورقة khatma
        df = pd.read_csv(DATA_URL)
        # تنظيف البيانات (عرض الأعمدة المهمة فقط)
        if not df.empty:
            # نختار الأعمدة حسب ترتيبها في الشيت (الاسم ورقم الجزء)
            display_df = df.iloc[:, [2, 3]] # تخطي الطابع الزمني والبريد
            display_df.columns = ["الاسم", "رقم الجزء"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("في انتظار أول بطل يسجل إنجازه!")
    except Exception as e:
        st.warning("البيانات قيد المزامنة.. سجل إنجازك بالأعلى وسيظهر هنا فوراً.")

# --- الأقسام الأخرى ---
with tab2:
    st.subheader("✅ قائمة الطاعات اليومية")
    st.checkbox("الصلوات الخمس في المسجد")
    st.checkbox("صلاة التراويح")
    st.checkbox("ورد القرآن اليومي")

with tab3:
    st.subheader("🤲 مساحة الأدعية المشتركة")
    st.text_area("اكتب دعاءً ليؤمن عليه أصدقاؤك:")
    st.button("نشر")

with tab4:
    st.subheader("🕌 مواعيد الصلاة - سوهاج")
    st.info("الفجر: 04:42 | المغرب: 06:05")
