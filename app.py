import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="رمضان في سوهاج", page_icon="🌙", layout="wide")

# 2. تصميم الواجهة ودعم اللغة العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    iframe { border-radius: 15px; border: 2px solid #ffcc00; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #262730; border-radius: 10px; color: white; padding: 8px 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 تطبيق رمضان المتكامل | سوهاج")

# 3. الروابط الخاصة بك (تم تحديثها برابط النشر الجديد)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdD0jIvIAxD7MVu9xypZG_tXESCfF89UVwJB585Tuu7qnBeUQ/viewform?embedded=true"
SHEET_ID = "1ZO143By7FOmskmGri9d5N24V4WiE0P7SOoUmY27-Cu4"
# رابط استخراج البيانات كـ CSV من ورقة khatma مباشرة
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=khatma"

# 4. إنشاء الأقسام
tab1, tab2, tab3, tab4 = st.tabs(["📖 متابعة الختمة", "✅ تحدي اليوم", "🤲 دفتر الأدعية", "🕌 الإمساكية"])

# --- القسم الأول: الختمة ---
with tab1:
    st.subheader("✍️ سجل إنجازك الآن")
    # عرض النموذج داخل التطبيق
    st.components.v1.iframe(FORM_URL, height=550, scrolling=True)
    
    st.divider()
    st.subheader("🏆 لوحة الأصدقاء")
    
    if st.button("تحديث الجدول 🔄"):
        st.cache_data.clear()
        st.rerun()
        
    try:
        # قراءة البيانات مباشرة
        df = pd.read_csv(DATA_URL)
        if not df.empty:
            # عرض أعمدة الاسم ورقم الجزء (نتخطى عمود الوقت)
            st.dataframe(df.iloc[:, 1:], use_container_width=True, hide_index=True)
        else:
            st.info("سجل أول إنجاز ليظهر الجدول هنا.")
    except:
        st.warning("البيانات تظهر فور تسجيل أول إنجاز في النموذج أعلاه.")

# --- بقية الأقسام ---
with tab2:
    st.subheader("✅ تحدي الطاعات اليومي")
    st.checkbox("صلوات الجماعة")
    st.checkbox("ورد القرآن")
    st.checkbox("أذكار الصباح والمساء")

with tab3:
    st.subheader("🤲 مساحة الأدعية المشتركة")
    st.text_area("اكتب دعاءً لأصحابك:")
    if st.button("نشر"):
        st.success("اللهم تقبل!")

with tab4:
    st.subheader("🕌 مواعيد الصلاة - سوهاج")
    st.info("الفجر: 04:42 | المغرب: 06:05")
    st.write("تقبل الله منا ومنكم.")
