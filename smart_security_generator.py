import json
import random
import os

def random_choice(options, multi_select=False):
    """Generate random choices for a question."""
    if multi_select:
        return random.sample(range(1, len(options) + 1), random.randint(1, len(options)))
    else:
        return random.randint(1, len(options))


def generate_dataset_security(num_samples):
    """Generate dialogues with random choices."""
    dialogues = []
    dataset = []
    for _ in range(num_samples):
        summary_plan = {"Scenarios": [], "Devices": {}, "Installation Complexity": 0, "Estimated Cost": 0}
        conversation = []

        # Step 1: Select scenarios
        scenarios = [
            "Remote Indoor Monitoring and Motion Detection",
            "Two-Way Communication and Smart Locks",
            "Integrated Alarms and Environmental Hazard Monitoring",
            "Package and Activity Monitoring",
            "Smart Lighting Integration",
            "Health Emergencies"
        ]
        question = "Please select the scenarios you are interested in smart security system: (choose multiple):"
        conversation.append({
            "role": "AI",
            "text": question + "\n" + "\n".join([f"{i+1}. {scenario}" for i, scenario in enumerate(scenarios)])
        })
        selected_scenarios = random_choice(scenarios, multi_select=True)
        user_text = ", ".join([scenarios[i - 1] for i in selected_scenarios])
        conversation.append({"role": "User", "text": user_text})
        for scenario_index in selected_scenarios:
            summary_plan["Scenarios"].append(scenarios[scenario_index - 1])

        # Handle each scenario
        for scenario_index in selected_scenarios:
            if scenario_index == 1:  # Scenario 1: Remote Indoor Monitoring
                question = "What are your main priorities for the camera? (Select all that apply)"
                options = [
                    "High video resolution and clarity (e.g., 2K or better)",
                    "Budget-friendly with essential features",
                    "Compatibility with a specific ecosystem (e.g., Google Home, Alexa, or HomeKit)",
                    "Advanced AI features like facial recognition or pet detection",
                    "Comprehensive local storage options and privacy"
                ]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_priorities = random_choice(options, multi_select=True)
                user_text = ", ".join([options[i - 1] for i in selected_priorities])
                conversation.append({"role": "User", "text": user_text})

                # Additional questions for Scenario 1
                questions_and_options = [
                    (
                        "What kind of detection capabilities do you need?",
                        [
                            "AI-based detection for people and pets",
                            "Basic motion detection (no advanced AI features)",
                            "Advanced AI for recognizing faces, pets, and gestures",
                            "Noise detection for events like breaking glass or loud sounds",
                            "No detection needed; just want live video"
                        ]
                    ),
                    (
                        "Do you prefer local storage, cloud storage, or both?",
                        [
                            "Local storage (e.g., MicroSD or NAS) to avoid subscription fees",
                            "Cloud storage for easy remote access and backups",
                            "Both local and cloud storage options"
                        ]
                    ),
                    (
                        "Which smart home ecosystem do you use or plan to use?",
                        [
                            "Google Home",
                            "Amazon Alexa",
                            "Apple HomeKit",
                            "A combination of ecosystems (multi-platform compatibility)"
                        ]
                    ),
                    (
                        "Do you prefer advanced field of view capabilities (e.g., pan, tilt, or wide-angle)?",
                        [
                            "Wide-angle view (e.g., 130° or more)",
                            "Full 360° pan and tilt for broader coverage",
                            "A standard fixed field of view is sufficient"
                        ]
                    ),
                    (
                        "Do you need two-way audio?",
                        [
                            "Yes, I need to communicate through the camera",
                            "No, I only need video monitoring"
                        ]
                    ),
                    (
                        "Is privacy protection (e.g., physical privacy shutter or local data storage) important to you?",
                        [
                            "Yes, I want a camera with hardware or software privacy features",
                            "No, privacy protection is not a priority"
                        ]
                    )
                ]

                responses = []
                for question, options in questions_and_options:
                    conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                    selected_option = random_choice(options)
                    responses.append(selected_option)
                    user_text = options[selected_option - 1]
                    conversation.append({"role": "User", "text": user_text})

                # Add camera recommendation
                summary_plan["Devices"]["Indoor Camera"] = {"Model": "Eufy Cam 2K", "Quantity": random.randint(1, 3), "Price": 45}

            elif scenario_index == 2:  # Scenario 2: Two-Way Communication and Smart Locks
                conversation.append({"role": "AI", "text": "You selected Scenario 2: Two-Way Communication and Smart Locks."})
                
                # Step 1: Smart locks
                question = "What type of doors do you want to equip with smart locks?"
                options = [
                    "All doors have a handle",
                    "All doors do not have a handle",
                    "Some doors have a handle, and some do not"
                ]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_option = random_choice(options)
                user_text = options[selected_option - 1]
                conversation.append({"role": "User", "text": user_text})

                if selected_option == 1:
                    summary_plan["Devices"]["Smart Locks"] = {"Model": "Aqara U200", "Quantity": random.randint(1, 5), "Price": 150}
                elif selected_option == 2:
                    summary_plan["Devices"]["Smart Locks"] = {"Model": "Aqara U300", "Quantity": random.randint(1, 5), "Price": 180}
                else:
                    summary_plan["Devices"]["Smart Locks with Handle"] = {"Model": "Aqara U200", "Quantity": random.randint(1, 3), "Price": 150}
                    summary_plan["Devices"]["Smart Locks without Handle"] = {"Model": "Aqara U300", "Quantity": random.randint(1, 3), "Price": 180}

                # Step 2: Doorbell
                question = "Do you want a doorbell with two-way communication, AI face recognition, and end-to-end encryption?"
                options = ["Yes", "No"]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_option = random_choice(options)
                user_text = options[selected_option - 1]
                conversation.append({"role": "User", "text": user_text})

                if selected_option == 1:
                    summary_plan["Devices"]["Doorbell"] = {"Model": "Aqara G4", "Quantity": 1, "Price": 120}

            elif scenario_index == 3:  # Scenario 3: Integrated Alarms and Environmental Hazard Monitoring
                conversation.append({"role": "AI", "text": "You selected Scenario 3: Integrated Alarms and Environmental Hazard Monitoring."})

                # Step 1: Environmental hazards
                question = "What kind of environmental hazards do you want to monitor? (Select all that apply)"
                options = [
                    "Smoke and Fire",
                    "Carbon Monoxide",
                    "Gas Leaks",
                    "Flood",
                    "Digital Security Threats"
                ]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_hazards = random_choice(options, multi_select=True)
                user_text = ", ".join([options[i - 1] for i in selected_hazards])
                conversation.append({"role": "User", "text": user_text})

                for hazard in selected_hazards:
                    hazard_name = options[hazard - 1]
                    quantity = random.randint(1, 3)
                    summary_plan["Devices"][hazard_name] = {"Model": f"{hazard_name} Sensor", "Quantity": quantity, "Price": 50}

                # Step 2: Penetration test for digital security
                if "Digital Security Threats" in [options[i - 1] for i in selected_hazards]:
                    question = "Would you like to learn more about penetration testing for your digital system?"
                    options = ["Yes", "No"]
                    conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                    selected_option = random_choice(options)
                    user_text = options[selected_option - 1]
                    conversation.append({"role": "User", "text": user_text})

                    if selected_option == 1:
                        summary_plan["Devices"]["Penetration Test"] = {"Model": "Digital Penetration Test", "Quantity": 1, "Price": 200}

            elif scenario_index == 4:  # Scenario 4: Package and Activity Monitoring
                conversation.append({"role": "AI", "text": "You selected Scenario 4: Package and Activity Monitoring."})

                # Step 1: Vulnerable areas
                question = "Which areas do you identify as vulnerable? (Select all that apply)"
                options = [
                    "Entrances",
                    "Driveways",
                    "Pathways",
                    "Windows",
                    "Backyard",
                    "Gates or Fences",
                    "Package Delivery Zones"
                ]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_areas = random_choice(options, multi_select=True)
                user_text = ", ".join([options[i - 1] for i in selected_areas])
                conversation.append({"role": "User", "text": user_text})

                # Step 2: Cameras or sensors for vulnerable areas
                for area in selected_areas:
                    if area <= len(options):  # Ensure the selected area index is within range
                        area_name = options[area - 1]
                        if area_name in ["Windows", "Gates or Fences"]:
                            question = f"Do you prefer a security camera or a sensor for {area_name}?"
                            options_camera_sensor = ["Security Camera", "Sensor"]
                            conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options_camera_sensor)])})
                            selected_option = random_choice(options_camera_sensor)
                            user_text = options_camera_sensor[selected_option - 1]
                            conversation.append({"role": "User", "text": user_text})
                
                            if selected_option == 2:
                                summary_plan["Devices"][f"{area_name} Sensor"] = {"Model": f"{area_name} Sensor", "Quantity": random.randint(1, 3), "Price": 50}
                            else:
                                summary_plan["Devices"][f"{area_name} Camera"] = {"Model": "Outdoor Security Camera", "Quantity": random.randint(1, 3), "Price": 200}
                        else:
                            summary_plan["Devices"][f"{area_name} Camera"] = {"Model": "Outdoor Security Camera", "Quantity": random.randint(1, 3), "Price": 200}
                    else:
                        # Log an error in the conversation if an invalid area is chosen
                        conversation.append({"role": "AI", "text": f"Invalid selection: {area} is out of range for available options."})

        
            elif scenario_index == 5:  # Scenario 5: Smart Lighting Integration
                conversation.append({"role": "AI", "text": "You selected Scenario 5: Smart Lighting Integration."})

                question = "Do you want to configure smart lighting systems for energy savings and security?"
                options = ["Yes", "No"]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_option = random_choice(options)
                user_text = options[selected_option - 1]
                conversation.append({"role": "User", "text": user_text})

                if selected_option == 1:
                    summary_plan["Devices"]["Smart Lighting System"] = {"Model": "Philips Hue", "Quantity": random.randint(1, 10), "Price": 20}

            elif scenario_index == 6:  # Scenario 6: Health Emergencies
                conversation.append({"role": "AI", "text": "You selected Scenario 6: Health Emergencies."})

                # Step 1: Abnormality detection or health monitoring
                question = "Do you want primary abnormality detection or a dedicated health monitoring system?"
                options = ["Primary Abnormality Detection", "Dedicated Health Monitoring System"]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_option = random_choice(options)
                user_text = options[selected_option - 1]
                conversation.append({"role": "User", "text": user_text})

                if selected_option == 2:
                    summary_plan["Devices"]["Health Monitoring System"] = {"Model": "Philips Lifeline", "Quantity": 1, "Price": 500}

                # Step 2: Fall detection or wearable devices
                question = "Do you also want fall detection sensors or wearable devices? (Select all that apply)"
                options = ["Fall Detection Sensors", "Wearable Devices"]
                conversation.append({"role": "AI", "text": question + "\n" + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])})
                selected_devices = random_choice(options, multi_select=True)
                user_text = ", ".join([options[i - 1] for i in selected_devices])
                conversation.append({"role": "User", "text": user_text})

                for device in selected_devices:
                    if device == 1:
                        summary_plan["Devices"]["Fall Detection Sensors"] = {"Model": "Aqara FP2 Sensor", "Quantity": random.randint(1, 5), "Price": 120}
                    elif device == 2:
                        summary_plan["Devices"]["Wearable Devices"] = {"Model": "Health Wearable", "Quantity": random.randint(1, 5), "Price": 150}
    

        # Generate summary
        total_cost = sum(device["Quantity"] * device["Price"] for device in summary_plan["Devices"].values())
        summary_plan["Estimated Cost"] = total_cost
        summary_plan["Installation Complexity"] = len(summary_plan["Devices"]) * 0.5
        summary_text = f"============= Smart Security Plan Summary =============\n\nScenarios Selected:\n"
        summary_text += "\n".join([f"  - {scenario}" for scenario in summary_plan["Scenarios"]])
        summary_text += "\n\nDevices Configured:\n"
        for device, details in summary_plan["Devices"].items():
            summary_text += f"  - {device}: {details['Quantity']} units ({details['Model']})\n"
        summary_text += f"\nTotal Estimated Cost: ${summary_plan['Estimated Cost']}\n"
        summary_text += f"Overall Installation Complexity: {summary_plan['Installation Complexity']:.1f}/5\n"
        conversation.append({"role": "AI", "text": summary_text})

        # Add conversation to dialogues
        dialogues.extend(conversation)
    # Add the dialogue to the dataset
    dataset.append(dialogues)
    return dataset
    
def generator_json_security(num_samples, output_file):
    #check if the file already exists
    if os.path.exists(output_file):
        # Load existing data from the file
        with open(output_file, "r") as f:
            existing_data = json.load(f)
    else:
        # if the file doesn't exist, initialize an empty list
        existing_data = []

    dataset = generate_dataset_security(num_samples)
    # Add the generated conversation to the dataset
    existing_data.extend(dataset)
    
    #Save the updated dateset to the JSON file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    print(f"Generated {num_samples} security dialogues and saved to {output_file}.")
        

# Run the function
if __name__ == "__main__":
    generator_json_security(num_samples=1, output_file="smart_home_dialogues.json") 
    # Adjust `num_samples` for the number of dialogues generated


