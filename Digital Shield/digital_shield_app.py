"""
Digital Shield - Flask Application Entry Point
TFGBV Response Tool for African Digital Spaces

Author: Eng. Stephen Odhiambo, Kenyan AI & Software Engineer
Privacy-by-design, mobile-first, security-hardened MVP
"""

from flask import Flask, render_template, session
from datetime import timedelta
import os
import json

# Import blueprints
from routes.chatbot import chatbot_bp
from routes.literacy import literacy_bp
from routes.health import health_bp

# Import configuration
from config import Config

def create_app():
    """Application factory pattern for Flask app initialization"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Configure session for privacy and security
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
    app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # 5-minute auto-expire
    
    # Security headers middleware
    @app.after_request
    def set_security_headers(response):
        """Apply Content Security Policy and security headers"""
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response
    
    # Register blueprints
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(literacy_bp, url_prefix='/api/literacy')
    app.register_blueprint(health_bp)
    
    # Main routes
    @app.route('/')
    def index():
        """Landing page - Entry point for users"""
        return render_template('index.html')
    
    @app.route('/chatbot')
    def chatbot_page():
        """Emergency triage chatbot interface"""
        # Initialize ephemeral session
        session.permanent = True
        return render_template('chatbot.html')
    
    @app.route('/literacy')
    def literacy_page():
        """Digital literacy guide interface"""
        return render_template('literacy.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        """Custom 404 handler"""
        return render_template('index.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        """Custom 500 handler - fail gracefully"""
        return {'error': 'Service temporarily unavailable'}, 500
    
    return app

# Application initialization
app = create_app()

if __name__ == '__main__':
    # Development server (Docker will use gunicorn in production)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )