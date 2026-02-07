import streamlit as st

# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(page_title="Interview Coach", page_icon="💬")

st.title("💬 Interview Coach")
st.write("Practice interview skills through text or video.")

# ------------------------------------------------------------
# CREATE BOTH TABS FIRST
# ------------------------------------------------------------
tab1, tab2 = st.tabs(["📝 Text Practice", "🎥 Video Interview"])


# ============================================================
#  TAB 1 — TEXT INTERVIEW PRACTICE
# ============================================================
with tab1:

    st.header("📝 Text-Based Interview Practice")

    questions = [
        "Tell me about yourself in a work or school context.",
        "What kind of work environment helps you do your best work?",
        "What does a good workday look like for you?",
        "What are your strongest skills or abilities?",
        "What tasks do you tend to pick up quickly?",
        "What type of work do you find most engaging or satisfying?",
        "What are you especially careful or detail-oriented about?",
        "Tell me about a task or project you completed successfully.",
        "Tell me about a challenge you faced and how you handled it.",
        "Tell me about a time something didn’t go as planned. What did you do?",
        "How do you usually approach solving a problem?",
        "How do you prefer to receive instructions or feedback?",
        "How do you usually communicate with teammates or coworkers?",
        "Tell me about a time you worked with someone who had a different style than you.",
        "What helps you communicate clearly at work?",
        "How do you stay organized or keep track of tasks?",
        "How do you handle multiple tasks or deadlines?",
        "What tools or strategies help you manage your work?",
        "How do you usually handle stress or pressure?",
        "What support helps you perform well at work?",
        "What accommodations or adjustments have helped you succeed in the past?",
        "How do you take care of yourself during demanding periods?",
        "How do you learn new tasks or skills best?",
        "Tell me about something new you learned recently.",
        "How do you respond to feedback?",
        "What values are important to you in a workplace?",
        "What kind of team culture do you work best in?",
        "What motivates you to do your best work?",
        "What kinds of roles or tasks are you interested in long-term?",
        "What skills would you like to develop next?",
        "Where do you see yourself growing professionally?",
        "Is there anything you would like your interviewer to understand about how you work?",
        "What questions would you like to ask the interviewer?"
    ]

    question = st.selectbox("Choose an interview question:", questions)
    answer = st.text_area("Type your answer below:", height=180)

    if st.button("Get feedback"):
        if not answer.strip():
            st.warning("Please type an answer first.")
        else:
            st.subheader("Feedback")
            st.write("✅ **What’s working:**")
            st.write("- You responded directly to the question.")
            st.write("- You shared relevant information.")

            st.write("🛠️ **Suggestions:**")
            st.write("- Add one specific example.")
            st.write("- Summarize your main point up front.")
            st.write("- Use: *context → action → result*.")

            st.write("💛 **Reminder:** You do not need to mask. Clear communication is enough.")
            st.write("🎯 Practice again in 3–4 sentences for clarity.")



# ============================================================
#  TAB 2 — SAFE PLACEHOLDER (NO ERRORS)
# ============================================================
with tab2:

    st.header("🎥 Video Interview Practice")

    st.info("""
    🔧 **The real-time AI body-language analysis module is coming next.**

    For now, this tab is a placeholder so your app deploys without errors.
    """)

    st.write("👇 This will soon become your live video feedback tool:")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1160/1160041.png",
        width=250,
        caption="Camera module loading soon…"
    )

    st.write("""
    ### What will be added:
    - Real-time posture tracking  
    - Head tilt detection  
    - Movement level analysis  
    - Neurodivergent-friendly feedback  
    """)

    st.success("Your app is working! Video AI module will be added safely.")
