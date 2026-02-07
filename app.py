import streamlit as st
import json
import numpy as np
import streamlit.components.v1 as components

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
            st.write("- Summarize your main point early.")
            st.write("- Use the structure: *context → action → result*.")

            st.write("💛 **Reminder:** Clear communication matters more than “perfect” delivery.")
            st.write("🎯 Try rewriting your answer in 3–4 sentences for clarity.")



# ============================================================
#  TAB 2 — REAL-TIME VIDEO AI (WORKING VERSION)
# ============================================================
with tab2:

    st.header("🎥 Real-Time Video Interview AI")
    st.write("This tool uses your webcam to analyze posture, head tilt, and movement in real time.")

    # Load camera + Mediapipe HTML module
    components.html(
        open("mediapipe_component.html").read(),
        height=0,
        width=0,
    )

    # Streamlit reads updated URL parameter
    query_params = st.experimental_get_query_params()
    raw_landmarks = query_params.get("landmarks", ["[]"])[0]

    try:
        landmarks = json.loads(raw_landmarks)
    except:
        landmarks = []

    st.write("Detected landmarks:", len(landmarks))

    if len(landmarks) < 33:
        st.info("Make sure your face + shoulders are visible and well-lit for the model to detect your posture.")
        st.stop()

    # Convert list -> numpy array
    lm = np.array([[p["x"], p["y"], p["z"]] for p in landmarks])

    # Extract key points
    nose = lm[0]
    left_eye = lm[2]
    right_eye = lm[5]
    left_shoulder = lm[11]
    right_shoulder = lm[12]

    # Calculate head tilt
    head_tilt = ((left_eye[1] + right_eye[1]) / 2) - nose[1]

    # Shoulder alignment angle
    posture_angle = np.degrees(np.arctan2(
        left_shoulder[1] - right_shoulder[1],
        left_shoulder[0] - right_shoulder[0]
    ))

    # Movement (frame-to-frame difference)
    prev_frame = st.session_state.get("prev_frame")
    if prev_frame is None:
        st.session_state.prev_frame = lm
        movement = 0
    else:
        movement = float(np.mean(np.abs(lm - prev_frame)))
        st.session_state.prev_frame = lm

    # Display analysis
    st.subheader("📊 Live Body-Language Analysis")
    st.json({
        "head_tilt": head_tilt,
        "posture_angle": posture_angle,
        "movement": movement
    })

    st.subheader("💡 Interpretation (Neurodivergent-Friendly)")

    # Head tilt
    if abs(head_tilt) < 0.03:
        st.write("✔ **Head centered** — great alignment.")
    else:
        st.write("➤ **Slight head tilt detected** — try adjusting camera height or sitting more upright.")

    # Posture
    if abs(posture_angle) < 8:
        st.write("✔ **Shoulders level** — balanced posture detected.")
    else:
        st.write("➤ **Uneven shoulders** — grounding your body or adjusting your seat may help.")

    # Movement
    if movement < 0.01:
        st.write("✔ **Movement steady** — low fidgeting detected.")
    else:
        st.write("➤ **Movement detected** — try grounding elbows or slowing breathing for comfort.")
