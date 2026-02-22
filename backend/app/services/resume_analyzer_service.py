import json
import google.generativeai as genai
from app.schemas.resume_analysis import ResumeAnalysisResult
from app.core.config import settings


class ResumeAnalyzerService:
    @staticmethod
    def analyze_resume(text: str) -> ResumeAnalysisResult:
        # 1️⃣ Validate API key
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. Please check your .env file."
            )

        # 2️⃣ Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # 3️⃣ CREATE the model (THIS WAS MISSING)
        model = genai.GenerativeModel("models/gemini-flash-lite-latest")

        # 4️⃣ Prompt
        prompt = f"""
You are an AI resume analyzer.

Extract the following from the resume text:
1. Technical skills (list of strings)
2. Total years of professional experience (number, estimate if needed)
3. Primary job role/title

Return ONLY valid JSON in this format:
{{
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "experience_years": 2.5,
  "role": "Software Engineer"
}}

Resume text:
{text}
"""

        try:
            response = model.generate_content(prompt)
            raw_text = response.text.strip()

            # 5️⃣ Clean markdown if Gemini wraps JSON
            if raw_text.startswith("```"):
                raw_text = raw_text.strip("```").replace("json", "").strip()

            data = json.loads(raw_text)
            return ResumeAnalysisResult(**data)

        except Exception as e:
            raise ValueError(f"Failed to analyze resume with Gemini API: {str(e)}")
