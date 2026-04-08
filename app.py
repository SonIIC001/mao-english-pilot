import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="MAO English Pilot", page_icon="🚀", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.info("الأبلكيشن ده متفصل لـ محمود أشرف (MAO) لتطوير الإنجليزية.")

# وظيفة لإرسال الطلبات للذكاء الاصطناعي مع معالجة الأخطاء
def get_ai_response(prompt_text):
    try:
        # ده "الجوكر" اللي شغال عالمياً ومستقر جداً
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        # لو فشل، بيجرب النسخة التانية كخطة بديلة (Backup)
        try:
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
        except:
            return f"⚠️ عذراً يا محمود، حصل خطأ: {str(e)}"

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        st.title("🚀 MAO English Pilot")
        
        tab1, tab2, tab3 = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات", "💬 محاكاة المقابلة"])

        # 1. القاموس المهني
        with tab1:
            word = st.text_input("ادخل كلمة أو جملة تقنية (مثلاً: Data Pipeline):")
            if word:
                with st.spinner('جاري التحليل...'):
                    prompt = f"Explain the term '{word}' in the context of Data Analysis and Document Control. Provide 2 professional examples."
                    result = get_ai_response(prompt)
                    st.markdown(result)

        # 2. مصحح اليوميات
        with tab2:
            user_text = st.text_area("اكتب روتينك أو ما تعلمته اليوم بالإنجليزية:", height=150)
            if st.button("تطوير وتحليل النص"):
                if user_text:
                    with st.spinner('جاري التصحيح...'):
                        prompt = f"Correct this English and make it sound like a professional data analyst: {user_text}"
                        result = get_ai_response(prompt)
                        st.success("النص المقترح:")
                        st.write(result)

        # 3. محاكاة المقابلة
        with tab3:
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if user_input := st.chat_input("تحدث مع المحاور..."):
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.chat_message("user").write(user_input)
                
                with st.spinner('جاري التفكير...'):
                    full_context = f"You are a tech recruiter interviewing Mahmoud for a Data Analyst role. Respond to: {user_input}"
                    ai_reply = get_ai_response(full_context)
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    st.chat_message("assistant").write(ai_reply)
                    
    except Exception as e:
        st.error(f"حدث خطأ في الإعدادات: {e}")
else:
    st.warning("⚠️ من فضلك أدخل الـ API Key في القائمة الجانبية لتفعيل المحرك الذكي.")
