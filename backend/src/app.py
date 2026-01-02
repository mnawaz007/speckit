"""
Flask application factory and configuration.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Configuration
    app.config['DEBUG'] = os.getenv('FLASK_ENV', 'development') == 'development'
    app.config['TESTING'] = False

    # Enable CORS for frontend requests
    # In development, allow all origins from localhost:5173
    # In production, restrict to specific domain
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173')
    CORS(app, resources={r'/api/*': {'origins': cors_origins.split(',')}})

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints (will add later when API routes are ready)
    # from .api.calculator import bp as calculator_bp
    # app.register_blueprint(calculator_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200

    return app


def register_error_handlers(app):
    """
    Register error handlers for consistent error responses.

    Args:
        app (Flask): Flask application instance
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': str(error.description or 'Bad request')
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        return jsonify({
            'error': 'Internal server error'
        }), 500
