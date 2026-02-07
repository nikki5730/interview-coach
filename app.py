import streamlit as st

st.set_page_config(page_title="Interview Coach", page_icon="💬")

st.title("💬 Interview Coach")
st.write("Practice interview skills through text or video.")

# -----------------------------
# Create TWO tabs
# -----------------------------
tab1, tab2 = st.tabs(["📝 Text Practice", "🎥 Video Interview"])

# ============================================================
#  TAB 1 — TEXT INTERVIEW PRACTICE
# ============================================================
with tab1:

    st.header("📝 Text-Based Interview Practice")

    questions = [
        # ---------- Getting Started / Low Pressure ----------
        "Tell me about yourself in a work or school context.",
        "What kind of work environment helps you do your best work?",
        "What does a good workday look like for you?",
        
        # ---------- Skills & Strengths (Universal) ----------
        "What are your strongest skills or abilities?",
        "What tasks do you tend to pick up quickly?",
        "What type of work do you find most engaging or satisfying?",
        "What are you especially careful or detail-oriented about?",
        
        # ---------- Experience & Problem Solving ----------
        "Tell me about a task or project you completed successfully.",
        "Tell me about a challenge you faced and how you handled it.",
        "Tell me about a time something didn’t go as planned. What did you do?",
        "How do you usually approach solving a problem?",
        
        # ---------- Communication & Collaboration ----------
        "How do you prefer to receive instructions or feedback?",
        "How do you usually communicate with teammates or coworkers?",
        "Tell me about a time you worked with someone who had a different style than you.",
        "What helps you communicate clearly at work?",
        
        # ---------- Organization & Work Style ----------
        "How do you stay organized or keep track of tasks?",
        "How do you handle multiple tasks or deadlines?",
        "What tools or strategies help you manage your work?",
        
        # ---------- Stress, Support, and Boundaries ----------
        "How do you usually handle stress or pressure?",
        "What support helps you perform well at work?",
        "What accommodations or adjustments have helped you succeed in the past?",
        "How do you take care of yourself during demanding periods?",
        
        # ---------- Learning & Growth ----------
        "How do you learn new tasks or skills best?",
        "Tell me about something new you learned recently.",
        "How do you respond to feedback?",
        
        # ---------- Values & Fit ----------
        "What values are important to you in a workplace?",
        "What kind of team culture do you work best in?",
        "What motivates you to do your best work?",
        
        # ---------- Future & Goals ----------
        "What kinds of roles or tasks are you interested in long-term?",
        "What skills would you like to develop next?",
        "Where do you see yourself growing professionally?",
        
        # ---------- Interview Closing ----------
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

            st.write("✅ **What’s working**")
            st.write("- You responded directly to the question.")
            st.write("- You shared information relevant to how you work.")

            st.write("🛠️ **Suggestions to improve**")
            st.write("- Add one specific example to make the answer clearer.")
            st.write("- Try to summarize your main point at the beginning.")
            st.write("- If helpful, use: *context → action → result*.")

            st.write("💛 **Neurodivergent-friendly reminder**")
            st.write(
                "You do not need to mask or perform. Clear, honest communication "
                "about how you work is valuable."
            )

            st.write("🎯 **Practice tip**")
            st.write("Try answering again in 3–4 sentences focusing on clarity.")

# ============================================================
#  TAB 2 — VIDEO INTERVIEW PRACTICE (Step 1: Camera Test)
# ============================================================
with tab2:

    st.header("🎥 Video Interview Practice")
    st.write("Step 1: Test your camera. If you can see yourself, it works!")

    from streamlit_webrtc import webrtc_streamer

    webrtc_streamer(
        key="camera-test",
        media_stream_constraints={"video": True, "audio": False}
    )

    st.info("If you see the webcam preview above, your camera is working.")

    st.write("⭐ Next steps will include:")
    st.write("- Body language feedback")
    st.write("- Posture analysis")
    st.write("- Facial framing and lighting tips")
    st.write("- Speaking + filler word analysis (optional voice mode)")

        
