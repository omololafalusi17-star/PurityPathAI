import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from prompts import build_system_prompt
from safety import assess_message
from learning_content import LEARNING_PATHS
from scenarios import SCENARIOS
from mentor_resources import MENTOR_RESOURCES
from ai_content_generator import generate_content


# Load environment variables
load_dotenv()


# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)


# Page configuration
st.set_page_config(
    page_title="PurityPathAI",
    page_icon="🌿",
    layout="wide",
)


# Custom styling
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 1.2rem;
    opacity: .8;
}

.card {
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,.25);
    margin-bottom: 1rem;
}

.small {
    font-size: .9rem;
    opacity: .75;
}
</style>
""", unsafe_allow_html=True)


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "age_group" not in st.session_state:
    st.session_state.age_group = "🌿 Teen (11–17)"

if "scenario_score" not in st.session_state:
    st.session_state.scenario_score = 0


# Sidebar
st.sidebar.title("🌿 PurityPathAI")
st.sidebar.caption("Your Worth. Your Choice. Your Path.")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📚 Learn",
        "🎮 Choose Your Path",
        "💬 Ask PurityPathAI",
        "✨ Create Content",
        "👩‍🏫 Mentor Resources",
    ],
)


st.sidebar.divider()


st.session_state.age_group = st.sidebar.selectbox(
    "Learning audience",
    list(LEARNING_PATHS.keys()),
    index=list(LEARNING_PATHS.keys()).index(
        st.session_state.age_group
    ),
)


st.sidebar.caption(
    "Age selection personalizes educational content; "
    "it is not age verification."
)


# Header function
def show_header(title, subtitle=""):
    st.markdown(
        f'<p class="main-title">{title}</p>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f'<p class="subtitle">{subtitle}</p>',
            unsafe_allow_html=True
        )

    st.divider()


# Home
if page == "🏠 Home":

    show_header(
        "🌿 PurityPathAI",
        "Your Worth. Your Choice. Your Path."
    )

    st.write(
        "PurityPathAI is an AI-powered youth education assistant designed to "
        "support learning about self-worth, healthy boundaries, peer pressure, "
        "healthy relationships, digital safety, and wise decision-making."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "📚 **Learn**\n\n"
            "Explore age-aware educational topics."
        )

    with c2:
        st.info(
            "🎮 **Choose Your Path**\n\n"
            "Practice decisions through interactive scenarios."
        )

    with c3:
        st.info(
            "💬 **Ask PurityPathAI**\n\n"
            "Ask questions and receive supportive guidance."
        )

    st.success(
        "PurityPathAI is designed to educate and empower—not shame. "
        "AI supports education, while trusted adults, mentors, and qualified "
        "professionals remain important sources of human care."
    )

    st.subheader("Our approach")

    st.write(
        "**ASK → LEARN → REFLECT → CONNECT**"
    )

    st.caption(
        "For serious safety concerns, users should seek help from a trusted "
        "adult or appropriate local professional."
    )


# Learn
elif page == "📚 Learn":

    show_header(
        "📚 Learning Center",
        "Choose a path and explore a topic."
    )

    audience = st.session_state.age_group
    content = LEARNING_PATHS[audience]

    st.subheader(audience)

    topic = st.selectbox(
        "Choose a topic",
        list(content["topics"].keys())
    )

    st.markdown(
        f"### {topic}"
    )

    st.write(
        content["topics"][topic]
    )

    st.divider()

    st.subheader("💡 Reflection")

    st.write(
        content["reflection"]
    )


# Choose Your Path
elif page == "🎮 Choose Your Path":

    show_header(
        "🎮 Choose Your Path",
        "Practice thinking through real-life situations."
    )

    scenario_names = list(SCENARIOS.keys())

    scenario_name = st.selectbox(
        "Choose a scenario",
        scenario_names
    )

    scenario = SCENARIOS[scenario_name]

    st.subheader(
        scenario["title"]
    )

    st.write(
        scenario["situation"]
    )

    answer = st.radio(
        "What would you do?",
        scenario["options"],
        key=f"scenario_{scenario_name}",
    )

    if st.button(
        "See Reflection",
        type="primary"
    ):

        feedback = scenario["feedback"][answer]

        st.info(
            feedback
        )

        st.success(
            "Reflection complete. "
            "Think about what you could do next time."
        )


# Ask PurityPathAI
elif page == "💬 Ask PurityPathAI":

    show_header(
        "💬 Ask PurityPathAI",
        "A supportive educational conversation space."
    )

    st.caption(
        "Please don't share your full name, address, phone number, school, "
        "passwords, or other unnecessary personal information."
    )


    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # Check Gemini API key
    if not GEMINI_API_KEY:

        st.warning(
            "The AI assistant is not connected yet. "
            "Add GEMINI_API_KEY to your .env file "
            "and restart the app."
        )


    # Chat input
    user_question = st.chat_input(
        "What would you like to ask?"
    )


    if user_question:

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )


        with st.chat_message(
            "user"
        ):

            st.write(
                user_question
            )


        # Safety check
        safety = assess_message(
            user_question
        )


        # High-risk message
        if safety["level"] == "high":

            response_text = safety["response"]

            with st.chat_message(
                "assistant"
            ):

                st.warning(
                    response_text
                )


        # Gemini not connected
        elif not client:

            response_text = (
                "The AI assistant is not connected yet. "
                "Please configure your Gemini API key."
            )

            with st.chat_message(
                "assistant"
            ):

                st.error(
                    response_text
                )


        # Gemini response
        else:

            history = (
                st.session_state.messages[-12:]
            )


            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🌿 PurityPathAI is thinking..."
                ):

                    try:

                        system_prompt = build_system_prompt(
                            st.session_state.age_group
                        )


                        conversation = "\n".join(
                            [
                                f"{message['role'].capitalize()}: "
                                f"{message['content']}"
                                for message in history
                            ]
                        )


                        full_prompt = f"""
{system_prompt}

You are PurityPathAI, a supportive educational assistant.

The selected learning audience is:
{st.session_state.age_group}

Conversation history:
{conversation}

Respond to the user's latest message in a supportive,
respectful, age-appropriate, educational way.

Do not shame the user.
Do not request unnecessary personal information.
Encourage trusted adult or professional support when appropriate.
"""


                        response = client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=full_prompt,
                        )


                        response_text = response.text


                        st.write(
                            response_text
                        )


                    except Exception as e:

                        st.error(
                            f"Gemini Error: {e}"
                        )


                        response_text = (
                            "I'm sorry, I couldn't process that right now. "
                            "Please try again. If this is an urgent safety concern, "
                            "please contact a trusted adult or appropriate local support."
                        )


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text
            }
        )


    # Clear conversation
    if st.button(
        "Clear conversation"
    ):

        st.session_state.messages = []

        st.rerun()


# Create Content
elif page == "✨ Create Content":

    show_header(
        "✨ AI Content Generator",
        "Create educational materials for mentors and educators."
    )


    content_type = st.selectbox(
        "What would you like to create?",
        [
            "Lesson Plan",
            "Social Media Campaign",
            "Poster Copy",
            "Short Video Script",
            "Quiz",
            "Discussion Guide"
        ],
    )


    topic = st.text_input(
        "Topic",
        "Peer pressure and healthy boundaries"
    )


    audience = st.selectbox(
        "Audience",
        list(LEARNING_PATHS.keys())
    )


    tone = st.selectbox(
        "Tone",
        [
            "Warm and encouraging",
            "Professional",
            "Youth-friendly",
            "Faith-sensitive"
        ]
    )


    if st.button(
        "Generate Content",
        type="primary"
    ):


        if not client:

            st.error(
                "Add GEMINI_API_KEY to your .env file "
                "before using the AI content generator."
            )


        else:

            with st.spinner(
                "Creating content..."
            ):

                try:

                    result = generate_content(
                        client,
                        content_type,
                        topic,
                        audience,
                        tone,
                        model=GEMINI_MODEL,
                    )


                    st.markdown(
                        result
                    )


                except Exception as e:

                    st.error(
                        f"I couldn't generate the content right now. "
                        f"Error: {e}"
                    )


# Mentor Resources
elif page == "👩‍🏫 Mentor Resources":

    show_header(
        "👩‍🏫 Mentor Resources",
        "Tools for parents, teachers, youth leaders, and mentors."
    )


    category = st.selectbox(
        "Choose a resource",
        list(MENTOR_RESOURCES.keys())
    )


    resource = MENTOR_RESOURCES[
        category
    ]


    st.subheader(
        resource["title"]
    )


    for item in resource["items"]:

        st.write(
            f"• {item}"
        )


    st.divider()


    st.info(
        "Mentor reminder: Listen without judgment, create a safe environment, "
        "and encourage appropriate human support when a young person may be unsafe."
    )


# Footer
st.divider()

st.caption(
    "🌿 PurityPathAI | Powered by responsible AI and human connection."
)