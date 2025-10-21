import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
import uuid
from datetime import datetime

def get_db_connection():
    """Create database connection"""
    conn = psycopg2.connect(
        current_app.config['DATABASE_URL'],
        cursor_factory=RealDictCursor
    )
    return conn

def create_analysis(session_id, job_title, match_percentage, total_skills_required, 
                   total_skills_matched, total_skills_missing, ai_feedback, model_name):
    """Create a new analysis record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO analyses 
        (session_id, job_title, match_percentage, total_skills_required, 
         total_skills_matched, total_skills_missing, ai_feedback, model_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (session_id, job_title, match_percentage, total_skills_required,
          total_skills_matched, total_skills_missing, ai_feedback, model_name))
    
    analysis_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    
    return analysis_id

def create_skill(analysis_id, skill_name, status, found_in_resume):
    """Create a skill record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO skills (analysis_id, skill_name, status, found_in_resume)
        VALUES (%s, %s, %s, %s)
    """, (analysis_id, skill_name, status, found_in_resume))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_analysis_by_session(session_id):
    """Get analysis by session ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM analyses WHERE session_id = %s
    """, (session_id,))
    
    analysis = cursor.fetchone()
    
    if analysis:
        # Get skills for this analysis
        cursor.execute("""
            SELECT * FROM skills WHERE analysis_id = %s
            ORDER BY status DESC, skill_name
        """, (analysis['id'],))
        
        skills = cursor.fetchall()
        analysis['skills'] = skills
    
    cursor.close()
    conn.close()
    
    return analysis

def get_recent_analyses(limit=10):
    """Get recent analyses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT session_id, created_at, job_title, match_percentage
        FROM analyses
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    
    analyses = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return analyses

def generate_session_id():
    """Generate unique session ID"""
    return str(uuid.uuid4())
