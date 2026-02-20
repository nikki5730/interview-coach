import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Interview Coach", page_icon="💬")
st.title("💬 Interview Coach")
st.write("Practice interview skills through text or recorded interview answers.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
TRANSCRIBE_MODEL = os.getenv("TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
FEEDBACK_MODEL = os.getenv("FEEDBACK_MODEL", "gpt-4.1-mini")

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

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"}


def get_client() -> Optional[OpenAI]:
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


def fallback_feedback(answer: str) -> dict:
    words = answer.split()
    filler_set = {"um", "uh", "like", "actually", "basically"}
    filler_count = sum(1 for w in words if w.lower().strip(".,!?") in filler_set)
    return {
        "overall_score": max(55, min(90, 72 + (len(words) // 20) - filler_count)),
        "strengths": [
            "You answered directly.",
            "Your message is understandable.",
        ],
        "improvements": [
            "Add one concrete example.",
            "Use context -> action -> result structure.",
            "Pause instead of filler words.",
        ],
        "encouragement": "Nice work. Keep practicing one question at a time.",
    }


def ai_feedback(question: str, answer: str) -> dict:
    client = get_client()
    if client is None:
        return fallback_feedback(answer)

    prompt = f"""
You are a supportive interview coach for neurodivergent candidates.
Provide kind, practical, and specific feedback.

Question: {question}
Answer: {answer}

Return JSON only in this shape:
{{
  "overall_score": 0-100 number,
  "strengths": ["...", "..."],
  "improvements": ["...", "...", "..."],
  "encouragement": "..."
}}
""".strip()

    try:
        completion = client.chat.completions.create(
            model=FEEDBACK_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        content = completion.choices[0].message.content or "{}"
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return fallback_feedback(answer)
        return parsed
    except Exception:
        return fallback_feedback(answer)


def extract_audio_to_wav(input_path: Path) -> Path:
    output_path = input_path.with_suffix(".wav")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def transcribe_media(file_bytes: bytes, filename: str) -> str:
    client = get_client()
    if client is None:
        raise RuntimeError("OPENAI_API_KEY missing. Add it to your .env file.")

    ext = Path(filename).suffix.lower()
    if ext not in VIDEO_EXTS and ext not in AUDIO_EXTS:
        raise RuntimeError("Unsupported file type. Upload audio/video file.")

    with tempfile.TemporaryDirectory() as td:
        in_path = Path(td) / f"upload{ext or '.webm'}"
        in_path.write_bytes(file_bytes)

        tx_path = in_path
        if ext in VIDEO_EXTS:
            try:
                tx_path = extract_audio_to_wav(in_path)
            except FileNotFoundError as exc:
                raise RuntimeError("ffmpeg is not installed. Install ffmpeg first.") from exc
            except subprocess.CalledProcessError as exc:
                msg = exc.stderr.decode("utf-8", errors="ignore")[:250]
                raise RuntimeError(f"ffmpeg failed: {msg}") from exc

        with tx_path.open("rb") as media_file:
            out = client.audio.transcriptions.create(model=TRANSCRIBE_MODEL, file=media_file)

    text = (getattr(out, "text", "") or "").strip()
    if not text:
        raise RuntimeError("No speech detected.")
    return text


def render_feedback(feedback: dict) -> None:
    st.subheader("Feedback")
    score = feedback.get("overall_score")
    if score is not None:
        st.metric("Overall Score", f"{score}/100")

    strengths = feedback.get("strengths", [])
    improvements = feedback.get("improvements", [])

    st.write("✅ **What is working**")
    for item in strengths:
        st.write(f"- {item}")

    st.write("🛠️ **What to improve next**")
    for item in improvements:
        st.write(f"- {item}")

    if feedback.get("encouragement"):
        st.info(feedback["encouragement"])


tab1, tab2 = st.tabs(["📝 Text Practice", "🎥 Video/Audio Practice"])

with tab1:
    st.header("📝 Text-Based Interview Practice")
    question = st.selectbox("Choose an interview question", QUESTIONS)
    answer = st.text_area("Type your answer", height=180)

    if st.button("Get text feedback", type="primary"):
        if not answer.strip():
            st.warning("Please type an answer first.")
        else:
            render_feedback(ai_feedback(question=question, answer=answer.strip()))

with tab2:
    st.header("🎥 Video/Audio Interview Practice")
    st.write("Upload a recorded answer and get transcript + AI feedback.")

    question2 = st.selectbox("Interview question", QUESTIONS, key="q2")
    uploaded = st.file_uploader(
        "Upload your answer (.mp4, .mov, .webm, .wav, .mp3, .m4a)",
        type=["mp4", "mov", "webm", "mkv", "avi", "wav", "mp3", "m4a", "aac", "ogg", "flac"],
    )

    if st.button("Analyze recording", type="primary"):
        if uploaded is None:
            st.warning("Please upload a recording first.")
        else:
            with st.spinner("Transcribing and generating feedback..."):
                try:
                    transcript = transcribe_media(uploaded.getvalue(), uploaded.name)
                    st.subheader("Transcript")
                    st.write(transcript)
                    feedback = ai_feedback(question=question2, answer=transcript)
                    render_feedback(feedback)
                except Exception as exc:
                    st.error(str(exc))

    st.caption("Note: real-time pose tracking through components.html is not supported without a custom Streamlit component.")
