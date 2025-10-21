import google.generativeai as genai
import json
from flask import current_app

def configure_gemini():
    """Configure Gemini API"""
    api_key = current_app.config['GEMINI_API_KEY']
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(current_app.config['AI_MODEL'])

def extract_skills_from_job(job_description):
    """Extract required skills from job posting using AI"""
    model = configure_gemini()
    
    prompt = f"""
    Analyze this job posting and extract ONLY the technical and professional skills required.
    Return a JSON array of skill names only.
    
    Rules:
    - Extract specific, measurable skills (e.g., "Python", "SQL", "Project Management")
    - Ignore soft skills like "team player" or "good communicator"
    - Return 5-15 most important skills
    - Format: ["skill1", "skill2", "skill3"]
    
    Job Posting:
    {job_description}
    
    Respond with ONLY a valid JSON array, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        # Parse JSON response
        skills_text = response.text.strip()
        # Remove markdown code blocks if present
        skills_text = skills_text.replace('```json', '').replace('```', '').strip()
        skills = json.loads(skills_text)
        return skills
    except Exception as e:
        print(f"Error extracting skills: {e}")
        return []

def analyze_resume_against_skills(resume_text, required_skills):
    """Analyze resume to find which skills are present, missing, or partial"""
    model = configure_gemini()
    
    prompt = f"""
    You are analyzing a resume against required job skills.
    
    Required Skills: {json.dumps(required_skills)}
    
    Resume:
    {resume_text}
    
    For each required skill, determine:
    - "present" if clearly demonstrated in the resume
    - "partial" if somewhat related experience exists
    - "missing" if not found at all
    
    Return a JSON object with this structure:
    {{
      "skill_analysis": [
        {{"skill": "Python", "status": "present", "evidence": "Built data pipeline using Python"}},
        {{"skill": "SQL", "status": "missing", "evidence": ""}},
        {{"skill": "Excel", "status": "partial", "evidence": "Mentioned data analysis"}}
      ],
      "match_percentage": 75,
      "feedback": "You have strong Python skills. Consider adding SQL projects to your resume."
    }}
    
    Respond with ONLY valid JSON, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        # Remove markdown code blocks
        result_text = result_text.replace('```json', '').replace('```', '').strip()
        result = json.loads(result_text)
        return result
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return {
            "skill_analysis": [],
            "match_percentage": 0,
            "feedback": "Error analyzing resume. Please try again."
        }

def generate_feedback(skill_analysis, match_percentage):
    """Generate personalized feedback based on analysis"""
    model = configure_gemini()
    
    present_skills = [s['skill'] for s in skill_analysis if s['status'] == 'present']
    missing_skills = [s['skill'] for s in skill_analysis if s['status'] == 'missing']
    partial_skills = [s['skill'] for s in skill_analysis if s['status'] == 'partial']
    
    prompt = f"""
    Generate encouraging, actionable career advice for a job seeker.
    
    Match Rate: {match_percentage}%
    Skills They Have: {', '.join(present_skills)}
    Skills Missing: {', '.join(missing_skills)}
    Partial Skills: {', '.join(partial_skills)}
    
    Write 2-3 sentences of positive, specific advice. Focus on:
    1. What they're doing well
    2. What to learn next
    3. How to improve their resume
    
    Keep it motivational and specific. No more than 100 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Keep building your skills and tailoring your resume to match job requirements!"
