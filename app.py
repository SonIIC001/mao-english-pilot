import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="MAO English Pilot", page_icon="🚀", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_key = st.text_input("Gemini API Key:", type="password")
    st.info("الأبلكيشن ده متفصل لـ محمود أشرف (MAO).")

# وظيفة الربط الذكية
def start_chat(api_key):
    genai.configure(api_key=api_key)
    # بنجرب أكتر من اسم للموديل عشان نتفادى خطأ 404
    for model_name in ['gemini-pro', 'models/gemini-pro', 'gemini-1.5-flash']:
        try:
            model = genai.GenerativeModel(model_name)
            # تجربة وهمية للتأكد أن الموديل يعمل
            model.generate_content("test") 
            return model
        except:
            continue
    return None

if api_key:
    model = start_chat(api_key)
    
    if model:
        st.title("🚀 MAO English Pilot")
        tab1, tab2, tab3 = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات", "💬 محاكاة المقابلة"])

        with tab1:
            word = st.text_input("ادخل كلمة أو جملة تقنية:")
            if word:
                response = model.generate_content(f"Explain '{word}' for a Data Analyst. Give 2 examples.")
                st.markdown(response.text)

        with tab2:
            user_text = st.text_area("اكتب روتينك اليومي بالإنجليزية:")
            if st.button("تطوير النص"):
                response = model.generate_content(f"Correct this English for a professional: {user_text}")
                st.success(response.text)

        with tab3:
            if "messages" not in st.session_state: st.session_state.messages = []
            for m in st.session_state.messages: st.chat_message(m["role"]).write(m["content"])
            
            if p := st.chat_input("تحدث مع المحاور..."):
                st.session_state.messages.append({"role": "user", "content": p})
                st.chat_message("user").write(p)
                resp = model.generate_content(f"Interview Mahmoud for a Data Analyst role: {p}")
                st.session_state.messages.append({"role": "assistant", "content": resp.text})
                st.chat_message("assistant").write(resp.text)
    else:
        st.error("⚠️ جوجل مش قادرة توصل للموديل حالياً، جرب API Key جديد أو تأكد من إعدادات الحساب.")
else:
    st.warning("⚠️ دخل الـ API Key في الجنب يا بطل.")
