from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
import datetime

# Page configuration
st.set_page_config(
    page_title="Resume AI Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with a lighter, more modern theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #3E64FF;
        --secondary-color: #5EDFFF;
        --accent-color: #FF9190;
        --text-color: #2D3748;
        --light-bg: #F9FAFE;
        --card-bg: #FFFFFF;
        --border-color: #E2E8F0;
    }
    
    /* Typography */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .tagline {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: var(--primary-color);
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(62, 100, 255, 0.15);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(62, 100, 255, 0.2);
    }
    
    /* Cards and sections */
    .upload-section {
        background-color: var(--card-bg);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-color);
    }
    
    .result-section {
        background-color: var(--card-bg);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding: 2rem 0;
        background-color: var(--light-bg);
        border-top: 1px solid var(--border-color);
        text-align: center;
    }
    
    .footer-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .footer-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .footer-text {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .footer-link {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer-copyright {
        color: #A0AEC0;
        font-size: 0.8rem;
    }
    
    /* Streamlit element customization */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0;
        max-width: 1200px;
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    /* Main page background */
    .main {
        background-color: var(--light-bg);
    }
    
    /* Success message */
    .stSuccess {
        background-color: #E6FFFA;
        color: #2C7A7B;
        border: 1px solid #81E6D9;
        border-radius: 8px;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed var(--border-color);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary-color);
    }
    
    /* Info box */
    .feature-box {
        background-color: #EBF4FF;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Preview box */
    .preview-box {
        background-color: #F7FAFC;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid var(--border-color);
    }
</style>
""", unsafe_allow_html=True)

# Configure the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Fallback to hardcoded key if environment variable is not set
    genai.configure(api_key="AIzaSyDydWxM_3IoML4ZPSe-YAlBQOZvXGCz8PI")

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        # Define poppler path - adjust this to your actual installation path
        poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"
        
        # Explicitly provide the poppler_path
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# App header section
st.markdown('<div class="main-header">Resume AI Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Powered by AI to help you land your dream job</div>', unsafe_allow_html=True)

# Feature boxes with improved contrast
st.markdown("""
<div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
    <div style="background-color: #E6F0FF; border-radius: 8px; padding: 1.2rem; margin-bottom: 1rem; border-left: 4px solid #3E64FF; flex: 1;">
        <div style="font-weight: 600; color: #3E64FF; margin-bottom: 0.5rem; font-size: 1.1rem;">📊 ATS Compatibility</div>
        <p style="color: #2D3748; font-size: 0.95rem; line-height: 1.5;">Check how well your resume aligns with job requirements and ATS systems</p>
    </div>
    <div style="background-color: #FFF0F0; border-radius: 8px; padding: 1.2rem; margin-bottom: 1rem; border-left: 4px solid #FF6B6B; flex: 1;">
        <div style="font-weight: 600; color: #FF6B6B; margin-bottom: 0.5rem; font-size: 1.1rem;">🎯 Skills Gap Analysis</div>
        <p style="color: #2D3748; font-size: 0.95rem; line-height: 1.5;">Identify missing skills and keywords that could improve your chances</p>
    </div>
    <div style="background-color: #F0F8FF; border-radius: 8px; padding: 1.2rem; margin-bottom: 1rem; border-left: 4px solid #4CAF50; flex: 1;">
        <div style="font-weight: 600; color: #4CAF50; margin-bottom: 0.5rem; font-size: 1.1rem;">✨ Expert Recommendations</div>
        <p style="color: #2D3748; font-size: 0.95rem; line-height: 1.5;">Get personalized suggestions to enhance your resume for specific roles</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="sub-header">Job Description</div>', unsafe_allow_html=True)
    input_text = st.text_area(
        "Paste the job description here",
        height=250,
        key="input",
        help="Copy and paste the entire job description from the posting"
    )

with col2:
    st.markdown('<div class="sub-header">Your Resume</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("✅ Resume uploaded successfully!")
        try:
            # Display a preview of the first page
            poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"
            images = pdf2image.convert_from_bytes(uploaded_file.getvalue(), poppler_path=poppler_path)
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)
            st.image(images[0], width=300, caption="Resume Preview")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not preview resume: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

# Action buttons in a centered layout
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        submit1 = st.button("✨ Analyze Resume", use_container_width=True)
    with col_btn2:
        submit3 = st.button("📊 Calculate Match", use_container_width=True)

input_prompt1 = """
You are an experienced Technical Human Resource Manager with expertise in resume evaluation. 
Your task is to review the provided resume against the job description.
Please provide a structured analysis including:
1. Overall alignment of the candidate's profile with the role
2. Key strengths that make the candidate a good fit
3. Areas where the candidate's experience or skills may be lacking
4. Specific recommendations to improve the resume for this position
5. Conclude with a final assessment of fit
"""

input_prompt3 = """
You are an advanced ATS (Applicant Tracking System) analyzer with deep understanding of recruiting technology.
Evaluate the resume against the job description and provide:
1. An overall match percentage (0-100%)
2. Key matching keywords and skills found in both the resume and job description
3. Important keywords or skills mentioned in the job description but missing from the resume
4. Recommendations for improving resume match rate
Format your response with clear sections and bullet points for readability.
"""

# Results section
if submit1 or submit3:
    if not input_text.strip():
        st.error("⚠️ Please enter a job description before analyzing.")
    elif uploaded_file is None:
        st.error("⚠️ Please upload your resume before analyzing.")
    else:
        with st.spinner("Analyzing your resume... This may take a few moments."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.markdown('<div class="sub-header">Analysis Results</div>', unsafe_allow_html=True)
                
                if submit1:
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                    st.markdown("### Resume Evaluation")
                elif submit3:
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                    st.markdown("### Match Assessment")
                
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# Enhanced footer section with team info
st.markdown("<hr>", unsafe_allow_html=True)
footer_container = st.container()
with footer_container:
    # App title and description
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #3E64FF; font-size: 1.2rem;'>Resume AI Analyzer</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #718096; font-size: 0.9rem;'>This tool uses advanced AI to analyze resumes against job descriptions and provide actionable feedback.</p>", unsafe_allow_html=True)
    
    # Mentor section - moved above team members
    st.markdown("<h4 style='text-align: center; color: #3E64FF; margin-top: 20px; font-size: 1.1rem;'>Mentor</h4>", unsafe_allow_html=True)
    
    mentor_col1, mentor_col2, mentor_col3 = st.columns([1, 1, 1])
    with mentor_col2:
        st.markdown("<div style='background-color: #E6F0FF; padding: 10px; border-radius: 8px; text-align: center; border-left: 4px solid #3E64FF;'><p style='font-weight: 600; color: #3E64FF; margin-bottom: 5px;'>Prathiba Swaraj</p><p style='color: #718096; font-size: 0.8rem;'>Project Mentor</p></div>", unsafe_allow_html=True)
    
    # Team section - after mentor
    st.markdown("<h4 style='text-align: center; color: #3E64FF; margin-top: 20px; font-size: 1.1rem;'>Team Members</h4>", unsafe_allow_html=True)
    
    team_cols = st.columns(3)
    with team_cols[0]:
        st.markdown("<div style='background-color: #E6F0FF; padding: 10px; border-radius: 8px; text-align: center; border-left: 4px solid #3E64FF;'><p style='font-weight: 600; color: #3E64FF; margin-bottom: 5px;'>Srakshin Chityala</p><p style='color: #718096; font-size: 0.8rem;'>Roll No: 23241A3321</p></div>", unsafe_allow_html=True)
    
    with team_cols[1]:
        st.markdown("<div style='background-color: #E6F0FF; padding: 10px; border-radius: 8px; text-align: center; border-left: 4px solid #3E64FF;'><p style='font-weight: 600; color: #3E64FF; margin-bottom: 5px;'>Bhanu Chandra Megharaj</p><p style='color: #718096; font-size: 0.8rem;'>Roll No: 23241A3338</p></div>", unsafe_allow_html=True)
    
    with team_cols[2]:
        st.markdown("<div style='background-color: #E6F0FF; padding: 10px; border-radius: 8px; text-align: center; border-left: 4px solid #3E64FF;'><p style='font-weight: 600; color: #3E64FF; margin-bottom: 5px;'>Akshaj</p><p style='color: #718096; font-size: 0.8rem;'>Roll No: 23241A3303</p></div>", unsafe_allow_html=True)
    
    # Copyright - removed links section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_year = datetime.datetime.now().year
        st.markdown(f"<p style='text-align: center; color: #A0AEC0; font-size: 0.8rem;'>© {current_year} Resume AI Analyzer. All rights reserved.</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #718096; font-size: 0.8rem;'>Powered by Google Gemini AI</p>", unsafe_allow_html=True)




