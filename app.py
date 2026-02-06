import streamlit as st

st.set_page_config(page_title="Interview Coach", page_icon="💬")

st.title("💬 Interview Coach")
st.write("Practice interview questions and get structured feedback.")

questions = [
    "Tell me about yourself.",
    "Why do you want this role?",
    "Tell me about a challenge you faced.",
    "What is your biggest strength?",
    "What is something you're working on improving?"
]

question = st.selectbox("Choose an interview question:", questions)
answer = st.text_area("Type your answer below:")

if st.button("Get feedback"):
    if not answer.strip():
        st.warning("Please type an answer first.")
    else:
        st.subheader("Feedback")
        st.write("✅ You answered the question clearly.")
        st.write("💡 Try adding one concrete example.")
        st.write("🎯 End with why this makes you a strong candidate.")
