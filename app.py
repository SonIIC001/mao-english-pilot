import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="MAO English Pilot", page_icon="🚀", layout="wide")

# القائمة الجانبية لإدخال المفتاح والإعدادات
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.info("الأبلكيشن ده متفصل لـ محمود أشرف (MAO) لتطوير الإنجليزية في مجال الـ Data Analysis.")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    st.title("🚀 MAO English Pilot")
    
    tab1, tab2, tab3 = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات", "💬 محاكاة المقابلة"])

    # 1. القاموس المهني (Data Analysis & DC Context)
    with tab1:
        word = st.text_input("ادخل كلمة أو جملة تقنية:")
        if word:
            with st.spinner('جاري التحليل...'):
                prompt = f"Explain '{word}' for a Data Analyst and Document Controller. Give 2 professional examples."
                response = model.generate_content(prompt)
                st.markdown(response.text)

    # 2. مصحح اليوميات
    with tab2:
        user_text = st.text_area("اكتب روتينك أو ما تعلمته اليوم بالإنجليزية:", height=150)
        if st.button("تطوير وتحليل النص"):
            with st.spinner('جاري التصحيح...'):
                prompt = f"Correct this English and make it sound like a professional engineer/data analyst: {user_text}"
                response = model.generate_content(prompt)
                st.success("النص المقترح:")
                st.write(response.text)

    # 3. محاكاة المقابلة (مع ذاكرة للمحادثة)
    with tab3:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("تحدث مع المحاور..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            full_context = f"You are a tech recruiter interviewing Mahmoud, a Document Controller transitioning to Data Analysis. Be professional. Respond to: {prompt}"
            response = model.generate_content(full_context)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)
else:
    st.warning("⚠️ من فضلك أدخل الـ API Key في القائمة الجانبية لتفعيل المحرك الذكي.")
