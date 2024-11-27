# Smart AV System Decision Tree
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
            "small": 300,  # For TVs 32-43 inches
            "medium": 350,  # For TVs 50-55 inches
            "large": 400   # For TVs 65 inches and larger
        }
    },
    "speaker_prices": {
        "low": (50, 100),
        "middle": (150, 300),
        "high": (400, 1000)
    },
    "speaker_types": {
        "Soundbar": 200,
        "Subwoofer": 150,
        "Bookshelf Speakers": 300,
        "Tower Speakers": 500,
        "Portable Bluetooth Speakers": 100,
        "Outdoor Speaker": 250
    },
    "spaces": ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
}

# Summary of user responses
summary = {
    "scenarios": [],
    "streaming_accessories": [],
    "lighting_sync_modules": [],
    "speakers": {},
    "technical_requirements": [],
    "cost_estimation": 0,
    "complexity_score": 0,
    "ecological_rating": 0
}

# Helper function for indexed questions with validation
def ask_question(prompt, choices, multi_select=False):
    while True:
        print(f"\n{prompt}")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")
        
        response = input("\nEnter your choice(s) (comma-separated if multiple): ").split(',')
        
        # Validate input: ensure only numbers separated by commas are allowed
        if not all(idx.strip().isdigit() for idx in response):
            print("I don't really understand your choice. Could you choose from the available options using comma-separated numbers?")
            continue
        
        try:
            if multi_select:
                return [choices[int(idx.strip()) - 1] for idx in response if idx.strip().isdigit()]
            else:
                return choices[int(response[0].strip()) - 1]
        except (IndexError, ValueError):
            print("Invalid input. Please choose from the available options.")

# Step 1: Ask Scenario Questions
def ask_scenario_questions():
    scenarios = list(smart_av_tree["scenarios"].keys())
    chosen_scenarios = ask_question(
        "Please select the scenarios you are interested in:",
        scenarios,
        multi_select=True
    )
    summary["scenarios"].extend(chosen_scenarios)

# Step 2: Scenario-Specific Questions
def ask_scenario_specific_questions():
    # Ensure the smart streaming accessory question is asked if relevant scenarios are chosen
    if any(s in ["Video Conferencing", "Fitness and Health", "Accessibility Features"] for s in summary["scenarios"]):
        accessories = ask_question(
            "Do you need a smart streaming accessory for your display?",
            list(smart_av_tree["smart_streaming_accessories"].keys()),
            multi_select=True
        )
        for accessory in accessories:
            units = int(input(f"How many {accessory}s do you need? "))
            summary["streaming_accessories"].append({"type": accessory, "units": units})
    
    if any(s in ["Home Theater Experience", "Gaming", "Fitness and Health"] for s in summary["scenarios"]):
        sync_lighting = ask_question(
            "Do you want ambiance light synchronization with video content?",
            ["Yes", "No"]
        )
        if sync_lighting == "Yes":
            setup = ask_question(
                "Do you want to sync the ambiance light to TV-based or PC-based setup?",
                ["TV-based", "PC-based"]
            )
            if setup == "TV-based":
                hue_lights = ask_question(
                    "Do you want additional designated Hue ambiance lights?",
                    list(smart_av_tree["hue_lights"].keys()),
                    multi_select=True
                )
                for light in hue_lights:
                    if light == "Philips Hue Play Light Bars":
                        pairs = int(input("How many pairs of Philips Hue Play Light Bars do you need? "))
                        summary["lighting_sync_modules"].append({"product": "Philips Hue Play Light Bars", "units": pairs})
                    elif light in ["Philips Hue Lightstrip Plus", "Philips Hue Gradient Lightstrip"]:
                        tv_size = int(input(f"How many inches is your TV for {light}? "))
                        if tv_size <= 43:
                            size_category = "small"
                        elif tv_size <= 55:
                            size_category = "medium"
                        else:
                            size_category = "large"
                        units = 1  # Assign one product per TV
                        product = f"{light} ({size_category})"
                        summary["lighting_sync_modules"].append({"product": product, "units": units})
                        print(f"Automatically assigned {product} for your {tv_size}-inch TV.")
            elif setup == "PC-based":
                nanoleaf = ask_question(
                    "Do you need additional Nanoleaf light modules?",
                    list(smart_av_tree["lighting_sync"]["PC-based"]["Nanoleaf"].keys()),
                    multi_select=True
                )
                for module in nanoleaf:
                    units = int(input(f"How many {module} modules do you need? "))
                    summary["lighting_sync_modules"].append({"module": module, "units": units})

# Step 3: Ask Speaker Relevant Questions
def ask_speaker_questions():
    # Add "I don't want any smart speaker" option
    speaker_choices = smart_av_tree["spaces"] + ["I don't want any smart speaker"]
    spaces = ask_question(
        "Where do you want to install smart speakers?",
        speaker_choices,
        multi_select=True
    )

    # If user selects "I don't want any smart speaker", skip further speaker-related questions
    if "I don't want any smart speaker" in spaces:
        print("No smart speakers selected.")
        return

    # Proceed with speaker budget and configurations if speakers are selected
    speaker_budget = ask_question(
        "Which price level are you ready to pay for a smart speaker?",
        ["low ($50-$100)", "middle ($150-$300)", "high ($400-$1000)"]
    )
    
    indoor_spaces = [space for space in spaces if space != "Outdoor"]
    outdoor_space_selected = "Outdoor" in spaces

    for space in indoor_spaces:
        speaker_types = ask_question(
            f"What type of speakers do you need in the {space}?",
            [stype for stype in smart_av_tree["speaker_types"] if stype != "Outdoor Speaker"],
            multi_select=True
        )
        for speaker in speaker_types:
            units = int(input(f"How many {speaker}s do you need in the {space}? "))
            summary["speakers"].setdefault(space, []).append({"type": speaker, "units": units, "budget": speaker_budget})
    
    if outdoor_space_selected:
        units = int(input("How many Outdoor Speakers do you need? "))
        summary["speakers"].setdefault("Outdoor", []).append({"type": "Outdoor Speaker", "units": units, "budget": speaker_budget})

# Step 4: Calculate Cost, Complexity, and Ecology
def calculate_metrics():
    total_cost = 0
    total_complexity = 0
    total_ecology = 0
    num_scenarios = len(summary["scenarios"])

    for scenario in summary["scenarios"]:
        scenario_details = smart_av_tree["scenarios"][scenario]
        total_cost += scenario_details["base_cost"]
        total_complexity += scenario_details["complexity"]
        total_ecology += scenario_details["ecology"]

    for accessory in summary["streaming_accessories"]:
        total_cost += smart_av_tree["smart_streaming_accessories"][accessory["type"]] * accessory["units"]

    for module in summary["lighting_sync_modules"]:
        if "product" in module:
            product_name, size = module["product"].rsplit(" ", 1)
            size = size.strip("()")
            if product_name == "Philips Hue Play Light Bars":
                total_cost += smart_av_tree["hue_lights"][product_name] * module["units"]
            elif product_name in ["Philips Hue Lightstrip Plus", "Philips Hue Gradient Lightstrip"]:
                total_cost += smart_av_tree["hue_lights"][product_name][size] * module["units"]
            total_complexity += 1.5
        elif "module" in module:
            total_cost += smart_av_tree["lighting_sync"]["PC-based"]["Nanoleaf"][module["module"]] * module["units"]
            total_complexity += 1.5

    for space, speaker_list in summary["speakers"].items():
        for speaker in speaker_list:
            total_cost += smart_av_tree["speaker_types"][speaker["type"]] * speaker["units"]

    summary["cost_estimation"] = total_cost
    summary["complexity_score"] = total_complexity / num_scenarios if num_scenarios > 0 else 0
    summary["ecological_rating"] = total_ecology / num_scenarios if num_scenarios > 0 else 0   

# Step 5: Print Summary
def print_summary():
    print("\n============= Smart AV Plan Summary =============")
    print(f"Scenarios Chosen:\n  - {', '.join(summary['scenarios'])}")
    print("\nProducts (excluding speakers):")
    for accessory in summary["streaming_accessories"]:
        print(f"  - {accessory['units']} units of {accessory['type']}")
    for module in summary["lighting_sync_modules"]:
        if "product" in module:
            print(f"  - {module['units']} units of {module['product']}")
        elif "module" in module:
            print(f"  - {module['units']} units of {module['module']}")

    print("\nSmart Speakers by Space:")
    for space, speaker_list in summary["speakers"].items():
        print(f"  - {space}:")
        for speaker in speaker_list:
            print(f"    - {speaker['units']} units of {speaker['type']} (Budget: {speaker['budget']})")

    print(f"\nTotal Estimated Cost: ${summary['cost_estimation']}")
    print(f"Installation Complexity: {summary['complexity_score']:.1f}/5")
    print(f"Ecological Rating: {summary['ecological_rating']:.1f}/5")

# Main function to execute
if __name__ == "__main__":
    ask_scenario_questions()
    ask_scenario_specific_questions()
    ask_speaker_questions()
    calculate_metrics()
    print_summary()

