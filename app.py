import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="MAO English Pilot", page_icon="🚀", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key:", type="password")
    
    # زرار استعراض الموديلات اللي إنت ضفته
    if st.button("🔍 استعراض الموديلات المتاحة"):
        if api_key:
            try:
                genai.configure(api_key=api_key)
                models = genai.list_models()
                st.write("الموديلات المتاحة لـ MAO:")
                for m in models:
                    if 'generateContent' in m.supported_generation_methods:
                        st.code(m.name)
            except Exception as e:
                st.error(f"فشل في جلب القائمة: {e}")
        else:
            st.warning("دخل الـ Key الأول يا برنس!")
            
    st.info("الأبلكيشن ده متفصل لـ محمود أشرف (MAO).")

# وظيفة جلب الرد
def get_response(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ عذراً يا محمود، حصل خطأ: {str(e)}"

# الجسم الأساسي للأبلكيشن
if api_key:
    st.title("🚀 MAO English Pilot")
    tabs = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات", "💬 محاكاة المقابلة"])

    with tabs[0]:
        word = st.text_input("ادخل مصطلح تقني:")
        if word:
            with st.spinner('جاري التحليل...'):
                prompt = f"Explain '{word}' simply for a Data Analyst. Provide 2 professional examples."
                st.markdown(get_response(api_key, prompt))

    with tabs[1]:
        text = st.text_area("اكتب روتينك بالإنجليزية:")
        if st.button("تطوير النص"):
            with st.spinner('جاري التصحيح...'):
                prompt = f"Correct this English and make it sound professional: {text}"
                st.success(get_response(api_key, prompt))

    with tabs[2]:
        if st.button("ابدأ سؤال مقابلة"):
            with st.spinner('جاري التحميل...'):
                prompt = "Ask me one tough interview question for a Data Analyst role."
                st.info(get_response(api_key, prompt))
else:
    st.warning("⚠️ من فضلك دخل الـ API Key في القائمة الجانبية.")
