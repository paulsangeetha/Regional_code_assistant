import os
import requests
import streamlit as st

# ----------------------------
# CONFIG
# ----------------------------
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"

SUPPORTED_LANGUAGES = {
    'en-IN': 'English',
    'hi-IN': 'हिंदी',
    'ta-IN': 'தமிழ்',
    'te-IN': 'తెలుగు',
    'bn-IN': 'বাংলা',
    'kn-IN': 'ಕನ್ನಡ'
}

SYSTEM_PROMPTS = {
    'concept_explanation': "Explain simply with examples.",
    'code_debugging': "Find bugs, fix code, explain clearly.",
    'code_sample': "Provide clean, well-commented code."
}

# ----------------------------
# API CLASS
# ----------------------------
class CodingAssistant:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SARVAM_API_KEY}",
            "Content-Type": "application/json"
        }

    def call_sarvam_api(self, messages):
        try:
            payload = {
                "messages": messages,
                "model": "sarvam-m",
                "temperature": 0.7
            }

            response = requests.post(
                SARVAM_API_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def explain_concept(self, concept, language):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS['concept_explanation']},
            {"role": "user", "content": f"Explain {concept} in {SUPPORTED_LANGUAGES[language]} with example"}
        ]
        return self.call_sarvam_api(messages)

    def debug_code(self, code, language):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS['code_debugging']},
            {"role": "user", "content": f"Debug this code in {SUPPORTED_LANGUAGES[language]}:\n{code}"}
        ]
        return self.call_sarvam_api(messages)

    def provide_code_sample(self, topic, language):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS['code_sample']},
            {"role": "user", "content": f"Provide code for {topic} in {SUPPORTED_LANGUAGES[language]}"}
        ]
        return self.call_sarvam_api(messages)

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="AI Coding Assistant", page_icon="👩‍💻")

st.title("👩‍💻 AI Coding Assistant for Indian Students")

# Check API key
if not SARVAM_API_KEY:
    st.error("❌ SARVAM_API_KEY not found. Please set it in environment variables.")
    st.stop()

assistant = CodingAssistant()

# Language selection
language = st.selectbox(
    "🌐 Select Language",
    options=list(SUPPORTED_LANGUAGES.keys()),
    format_func=lambda x: SUPPORTED_LANGUAGES[x]
)

# Feature selection
feature = st.radio(
    "⚙️ Choose Task",
    ["Explain Concept", "Debug Code", "Code Sample"]
)

# ----------------------------
# FEATURES
# ----------------------------
if feature == "Explain Concept":
    concept = st.text_input("📘 Enter concept")

    if st.button("Explain"):
        if concept.strip():
            with st.spinner("Thinking..."):
                result = assistant.explain_concept(concept, language)
                st.markdown(result)
        else:
            st.warning("Please enter a concept")

elif feature == "Debug Code":
    code = st.text_area("💻 Paste your code")

    if st.button("Debug"):
        if code.strip():
            with st.spinner("Analyzing..."):
                result = assistant.debug_code(code, language)
                st.markdown(result)
        else:
            st.warning("Please enter code")

else:
    topic = st.text_input("🧠 Enter topic")

    if st.button("Generate"):
        if topic.strip():
            with st.spinner("Generating..."):
                result = assistant.provide_code_sample(topic, language)
                st.markdown(result)
        else:
            st.warning("Please enter a topic")