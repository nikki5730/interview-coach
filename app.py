# ============================================================
#  TAB 2 — ADVANCED VIDEO INTERVIEW PRACTICE
# ============================================================
with tab2:

    st.header("🎥 Video Interview Practice")
    st.write("Record yourself answering a question. After you stop, the app will analyze posture, movement, lighting, and framing.")

    import cv2
    import numpy as np
    import mediapipe as mp
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

    mp_pose = mp.solutions.pose
    mp_face = mp.solutions.face_detection

    # -----------------------------
    # Utility function for posture angle
    # -----------------------------
    def angle_with_vertical(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        ang = np.degrees(np.arctan2(dx, -dy))
        return float(ang)

    # -----------------------------
    # Video analysis engine
    # -----------------------------
    class VideoAnalyzer(VideoTransformerBase):
        def __init__(self):
            self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.face = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

            # store metrics
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

            # brightness
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.brightness_values.append(float(np.mean(gray)))

            # motion detection
            if self.prev_gray is not None:
                diff = cv2.absdiff(gray, self.prev_gray)
                self.motion_values.append(float(np.mean(diff)))
            self.prev_gray = gray

            # face detection
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_res = self.face.process(rgb)
            if face_res.detections:
                self.face_visible += 1

            # pose analysis
            pose_res = self.pose.process(rgb)
            if pose_res.pose_landmarks:
                lm = pose_res.pose_landmarks.landmark

                left_sh = (
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h,
                )
                left_hip = (
                    lm[mp_pose.PoseLandmark.LEFT_HIP].x * w,
                    lm[mp_pose.PoseLandmark.LEFT_HIP].y * h,
                )

                torso_angle = angle_with_vertical(left_hip, left_sh)
                self.posture_angles.append(torso_angle)

                # head tilt (approx)
                nose = (
                    lm[mp_pose.PoseLandmark.NOSE].x * w,
                    lm[mp_pose.PoseLandmark.NOSE].y * h,
                )
                left_eye = (
                    lm[mp_pose.PoseLandmark.LEFT_EYE].x * w,
                    lm[mp_pose.PoseLandmark.LEFT_EYE].y * h,
                )
                head_tilt = left_eye[1] - nose[1]
                self.head_tilt_values.append(head_tilt)

            self.frame_count += 1
            return img

    # -----------------------------
    # Summarize results
    # -----------------------------
    def summarize(analyzer: VideoAnalyzer):
        if analyzer.frame_count < 20:
            return {"error": "Not enough video data to analyze. Please record longer."}

        face_ratio = analyzer.face_visible / analyzer.frame_count
        brightness = float(np.mean(analyzer.brightness_values))
        motion = float(np.mean(analyzer.motion_values))
        posture_mean = float(np.mean(analyzer.posture_angles))
        posture_var = float(np.std(analyzer.posture_angles))
        head_tilt = float(np.mean(analyzer.head_tilt_values))

        strengths = []
        tips = []

        # Face framing
        if face_ratio > 0.7:
            strengths.append("Your face stayed visible most of the time — good framing.")
        else:
            tips.append("Try sitting so your face remains centered in the frame.")

        # Lighting
        if brightness < 60:
            tips.append("Lighting appears dim. Try adding a soft light source in front of you.")
        else:
            strengths.append("Lighting appears clear enough on camera.")

        # Posture
        if abs(posture_mean) < 12:
            strengths.append("Your posture appears mostly upright.")
        else:
            tips.append("You may be leaning — try relaxing shoulders and keeping chest open.")

        # Movement
        if motion > 20:
            tips.append("There is noticeable movement. If you want steadiness, try resting elbows on a desk.")
        else:
            strengths.append("Your movement level appears steady.")

        # Head tilt
        if abs(head_tilt) > 15:
            tips.append("Your head tilts noticeably — adjust your sitting height or camera angle.")
        else:
            strengths.append("Your head position appears natural and stable.")

        return {
            "strengths": strengths,
            "tips": tips,
            "metrics": {
                "face_visibility_ratio": round(face_ratio, 2),
                "brightness": round(brightness, 1),
                "avg_motion": round(motion, 1),
                "posture_angle_mean": round(posture_mean, 1),
                "posture_variability": round(posture_var, 1),
                "head_tilt": round(head_tilt, 1)
            }
        }

    st.subheader("🎥 Record Your Answer")

    analyzer_ctx = webrtc_streamer(
        key="advanced-analysis",
        video_transformer_factory=VideoAnalyzer,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if analyzer_ctx.video_transformer:
        if st.button("Generate Video Feedback"):
            report = summarize(analyzer_ctx.video_transformer)

            if "error" in report:
                st.warning(report["error"])
            else:
                st.subheader("✅ Strengths")
                for s in report["strengths"]:
                    st.write("• " + s)

                st.subheader("💡 Suggestions")
                for t in report["tips"]:
                    st.write("• " + t)

                st.subheader("📊 Metrics (estimated)")
                st.json(report["metrics"])
