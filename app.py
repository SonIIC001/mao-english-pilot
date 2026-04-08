import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة لـ MAO
st.set_page_config(page_title="MAO English Pilot", page_icon="🚀", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.info("الأبلكيشن ده متفصل لـ محمود أشرف (MAO) لتطوير الإنجليزية في مجال الـ Data Analysis.")

# وظيفة طلب الرد من Gemini
def get_response(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        # استخدام موديل 1.5 flash لأنه الأسرع والأحدث حالياً
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ عذراً يا محمود، حصل خطأ: {str(e)}"

if api_key:
    st.title("🚀 MAO English Pilot")
    
    tabs = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات", "💬 محاكاة المقابلة"])

    # 1. القاموس المهني
    with tabs[0]:
        word = st.text_input("ادخل مصطلح تقني (مثلاً: Version Control):")
        if word:
            with st.spinner('جاري التحليل...'):
                prompt = f"Explain '{word}' simply for a Data Analyst. Provide 2 professional examples."
                st.markdown(get_response(api_key, prompt))

    # 2. مصحح اليوميات
    with tabs[1]:
        text = st.text_area("اكتب روتينك أو اللي اتعلمته النهاردة بالإنجليزية:")
        if st.button("تطوير النص"):
            with st.spinner('جاري التصحيح...'):
                prompt = f"Correct this English and make it sound professional for a Data Analyst: {text}"
                st.success(get_response(api_key, prompt))

    # 3. محاكاة المقابلة
    with tabs[2]:
        st.write("تدرب على أسئلة الـ Interview!")
        if st.button("ابدأ سؤال عشوائي"):
            with st.spinner('جاري التحميل...'):
                prompt = "Ask me one tough interview question for a Data Analyst role."
                st.info(get_response(api_key, prompt))
else:
    st.warning("⚠️ من فضلك دخل الـ API Key في القائمة الجانبية.")
