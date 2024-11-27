import random

# Decision tree for smart heating
heating_decision_tree = {
    "scenarios": {
        "Scheduled Heating": {"attributes": ["Time Scheduling"], "cost_range": (50, 100), "complexity": 2, "ecology": 3},
        "Geo-Fencing": {"attributes": ["Location-Based Control"], "cost_range": (100, 150), "complexity": 4, "ecology": 4},
        "Zonal Heating": {"attributes": ["Room-Specific Control"], "cost_range": (70, 120), "complexity": 3, "ecology": 3},
        "Energy Monitoring": {"attributes": ["Usage Tracking"], "cost_range": (60, 90), "complexity": 3, "ecology": 4},
        "Voice Control": {"attributes": ["Voice Commands"], "cost_range": (30, 50), "complexity": 1, "ecology": 2},
        "Adaptive Learning": {"attributes": ["Self-Learning Adjustments"], "cost_range": (120, 180), "complexity": 5, "ecology": 5},
        "Weather Responsive": {"attributes": ["Weather-Adaptive Heating"], "cost_range": (80, 140), "complexity": 3, "ecology": 4}
    },
    "spaces": ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Indoor Garden"]
}

# Summary of responses
summary = {
    "scenarios": [],
    "technical_requirements": [],
    "room_requirements": {},
    "cost_estimation": 0,
    "complexity_score": 0,
    "ecological_rating": 0
}


# Question and answer functions
def ask_scenario_questions():
    print("Please select the scenarios you are interested in:")
    for idx, (scenario, details) in enumerate(heating_decision_tree["scenarios"].items(), 1):
        print(f"{idx}. {scenario} (attributes: {', '.join(details['attributes'])})")

    selected_indices = input("\nEnter the numbers of your chosen scenarios, separated by commas: ").split(',')
    for index in selected_indices:
        idx = int(index.strip()) - 1
        if 0 <= idx < len(heating_decision_tree["scenarios"]):
            scenario_name = list(heating_decision_tree["scenarios"].keys())[idx]
            summary["scenarios"].append(scenario_name)
            summary["technical_requirements"].extend(heating_decision_tree["scenarios"][scenario_name]["attributes"])


def ask_space_questions():
    print("\nWhere do you want to configure the smart heating system?")
    for idx, space in enumerate(heating_decision_tree["spaces"], 1):
        print(f"{idx}. {space}")

    selected_indices = input("\nEnter the numbers of your chosen spaces, separated by commas: ").split(',')
    for index in selected_indices:
        idx = int(index.strip()) - 1
        if 0 <= idx < len(heating_decision_tree["spaces"]):
            space_name = heating_decision_tree["spaces"][idx]
            summary["room_requirements"][space_name] = {}


def ask_unit_questions():
    for space in summary["room_requirements"]:
        print(f"\nIn the {space}, how many heating units do you need?")
        units = int(input("Enter the number of units: "))
        summary["room_requirements"][space]["units"] = units


def calculate_cost_complexity_ecology(session_summary):
    """
    Calculate the total cost, complexity, and ecological rating for a given session summary.
    Considers scenario difficulty weights and unit counts with smaller weights.
    Updates the session_summary dictionary with these metrics.
    """
    total_cost_min = total_cost_max = 0
    total_complexity = 0
    total_ecology = 0
    num_scenarios = len(session_summary["scenarios"])

    # Calculate cost, complexity, and ecological impact based on chosen scenarios
    for scenario in session_summary["scenarios"]:
        details = heating_decision_tree["scenarios"][scenario]
        cost_min, cost_max = details["cost_range"]
        total_cost_min += cost_min
        total_cost_max += cost_max
        total_complexity += details["complexity"]  # Scenario difficulty weight
        total_ecology += details["ecology"]

    # Add a smaller weight for the number of heating units in the rooms
    total_units = sum(details["units"] for details in session_summary["room_requirements"].values())
    unit_complexity_weight = 0.1  # Small weight for unit count
    total_complexity += total_units * unit_complexity_weight

    # Update session summary
    session_summary["cost_estimation"] = (total_cost_min, total_cost_max)
    session_summary["complexity_score"] = total_complexity / num_scenarios if num_scenarios > 0 else 0
    session_summary["ecological_rating"] = total_ecology / num_scenarios if num_scenarios > 0 else 0


def print_summary():
    print("\n============= Smart Heating Plan Summary =============\n")
    print("Scenarios Selected:")
    for scenario in summary["scenarios"]:
        print(f"  - {scenario}")

    print("\nSpaces Configured:")
    for space, details in summary["room_requirements"].items():
        print(f"  - {space}: {details['units']} units")

    print("\nTechnical Requirements:")
    print(f"  - {', '.join(set(summary['technical_requirements']))}")

    cost_min, cost_max = summary["cost_estimation"]
    print(f"\nTotal Estimated Cost: ${cost_min} - ${cost_max}")
    print(f"Overall Installation Complexity: {summary['complexity_score']:.1f}/5")
    print(f"Ecological Rating: {summary['ecological_rating']:.1f}/5")
    print("\n⚠️ Note: Installation costs are not included. Professional installation is recommended for complexity ratings above 3.")


# Main function to run interactively
if __name__ == "__main__":
    ask_scenario_questions()
    ask_space_questions()
    ask_unit_questions()
    calculate_cost_complexity_ecology(summary)
    print_summary()

