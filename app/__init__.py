from flask import Flask
import os

def create_app():
    """Application factory"""
    # Specify template and static folders explicitly
    template_dir = os.path.abspath('templates')
    static_dir = os.path.abspath('static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Load config
    app.config.from_object('config.Config')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app
