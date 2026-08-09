import streamlit as st
import google.generativeai as genai

# 1. ضبط عنوان الصفحة
st.set_page_config(page_title="مكتبة كلية الآداب - جامعة طنطا", page_icon="📚")
st.title("📚 أخصائي المراجع الرقمي - جامعة طنطا")
st.write("أهلاً بك! كيف يمكنني مساعدتك في البحث أو خدمات المكتبة اليوم؟")

# 2. إدخال مفتاح الـ API (يمكنك وضعه هنا أو إدخاله في الصفحة)
api_key = st.sidebar.text_input("🔑 أدخل API Key الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 3. تحديد شخصية الوكيل وتفعيل البحث في جوجل
    system_instruction = """
    أنت أخصائي المراجع الرقمي بمكتبة كلية الآداب - جامعة طنطا.
    تتحدث بأسلوب رسمي وودود. مهمتك مساعدة الطلاب والباحثين في استفساراتهم.
    ابحث دائماً في مصادر المكتبة أو استخدم البحث في جوجل لإعطاء إجابات دقيقة.
    """
    
    # 4. اختيار النموذج مع تفعيل أداة البحث في جوجل (Google Search)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction,
        tools=[{'google_search': {}}] # تفعيل ميزة البحث الخارجي تلقائياً
    )

    # 5. بناء واجهة الدردشة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(" اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # الحصول على الرد من النموذج
        response = model.generate_content(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
else:
    st.info("💡 يرجى إدخال مفتاح الـ API Key في القائمة الجانبية لبدء المحادثة.")