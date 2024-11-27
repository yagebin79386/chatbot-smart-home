import os
import random
import json

# Set working directory
os.chdir("/Users/rickytan/Virtual_Machines/Ubuntu")

# Import smart home system functions and classes
from smart_heating_generator import generate_dataset_heating
from smart_lighting_generator import generate_dataset_light
from smart_AV_generator import generate_dataset_AV
from smart_security_generator import generate_dataset_security
from smart_shutter_generator import generate_dataset_shutter
from smart_venting_generator import SmartAirSystem

# Define smart system choices
smart_systems = {
    1: {"name": "Smart Lighting System", "function": generate_dataset_light},
    2: {"name": "Smart Heating System", "function": generate_dataset_heating},
    3: {"name": "Smart AV (Audio-Visual) System", "function": generate_dataset_AV},
    4: {"name": "Smart Security/Surveillance System", "function": generate_dataset_security},
    5: {"name": "Smart Shade/Shutter System", "function": generate_dataset_shutter},
    6: {"name": "Smart Air/Venting System", "class": SmartAirSystem}
}

# General questions generator
def generate_general_dialogue():
    mobility_abilities = ["fully mobile", "limited mobility"]
    residence_types = ["shared residence", "own residence"]
    budgets = ["low", "medium", "high"]
    mobile_os = ["iOS", "Android"]
    streaming_services = ["Google Home", "Amazon Alexa", "HomeKit", "None"]
    smart_devices_owned = ["yes", "no"]
    compatibility_concerns = ["yes", "no", "No idea"]
    reliability_preference = ["very safe", "moderately safe", "basic safety"]
    automation_rule_concerns = ["yes", "no"]

    age = random.randint(15, 100)
    mobility = random.choice(mobility_abilities)
    residence = random.choice(residence_types)
    budget = random.choice(budgets)
    os = random.choice(mobile_os)
    streaming_service = random.choice(streaming_services)
    owns_devices = random.choice(smart_devices_owned)
    compatibility = random.choice(compatibility_concerns) if owns_devices == "yes" else None
    safety_preference = random.choice(reliability_preference)
    automation_rule = random.choice(automation_rule_concerns)

    # Ask smart system preference (allow multiple choices)
    smart_system_names = [system["name"] for system in smart_systems.values()]
    smart_system_choices = random.sample(smart_system_names, random.randint(1, len(smart_system_names)))

    dialogue = [
        {"role": "AI", "text": "What is your age?"},
        {"role": "User", "text": str(age)},
        {"role": "AI", "text": "Do you have any mobility limitations?"},
        {"role": "User", "text": mobility},
        {"role": "AI", "text": "Do you live in a shared residence or your own residence?"},
        {"role": "User", "text": residence},
        {"role": "AI", "text": "What budget level are you looking at for setting up your smart home? (low, medium, high)"},
        {"role": "User", "text": budget},
        {"role": "AI", "text": "What operating system does your mobile phone use? (iOS or Android)"},
        {"role": "User", "text": os},
        {"role": "AI", "text": "Do you use any streaming services related to smart ecosystems, like Google Home, Amazon Alexa, or HomeKit?"},
        {"role": "User", "text": streaming_service},
        {"role": "AI", "text": "Do you already own any smart devices at home? (yes or no)"},
        {"role": "User", "text": owns_devices}
    ]

    if owns_devices == "yes":
        dialogue.extend([
            {"role": "AI", "text": "If you own devices, are they compatible with matter standard? (yes or no)"},
            {"role": "User", "text": compatibility},
            {"role": "AI", "text": "Have you configured by yourself any automation or rule? (yes or no)"},
            {"role": "User", "text": automation_rule}
        ])

    # Add smart system preferences
    dialogue.append({"role": "AI", "text": f"Which smart systems are you most interested in? (Options: {', '.join(smart_system_names)})"})
    dialogue.append({"role": "User", "text": ", ".join(smart_system_choices)})

    # Final recommendation
    dialogue.append({"role": "AI", "text": f"Based on your answers, I would recommend focusing on '{', '.join(smart_system_choices)}' with a '{safety_preference}' safety and reliability level."})
    
    return dialogue, smart_system_choices

# Main function to run the chosen smart systems
def smart_home_system(num_rounds=1, output_file="smart_home_dialogues.json"):
    total_dialogues = 0  # To track the total dialogues generated
    #all_dialogues = []  # To store all dialogues

    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}: Simulating user choices...")

        # Generate general dialogue and get smart system preferences
        general_dialogue, preferred_systems = generate_general_dialogue()
        round_dialogues = general_dialogue  # Start with general dialogue
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.extend(round_dialogues)

        with open(output_file, "w") as f:
            json.dump(existing_data, f, indent=4)
        # Generate dialogues for each preferred system
        for preferred_system in preferred_systems:
            preferred_system_index = next((key for key, value in smart_systems.items() if value["name"] == preferred_system), None)
            if preferred_system_index:
                system_info = smart_systems[preferred_system_index]
                if "function" in system_info:
                    # Call the corresponding generator function
                    system_info["function"](num_samples=1, output_file=output_file)
                elif "class" in system_info:
                    # Call the corresponding class and method
                    instance = system_info["class"]()
                    instance.generate_dataset_venting(num_samples=1, output_file=output_file)

        
        #all_dialogues.extend(round_dialogues)  # Append this round's dialogues as a single block
        total_dialogues += len(preferred_systems)

        print(f"Round {round_num + 1} generated {len(preferred_systems)} dialogues for {', '.join(preferred_systems)}.\n")
    print(f"Total dialogues generated across {num_rounds} rounds: {total_dialogues}")

# Run the program
if __name__ == "__main__":
    # Specify the number of rounds (how many times the user will make random choices)
    num_rounds = 5
    smart_home_system(num_rounds=num_rounds, output_file="smart_home_dialogues.json")
