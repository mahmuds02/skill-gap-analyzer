from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from app.models import (
    create_analysis, create_skill, get_analysis_by_session, 
    get_recent_analyses, generate_session_id
)
from app.ai_service import (
    extract_skills_from_job, analyze_resume_against_skills
)
from app.utils import extract_text_from_pdf, allowed_file

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page - upload resume and paste job description"""
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    """Process resume and job description analysis"""
    try:
        # Get form data
        resume_text = request.form.get('resume_text', '').strip()
        job_description = request.form.get('job_description', '').strip()
        job_title = request.form.get('job_title', 'Job Position').strip()
        
        # Check if PDF was uploaded
        resume_file = request.files.get('resume_file')
        
        # Extract text from PDF if uploaded
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join('uploads', filename)
            resume_file.save(filepath)
            
            # Extract text from PDF
            pdf_text = extract_text_from_pdf(filepath)
            
            # Use PDF text if resume_text is empty
            if not resume_text:
                resume_text = pdf_text
            
            # Delete uploaded file after extraction (privacy)
            os.remove(filepath)
        
        # Validate inputs
        if not resume_text or not job_description:
            flash('Please provide both resume and job description', 'error')
            return redirect(url_for('main.index'))
        
        # Step 1: Extract skills from job description using AI
        print("🔍 Extracting skills from job posting...")
        required_skills = extract_skills_from_job(job_description)
        
        if not required_skills:
            flash('Could not extract skills from job description. Please try again.', 'error')
            return redirect(url_for('main.index'))
        
        print(f"✅ Found {len(required_skills)} required skills")
        
        # Step 2: Analyze resume against required skills using AI
        print("🔍 Analyzing resume...")
        analysis_result = analyze_resume_against_skills(resume_text, required_skills)
        
        skill_analysis = analysis_result.get('skill_analysis', [])
        match_percentage = analysis_result.get('match_percentage', 0)
        ai_feedback = analysis_result.get('feedback', '')
        
        # Calculate statistics
        total_skills = len(skill_analysis)
        skills_matched = sum(1 for s in skill_analysis if s['status'] == 'present')
        skills_missing = sum(1 for s in skill_analysis if s['status'] == 'missing')
        
        # Step 3: Save to database
        session_id = generate_session_id()
        
        analysis_id = create_analysis(
            session_id=session_id,
            job_title=job_title,
            match_percentage=match_percentage,
            total_skills_required=total_skills,
            total_skills_matched=skills_matched,
            total_skills_missing=skills_missing,
            ai_feedback=ai_feedback,
            model_name='gemini-2.5-flash'
        )
        
        # Save individual skills
        for skill_item in skill_analysis:
            create_skill(
                analysis_id=analysis_id,
                skill_name=skill_item['skill'],
                status=skill_item['status'],
                found_in_resume=(skill_item['status'] == 'present')
            )
        
        print(f"✅ Analysis saved with session ID: {session_id}")
        
        # Redirect to results page
        return redirect(url_for('main.results', session_id=session_id))
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        flash(f'An error occurred during analysis: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main.route('/results/<session_id>')
def results(session_id):
    """Display analysis results"""
    analysis = get_analysis_by_session(session_id)
    
    if not analysis:
        flash('Analysis not found', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('results.html', analysis=analysis)

@main.route('/history')
def history():
    """Show recent analyses"""
    recent = get_recent_analyses(limit=20)
    return render_template('history.html', analyses=recent)

@main.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
