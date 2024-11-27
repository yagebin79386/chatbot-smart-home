#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

import random

# Decision tree structure
decision_tree = {
    "scenarios": {
        "Sleep/Wake-Up": ["Dimmable", "Color Temperature Control", "Scheduling"],
        "Security Enhancement": ["Motion Sensor", "Remote Control", "Weather Resistance"],
        "Energy Efficiency": ["Low Power", "Scheduling"],
        "Personalized Scenes": ["Color Changing", "Voice Control", "App Control"],
        "Voice-Controlled Operation": ["Voice Control", "Smart Hub Compatibility"],
        "Health and Well-being": ["Circadian Rhythm Lighting", "Dimmable"],
        "Outdoor Safety": ["Weather Resistance", "Motion Sensor"],
        "Entertainment Sync": ["Color Changing", "Sync with Audio/Video"]
    },
    "spaces": [
        "living room", "bedroom", "kitchen", "bathroom", "dining room", 
        "office", "hallway", "garage", "outdoor area"
    ],
    "light_types": {
        "light_bulb": ["E27", "GU10", "E14", "B22"],
        "light_strip": ["per_meter"],
        "ceiling_lamp": ["per_unit", "rail_system"],
        "wall_light": ["per_unit"],
        "desk_lamp": ["per_unit"],
        "floor_lamp": ["per_unit"],
        "spotlight": ["per_unit"],
        "security_light": ["per_unit"]
    },
    "scenario_complexity": {
        "Sleep/Wake-Up": 1,
        "Security Enhancement": 3,
        "Energy Efficiency": 2,
        "Personalized Scenes": 2,
        "Voice-Controlled Operation": 3,
        "Health and Well-being": 2,
        "Outdoor Safety": 3,
        "Entertainment Sync": 4
    }
}

# Summary to store user responses
summary = {
    "scenarios": [],
    "technical_requirements": set(),
    "room_requirements": {},
    "cost_estimation": 0,
    "complexity_score": 0,
    "ecological_rating": 0
}

# Question generator functions
def ask_scenario_questions():
    print("Please select the scenarios you are interested in (choose multiple):")
    for idx, (key, scenario) in enumerate(decision_tree["scenarios"].items(), 1):
        print(f"{idx}. {key}: {scenario[0]} (attributes: {', '.join(scenario)})")
    
    chosen_indices = input("\nEnter the numbers of your chosen scenarios, separated by commas: ").split(',')
    for index in chosen_indices:
        idx = int(index.strip()) - 1
        if 0 <= idx < len(decision_tree["scenarios"]):
            key = list(decision_tree["scenarios"].keys())[idx]
            summary["scenarios"].append(key)
            summary["technical_requirements"].update(decision_tree["scenarios"][key])

def ask_space_questions():
    print("\nWhere do you want to install the smart lighting system? (choose multiple spaces):")
    for idx, space in enumerate(decision_tree["spaces"], 1):
        print(f"{idx}. {space.capitalize()}")
    
    chosen_indices = input("\nEnter the numbers of your chosen spaces, separated by commas: ").split(',')
    for index in chosen_indices:
        idx = int(index.strip()) - 1
        if 0 <= idx < len(decision_tree["spaces"]):
            space = decision_tree["spaces"][idx]
            summary["room_requirements"][space] = {}

def ask_light_body_questions():
    for room in summary["room_requirements"]:
        print(f"\nIn the {room.capitalize()}, what type of light body do you need?")
        for idx, light_type in enumerate(decision_tree["light_types"], 1):
            print(f"{idx}. {light_type.replace('_', ' ').title()}")
        
        chosen_indices = input("Enter the numbers of the light types you need, separated by commas: ").split(',')
        room_details = summary["room_requirements"][room]
        
        for index in chosen_indices:
            index = index.strip()
            if not index:  # Skip empty entries
                continue
            idx = int(index) - 1
            if 0 <= idx < len(decision_tree["light_types"]):
                light_type = list(decision_tree["light_types"].keys())[idx]
                
                # Ask specific questions based on light type
                if light_type == "light_bulb":
                    print("\nChoose the types of bulb interface (you can select multiple):")
                    for i, bulb_type in enumerate(decision_tree["light_types"]["light_bulb"], 1):
                        print(f"{i}. {bulb_type}")
                    
                    bulb_choices = input("Enter the numbers for the bulb types you need, separated by commas: ").split(',')
                    room_details[light_type] = {}
                    
                    for bulb_choice in bulb_choices:
                        bulb_choice = bulb_choice.strip()
                        if not bulb_choice:  # Skip empty entries
                            continue
                        bulb_idx = int(bulb_choice) - 1
                        if 0 <= bulb_idx < len(decision_tree["light_types"]["light_bulb"]):
                            bulb_type = decision_tree["light_types"]["light_bulb"][bulb_idx]
                            quantity = int(input(f"How many {bulb_type} bulbs do you need? "))
                            room_details[light_type][bulb_type] = {"quantity": quantity}
                
                elif light_type == "light_strip":
                    length = float(input("How many meters of light strip do you need? "))
                    room_details[light_type] = {"length": length}
                
                elif light_type == "ceiling_lamp":
                    rail_system = input("Do you need a rail system for the ceiling lamp? (yes/no): ").strip().lower() == "yes"
                    if rail_system:
                        length = float(input("How many meters of rail system do you need? "))
                        room_details[light_type] = {"rail_system": True, "length": length}
                    else:
                        quantity = int(input("How many ceiling lamps do you need? "))
                        room_details[light_type] = {"rail_system": False, "quantity": quantity}
                
                else:  # For other types like wall light, desk lamp, etc.
                    quantity = int(input(f"How many {light_type.replace('_', ' ')}s do you need? "))
                    room_details[light_type] = {"quantity": quantity}


# Cost, complexity, and ecological rating estimation
def calculate_cost_complexity_ecology(session_summary):
    cost_per_type = {
        "light_bulb": 20,
        "light_strip": 32,
        "ceiling_lamp": 115,
        "wall_light": 67,
        "desk_lamp": 60,
        "floor_lamp": 100,
        "spotlight": 40,
        "security_light": 90
    }
    complexity_per_type = {
        "light_bulb": 1,
        "light_strip": 2,
        "ceiling_lamp": 4,
        "wall_light": 3,
        "desk_lamp": 1,
        "floor_lamp": 1,
        "spotlight": 3,
        "security_light": 4
    }
    ecological_score_per_type = {
        "light_bulb": 4,
        "light_strip": 3,
        "ceiling_lamp": 3,
        "wall_light": 3,
        "desk_lamp": 4,
        "floor_lamp": 4,
        "spotlight": 2,
        "security_light": 2
    }
    
    total_cost = 0
    total_complexity = 0
    total_ecological_score = 0
    count = 0

    # Add complexity based on scenarios
    for scenario in session_summary["scenarios"]:
        total_complexity += decision_tree["scenario_complexity"].get(scenario, 1)

    # Add complexity based on the number of spaces
    total_complexity += len(session_summary["room_requirements"]) * 0.5  # Each space adds 0.5 to the complexity

    # Calculate cost, complexity, and ecology for light types
    for room, details in session_summary["room_requirements"].items():
        for light_type, spec in details.items():
            if light_type == "light_bulb":
                for bulb_type, bulb_spec in spec.items():
                    quantity = bulb_spec["quantity"]
                    cost = quantity * cost_per_type[light_type]
                    complexity = complexity_per_type[light_type]
                    ecology = ecological_score_per_type[light_type]
                    
                    total_cost += cost
                    total_complexity += complexity
                    total_ecological_score += ecology
                    count += 1
            elif light_type == "light_strip":
                length = spec["length"]
                cost = length * cost_per_type[light_type]
                complexity = complexity_per_type[light_type]
                ecology = ecological_score_per_type[light_type]
                
                total_cost += cost
                total_complexity += complexity
                total_ecological_score += ecology
                count += 1
            elif light_type == "ceiling_lamp" and spec["rail_system"]:
                length = spec["length"]
                cost = length * cost_per_type[light_type]
                complexity = complexity_per_type[light_type]
                ecology = ecological_score_per_type[light_type]
                
                total_cost += cost
                total_complexity += complexity
                total_ecological_score += ecology
                count += 1
            else:
                quantity = spec["quantity"]
                cost = quantity * cost_per_type[light_type]
                complexity = complexity_per_type[light_type]
                ecology = ecological_score_per_type[light_type]
                
                total_cost += cost
                total_complexity += complexity
                total_ecological_score += ecology
                count += 1
    
    # Update the session summary with calculated values
    session_summary["cost_estimation"] = total_cost
    session_summary["complexity_score"] = total_complexity / count if count > 0 else 0
    session_summary["ecological_rating"] = total_ecological_score / count if count > 0 else 0


# Summary output
def print_summary():
    print("\n============= Smart Lighting Plan Summary =============\n")
    
    for room, details in summary["room_requirements"].items():
        print(f"📍 {room.capitalize()}:")
        for light_type, spec in details.items():
            if light_type == "light_bulb":
                for bulb_type, bulb_spec in spec.items():
                    print(f"  • {bulb_spec['quantity']} units of {bulb_type} light bulbs with technical attributes: {', '.join(summary['technical_requirements'])}")
            elif light_type == "light_strip":
                print(f"  • {spec['length']} meters of light strip with technical attributes: {', '.join(summary['technical_requirements'])}")
            elif light_type == "ceiling_lamp" and spec["rail_system"]:
                print(f"  • {spec['length']} meters of ceiling rail system with technical attributes: {', '.join(summary['technical_requirements'])}")
            else:
                print(f"  • {spec['quantity']} units of {light_type.replace('_', ' ')} with technical attributes: {', '.join(summary['technical_requirements'])}")

    # Cost, complexity, and ecological rating summary
    print("\nTotal Estimated Cost: €{:.2f}".format(summary["cost_estimation"]))
    print("Overall Installation Complexity: {:.1f}/5".format(summary["complexity_score"]))
    print("Ecological Rating: {:.1f}/5".format(summary["ecological_rating"]))
    print("\n⚠️ Note: Installation costs are not included. Professional installation is recommended for complexity ratings above 3.")


def generate_random_response(options):
    """Helper function to randomly select one or more options."""
    num_choices = random.randint(1, len(options))  # Choose at least one option
    return random.sample(options, num_choices)

    
# Export generate_dialogue for dataset generation
def generate_dialogue():
    # Start a new session summary for each dialogue
    session_summary = {
        "scenarios": [],
        "technical_requirements": set(),  # Using a set initially for unique items
        "room_requirements": {}
    }
    
    # Randomly select scenarios
    chosen_scenarios = generate_random_response(list(decision_tree["scenarios"].keys()))
    for scenario in chosen_scenarios:
        session_summary["scenarios"].append(scenario)
        session_summary["technical_requirements"].update(decision_tree["scenarios"][scenario])

    # Randomly select spaces
    chosen_spaces = generate_random_response(decision_tree["spaces"])
    for space in chosen_spaces:
        session_summary["room_requirements"][space] = {}

    # Randomly select light bodies and their specifications for each room
    for room in session_summary["room_requirements"]:
        chosen_light_types = generate_random_response(list(decision_tree["light_types"].keys()))
        
        room_details = session_summary["room_requirements"][room]
        for light_type in chosen_light_types:
            if light_type == "light_bulb":
                chosen_bulbs = generate_random_response(decision_tree["light_types"]["light_bulb"])
                room_details[light_type] = {}
                
                for bulb_type in chosen_bulbs:
                    quantity = random.randint(1, 5)  # Random quantity for the bulb type
                    room_details[light_type][bulb_type] = {"quantity": quantity}
            
            elif light_type == "light_strip":
                length = round(random.uniform(1, 10), 1)  # Random length in meters
                room_details[light_type] = {"length": length}
            
            elif light_type == "ceiling_lamp":
                rail_system = random.choice([True, False])
                if rail_system:
                    length = round(random.uniform(1, 5), 1)  # Random rail length in meters
                    room_details[light_type] = {"rail_system": True, "length": length}
                else:
                    quantity = random.randint(1, 3)  # Random quantity for ceiling lamps
                    room_details[light_type] = {"rail_system": False, "quantity": quantity}
            
            else:  # For other types like wall light, desk lamp, etc.
                quantity = random.randint(1, 3)  # Random quantity for the light type
                room_details[light_type] = {"quantity": quantity}
    
    # Convert technical_requirements to a list for JSON compatibility
    session_summary["technical_requirements"] = list(session_summary["technical_requirements"])
    
    return session_summary


# Optionally, if you'd like to run the Q&A functions interactively
if __name__ == "__main__":
    ask_scenario_questions()
    ask_space_questions()
    ask_light_body_questions()
    calculate_cost_complexity_ecology()
    print_summary()


# In[ ]:





# In[ ]:




