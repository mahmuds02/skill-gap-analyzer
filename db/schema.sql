-- Drop tables if they exist (for fresh start)
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS analyses CASCADE;

-- Analyses table: stores each resume analysis session
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_name VARCHAR(100) DEFAULT 'gemini-2.5-flash',
    match_percentage DECIMAL(5,2),
    total_skills_required INTEGER,
    total_skills_matched INTEGER,
    total_skills_missing INTEGER,
    job_title VARCHAR(500),
    ai_feedback TEXT
);

-- Skills table: stores individual skill analysis results
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    analysis_id INTEGER REFERENCES analyses(id) ON DELETE CASCADE,
    skill_name VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('present', 'missing', 'partial')),
    found_in_resume BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_analyses_session_id ON analyses(session_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_skills_analysis_id ON skills(analysis_id);
CREATE INDEX idx_skills_status ON skills(status);

-- Create a view for easy querying
CREATE VIEW analysis_summary AS
SELECT 
    a.session_id,
    a.created_at,
    a.match_percentage,
    a.job_title,
    COUNT(s.id) as total_skills_analyzed,
    SUM(CASE WHEN s.status = 'present' THEN 1 ELSE 0 END) as skills_present,
    SUM(CASE WHEN s.status = 'missing' THEN 1 ELSE 0 END) as skills_missing,
    SUM(CASE WHEN s.status = 'partial' THEN 1 ELSE 0 END) as skills_partial
FROM analyses a
LEFT JOIN skills s ON a.id = s.analysis_id
GROUP BY a.id, a.session_id, a.created_at, a.match_percentage, a.job_title;
