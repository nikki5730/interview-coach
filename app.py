with tab2:

    st.header("🎥 Video Interview Practice (Mediapipe JS)")
    st.write("Your browser will analyze posture, head tilt, and movement in real time.")

    import json
    import numpy as np
    import streamlit.components.v1 as components

    # -----------------------------
    # Load the JS component
    # -----------------------------
    component = components.html(
        open("mediapipe_component.html").read(),
        height=10,  # hidden video
        width=10,
    )

    # -----------------------------
    # Listen for landmark messages
    # -----------------------------
    landmarks_json = st.session_state.get("landmarks", "[]")

    # Streamlit listens for JS messages:
    def on_js_event():
        st.session_state.landmarks = st.experimental_get_query_params().get("landmarks", ["[]"])[0]

    st.experimental_on_query_params_change(on_js_event)

    # -----------------------------
    # If we have new landmarks, parse them
    # -----------------------------
    try:
        landmarks = json.loads(landmarks_json)
        if isinstance(landmarks, str):
            landmarks = json.loads(landmarks)
    except:
        landmarks = []

    st.write("Detected landmarks:", len(landmarks))

    # -----------------------------
    # ANALYSIS
    # -----------------------------
    def analyze_landmarks(lm):

        if len(lm) < 33:
            return None

        # Convert to NumPy arrays
        lm = np.array([[p["x"], p["y"], p["z"]] for p in lm])

        # Key points
        nose = lm[0]
        left_eye = lm[2]
        right_eye = lm[5]
        left_shoulder = lm[11]
        right_shoulder = lm[12]

        # Head tilt
        head_tilt = (left_eye[1] + right_eye[1]) / 2 - nose[1]

        # Posture: shoulder alignment
        posture_angle = np.degrees(np.arctan2(
            left_shoulder[1] - right_shoulder[1],
            left_shoulder[0] - right_shoulder[0]
        ))

        # Movement (frame-to-frame difference)
        if "prev" not in st.session_state:
            st.session_state.prev = lm
            movement = 0
        else:
            movement = np.mean(np.abs(lm - st.session_state.prev))
            st.session_state.prev = lm

        return {
            "head_tilt": head_tilt,
            "posture_angle": posture_angle,
            "movement": movement,
        }

    result = analyze_landmarks(landmarks)

    if result:
        st.subheader("📊 Live Analysis")
        st.write(result)

        st.subheader("💡 Interpretation")

        if abs(result["head_tilt"]) < 0.03:
            st.write("✔ Head appears centered.")
        else:
            st.write("➤ Your head tilts slightly — try adjusting camera height.")

        if abs(result["posture_angle"]) < 8:
            st.write("✔ Shoulders look level — good upright posture.")
        else:
            st.write("➤ Shoulders uneven — try sitting tall or adjusting camera.")

        if result["movement"] < 0.01:
            st.write("✔ Movement level is steady.")
        else:
            st.write("➤ Some movement detected — resting elbows may help.")
