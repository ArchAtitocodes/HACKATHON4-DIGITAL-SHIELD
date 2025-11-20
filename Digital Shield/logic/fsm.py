import json
import os

class ChatbotFSM:
    def __init__(self, scenario_data):
        """
        Initializes the FSM with data for a specific scenario.
        :param scenario_data: Dictionary containing the scenario's states and actions.
        """
        self.scenario_data = scenario_data
        self.current_state_key = "start"
        self.current_state = self.scenario_data["states"]["start"]

    def get_current_message(self):
        """
        Returns the message of the current state.
        """
        return self.current_state["message"]

    def get_current_options(self):
        """
        Returns the options available from the current state.
        """
        return self.current_state.get("options", [])

    def transition(self, user_input):
        """
        Transitions the FSM to the next state based on user input.
        :param user_input: The user's choice, corresponding to an option.
        :return: True if transition successful, False otherwise.
        """
        if "next_state" in self.current_state:
            next_state_key = self.current_state["next_state"].get(user_input)
            if next_state_key and next_state_key in self.scenario_data["states"]:
                self.current_state_key = next_state_key
                self.current_state = self.scenario_data["states"][next_state_key]
                return True
        return False

    def is_terminal(self):
        """
        Checks if the current state is a terminal state.
        """
        return self.current_state.get("terminal", False)

    def get_actions(self):
        """
        Returns the actions associated with the scenario if the current state is terminal.
        """
        if self.is_terminal():
            return self.scenario_data.get("actions", [])
        return []

def load_scenarios(file_path="data/scenarios_json.json"):
    """
    Loads scenario data from a JSON file.
    :param file_path: Path to the JSON file.
    :return: Dictionary of scenarios or None if file not found/invalid.
    """
    try:
        current_dir = os.path.dirname(__file__)
        # Adjust path for when the function is called from app.py or routes
        abs_file_path = os.path.join(current_dir, '..', file_path)
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Scenario file not found at {abs_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {abs_file_path}")
        return None
