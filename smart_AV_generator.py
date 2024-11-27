import json
import random
import os

# Mock smart_av_tree structure
smart_av_tree = {
    "scenarios": {
        "Home Theater Experience": {"complexity": 4, "ecology": 3, "base_cost": 300},
        "Multi-Room Audio": {"complexity": 3, "ecology": 4, "base_cost": 200},
        "Video Conferencing": {"complexity": 2, "ecology": 3, "base_cost": 150},
        "Gaming": {"complexity": 5, "ecology": 3, "base_cost": 400},
        "Learning and Education": {"complexity": 2, "ecology": 5, "base_cost": 100},
        "Fitness and Health": {"complexity": 3, "ecology": 4, "base_cost": 250},
        "Accessibility Features": {"complexity": 2, "ecology": 5, "base_cost": 150},
        "Smart Alarms and Notifications": {"complexity": 1, "ecology": 4, "base_cost": 50}
    },
    "smart_streaming_accessories": {
        "Amazon Fire TV Stick": 50,
        "Google Chromecast with Google TV": 60,
        "Apple TV": 150,
        "Roku Streaming Stick": 40
    },
    "lighting_sync": {
        "TV-based": {"Philips Hue Sync Box": 250},
        "PC-based": {"Nanoleaf": {"Shapes": 200, "Canvas": 250, "Elements": 300}}
    },
    "hue_lights": {
        "Philips Hue Play Light Bars": 170,
        "Philips Hue Lightstrip Plus": {"small": 100, "medium": 120, "large": 150},
        "Philips Hue Gradient Lightstrip": {
            "small": 300, "medium": 350, "large": 400
        }
    },
    "spaces": ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"],
    "speaker_types": {
        "Soundbar": 200,
        "Subwoofer": 150,
        "Bookshelf Speakers": 300,
        "Tower Speakers": 500,
        "Portable Bluetooth Speakers": 100,
        "Outdoor Speaker": 250
    }
}

def generate_random_response(options):
    return random.sample(options, k=random.randint(1, len(options)))

def calculate_cost_complexity_ecology(session_summary):
    total_cost = 0
    total_complexity = 0
    total_ecology = 0
    num_scenarios = len(session_summary["scenarios"])

    for scenario in session_summary["scenarios"]:
        details = smart_av_tree["scenarios"][scenario]
        total_cost += details["base_cost"]
        total_complexity += details["complexity"]
        total_ecology += details["ecology"]

    for accessory in session_summary["streaming_accessories"]:
        total_cost += smart_av_tree["smart_streaming_accessories"][accessory["type"]] * accessory["units"]

    for module in session_summary["lighting_sync_modules"]:
        if "product" in module:
            product_name, size = module["product"].rsplit(" ", 1)
            size = size.strip("()")
            product_cost = smart_av_tree["hue_lights"][product_name]
            if isinstance(product_cost, dict):
                total_cost += product_cost.get(size, 0) * module["units"]
            else:
                total_cost += product_cost * module["units"]
        elif "module" in module:
            module_name = module["module"]
            total_cost += smart_av_tree["lighting_sync"]["PC-based"]["Nanoleaf"][module_name] * module["units"]

    for space, speakers in session_summary["speakers"].items():
        for speaker in speakers:
            total_cost += smart_av_tree["speaker_types"].get(speaker["type"], 0) * speaker["units"]

    session_summary["cost_estimation"] = total_cost
    session_summary["complexity_score"] = round(total_complexity / num_scenarios, 1) if num_scenarios > 0 else 0
    session_summary["ecological_rating"] = round(total_ecology / num_scenarios, 1) if num_scenarios > 0 else 0

def generate_dialogue():
    dialogue = []
    session_summary = {
        "scenarios": [],
        "streaming_accessories": [],
        "lighting_sync_modules": [],
        "speakers": {},
        "cost_estimation": 0,
        "complexity_score": 0,
        "ecological_rating": 0
    }

    # Step 1: Scenario Selection
    scenarios = list(smart_av_tree["scenarios"].keys())
    chosen_scenarios = generate_random_response(scenarios)
    session_summary["scenarios"].extend(chosen_scenarios)

    dialogue.append({
        "role": "AI",
        "text": "Please select the scenarios you are interested in:"
    })
    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_scenarios)
    })

    # Step 2: Ask about smart streaming accessories if applicable
    if any(s in ["Video Conferencing", "Fitness and Health", "Accessibility Features"] for s in chosen_scenarios):
        accessories = list(smart_av_tree["smart_streaming_accessories"].keys())
        chosen_accessories = generate_random_response(accessories)
        
        dialogue.append({
            "role": "AI",
            "text": "Do you need a smart streaming accessory for your display?"
        })
        dialogue.append({
            "role": "User",
            "text": ", ".join(chosen_accessories)
        })

        for accessory in chosen_accessories:
            units = random.randint(1, 3)
            session_summary["streaming_accessories"].append({"type": accessory, "units": units})
            dialogue.append({
                "role": "AI",
                "text": f"How many {accessory}s do you need?"
            })
            dialogue.append({
                "role": "User",
                "text": str(units)
            })

    # Step 3: Ask about lighting sync options if applicable
    if any(s in ["Home Theater Experience", "Gaming", "Fitness and Health"] for s in chosen_scenarios):
        sync_lighting = random.choice(["Yes", "No"])
        
        dialogue.append({
            "role": "AI",
            "text": "Do you want ambiance light synchronization with video content?"
        })
        dialogue.append({
            "role": "User",
            "text": sync_lighting
        })

        if sync_lighting == "Yes":
            setup = random.choice(["TV-based", "PC-based"])
            dialogue.append({
                "role": "AI",
                "text": "Do you want to sync the ambiance light to TV-based or PC-based setup?"
            })
            dialogue.append({
                "role": "User",
                "text": setup
            })

            if setup == "TV-based":
                hue_lights = list(smart_av_tree["hue_lights"].keys())
                chosen_lights = generate_random_response(hue_lights)
                
                for light in chosen_lights:
                    tv_size = random.choice([32, 43, 55, 65, 75])
                    size_category = "small" if tv_size <= 43 else "medium" if tv_size <= 55 else "large"
                    session_summary["lighting_sync_modules"].append({"product": f"{light} ({size_category})", "units": 1})
                    
                    dialogue.append({
                        "role": "AI",
                        "text": f"How many inches is your TV for {light}?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": str(tv_size)
                    })

            elif setup == "PC-based":
                nanoleaf_options = list(smart_av_tree["lighting_sync"]["PC-based"]["Nanoleaf"].keys())
                chosen_modules = generate_random_response(nanoleaf_options)
                
                dialogue.append({
                    "role": "AI",
                    "text": "Do you need additional Nanoleaf light modules?"
                })
                dialogue.append({
                    "role": "User",
                    "text": ", ".join(chosen_modules)
                })

                for module in chosen_modules:
                    units = random.randint(1, 3)
                    session_summary["lighting_sync_modules"].append({"module": module, "units": units})
                    
                    dialogue.append({
                        "role": "AI",
                        "text": f"How many {module} modules do you need?"
                    })
                    dialogue.append({
                        "role": "User",
                        "text": str(units)
                    })

    # Step 4: Speaker Budget and Selection
    spaces = smart_av_tree["spaces"] + ["I don't want any smart speaker"]
    chosen_spaces = generate_random_response(spaces)
    
    dialogue.append({
        "role": "AI",
        "text": "Where do you want to install smart speakers?"
    })
    dialogue.append({
        "role": "User",
        "text": ", ".join(chosen_spaces)
    })

    if "I don't want any smart speaker" not in chosen_spaces:
        # Ask for speaker budget
        speaker_budget = random.choice(["low ($50-$100)", "middle ($150-$300)", "high ($400-$1000)"])
        dialogue.append({
            "role": "AI",
            "text": "Which price level are you ready to pay for a smart speaker?"
        })
        dialogue.append({
            "role": "User",
            "text": speaker_budget
        })

        indoor_spaces = [space for space in chosen_spaces if space != "Outdoor"]
        outdoor_space_selected = "Outdoor" in chosen_spaces

        for space in indoor_spaces:
            speaker_types = generate_random_response([stype for stype in smart_av_tree["speaker_types"] if stype != "Outdoor Speaker"])
            for speaker in speaker_types:
                units = random.randint(1, 3)
                session_summary["speakers"].setdefault(space, []).append({"type": speaker, "units": units, "budget": speaker_budget})
                
                dialogue.append({
                    "role": "AI",
                    "text": f"What type of speakers do you need in the {space}?"
                })
                dialogue.append({
                    "role": "User",
                    "text": speaker
                })
                dialogue.append({
                    "role": "AI",
                    "text": f"How many {speaker}s do you need in the {space}?"
                })
                dialogue.append({
                    "role": "User",
                    "text": str(units)
                })

        if outdoor_space_selected:
            units = random.randint(1, 3)
            session_summary["speakers"].setdefault("Outdoor", []).append({"type": "Outdoor Speaker", "units": units, "budget": speaker_budget})
            
            dialogue.append({
                "role": "AI",
                "text": "What type of speakers do you need in the Outdoor?"
            })
            dialogue.append({
                "role": "User",
                "text": "Outdoor Speaker"
            })
            dialogue.append({
                "role": "AI",
                "text": f"How many Outdoor Speakers do you need?"
            })
            dialogue.append({
                "role": "User",
                "text": str(units)
            })

    # Calculate metrics
    calculate_cost_complexity_ecology(session_summary)

    # Generate the final summary text
    summary_text = (
        "============= Smart AV Plan Summary =============\n\n" +
        f"Scenarios Chosen: {', '.join(session_summary['scenarios'])}\n\nProducts:\n" +
        "\n".join([
            f"  - {accessory['units']} units of {accessory['type']}"
            for accessory in session_summary["streaming_accessories"]
        ]) +
        "\n\nLighting Sync Modules:\n" +
        "\n".join([
            f"  - {module['units']} units of {module['product'] if 'product' in module else module['module']}"
            for module in session_summary["lighting_sync_modules"]
        ]) +
        "\n\nSpeakers:\n" +
        "\n".join([
            f"  - {space}: {details['units']} units of {details['type']} (Budget: {details['budget']})"
            for space, speakers in session_summary["speakers"].items() for details in speakers
        ]) +
        f"\n\nTotal Estimated Cost: ${session_summary['cost_estimation']}\n" +
        f"Installation Complexity: {session_summary['complexity_score']}/5\n" +
        f"Ecological Rating: {session_summary['ecological_rating']}/5"
    )

    dialogue.append({
        "role": "AI",
        "text": summary_text
    })

    return dialogue

def generate_dataset_AV(num_samples, output_file="smart_home_dialogues.json"):
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
        
    print(f"Generated {num_samples} AV dialogues and saved to {output_file}.")


if __name__ == "__main__":
    generate_dataset_AV(3, output_file="smart_home_dialogues.json")
    
