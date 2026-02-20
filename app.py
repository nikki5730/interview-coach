import re
import tempfile
from pathlib import Path

import streamlit as st
from faster_whisper import WhisperModel

st.set_page_config(page_title="Interview Coach (Local Free)", page_icon="💬")
st.title("💬 Interview Coach (Local Free)")
st.write("Local transcription + feedback. No OpenAI API key needed.")

QUESTIONS = [
    "Tell me about yourself in a work or school context.",
    "What kind of work environment helps you do your best work?",
    "What does a good workday look like for you?",
    "What are your strongest skills or abilities?",
    "Tell me about a challenge you faced and how you handled it.",
    "How do you usually communicate with teammates or coworkers?",
    "How do you stay organized or keep track of tasks?",
    "How do you respond to feedback?",
    "What motivates you to do your best work?",
    "What questions would you like to ask the interviewer?",
]

FILLERS = {"um", "uh", "like", "actually", "basically", "you know"}
ACTION_WORDS = {"built", "created", "led", "organized", "improved", "managed", "delivered", "solved", "implemented"}
RESULT_WORDS = {"result", "improved", "increased", "reduced", "%", "faster", "on time", "completed"}


@st.cache_resource
def load_model():
    return WhisperModel("tiny", device="cpu", compute_type="int8")


def transcribe_local(file_bytes, filename):
    ext = Path(filename).suffix.lower() or ".mp4"
    with tempfile.TemporaryDirectory() as td:
        file_path = Path(td) / ("upload" + ext)
        file_path.write_bytes(file_bytes)
        model = load_model()
        segments, _ = model.transcribe(str(file_path), vad_filter=True, beam_size=1)
        text = " ".join(seg.text.strip() for seg in segments).strip()
    return text


def analyze_answer(answer):
    text = answer.strip()
    words = re.findall(r"\b[\w']+\b", text.lower())
    word_count = len(words)
    filler_count = sum(1 for w in words if w in FILLERS)

    has_action = any(w in words for w in ACTION_WORDS)
    has_result = any(token in text.lower() for token in RESULT_WORDS)
    has_number = bool(re.search(r"\d", text))

    score = 60
    if 60 <= word_count <= 180:
        score += 10
    elif word_count < 40:
        score -= 8

    score -= min(10, filler_count * 2)
    if has_action:
        score += 8
    if has_result:
        score += 8
    if has_number:
        score += 6
    score = max(40, min(95, score))

    strengths = []
    improvements = []

    if word_count >= 40:
        strengths.append("Your answer has enough detail.")
    else:
        improvements.append("Add more detail (target 60-120 words).")

    if filler_count <= 2:
        strengths.append("Your delivery sounds reasonably clear.")
    else:
        improvements.append("Reduce filler words by pausing between ideas.")

    if has_action:
        strengths.append("You described actions you took.")
    else:
        improvements.append("Use action verbs like built, led, solved, improved.")

    if has_result or has_number:
        strengths.append("You included outcome-focused language.")
    else:
        improvements.append("Add measurable results (number, %, time saved).")

    if len(improvements) < 3:
        improvements.append("Use STAR: Situation, Task, Action, Result.")

    return {
        "overall_score": score,
        "word_count": word_count,
        "filler_count": filler_count,
        "strengths": strengths[:3],
        "improvements": improvements[:3],
    }


def render_feedback(feedback):
    st.subheader("Feedback")
    st.metric("Overall Score", f"{feedback['overall_score']}/100")
    st.write(f"Words: **{feedback['word_count']}** | Filler words: **{feedback['filler_count']}**")

    st.write("✅ **What is working**")
    for s in feedback["strengths"]:
        st.write(f"- {s}")

    st.write("🛠️ **What to improve next**")
    for i in feedback["improvements"]:
        st.write(f"- {i}")


tab1, tab2 = st.tabs(["📝 Text Practice", "🎥 Video/Audio Practice"])

with tab1:
    q1 = st.selectbox("Question", QUESTIONS)
    a1 = st.text_area("Type your answer", height=180)
    if st.button("Get feedback"):
        if a1.strip():
            render_feedback(analyze_answer(a1))
        else:
            st.warning("Please type an answer first.")

with tab2:
    q2 = st.selectbox("Interview question", QUESTIONS, key="q2")
    uploaded = st.file_uploader(
        "Upload recording (.mp4, .mov, .webm, .wav, .mp3, .m4a)",
        type=["mp4", "mov", "webm", "mkv", "avi", "wav", "mp3", "m4a", "aac", "ogg", "flac"]
    )

    if st.button("Analyze recording", type="primary"):
        if uploaded is None:
            st.warning("Please upload a recording first.")
        else:
            try:
                with st.spinner("Transcribing locally..."):
                    transcript = transcribe_local(uploaded.getvalue(), uploaded.name)
                if not transcript:
                    st.error("No speech detected.")
                else:
                    st.subheader("Transcript")
                    st.write(transcript)
                    st.write(f"Question: **{q2}**")
                    render_feedback(analyze_answer(transcript))
            except Exception:
                st.error("Local transcription failed on this file format.")
                st.info("Try .m4a or .wav, or paste transcript manually below.")
                manual = st.text_area("Paste transcript", height=150)
                if manual.strip():
                    render_feedback(analyze_answer(manual.strip()))
