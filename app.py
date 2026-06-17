
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BDO Office AI Assistant")

st.title("BDO Office AI Assistant")

api_key = st.text_input("Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

task = st.selectbox(
    "Select Task",
    ["Letter Drafting", "GR Analysis", "Note Sheet", "WhatsApp Message"]
)

text = st.text_area("Enter details")

if st.button("Generate") and api_key and text:
    prompt = f"Government office task: {task}\n\n{text}"
    response = model.generate_content(prompt)
    st.write(response.text)
