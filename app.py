import streamlit as st
from conversation_state import ConversationState
from prompts import (
    greeting_prompt,
    fallback_prompt,
    build_first_tech_question_prompt,
    build_next_tech_question_prompt,
)
from utils import query_gemini

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🧠")
st.title("🧠 TalentScout – Hiring Assistant Chatbot")

# Sidebar layout
col1, col2 = st.columns([1, 2])

with col1:
    st.image("talentscout_chatbot/img/chat.png", width=150)
    st.write("")
    st.image("talentscout_chatbot/img/girl.jpg", width=150)

with col2:
    st.markdown(
            """
            <div style="background-color:#f0f8ff; padding:10px; border-radius:10px;">
                <h3 style="color:#333; font-family:Arial, sans-serif;">💬 Hiring Assistant Bot</h3>
                <p style="color:#444; font-size:15px; font-family:Verdana;">
                    This <strong>AI-powered chatbot</strong> helps simulate a technical interview.<br><br>
                    It collects basic candidate details and asks personalized questions based on their <em>tech stack</em>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
    )




# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = ConversationState()
if "messages" not in st.session_state:
    st.session_state.messages = [("assistant", greeting_prompt())]

# Display chat history
for sender, message in st.session_state.messages:
    with st.chat_message(sender):
        st.write(message)

user_input = st.chat_input("Type here to begin...")

def handle_user_input(user_input):
    state = st.session_state.state
    exit_keywords = ["bye", "exit", "quit", "goodbye"]

    if any(word in user_input.lower() for word in exit_keywords):
        state.finished = True
        return "Thanks again! We'll be in touch shortly."

    if state.stage == "greeting":
        state.stage = "gather_info"
        return state.next_info_question()

    elif state.stage == "gather_info":
        state.record_info_answer(user_input)
        if state.stage == "questions":
            return "Awesome! I’ll now ask you a few technical questions based on your tech stack. Please answer them one by one."
        else:
            return state.next_info_question()

    elif state.stage == "questions":
            # Now generate the first tech question using Gemini
            tech_stack = state.data.get("Tech Stack", "")
            prompt = build_first_tech_question_prompt(tech_stack)
            first_question = query_gemini(prompt)
            state.add_tech_question(first_question)
            state.stage = "tech_questions"
            return first_question

    elif state.stage == "tech_questions":
        # Record the user's answer to the last question
        state.add_tech_answer(user_input)

        # Stop after 4 technical questions
        if len(state.tech_questions) >= 4:
            state.stage = "finished"
            state.finished = True
            return "Thanks for completing the process! Our team will get back to you soon. Have a great day!👋"

        # Otherwise, ask the next question
        tech_stack = state.data.get("Tech Stack", "")
        history = state.get_tech_history()
        prompt = build_next_tech_question_prompt(tech_stack, history)
        next_question = query_gemini(prompt)

        if not next_question or "no more questions" in next_question.lower():
            state.stage = "finished"
            state.finished = True
            return "Thanks for completing the process! Our team will get back to you soon."

        state.add_tech_question(next_question)
        return next_question


    elif state.stage == "finished":
        return "Thanks again! We'll be in touch shortly."

    else:
        return fallback_prompt()

# Handle user input
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response = handle_user_input(user_input)

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("assistant", response))

    with st.chat_message("assistant"):
        st.write(response)
