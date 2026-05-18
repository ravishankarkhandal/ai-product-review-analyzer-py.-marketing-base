# AI Product Review Analyzer

AI Product Review Analyzer is a powerful tool that collects product reviews from **Google, YouTube, and Amazon** and analyzes them using **Gemini** and **Groq** AI models to provide brutally honest insights, including critical flaws, pros, and a final verdict.

## Features
- 🔍 Collects real-time reviews from top sources (Google, YouTube, Amazon).
- 🤖 Analyzes sentiment and extracts flaws/pros using **Google Gemini** and **Groq** models.
- 💻 Offers both a Command-Line Interface (CLI) and a Web-based Interface (Streamlit).

## Prerequisites
Make sure you have API keys for:
- Google Custom Search API
- YouTube Data API v3
- Google Gemini API
- Groq API

## Installation
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   ```
2. Navigate to the project directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_google_cse_id_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage
**1. For CLI Application:**  
Run `python main.py`

**2. For Web Interface (Streamlit):**  
Run `streamlit run app.py`