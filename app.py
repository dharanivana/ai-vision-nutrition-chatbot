
import re
import urllib.parse
import streamlit as st
from google import genai
from google.genai import types

from prompts import (
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)

MODEL_NAME = "gemini-3.8-flash"

st.set_page_config(
    page_title="MacroSnap",
    page_icon="🥗",
    layout="centered",
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


def ask_gemini(parts):
    """Send a request using a fresh Gemini client."""
    client = None

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=parts,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )

        if response.text:
            return response.text

        return "AI response was empty. Please try again."

    except Exception as error:
        return f"AI_ERROR: {error}"

    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "image":
            st.image(message["content"])
        else:
            st.write(message["content"])


def add_message(role, kind, content, mime_type=None):
    message = {
        "role": role,
        "kind": kind,
        "content": content,
        "mime_type": mime_type,
    }

    st.session_state.messages.append(message)
    render_message(message)


# STEP 1: User setup
if "onboarded" not in st.session_state:
    st.title("🥗 MacroSnap")
    st.caption("Your AI Vision Nutrition Chatbot")

    with st.form("onboarding_form"):
        name = st.text_input("Your name")

        whatsapp_number = st.text_input(
            "WhatsApp number with country code",
            placeholder="+91XXXXXXXXXX",
        )

        submitted = st.form_submit_button("Let's go 🚀")

    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("Please enter your name and WhatsApp number.")
        else:
            phone = re.sub(r"\D", "", whatsapp_number)

            if not 10 <= len(phone) <= 15:
                st.warning("Please enter a valid phone number with country code.")
            else:
                st.session_state.name = name.strip()
                st.session_state.whatsapp_number = phone
                st.session_state.messages = []
                st.session_state.pop("whatsapp_url", None)
                st.session_state.onboarded = True
                st.rerun()

    st.stop()


# STEP 2: Header and WhatsApp report
header_col, button_col = st.columns([5, 2])

with header_col:
    st.title("🥗 MacroSnap")

with button_col:
    st.write("")

    if st.button("📤 Send to WhatsApp", use_container_width=True):
        report_parts = [
            "Create a complete nutrition report from the meal details in this conversation. Include each meal, estimated total calories (kcal), protein (g), carbohydrates (g), and fat (g). Do not give a welcome message. If meal details are present, summarize them directly.",
            "Prepare a nutrition report based on this conversation:",
        ]

        for item in st.session_state.messages:
            if item["kind"] == "text":
                report_parts.append(
                    f'{item["role"].upper()}: {item["content"]}'
                )
            elif item["kind"] == "image":
                report_parts.append(
                    f'{item["role"].upper()}: Previously uploaded meal photo.'
                )
                report_parts.append(
                    types.Part.from_bytes(
                        data=item["content"],
                        mime_type=item.get("mime_type") or "image/jpeg",
                    )
                )

        with st.spinner("Preparing your nutrition report..."):
            summary = ask_gemini(report_parts)

        if summary.startswith("AI_ERROR:"):
            st.error(summary)

        else:
            phone = st.session_state.whatsapp_number
            message = urllib.parse.quote(
                f"🥗 MacroSnap Nutrition Report\n\n{summary}"
            )

            st.session_state.whatsapp_url = (
                f"https://wa.me/{phone}?text={message}"
            )

            st.success("Your nutrition report is ready!")

if st.session_state.get("whatsapp_url"):
    st.link_button(
        "Open WhatsApp and Send Report",
        st.session_state.whatsapp_url,
        use_container_width=True,
    )

st.caption(
    f"Logged in as {st.session_state.name} | "
    "Your nutrition assistant"
)


# STEP 3: Chat history
if not st.session_state.messages:
    welcome = WELCOME_MESSAGE_TEMPLATE.format(
        name=st.session_state.name
    )

    add_message("assistant", "text", welcome)

else:
    for item in st.session_state.messages:
        render_message(item)


# STEP 4: Text questions and meal photos
user_input = st.chat_input(
    "Ask a question or attach a meal photo",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    parts = []

    photo = user_input.files[0] if user_input.files else None
    text = (user_input.text or "").strip()

    if photo is not None:
        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes,
            mime_type=photo.type,
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type or "image/jpeg",
            )
        )

    if text:
        add_message("user", "text", text)
        parts.append(text)

    elif photo is not None:
        parts.append(
            "Identify this meal and estimate calories, protein, "
            "carbohydrates, and fat. Explain that estimates may vary."
        )

    if parts:
        with st.spinner("Analyzing your meal..."):
            answer = ask_gemini(parts)

        if answer.startswith("AI_ERROR:"):
            st.error(answer)
        else:
            add_message("assistant", "text", answer)
