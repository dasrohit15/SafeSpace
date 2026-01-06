# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
#st.title("🧠 SafeSpace – AI Mental Health Therapist")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #f0f4ff, #e8f8f5);
}

/* Title */
.title-text {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #2c3e50;
}

.subtitle-text {
    text-align: center;
    font-size: 18px;
    color: #5d6d7e;
    margin-bottom: 30px;
}

/* Chat bubbles */
.chat-user {
    background-color: #d6eaf8;
    padding: 14px;
    border-radius: 15px;
    margin-bottom: 10px;
    width: fit-content;
    max-width: 80%;
    margin-left: auto;
    color: #1b4f72;
    font-size: 16px;
}

.chat-ai {
    background-color: #e8f8f5;
    padding: 14px;
    border-radius: 15px;
    margin-bottom: 10px;
    width: fit-content;
    margin-right: auto;
    max-width: 80%;
    color: #145a32;
    font-size: 16px;
}
            
/* Optional subtle shadow */
.user-bubble, .ai-bubble {
    box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
}

/* Center chat area */
.block-container {
    max-width: 900px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown("<div class='title-text'>🧠 SafeSpace</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle-text'>Your AI-powered mental health companion. You're not alone.</div>",
    unsafe_allow_html=True
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # AI Agent exists here
    #response = requests.post(BACKEND_URL, json={"message": user_input})
    #st.session_state.chat_history.append({"role": "assistant", "content": f'{response.json()["response"]} WITH TOOL: [{response.json() ["tool_called"]}]'})
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input},
            timeout=300
        )

        if response.status_code == 200:
            try:
                data = response.json()

                assistant_text = data.get(
                    "response",
                    "⚠️ Backend returned no 'response' field."
                )
                tool_used = data.get(
                    "tool_called",
                    "None"
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"{assistant_text}\n\n🛠 Tool used: {tool_used}"
                })

            except ValueError:
                # Invalid JSON
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "⚠️ Backend returned invalid JSON.\n\n"
                               f"Raw response:\n{response.text}"
                })
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"⚠️ Backend error {response.status_code}.\n\n"
                           f"{response.text}"
            })

    except requests.exceptions.RequestException as e:
        # Connection, timeout, DNS, etc.
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"⚠️ Could not connect to backend.\n\nError:\n{str(e)}"
        })


# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
    