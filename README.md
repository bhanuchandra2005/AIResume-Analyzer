# Resume AI Analyzer

A Streamlit application that analyzes resumes against job descriptions using Google's Gemini AI.

## Features

- Upload your resume in PDF format
- Paste a job description
- Get an AI-powered analysis of how well your resume matches the job
- Receive suggestions for improvement
- Calculate match percentage and identify skill gaps

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI API key
- pdf2image library with poppler-utils

## Deployment Instructions

### Local Development

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Install poppler:
   - **Windows**: Download and install from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
   - **macOS**: `brew install poppler`
   - **Ubuntu/Debian**: `apt-get install poppler-utils`

4. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. Push your code to a GitHub repository

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)

3. Click "New app" and select your repository

4. Configure the deployment:
   - Set the main file path to: `app.py`
   - Add the required secrets:
     - `GOOGLE_API_KEY`: Your Google Gemini API key

5. Advanced Settings:
   - Add the following packages to the requirements section:
     ```
     streamlit==1.44.1
     google-generativeai==0.8.4
     pdf2image==1.17.0
     pillow==11.1.0
     python-dotenv==1.1.0
     ```
   - For Streamlit Cloud, add this to the "packages" section:
     ```
     poppler-utils
     ```

6. Click "Deploy"

## Usage

1. Enter a job description in the left panel
2. Upload your resume (PDF format) on the right panel
3. Choose either "Analyze Resume" or "Calculate Match" to get results

## API Key Setup

To get a Google Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Navigate to "Get API key" in the settings
4. Create a new API key and copy it
5. Add it to your environment variables or .env file

## License

This project is licensed under the MIT License - see the LICENSE file for details. 