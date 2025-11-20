from flask import Blueprint, jsonify
from logic.fsm import load_scenarios # Assuming this will be used for data_files check
# from logic.session_manager import SessionManager # Assuming session manager will track active sessions

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    # Placeholder for checking if scenarios.json is loaded
    scenarios_loaded = True if load_scenarios() else False
    
    # Placeholder for active sessions (will integrate with SessionManager later)
    active_sessions_count = 0 
    # if SessionManager:
    #     active_sessions_count = SessionManager.get_active_sessions_count()

    return jsonify({
        "status": "healthy",
        "service": "Digital Shield",
        "data_files": {
            "scenarios": scenarios_loaded,
            "literacy": True # Placeholder, assuming literacy data is always available
        },
        "active_sessions": active_sessions_count
    })