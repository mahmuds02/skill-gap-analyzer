import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask configuration"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_URL = os.getenv('DATABASE_URL')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # AI Model settings
    AI_MODEL = 'gemini-2.5-flash'
    
    # Logging
    LOG_FILE = 'logs/app.log'
