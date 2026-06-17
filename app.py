import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KHAN SIR BADNAPUR AI Office Assistant")

# Streamlit Secret se API key lena
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("KHAN SIR BADNAPUR OFFICE AI ASSISTANT")

task = st.selectbox(
    "Select Task",
    [
        "Letter Drafting",
        "GR Analysis",
        "Note Sheet",
        "WhatsApp Message"
    ]
)

text = st.text_area("Enter details")

if st.button("Generate") and text:

    prompt = f"""
    You are an expert Government Office Assistant.

    Task Type: {task}

    Rules:
    - Use official Marathi language.
    - Generate complete output.
    - For letters include Subject, Reference and Main Body.
    - For WhatsApp create concise official messages.
    - For Note Sheet use government format.

    User Request:
    {text}
    """

    response = model.generate_content(prompt)

    st.write(response.text)
