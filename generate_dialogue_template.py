import random
import json

def generate_dialogue():
    # Sample options for each data field
    mobility_abilities = ["fully mobile", "limited mobility"]
    residence_types = ["shared residence", "own residence"]
    budgets = ["low", "medium", "high"]
    smart_systems = ["Lighting", "Heating", "Audio-Visual", "Security and Alarm", "Shades/Shutters", "Air and Ventilation"]
    mobile_os = ["iOS", "Android"]
    streaming_services = ["Google Home", "Amazon Alexa", "HomeKit", "None"]
    smart_devices_owned = ["yes", "no"]
    compatibility_concerns = ["yes", "no", "No idea"]
    reliability_preference = ["very safe", "moderately safe", "basic safety"]
    automation_rule_concerns = ["yes", "no"]

    # Randomly select options for each user
    age = random.randint(15, 100)  # Randomly choose an age between 15 and 100
    mobility = random.choice(mobility_abilities)
    residence = random.choice(residence_types)
    budget = random.choice(budgets)
    smart_system = random.choice(smart_systems)
    os = random.choice(mobile_os)
    streaming_service = random.choice(streaming_services)
    owns_devices = random.choice(smart_devices_owned)
    compatibility = random.choice(compatibility_concerns) if owns_devices == "yes" else None  # Only generate compatibility answer if ow
ns_devices is 'yes'
    safety_preference = random.choice(reliability_preference)
    automation_rule = random.choice()

# Structure dialogue
    dialogue = [
        {"role": "AI", "text": "What is your age?"},
        {"role": "User", "text": age},
        {"role": "AI", "text": "Do you have any mobility limitations?"},
        {"role": "User", "text": mobility},
        {"role": "AI", "text": "Do you live in a shared residence or your own residence?"},
        {"role": "User", "text": residence},
        {"role": "AI", "text": "What budget level are you looking at for setting up your smart home? (low, medium, high)"},
        {"role": "User", "text": budget},
        {"role": "AI", "text": f"Which smart system are you most interested in? (Options: {', '.join(smart_systems)})"},
        {"role": "User", "text": smart_system},
        {"role": "AI", "text": "What operating system does your mobile phone use? (iOS or Android)"},
        {"role": "User", "text": os},
        {"role": "AI", "text": "Do you use any streaming services related to smart ecosystems, like Google Home, Amazon Alexa, or HomeKit?"},
        {"role": "User", "text": streaming_service},
        {"role": "AI", "text": "Do you already own any smart devices at home? (yes or no)"},
        {"role": "User", "text": owns_devices}
    ]
    
    # Add compatibility question only if the answer to owns_devices is "yes"
    if owns_devices == "yes":
        dialogue.extend([
            {"role": "AI", "text": "If you own devices, are they compatible with matter standard? (yes or no)"},
            {"role": "User", "text": compatibility}
            {"role": "AI", "text": "Have you configured by yourself any automation or rule? (yes or no)"},
            {"role": "User", "text": automation_rule}
        ])

# Final recommendation based on answers
    dialogue.append({"role": "AI", "text": f"Based on your answers, I would recommend a '{smart_system}'-focused configuration with a '{safety_preference}' safety and reliability level."})

    return dialogue

# Generate multiple dialogues and save to JSON
def generate_dataset(num_samples=50):
    dataset = [generate_dialogue() for _ in range(num_samples)]
    
    # Save dataset to JSON file
    with open("smart_home_dialogues.json", "w") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"Generated {num_samples} dialogues and saved to 'smart_home_dialogues.json'.")

# Generate dataset
generate_dataset()
