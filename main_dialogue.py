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

# Function to simulate a random multi-choice selection
def random_multi_choice(options, num_choices=None):
    num_choices = num_choices or random.randint(1, len(options))
    return random.sample(list(options.keys()), num_choices)

# Main function to run the chosen smart systems
def smart_home_system(num_rounds=1, output_file="smart_home_dialogues.json"):
    total_dialogues = 0  # To track the total dialogues generated

    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}: Simulating user choices...")
        
        # Simulate random user choices for smart systems
        selected_systems = random_multi_choice(smart_systems)
        print(f"User selected systems: {[smart_systems[choice]['name'] for choice in selected_systems]}")
        
        # Count dialogues generated in this round
        dialogues_this_round = len(selected_systems)
        total_dialogues += dialogues_this_round

        # Loop through selected systems and generate dialogues
        for system in selected_systems:
            system_info = smart_systems[system]
            if "function" in system_info:
                # Call the corresponding generator function
                system_info["function"](num_samples=1, output_file=output_file)
            elif "class" in system_info:
                # Call the corresponding class and method
                instance = system_info["class"]()
                instance.generate_dataset_venting(num_samples=1, output_file=output_file)

        print(f"Round {round_num + 1} generated {dialogues_this_round} dialogues.\n")

    # Output total dialogues generated
    print(f"Total dialogues generated across {num_rounds} rounds: {total_dialogues}")

# Run the program
if __name__ == "__main__":
    # Specify the number of rounds (how many times the user will make random choices)
    num_rounds = 3
    smart_home_system(num_rounds=num_rounds, output_file="smart_home_dialogues.json")

