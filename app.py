import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

# تحسين التصميم للعربية (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    iframe { border-radius: 15px; border: 2px solid #ffcc00; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #262730; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المتكامل | سوهاج")

# الروابط الخاصة بك
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdD0jIvIAxD7MVu9xypZG_tXESCfF89UVwJB585Tuu7qnBeUQ/viewform?embedded=true"
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
# رابط استخراج البيانات كـ CSV (تم تعديله ليقرأ من الشيت الصحيح)
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# إنشاء الأقسام
tab1, tab2, tab3, tab4 = st.tabs(["📖 متابعة الختمة", "✅ تحدي الطاعات", "🤲 دفتر الأدعية", "🕌 الإمساكية"])

# --- 1. قسم الختمة ---
with tab1:
    st.subheader("✍️ سجل إنجازك الآن")
    # عرض النموذج داخل التطبيق مباشرة
    st.components.v1.iframe(FORM_URL, height=550, scrolling=True)
    
    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    if st.button("تحديث الجدول 🔄"):
        st.rerun()
        
    try:
        # قراءة البيانات
        df = pd.read_csv(DATA_URL)
        # عرض البيانات (سيظهر الأعمدة التي أنشأها النموذج تلقائياً)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("سجل أول إنجاز عبر النموذج أعلاه ليظهر الجدول هنا.")

# --- 2. تحدي الطاعات ---
with tab2:
    st.subheader("✅ مهامك الرمضانية اليومية")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("الصلوات الخمس في المسجد")
        st.checkbox("صلاة التراويح")
    with col2:
        st.checkbox("ورد القرآن اليومي")
        st.checkbox("أذكار الصباح والمساء")

# --- 3. دفتر الأدعية ---
with tab3:
    st.subheader("🤲 دعاء اليوم")
    st.text_area("اكتب دعاءً ليشاركك أصدقاؤك التأمين عليه:")
    if st.button("نشر"):
        st.success("اللهم تقبل!")

# --- 4. الإمساكية ---
with tab4:
    st.subheader("🕌 مواعيد الصلاة - سوهاج")
    st.info("الفجر: 04:42 | المغرب: 06:05")
    st.write("تقبل الله منا ومنكم صالح الأعمال")
