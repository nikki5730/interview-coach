import streamlit as st

st.set_page_config(page_title="Interview Coach", page_icon="💬")

st.title("💬 Interview Coach")
st.write("Practice interview skills through text or video.")

# ------------------------------------------------------------
# Create BOTH tabs BEFORE using them
# ------------------------------------------------------------
tab1, tab2 = st.tabs(["📝 Text Practice", "🎥 Video Interview"])

# ============================================================
#  TAB 1 — TEXT INTERVIEW PRACTICE (UNCHANGED)
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
            st.write("- You shared relevant information.")

            st.write("🛠️ **Suggestions**")
            st.write("- Add one specific example.")
            st.write("- Summarize your main point up front.")
            st.write("- Use: *context → action → result*.")

            st.write("💛 **Reminder**")
            st.write("You do not need to mask. Clear communication is enough.")

            st.write("🎯 **Practice tip**")
            st.write("Try again in 3–4 sentences for clarity.")

# ============================================================
#  TAB 2 — ADVANCED VIDEO ANALYSIS (SAFE, FIXED)
# ============================================================
with tab2:

    st.header("🎥 Video Interview Practice")
    st.write("Record yourself, then click Generate Feedback.")

    import cv2
    import numpy as np
    import mediapipe as mp
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

    mp_pose = mp.solutions.pose
    mp_face = mp.solutions.face_detection

    def angle_with_vertical(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return float(np.degrees(np.arctan2(dx, -dy)))

    class VideoAnalyzer(VideoTransformerBase):
        def __init__(self):
            self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.face = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

            self.frame_count = 0
            self.face_visible = 0
            self.brightness_values = []
            self.motion_values = []
            self.posture_angles = []
            self.head_tilt_values = []
            self.prev_gray = None

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.brightness_values.append(float(np.mean(gray)))

            if self.prev_gray is not None:
                diff = cv2.absdiff(gray, self.prev_gray)
                self.motion_values.append(float(np.mean(diff)))
            self.prev_gray = gray

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_res = self.face.process(rgb)
            if face_res.detections:
                self.face_visible += 1

            pose_res = self.pose.process(rgb)
            if pose_res.pose_landmarks:
                lm = pose_res.pose_landmarks.landmark
                ls = (lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                      lm[mp_pose.P_]()
