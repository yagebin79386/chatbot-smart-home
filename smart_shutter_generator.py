import json
import random
import os

def random_choice(options, multi_select=False):
    """Simulate user input for a choice."""
    if multi_select:
        return random.sample(range(1, len(options) + 1), random.randint(1, len(options)))
    else:
        return random.randint(1, len(options))


def generate_dataset_shutter(num_samples):
    """Generate multiple dialogues and plan summaries based on num_samples."""
    dataset = []

    for _ in range(num_samples):
        spaces = []
        summary_plan = {"Devices": {}, "Scenarios": []}
        dialogue = []

        # Step 1: Select Smart Curtain/Shutter/Both
        dialogue.append({"role": "AI", "text": "Do you want to configure a Smart Curtain System, Smart Shutter System, or Both?"})
        options = ["Smart Curtain System", "Smart Shutter System", "Both"]
        selected_option = random_choice(options)
        dialogue.append({"role": "User", "text": options[selected_option - 1]})
        summary_plan["Scenarios"].append(options[selected_option - 1])

        # Step 2: Configure Smart Curtain System
        if selected_option in [1, 3]:
            spaces_options = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
            dialogue.append({"role": "AI", "text": "In which spaces do you want a smart curtain system?"})
            selected_spaces = random_choice(spaces_options, multi_select=True)
            dialogue.append({"role": "User", "text": ", ".join([spaces_options[i - 1] for i in selected_spaces])})

            for space_index in selected_spaces:
                space_name = spaces_options[space_index - 1]
                num_units = random.randint(1, 3)
                dialogue.append({"role": "AI", "text": f"How many {space_name}s do you want to install smart curtains in?"})
                dialogue.append({"role": "User", "text": str(num_units)})
                for i in range(num_units):
                    spaces.append(f"{space_name} {i + 1}")

            for space in spaces:
                curtain_types = ["Roller", "Double Roller", "Venetian", "Honeycomb", "Curtain", "Pleated", "Vertical", "Roman"]
                dialogue.append({"role": "AI", "text": f"What type of curtain do you have in {space}?"})
                selected_types = random_choice(curtain_types, multi_select=True)
                dialogue.append({"role": "User", "text": ", ".join([curtain_types[i - 1] for i in selected_types])})

                for curtain_type_index in selected_types:
                    curtain_type = curtain_types[curtain_type_index - 1]
                    quantity = random.randint(1, 3)
                    dialogue.append({"role": "AI", "text": f"How many {curtain_type} curtains do you have in {space}?"})
                    dialogue.append({"role": "User", "text": str(quantity)})

                    for unit in range(1, quantity + 1):
                        length = round(random.uniform(1, 3), 2)
                        dialogue.append({"role": "AI", "text": f"Enter the length of this {curtain_type} curtain (Unit {unit}) in meters:"})
                        dialogue.append({"role": "User", "text": str(length)})

                        product_name = f"MotionBlind {curtain_type} Motor"
                        price = 100 + int(length * 50)  # Example pricing logic
                        if product_name in summary_plan["Devices"]:
                            summary_plan["Devices"][product_name]["Quantity"] += 1
                        else:
                            summary_plan["Devices"][product_name] = {"Quantity": 1, "Price": price, "Complexity": 1}

        # Step 3: Configure Smart Shutter System
        if selected_option in [2, 3]:
            spaces_options = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
            dialogue.append({"role": "AI", "text": "In which spaces do you want a smart shutter system?"})
            selected_spaces = random_choice(spaces_options, multi_select=True)
            dialogue.append({"role": "User", "text": ", ".join([spaces_options[i - 1] for i in selected_spaces])})

            for space_index in selected_spaces:
                space_name = spaces_options[space_index - 1]
                num_units = random.randint(1, 3)
                dialogue.append({"role": "AI", "text": f"How many {space_name}s do you want to install smart shutters in?"})
                dialogue.append({"role": "User", "text": str(num_units)})
                for i in range(num_units):
                    spaces.append(f"{space_name} {i + 1}")

            for space in spaces:
                need_shutter = random_choice(["Yes", "No"])
                dialogue.append({"role": "AI", "text": f"Do you want a smart shutter system in {space}?"})
                dialogue.append({"role": "User", "text": "Yes" if need_shutter == 1 else "No"})

                if need_shutter == 1:
                    shutter_types = ["Electric Motor", "Manual Belt Winder"]
                    dialogue.append({"role": "AI", "text": f"What type of shutter system do you have in {space}?"})
                    shutter_type = random_choice(shutter_types)
                    dialogue.append({"role": "User", "text": shutter_types[shutter_type - 1]})

                    if shutter_type == 1:
                        quantity = random.randint(1, 3)
                        dialogue.append({"role": "AI", "text": f"How many Aqara Smart Shutter Switches do you need in {space}?"})
                        dialogue.append({"role": "User", "text": str(quantity)})
                        if "Aqara Smart Shutter Switch" in summary_plan["Devices"]:
                            summary_plan["Devices"]["Aqara Smart Shutter Switch"]["Quantity"] += quantity
                        else:
                            summary_plan["Devices"]["Aqara Smart Shutter Switch"] = {"Quantity": quantity, "Price": 40, "Complexity": 2}

                    elif shutter_type == 2:
                        if "HomePilot Premium Gateway" not in summary_plan["Devices"]:
                            summary_plan["Devices"]["HomePilot Premium Gateway"] = {"Quantity": 1, "Price": 120, "Complexity": 1}
                        quantity = random.randint(1, 3)
                        dialogue.append({"role": "AI", "text": f"How many HomePilot Smart Belt Winders do you need in {space}?"})
                        dialogue.append({"role": "User", "text": str(quantity)})
                        if "HomePilot Smart Belt Winder" in summary_plan["Devices"]:
                            summary_plan["Devices"]["HomePilot Smart Belt Winder"]["Quantity"] += quantity
                        else:
                            summary_plan["Devices"]["HomePilot Smart Belt Winder"] = {"Quantity": quantity, "Price": 80, "Complexity": 2}

        # Step 4: Scenario-Specific Questions
        scenarios = [
            "Automated environment light control",
            "Privacy management",
            "Energy efficiency",
            "Sleep quality improvement",
            "Voice-controlled convenience"
        ]

        dialogue.append({"role": "AI", "text": "Do you want to configure additional automation based on specific scenarios?"})
        selected_scenarios = random_choice(scenarios, multi_select=True)
        dialogue.append({"role": "User", "text": ", ".join([scenarios[i - 1] for i in selected_scenarios])})

        # Common logic for scenarios 1, 2, 3
        if any(scenario in [1, 2, 3] for scenario in selected_scenarios):
            dialogue.append({"role": "AI", "text": "If you want to achieve the best effect of the light control and view shuttering or warmth sheltering, it's better to add also the light/temperature sensor."})
            add_temp_sensor = random_choice(spaces, multi_select=True)
            dialogue.append({"role": "User", "text": ", ".join([spaces[i - 1] for i in add_temp_sensor])})

            for space_index in add_temp_sensor:
                space_name = spaces[space_index - 1]
                sensor_name = f"Light/Temperature Sensor for {space_name}"
                if sensor_name not in summary_plan["Devices"]:
                    summary_plan["Devices"][sensor_name] = {"Quantity": 1, "Price": 30, "Complexity": 1}

        # Scenario 2: Presence-based automation
        if 2 in selected_scenarios:
            dialogue.append({"role": "AI", "text": "We recommend setting up automation based on your absence/presence and outdoor/indoor light contrast."})
            summary_plan["Scenarios"].append("Presence-based automation (Complexity added)")

        # Scenario 3: Weather and temperature sensor configuration
        if 3 in selected_scenarios:
            dialogue.append({"role": "AI", "text": "We suggest setting up automation depending on weather conditions and interior temperature sensors."})
            need_temp_sensor = random_choice(spaces, multi_select=True)
            dialogue.append({"role": "User", "text": ", ".join([spaces[i - 1] for i in need_temp_sensor])})

            for space_index in need_temp_sensor:
                space_name = spaces[space_index - 1]
                sensor_name = f"Light/Temperature Sensor for {space_name}"
                if sensor_name not in summary_plan["Devices"]:
                    summary_plan["Devices"][sensor_name] = {"Quantity": 1, "Price": 30, "Complexity": 1}

        # Scenario 4: Sleep automation
        if 4 in selected_scenarios:
            dialogue.append({"role": "AI", "text": "For sleep quality improvement, we suggest automating shutters with sunrise/sunset schedules."})
            summary_plan["Scenarios"].append("Sleep automation (additional complexity added)")

        # Scenario 5: Voice-controlled convenience
        if 5 in selected_scenarios:
            dialogue.append({"role": "AI", "text": "Do you need smart speakers in any spaces?"})
            speaker_spaces = random_choice(spaces, multi_select=True)
            dialogue.append({"role": "User", "text": ", ".join([spaces[i - 1] for i in speaker_spaces])})

            for space_index in speaker_spaces:
                space_name = spaces[space_index - 1]
                speaker_name = f"Smart Speaker in {space_name}"
                if speaker_name in summary_plan["Devices"]:
                    summary_plan["Devices"][speaker_name]["Quantity"] += 1
                else:
                    summary_plan["Devices"][speaker_name] = {"Quantity": 1, "Price": 50, "Complexity": 1}

       
        # Step 5: Summary
        total_cost = 0
        total_device_complexity = 0
        scenario_weight = len(summary_plan["Scenarios"])
        device_count = len(summary_plan["Devices"])
        max_possible_complexity = 5

        # Group devices by spaces
        space_summary = {space: [] for space in spaces}
        for device, details in summary_plan["Devices"].items():
            for space in spaces:
                if space in device:
                    space_summary[space].append(f"{details['Quantity']} x {device} (€{details['Price']} each)")

        # Calculate total cost and complexity
        for device, details in summary_plan["Devices"].items():
            total_cost += details['Quantity'] * details['Price']
            total_device_complexity += details['Complexity'] * details['Quantity']

        # Calculate installation complexity and ecological rating
        complexity_from_scenarios = scenario_weight / 5 * 2.5
        complexity_from_devices = min(total_device_complexity / max(1, device_count), 2.5)
        installation_complexity = min(max_possible_complexity, complexity_from_scenarios + complexity_from_devices)
        ecological_rating = round(5 - installation_complexity, 1)

        # Format the summary as a string for inclusion in the dialogue
        summary_text = (
            "============= Smart Curtain/Shutter Plan Summary =============\n\n"
            "Scenarios Selected:\n"
            f"  - {', '.join(summary_plan['Scenarios'])}\n\n"
            "Devices Configured by Space:\n"
        )

        for space, devices in space_summary.items():
            summary_text += f"  {space}:\n"
            for device in devices:
                summary_text += f"    - {device}\n"

        summary_text += (
            f"\nTotal Estimated Cost: €{total_cost}\n"
            f"Ecological Rating: {ecological_rating}/5\n"
            f"Installation Complexity: {round(installation_complexity, 1)}/5\n"
        )

        # Append the summary as an AI role to the dialogue list
        dialogue.append({"role": "AI", "text": summary_text})

        # Add the dialogue to the dataset
        dataset.append(dialogue)
    return dataset

    
        
def generate_json_shutter(num_samples, output_file):
    #check if the file already exists
    if os.path.exists(output_file):
        # Load existing data from the file
        with open(output_file, "r") as f:
            existing_data = json.load(f)
    else:
        # if the file doesn't exist, initialize an empty list
        existing_data = []

    dataset = generate_dataset_shutter(num_samples)
    # Add the generated conversation to the dialogue
    existing_data.extend(dataset)

    #Save the updated dateset to the JSON file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    print(f"Generated {num_samples} shutter dialogues and saved to {output_file}.")


# Run the function with desired number of loops
if __name__ == "__main__":
    generate_json_shutter(num_samples=1, output_file="smart_home_dialogues.json")
    
