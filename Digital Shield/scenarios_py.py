"""
Scenario Definitions Module
This module is currently unused in the MVP as scenarios are loaded from JSON.
It can be used in future versions for programmatic scenario generation or validation.

Author: Eng. Stephen Odhiambo, Kenyan AI & Software Engineer
"""

from typing import Dict, List


class ScenarioDefinition:
    """
    Base class for scenario definitions
    Can be extended for programmatic scenario creation
    """
    
    def __init__(self, scenario_id: str, name: str, description: str):
        self.scenario_id = scenario_id
        self.name = name
        self.description = description
        self.states = {}
        self.actions = []
    
    def add_state(self, state_id: str, state_data: Dict):
        """Add a state to the scenario"""
        self.states[state_id] = state_data
    
    def add_action(self, action_data: Dict):
        """Add an action to the scenario"""
        self.actions.append(action_data)
    
    def to_dict(self) -> Dict:
        """Convert scenario to dictionary format"""
        return {
            'id': self.scenario_id,
            'name': self.name,
            'description': self.description,
            'states': self.states,
            'actions': self.actions
        }


# Scenario validation utilities
def validate_scenario_structure(scenario: Dict) -> bool:
    """
    Validate that a scenario has the required structure
    
    Args:
        scenario: Scenario dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['id', 'name', 'description', 'states', 'actions']
    
    # Check top-level keys
    if not all(key in scenario for key in required_keys):
        return False
    
    # Check that states exist
    if 'start' not in scenario['states']:
        return False
    
    # Check state structure
    for state_id, state in scenario['states'].items():
        if 'message' not in state:
            return False
    
    # Check actions structure
    for action in scenario['actions']:
        if not all(key in action for key in ['priority', 'category', 'title', 'steps', 'why']):
            return False
    
    return True


def get_scenario_metadata(scenario: Dict) -> Dict:
    """
    Extract metadata from a scenario
    
    Args:
        scenario: Scenario dictionary
        
    Returns:
        Dictionary with scenario metadata
    """
    return {
        'id': scenario.get('id'),
        'name': scenario.get('name'),
        'description': scenario.get('description'),
        'num_states': len(scenario.get('states', {})),
        'num_actions': len(scenario.get('actions', []))
    }


# Example scenario builder (for future use)
def create_example_scenario() -> ScenarioDefinition:
    """
    Create an example scenario programmatically
    This demonstrates how scenarios could be built in code
    """
    scenario = ScenarioDefinition(
        scenario_id='example',
        name='Example Scenario',
        description='This is an example scenario for demonstration'
    )
    
    # Add start state
    scenario.add_state('start', {
        'message': 'This is the starting message',
        'options': ['yes', 'no'],
        'next_state': {
            'yes': 'state_yes',
            'no': 'state_no'
        }
    })
    
    # Add yes state
    scenario.add_state('state_yes', {
        'message': 'You selected yes',
        'terminal': True
    })
    
    # Add no state
    scenario.add_state('state_no', {
        'message': 'You selected no',
        'terminal': True
    })
    
    # Add actions
    scenario.add_action({
        'priority': 1,
        'category': 'immediate',
        'title': 'Take Action',
        'steps': ['Step 1', 'Step 2', 'Step 3'],
        'why': 'This is important because...'
    })
    
    return scenario


# Scenario registry (for future expansion)
SCENARIO_REGISTRY = {
    'image_abuse': 'Image-Based Abuse',
    'cyberstalking': 'Cyberstalking',
    'online_harassment': 'Online Harassment'
}


def get_available_scenarios() -> List[str]:
    """
    Get list of available scenario IDs
    
    Returns:
        List of scenario ID strings
    """
    return list(SCENARIO_REGISTRY.keys())


def get_scenario_name(scenario_id: str) -> str:
    """
    Get human-readable name for a scenario
    
    Args:
        scenario_id: Scenario identifier
        
    Returns:
        Human-readable scenario name
    """
    return SCENARIO_REGISTRY.get(scenario_id, 'Unknown Scenario')