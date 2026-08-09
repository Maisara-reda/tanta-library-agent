import streamlit as st
import google.generativeai as genai

# 1. إعداد عنوان الصفحة
st.set_page_config(page_title="مكتبة كلية الآداب - جامعة طنطا", page_icon="📚")
st.title("📚 أخصائي المراجع الرقمي - جامعة طنطا")
st.write("أهلاً بك! كيف يمكنني مساعدتك في البحث أو خدمات المكتبة اليوم؟")

# 2. القائمة الجانبية للمفتاح
api_key = st.sidebar.text_input("🔑 أدخل API Key الخاص بك:", type="password")

if api_key:
    try:
        # إعداد المفتاح والنموذج الأساسي
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        # 3. إدارة سجل المحادثة
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # 4. استقبال سؤال المستخدم وإرسال الرد
        if prompt := st.chat_input("اكتب سؤالك هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # طلب الإجابة من النموذج
            response = model.generate_content(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)

    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء الاتصال: {e}")
else:
    st.info("💡 يرجى إدخال مفتاح الـ API Key في القائمة الجانبية لبدء المحادثة.")
