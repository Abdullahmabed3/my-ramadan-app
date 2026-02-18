import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="روحانيات رمضان", page_icon="🌙", layout="centered")

# تحسين المظهر ودعم اللغة العربية (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: RTL; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; }
    .stTextInput>div>div>input { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# --- الاتصال بـ Google Sheets ---
# تأكد أنك وضعت الرابط في Secrets كما شرحنا في المرحلة الثالثة
conn = st.connection("gsheets", type=GSheetsConnection)

# --- القائمة الجانبية ---
st.sidebar.title("⭐ قائمة رمضان")
menu = ["🏠 الرئيسية", "📖 متابعة الختمة", "✅ تحدي الطاعات", "🤲 دفتر الأدعية", "⏳ الإمساكية"]
choice = st.sidebar.radio("انتقل إلى:", menu)

# --- 1. الصفحة الرئيسية ---
if choice == "🏠 الرئيسية":
    st.title("🌙 رمضان كريم")
    st.subheader("أهلاً بك يا صديقي في مساحتنا الروحانية")
    st.image("https://images.unsplash.com/photo-1511210103723-559639e7350c?q=80&w=800")
    st.info("💡 نصيحة اليوم: 'خيركم من تعلم القرآن وعلمه'.. اجعل لنفسك نصيباً من القراءة اليوم.")

# --- 2. متابعة الختمة ---
elif choice == "📖 متابعة الختمة":
    st.header("📖 متابعة الختمة المشتركة")
    
    # نموذج لإدخال البيانات
    with st.form("khatma_form"):
        name = st.text_input("اسمك:")
        part = st.number_input("وصلت للجزء رقم:", min_value=1, max_value=30)
        submit = st.form_submit_button("تحديث إنجازي")
        
        if submit:
            # هنا الكود يقرأ البيانات الحالية من جوجل شيت
            existing_data = conn.read(worksheet="khatma", usecols=[0,1,2])
            new_entry = pd.DataFrame([{"Name": name, "Part": part, "Date": datetime.now().strftime("%Y-%m-%d")}])
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            
            # تحديث الملف في جوجل شيت
            conn.update(worksheet="khatma", data=updated_df)
            st.success(f"بارك الله فيك يا {name}! تم تحديث إنجازك.")

    # عرض جدول الإنجازات
    st.write("### 🏆 لوحة إنجاز الأصدقاء")
    df = conn.read(worksheet="khatma")
    if not df.empty:
        st.table(df.tail(10)) # عرض آخر 10 تحديثات

# --- 3. تحدي الطاعات ---
elif choice == "✅ تحدي الطاعات":
    st.header("🏆 تحديات اليوم")
    st.write("أتممت اليوم:")
    
    c1 = st.checkbox("الصلوات الخمس في المسجد/وقتها")
    c2 = st.checkbox("صلاة التراويح")
    c3 = st.checkbox("ورد القرآن اليومي")
    c4 = st.checkbox("صدقة أو جبر خاطر")

    score = sum([c1, c2, c3, c4])
    st.progress(score / 4)
    if score == 4:
        st.balloons()
        st.success("ما شاء الله! يومك كامل الدسم بالحسنات.")

# --- 4. دفتر الأدعية ---
elif choice == "🤲 دفتر الأدعية":
    st.header("🤲 دعاء من القلب")
    with st.form("dua_form"):
        user_name = st.text_input("اسمك:")
        dua_text = st.text_area("اكتب دعاءً لنا وللمسلمين:")
        post_dua = st.form_submit_button("انشر الدعاء")
        
        if post_dua:
            st.warning("تم إرسال دعائك.. جزاك الله خيراً.")

# --- 5. الإمساكية ---
elif choice == "⏳ الإمساكية":
    st.header("⏳ مواقيت الصلاة")
    # يمكنك وضع مواقيت ثابتة لمدينتك هنا
    data = {
        "الصلاة": ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"],
        "الوقت": ["04:30", "12:10", "03:45", "06:15", "07:35"]
    }
    st.table(pd.DataFrame(data))
