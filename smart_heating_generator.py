import json
import random
from smart_heating import heating_decision_tree, calculate_cost_complexity_ecology

def generate_random_response(options):
    """
    Helper function to randomly select one or more options.
    """
    num_choices = random.randint(1, len(options))  # Choose at least one option
    return random.sample(options, num_choices)


def generate_dialogue():
    """
    Generate a single dialogue for the smart heating system configuration.
    Returns a list of dialogue turns and a session summary.
    """
    dialogue = []
    session_summary = {
        "scenarios": [],
        "technical_requirements": [],
        "room_requirements": {}
    }

    # Step 1: Scenario selection
    dialogue.append({
        "role": "AI",
        "text": "Please select the scenarios you are interested in smart heating system: (choose multiple):\n" +
                "\n".join([f"{idx + 1}. {key} (attributes: {', '.join(value['attributes'])})"
                           for idx, (key, value) in enumerate(heating_decision_tree["scenarios"].items())])
    })

    scenario_list = list(heating_decision_tree["scenarios"].keys())
    chosen_scenarios = generate_random_response(scenario_list)
    session_summary["scenarios"].extend(chosen_scenarios)
    for scenario in chosen_scenarios:
        session_summary["technical_requirements"].extend(heating_decision_tree["scenarios"][scenario]["attributes"])

    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_scenarios)
    })

    # Step 2: Space selection
    dialogue.append({
        "role": "AI",
        "text": "Where do you want to install the smart heating system? (choose multiple spaces):\n" +
                "\n".join([f"{idx + 1}. {space}" for idx, space in enumerate(heating_decision_tree["spaces"])])
    })

    chosen_spaces = generate_random_response(heating_decision_tree["spaces"])
    for space in chosen_spaces:
        session_summary["room_requirements"][space] = {}

    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_spaces)
    })

    # Step 3: Unit configuration for each space
    for space in session_summary["room_requirements"]:
        dialogue.append({
            "role": "AI",
            "text": f"In the {space}, how many heating units do you need?"
        })

        num_units = random.randint(1, 5)  # Randomly decide number of units
        session_summary["room_requirements"][space] = {"units": num_units}

        dialogue.append({
            "role": "User",
            "text": str(num_units)
        })

    # Calculate cost, complexity, and ecological ratings
    calculate_cost_complexity_ecology(session_summary)

    # Format and include the summary output in the dialogue
    cost_min, cost_max = session_summary["cost_estimation"]
    summary_text = (
        "============= Smart Heating Plan Summary =============\n\n" +
        "Scenarios Selected:\n" +
        "\n".join([f"  - {scenario}" for scenario in session_summary["scenarios"]]) +
        "\n\nSpaces Configured:\n" +
        "\n".join([f"  - {space}: {details['units']} units"
                  for space, details in session_summary["room_requirements"].items()]) +
        "\n\nTechnical Requirements:\n" +
        f"  - {', '.join(set(session_summary['technical_requirements']))}\n" +
        f"\nTotal Estimated Cost: ${cost_min} - ${cost_max}\n" +
        f"Overall Installation Complexity: {session_summary['complexity_score']:.1f}/5\n" +
        f"Ecological Rating: {session_summary['ecological_rating']:.1f}/5\n\n" +
        "⚠️ Note: Installation costs are not included. Professional installation is recommended for complexity ratings above 3."
    )

    dialogue.append({
        "role": "AI",
        "text": summary_text
    })

    return dialogue


def generate_dataset_heating(num_samples):
    """
    Generate a dataset of dialogues for the smart heating system.
    Saves the dataset to a JSON file.
    """
    dataset = [generate_dialogue() for _ in range(num_samples)]
    return dataset

    
def generate_json_heating(num_samples, output_file):
    #check if the file already exists
    if os.path.exists(output_file):
        # Load existing data from the file
        with open(output_file, "r") as f:
            existing_data = json.load(f)
    else:
        # if the file doesn't exist, initialize an empty list
        existing_data = []
    
    # Add the generated conversation to the dataset
    dataset = generate_dataset_heating(num_samples)
    existing_data.extend(dataset)
        
    #Save the updated dateset to the JSON file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)
                
    print(f"Generated {num_samples} heating dialogues and saved to {output_file}.")
    


# Run the script to generate a dataset
if __name__ == "__main__":
    generate_json_heating(num_samples=1, output_file="smart_home_dialogues.json")  # Change the number of samples as needed

