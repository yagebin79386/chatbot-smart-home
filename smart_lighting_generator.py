import json
import os
import random
from smart_lighting import decision_tree, generate_random_response, calculate_cost_complexity_ecology  # Assuming these functions are defined in smart_lighting

def generate_dialogue():
    dialogue = []
    session_summary = {
        "scenarios": [],
        "technical_requirements": set(),
        "room_requirements": {}
    }
    
    # Display and simulate scenario selection
    dialogue.append({
        "role": "AI",
        "text": "Please select the scenarios you are interested in (choose multiple):\n" +
                "\n".join([f"{idx + 1}. {key}: {value[0]} (attributes: {', '.join(value)})"
                          for idx, (key, value) in enumerate(decision_tree["scenarios"].items())])
    })
    scenario_list = list(decision_tree["scenarios"].keys())
    chosen_scenarios = generate_random_response(scenario_list)
    session_summary["scenarios"].extend(chosen_scenarios)
    session_summary["technical_requirements"].update(
        tech for scenario in chosen_scenarios for tech in decision_tree["scenarios"][scenario]
    )
    
    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_scenarios)
    })

    # Display and simulate space selection
    dialogue.append({
        "role": "AI",
        "text": "Where do you want to install the smart lighting system? (choose multiple spaces):\n" +
                "\n".join([f"{idx + 1}. {space.capitalize()}" for idx, space in enumerate(decision_tree["spaces"])])
    })
    chosen_spaces = generate_random_response(decision_tree["spaces"])
    for space in chosen_spaces:
        session_summary["room_requirements"][space] = {}
    
    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_spaces)
    })

    # Display and simulate light body selection for each room
    for room in session_summary["room_requirements"]:
        dialogue.append({
            "role": "AI",
            "text": f"In the {room.capitalize()}, what type of light body do you need?\n" +
                    "\n".join([f"{idx + 1}. {light_type.replace('_', ' ').title()}"
                              for idx, light_type in enumerate(decision_tree["light_types"])])
        })
        light_type_list = list(decision_tree["light_types"].keys())
        chosen_light_types = generate_random_response(light_type_list)
        room_details = session_summary["room_requirements"][room]
        
        dialogue.append({
            "role": "User",
            "text": ", ".join(chosen_light_types)
        })
        
        for light_type in chosen_light_types:
            if light_type == "light_bulb":
                dialogue.append({
                    "role": "AI",
                    "text": "Choose the types of bulb interface (you can select multiple):\n" +
                            "\n".join([f"{i + 1}. {bulb_type}" for i, bulb_type in enumerate(decision_tree["light_types"]["light_bulb"])])
                })
                bulb_type_list = decision_tree["light_types"]["light_bulb"]
                chosen_bulbs = generate_random_response(bulb_type_list)
                room_details[light_type] = {}

                dialogue.append({
                    "role": "User",
                    "text": ", ".join(chosen_bulbs)
                })

                for bulb_type in chosen_bulbs:
                    quantity = random.randint(1, 5)
                    room_details[light_type][bulb_type] = {"quantity": quantity}
                    dialogue.append({
                        "role": "AI",
                        "text": f"How many {bulb_type} bulbs do you need?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": str(quantity)
                    })

            elif light_type == "light_strip":
                length = round(random.uniform(1, 10), 1)
                room_details[light_type] = {"length": length}
                dialogue.append({
                    "role": "AI",
                    "text": "How many meters of light strip do you need?"
                })
                dialogue.append({
                    "role": "User",
                    "text": str(length)
                })

            elif light_type == "ceiling_lamp":
                rail_system = random.choice([True, False])
                if rail_system:
                    length = round(random.uniform(1, 5), 1)
                    room_details[light_type] = {"rail_system": True, "length": length}
                    dialogue.append({
                        "role": "AI",
                        "text": "Do you need a rail system for the ceiling lamp?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": "yes"
                    })
                    dialogue.append({
                        "role": "AI",
                        "text": "How many meters of rail system do you need?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": str(length)
                    })
                else:
                    quantity = random.randint(1, 3)
                    room_details[light_type] = {"rail_system": False, "quantity": quantity}
                    dialogue.append({
                        "role": "AI",
                        "text": "Do you need a rail system for the ceiling lamp?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": "no"
                    })
                    dialogue.append({
                        "role": "AI",
                        "text": "How many ceiling lamps do you need?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": str(quantity)
                    })

            else:  # Other types like wall light, desk lamp, etc.
                quantity = random.randint(1, 3)
                room_details[light_type] = {"quantity": quantity}
                dialogue.append({
                    "role": "AI",
                    "text": f"How many {light_type.replace('_', ' ')}s do you need?"
                })
                dialogue.append({
                    "role": "User",
                    "text": str(quantity)
                })

    # Convert set to list for JSON compatibility
    session_summary["technical_requirements"] = list(session_summary["technical_requirements"])

    # Calculate cost, complexity, and ecological rating
    calculate_cost_complexity_ecology(session_summary)

    # Format and include the summary output in the dialogue

    summary_text = (
        "============= Smart Lighting Plan Summary =============\n\n" +
        "\n".join([
            f"📍 {room_name.capitalize()}:\n" +
            "\n".join([
                f"  • {details.get('quantity', 0)} units of {light_type.replace('_', ' ')}"
                if 'quantity' in details else
                f"  • {details.get('length', 0)} meters of {light_type.replace('_', ' ')}"
                for light_type, details in room_details.items()
            ])
            for room_name, room_details in session_summary["room_requirements"].items()
        ]) +
        f"\n\nTotal Estimated Cost: €{session_summary.get('cost_estimation', 0):.2f}\n" +
        f"Overall Installation Complexity: {session_summary.get('complexity_score', 0):.1f}/5\n" +
        f"Ecological Rating: {session_summary.get('ecological_rating', 0):.1f}/5\n\n" +
        "⚠️ Note: Installation costs are not included. Professional installation is recommended for complexity ratings above 3."
    )



    dialogue.append({
        "role": "AI",
        "text": summary_text
    })

    return dialogue

def generate_dataset_light (num_samples=1, output_file="smart_home_dialogues.json"):
    dataset = [generate_dialogue() for _ in range(num_samples)]
    
    #check if the file already exists
    if os.path.exists(output_file):
        # Load existing data from the file
        with open(output_file, "r") as f:
            existing_data = json.load(f)
    else:
        # if the file doesn't exist, initialize an empty list
        existing_data = []

    # Add the generated conversation to the dataset
    existing_data.extend(dataset)

    #Save the updated dateset to the JSON file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    print(f"Generated {num_samples} lighting dialogues and saved to '{output_file}'.")

# Generate dataset with a specified number of samples
if __name__ == "__main__":
    generate_dataset_light(5)  # Adjust the number of samples as needed


