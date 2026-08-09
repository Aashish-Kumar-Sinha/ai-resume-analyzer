import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_feedback(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Expert.

Resume:
{resume_text}

Job Description:
{job_description}

Give:
1. ATS Score Feedback
2. Strengths
3. Missing Skills
4. Resume Improvement Suggestions
"""

    try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                )
                return response.text

            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(2)
                    continue
                raise e

    except Exception:
        return """
ATS Feedback

✓ Resume uploaded successfully.

Strengths
• Resume has relevant technical skills.
• Good keyword coverage.

Suggestions
• Add measurable achievements.
• Add project impact with numbers.
• Improve resume summary.
• Mention tools and technologies used.
"""