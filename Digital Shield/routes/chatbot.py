from flask import Blueprint, jsonify, request, session
from logic.fsm import ChatbotFSM, load_scenarios
import time

chatbot_bp = Blueprint('chatbot', __name__)

# Load scenarios once when the blueprint is initialized
SCENARIOS = load_scenarios()

# Session timeout in seconds (5 minutes as per Readme)
SESSION_TIMEOUT = 5 * 60

@chatbot_bp.before_request
def before_request():
    """
    Handle session management before each request.
    Resets session if timed out or if no scenario is active.
    """
    last_active = session.get('last_active', 0)
    if time.time() - last_active > SESSION_TIMEOUT:
        session.clear()
        session['active_scenario_id'] = None
    session['last_active'] = time.time()

@chatbot_bp.route('/start', methods=['POST'])
def start_chat():
    """
    Starts a new chat session with a selected scenario.
    """
    data = request.get_json()
    scenario_id = data.get('scenario_id')

    if not scenario_id or scenario_id not in SCENARIOS:
        return jsonify({"error": "Invalid scenario ID"}), 400

    scenario_data = SCENARIOS[scenario_id]
    fsm = ChatbotFSM(scenario_data)

    # Store FSM state in session
    session['active_scenario_id'] = scenario_id
    session['fsm_current_state_key'] = fsm.current_state_key

    return jsonify({
        "message": fsm.get_current_message(),
        "options": fsm.get_current_options(),
        "terminal": fsm.is_terminal(),
        "scenario_name": scenario_data['name']
    })

@chatbot_bp.route('/respond', methods=['POST'])
def respond_to_chat():
    """
    Responds to user input and transitions the FSM.
    """
    user_input = request.get_json().get('input')
    scenario_id = session.get('active_scenario_id')
    fsm_current_state_key = session.get('fsm_current_state_key')

    if not scenario_id or not fsm_current_state_key:
        return jsonify({"error": "No active chat session. Please start a new chat."}), 400

    scenario_data = SCENARIOS.get(scenario_id)
    if not scenario_data:
        return jsonify({"error": "Active scenario not found."}), 400

    # Reconstruct FSM state from session
    fsm = ChatbotFSM(scenario_data)
    fsm.current_state_key = fsm_current_state_key
    fsm.current_state = scenario_data["states"][fsm_current_state_key]

    if fsm.transition(user_input):
        session['fsm_current_state_key'] = fsm.current_state_key
        response_data = {
            "message": fsm.get_current_message(),
            "options": fsm.get_current_options(),
            "terminal": fsm.is_terminal()
        }
        if fsm.is_terminal():
            response_data["actions"] = fsm.get_actions()
            session.clear() # Clear session after terminal state
        return jsonify(response_data)
    else:
        return jsonify({"error": "Invalid option or transition."}), 400

@chatbot_bp.route('/current_state', methods=['GET'])
def get_current_chat_state():
    """
    Retrieves the current state of the active chat session.
    """
    scenario_id = session.get('active_scenario_id')
    fsm_current_state_key = session.get('fsm_current_state_key')

    if not scenario_id or not fsm_current_state_key:
        return jsonify({"message": "No active chat session. Please start a new chat.", "options": [], "terminal": False}), 200

    scenario_data = SCENARIOS.get(scenario_id)
    if not scenario_data:
        session.clear()
        return jsonify({"error": "Active scenario not found, session cleared."}), 400

    # Reconstruct FSM state from session
    fsm = ChatbotFSM(scenario_data)
    fsm.current_state_key = fsm_current_state_key
    fsm.current_state = scenario_data["states"][fsm_current_state_key]

    response_data = {
        "message": fsm.get_current_message(),
        "options": fsm.get_current_options(),
        "terminal": fsm.is_terminal(),
        "scenario_name": scenario_data['name']
    }
    if fsm.is_terminal():
        response_data["actions"] = fsm.get_actions()
    return jsonify(response_data)

@chatbot_bp.route('/scenarios', methods=['GET'])
def get_scenarios():
    """
    Returns a list of available scenario IDs and names.
    """
    if SCENARIOS:
        return jsonify([{"id": s_id, "name": SCENARIOS[s_id]["name"]} for s_id in SCENARIOS]), 200
    return jsonify([]), 200

@chatbot_bp.route('/end_session', methods=['POST'])
def end_chat_session():
    """
    Ends the current chat session by clearing the session data.
    """
    session.clear()
    session['active_scenario_id'] = None
    return jsonify({"message": "Chat session ended."}), 200