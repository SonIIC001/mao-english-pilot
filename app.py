import streamlit as st
from openai import OpenAI

# إعدادات الصفحة
st.set_page_config(page_title="MAO English Pilot (Copilot Mode)", page_icon="🤖", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    # هنا هتحتاج OpenAI API Key بدل Gemini
    api_key = st.text_input("OpenAI API Key:", type="password")
    st.info("تم التحديث للعمل بمحرك GPT-4 (Copilot Engine).")

if api_key:
    try:
        # تعريف العميل (Client)
        client = OpenAI(api_key=api_key)
        
        st.title("🤖 MAO Copilot Pilot")
        
        tab1, tab2 = st.tabs(["🎯 القاموس المهني", "📝 مصحح اليوميات"])

        with tab1:
            word = st.text_input("ادخل المصطلح التقني:")
            if word:
                with st.spinner('جاري التحليل...'):
                    # هنا بنادي موديل gpt-4o وهو الأحدث
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Explain '{word}' for a Data Analyst."}]
                    )
                    st.markdown(response.choices[0].message.content)

        with tab2:
            user_text = st.text_area("اكتب نصك هنا:")
            if st.button("تصحيح"):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": f"Correct this English: {user_text}"}]
                )
                st.success(response.choices[0].message.content)

    except Exception as e:
        st.error(f"حصلت مشكلة: {e}")
else:
    st.warning("⚠️ دخل الـ OpenAI API Key عشان نفتح المحرك الجديد.")
