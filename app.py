import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey! Act like a seasoned ATS (Application Tracking System) with a deep understanding of the tech industry, specifically in software engineering. Your task is to evaluate the resume based on the provided job description, focusing on software engineering skills and experience. Consider the competitiveness of the job market and provide comprehensive assistance for improving the resumes. Assign a percentage match based on the JD and identify any missing keywords with high accuracy.

Resume:
{text}

Job Description:
{jd}

Please provide your response in a single string with the following structure:
{{"JD Match": "%", "Missing Keywords": [], "Profile Summary": ""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt.format(text=text, jd=jd))
        st.subheader(response)
