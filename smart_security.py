import json

def ask_question(question, options, multi_select=False):
    print(f"\n{question}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    if multi_select:
        response = input("Select all that apply (e.g., 1,3,4): ")
        return [int(x) for x in response.split(",") if x.isdigit()]
    else:
        response = input("Select one option (e.g., 1): ")
        return int(response)

def ask_number(question):
    while True:
        try:
            response = int(input(f"\n{question}\nEnter a number: "))
            if response > 0:
                return response
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Sorry, I don't understand your answer. Please enter a valid number.")


def calculate_installation_complexity_and_cost(devices):
    installation_complexity = 0
    estimated_cost = 0

    for device, details in devices.items():
        if "Quantity" in details and details["Quantity"] != "Custom":
            quantity = int(details["Quantity"])  # Ensure quantity is an integer
            installation_complexity += quantity
            estimated_cost += quantity * (details.get("Price", 0))

    return installation_complexity, estimated_cost

def ask_property_and_country(summary_plan, applicable_scenarios):
    property_types = ["Apartment", "Single-Family Home", "Multi-Story House", "Shared Property"]
    countries = ["Germany", "France", "Luxembourg", "Belgium"]
    if any(scenario in summary_plan["Scenarios"] for scenario in applicable_scenarios):
        selected_property = ask_question("What type of property is your household?", property_types)
        selected_country = ask_question("Which country is your household located in?", countries)
        if selected_property in [1, 4]:  # Shared Property or Apartment
            print(f"Reminder: Please ensure your setup complies with GDPR laws in {countries[selected_country - 1]}.")


def scenario_1(summary_plan):
    print("\nYou selected Scenario 1: Remote Indoor Monitoring and Motion Detection.")

    # Step 1: Main priorities for the camera (multi-choice)
    indoor_camera_priorities = [
        "High video resolution and clarity (e.g., 2K or better)",
        "Budget-friendly with essential features",
        "Compatibility with a specific ecosystem (e.g., Google Home, Alexa, or HomeKit)",
        "Advanced AI features like facial recognition or pet detection",
        "Comprehensive local storage options and privacy"
    ]
    selected_priorities = ask_question("What are your main priorities for the camera? (Select all that apply)", indoor_camera_priorities, multi_select=True)

    # Step 2 to Step 7 questions
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
        responses.append(ask_question(question, options))

    # Camera recommendation based on all answers
    camera_table = [
        {
            "Name": "Google Nest Cam",
            "Price": 120,
            "Features": ["High video resolution and clarity", "AI-based detection", "Google Home", "Cloud storage"]
        },
        {
            "Name": "Blink Indoor",
            "Price": 90,
            "Features": ["Budget-friendly", "Basic motion detection", "Amazon Alexa", "Local or cloud storage"]
        },
        {
            "Name": "Eufy Cam 2K",
            "Price": 45,
            "Features": ["High video resolution", "AI-based detection", "Local storage", "Wide-angle view"]
        },
        {
            "Name": "Wyze Cam v3",
            "Price": 35,
            "Features": ["Budget-friendly", "Basic motion detection", "Local storage", "Two-way audio"]
        },
        {
            "Name": "Aqara Camera E1",
            "Price": 60,
            "Features": ["High video resolution", "Advanced AI", "Apple HomeKit", "Pan and tilt"]
        },
        {
            "Name": "Aqara G2H Pro",
            "Price": 70,
            "Features": ["Advanced AI", "Privacy protection", "Apple HomeKit", "Comprehensive local storage"]
        },
        {
            "Name": "Aqara G3",
            "Price": 100,
            "Features": ["Advanced AI", "High video resolution", "Apple HomeKit", "Full 360° pan and tilt", "Privacy protection"]
        }
    ]

    # Matching logic: prioritize cameras that match the most user-selected features
    best_match = None
    max_match_count = 0

    for camera in camera_table:
        match_count = 0
        # Match priorities
        for priority in selected_priorities:
            if indoor_camera_priorities[priority - 1] in camera["Features"]:
                match_count += 1
        # Match responses
        for i, response in enumerate(responses):
            option_text = questions_and_options[i][1][response - 1]
            if option_text in camera["Features"]:
                match_count += 1
        # Check if this camera is the best match so far
        if match_count > max_match_count:
            best_match = camera
            max_match_count = match_count

    if not best_match:
        best_match = camera_table[0]  # Default to the first option if no match is found

    # Recommendation
    print(f"\nWe recommend: {best_match['Name']} ({', '.join(best_match['Features'])})")
    quantity = ask_question(f"How many {best_match['Name']} cameras do you need?", [])
    summary_plan["Devices"]["Indoor Camera"] = {"Model": best_match["Name"], "Quantity": quantity, "Price": best_match["Price"]}



def scenario_2(summary_plan):
    print("\nYou selected Scenario 2: Two-Way Communication and Smart Locks.")

    # Ask about the type of doors for smart locks
    door_lock_options = [
        "All doors have a handle",
        "All doors do not have a handle",
        "Some doors have a handle, and some do not"
    ]
    door_lock_choice = ask_question("What type of doors do you want to equip with smart locks?", door_lock_options)

    if door_lock_choice == 1:  # All doors have handles
        print("Recommended: Aqara U200 Smart Locks.")
        quantity = ask_number("How many Aqara U200 locks do you need?")
        summary_plan["Devices"]["Smart Locks"] = {"Model": "Aqara U200", "Quantity": quantity, "Price": 150}

    elif door_lock_choice == 2:  # All doors do not have handles
        print("Recommended: Aqara U300 Smart Locks.")
        quantity = ask_number("How many Aqara U300 locks do you need?")
        summary_plan["Devices"]["Smart Locks"] = {"Model": "Aqara U300", "Quantity": quantity, "Price": 180}

    else:  # Some doors have handles and some do not
        print("Recommended: Aqara U200 and U300 Smart Locks.")
        u200_quantity = ask_number("How many Aqara U200 locks (for door with handel) do you need?")
        u300_quantity = ask_number("How many Aqara U300 locks (for door without handel) do you need?")
        summary_plan["Devices"]["Smart Locks with Handle"] = {"Model": "Aqara U200", "Quantity": u200_quantity, "Price": 150}
        summary_plan["Devices"]["Smart Locks without Handle"] = {"Model": "Aqara U300", "Quantity": u300_quantity, "Price": 180}

    # Ask about the doorbell with two-way communication and AI face recognition
    doorbell = ask_question(
        "Do you want a doorbell with two-way communication, AI face recognition, and end-to-end encryption?",
        ["Yes", "No"]
    )
    if doorbell == 1:
        print("Recommended: Aqara G4 Doorbell.")
        summary_plan["Devices"]["Doorbell"] = {"Model": "Aqara G4", "Quantity": 1, "Price": 120}


def scenario_3(summary_plan):
    print("\nYou selected Scenario 3: Integrated Alarms and Environmental Hazard Monitoring.")

    # Environmental hazards with short explanations
    hazards = [
        "Smoke and Fire: Detects smoke or flames to prevent fire-related incidents.",
        "Carbon Monoxide: Monitors CO levels to detect potentially deadly gas leaks.",
        "Gas Leaks: Alerts for dangerous gas leaks (e.g., natural gas or propane).",
        "Flood: Detects water leakage or flooding in critical areas.",
        "Digital Security Threats: Identifies and eliminates weak points in your digital system."
    ]

    # Ask which hazards the user wants to monitor
    selected_hazards = ask_question("What kind of environmental hazards do you want to monitor? (Select all that apply)", hazards, multi_select=True)

    # Process the user's choices
    for hazard_index in selected_hazards:
        hazard_name = hazards[hazard_index - 1].split(":")[0]  # Get the hazard name (e.g., "Smoke and Fire")

        if hazard_name == "Digital Security Threats":
            # Ask about penetration testing
            learn_pen_test = ask_question(
                "Would you like to learn more about how a penetration test can benefit your digital system?",
                ["Yes", "No"]
            )
            if learn_pen_test == 1:
                print(
                    "\nPenetration Testing Overview:\n"
                    "This test identifies vulnerabilities in your home network, ensuring your devices and data are secure from unauthorized access."
                )
            # Add penetration test if chosen
            add_pen_test = ask_question("Do you want a penetration test for your digital system?", ["Yes", "No"])
            if add_pen_test == 1:
                print("Added penetration test to the plan.")
                summary_plan["Devices"]["Penetration Test"] = {"Model": "Digital Penetration Test", "Quantity": 1, "Price": 200}
        else:
            # Ask how many units they need for other hazards
            quantity = ask_number(f"How many sensors do you need for {hazard_name}?")
            summary_plan["Devices"][hazard_name] = {"Model": f"{hazard_name} Sensor", "Quantity": quantity, "Price": 50}

def scenario_4(summary_plan):
    print("\nYou selected Scenario 4: Package and Activity Monitoring.")

    # Vulnerable areas with user selection
    vulnerable_areas = [
        "Entrances",
        "Driveways",
        "Pathways",
        "Windows",
        "Backyard",
        "Gates or Fences",
        "Package Delivery Zones"
    ]
    selected_areas = ask_question(
        "Which areas do you identify as vulnerable? (Select all that apply)",
        vulnerable_areas,
        multi_select=True
    )

    # Track areas where sensors are preferred
    sensor_areas = []  # Areas where user prefers sensors
    camera_areas = []  # Areas where user prefers cameras

    for area_index in selected_areas:
        area_name = vulnerable_areas[area_index - 1]
        if area_name in ["Windows", "Gates or Fences"]:
            # Ask if they prefer a sensor or a security camera for Windows/Gates
            preferred_solution = ask_question(
                f"Do you prefer a security camera system or a {area_name.lower()} sensor for {area_name}?",
                ["Security Camera System", f"{area_name} Sensor"]
            )
            if preferred_solution == 2:  # Sensor
                quantity = ask_number(f"How many {area_name} sensors do you need?")
                summary_plan["Devices"][f"{area_name} Sensor"] = {"Model": f"{area_name} Sensor", "Quantity": quantity, "Price": 50}
                sensor_areas.append(area_name)
            else:
                print(f"Continuing with security camera selection for {area_name}.")
                camera_areas.append(area_name)
        else:
            camera_areas.append(area_name)

    # If the user prefers cameras for some areas, continue with camera selection
    if camera_areas:
        # Outdoor camera questions
        outdoor_camera_questions = [
            "What is your main use case for the outdoor camera?",
            "What level of video resolution do you prefer?",
            "What kind of field of view do you need?",
            "What AI detection features do you need?",
            "What kind of storage option do you prefer?",
            "Which smart home ecosystem do you use or plan to use?",
            "Do you need additional features? (Choose all that apply)",
            "Do you need a privacy-focused camera?"
        ]
        outdoor_camera_options = [
            ["Package and delivery monitoring", "Vehicle monitoring", "General security", "All of the above"],
            ["1080p (HD)", "2K or higher"],
            ["Wide-angle (130°–170°)", "Standard (100°)"],
            ["Person detection", "Package detection", "Vehicle detection", "All of the above", "No AI detection"],
            ["Local storage", "Cloud storage", "Both local and cloud storage"],
            ["Apple HomeKit", "Google Home", "Amazon Alexa", "Multi-platform compatibility"],
            ["Built-in Zigbee hub", "Floodlight integration", "Solar-powered", "Night vision", "Two-way audio"],
            ["Yes", "No"]
        ]

        # Collect responses for camera preferences
        outdoor_responses = []
        for i, question in enumerate(outdoor_camera_questions):
            multi = True if i == 6 else False  # Multi-select for additional features
            outdoor_responses.append(ask_question(question, outdoor_camera_options[i], multi_select=multi))

        # Feature table for outdoor cameras
        outdoor_camera_table = [
            {"Name": "Eufy Cam 2K", "Resolution": "2K", "Field of View": "Wide-angle", "AI": "All of the above",
             "Storage": "Local and Cloud", "Ecosystem": "Multi-platform", "Features": ["Night vision", "Two-way audio"], "Price": 200},
            {"Name": "Ring Spotlight Cam", "Resolution": "1080p", "Field of View": "Wide-angle", "AI": "Person detection",
             "Storage": "Cloud", "Ecosystem": "Amazon Alexa", "Features": ["Floodlight integration", "Two-way audio"], "Price": 180},
            {"Name": "Google Nest Cam Outdoor", "Resolution": "1080p", "Field of View": "Standard", "AI": "Vehicle detection",
             "Storage": "Cloud", "Ecosystem": "Google Home", "Features": ["Night vision"], "Price": 150},
            {"Name": "Arlo Ultra 2", "Resolution": "2K", "Field of View": "Wide-angle", "AI": "All of the above",
             "Storage": "Local and Cloud", "Ecosystem": "Multi-platform", "Features": ["Night vision", "Solar-powered"], "Price": 250}
        ]

        # Calculate overlap with user preferences
        best_camera = None
        max_overlap = 0
        for camera in outdoor_camera_table:
            overlap = 0
            # Compare user responses with camera features
            if outdoor_responses[1] == 2 and camera["Resolution"] == "2K":  # Resolution preference
                overlap += 1
            if outdoor_responses[2] == 1 and camera["Field of View"] == "Wide-angle":  # Field of view preference
                overlap += 1
            if outdoor_responses[3] in [1, 4] and camera["AI"] == "All of the above":  # AI detection
                overlap += 1
            if outdoor_responses[4] == 3 and camera["Storage"] == "Local and Cloud":  # Storage option
                overlap += 1
            if outdoor_responses[5] == 4 and camera["Ecosystem"] == "Multi-platform":  # Ecosystem compatibility
                overlap += 1
            if set(outdoor_responses[6]).intersection(camera["Features"]):  # Additional features
                overlap += len(set(outdoor_responses[6]).intersection(camera["Features"]))

            # Update the best camera if the overlap is higher
            if overlap > max_overlap:
                best_camera = camera
                max_overlap = overlap

        # Recommend the best camera
        if best_camera:
            print(f"\nWe recommend: {best_camera['Name']} (Features: {best_camera})")
            summary_plan["Devices"]["Outdoor Camera"] = {"Model": best_camera["Name"], "Quantity": 0, "Price": best_camera["Price"]}

        # Ask how many cameras are needed for each area (excluding sensor areas)
        for area in camera_areas:
            quantity = ask_number(f"How many cameras do you need for {area}?")
            summary_plan["Devices"][f"{area} Camera"] = {"Model": best_camera['Name'], "Quantity": quantity, "Price": best_camera["Price"]}


def scenario_5(summary_plan):
    print("\nYou selected Scenario 5: Smart Lighting Integration.")
    print("You need to configure smart lighting systems to create the illusion of presence and deter potential intruders.")
    summary_plan["Devices"]["Smart Lighting System"] = {"Model": "Smart Lighting System", "Quantity": "Custom", "Price": 200}

def scenario_6(summary_plan):
    print("\nYou selected Scenario 6: Health Emergencies.")

    # Ask if the user wants primary abnormality detection or dedicated health monitoring
    detection_type = ask_question(
        "Do you want primary abnormality detection (e.g., fall detection, movement monitoring) or a dedicated health monitoring system?",
        ["Primary Abnormality Detection", "Dedicated Health Monitoring System"]
    )

    if detection_type == 2:  # Dedicated Health Monitoring System
        print("We recommend configuring the Philips Lifeline system for comprehensive health monitoring.")
        summary_plan["Devices"]["Philips Lifeline System"] = {"Model": "Philips Lifeline", "Quantity": 1, "Price": 500}

    # Continue asking questions for other devices
    health_devices = ask_question(
        "Do you also want a fall detection sensor or a wearable device for monitoring health emergencies? (Select all that apply)",
        ["Fall Detection Sensor", "Wearable Device"],
        multi_select=True
    )

    # Process Wearable Devices
    if 2 in health_devices:
        wearable_quantity = ask_number("How many users need wearable devices?")
        wearable_cost = 150  # Approximate cost per wearable
        summary_plan["Devices"]["Wearable Device"] = {"Model": "Health Wearable", "Quantity": wearable_quantity, "Price": wearable_cost}

    # Process Fall Detection Sensor
    if 1 in health_devices:
        print("We recommend using Aqara's Life Sign System (Aqara FP2 Sensor and Aqara Camera E1).")

        # Ask about spaces where the Aqara Life Sign System will be installed
        spaces = ask_question("In which spaces do you want to install the Aqara Life Sign System? (Select all that apply)",
                              ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Hallway"],
                              multi_select=True)

        total_rooms = 0
        for space in spaces:
            space_name = ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Hallway"][space - 1]
            room_count = ask_number(f"How many {space_name}s do you want to monitor?")
            total_rooms += room_count

        # Each room requires one Aqara Camera E1 and one FP2 sensor
        summary_plan["Devices"]["Aqara Life Sign System"] = {
            "Model": "Aqara FP2 + Aqara Camera E1",
            "Quantity": total_rooms,
            "Price": 120  # Combined price of both devices per room
        }


def calculate_installation_complexity_and_cost(devices, num_scenarios):
    """
    Calculates installation complexity and total cost.
    Ensures normalized installation complexity stays within the range of 0 to 5.
    """
    raw_complexity = 0
    estimated_cost = 0

    # Calculate raw complexity and total cost
    for device, details in devices.items():
        if "Quantity" in details and details["Quantity"] != "Custom":
            quantity = int(details.get("Quantity", 0))  # Ensure quantity is an integer
            price_per_unit = details.get("Price", 0)   # Get price per unit
            raw_complexity += quantity
            estimated_cost += quantity * price_per_unit

    # Define max possible complexity based on scenarios and devices
    max_possible_complexity = num_scenarios * 2 + len(devices) * 3  # Adjust weights as needed for fairness

    # Normalize complexity to a scale of 0 to 5
    if max_possible_complexity > 0:
        normalized_complexity = (raw_complexity / max_possible_complexity) * 5
    else:
        normalized_complexity = 0

    # Ensure the normalized value is within 0 to 5
    normalized_complexity = min(5, max(0, normalized_complexity))

    return round(normalized_complexity, 1), estimated_cost



def print_final_summary(summary_plan):
    print("\n============= Smart Security/Surveillance Plan Summary =============")

    # Scenarios Selected
    if "Scenarios" in summary_plan and summary_plan["Scenarios"]:
        print("\nScenarios Selected:")
        for scenario in summary_plan["Scenarios"]:
            print(f"  - {scenario}")

    # Devices Configured
    if "Devices" in summary_plan and summary_plan["Devices"]:
        print("\nDevices Configured:")
        total_cost = 0
        total_units = 0
        for device, details in summary_plan["Devices"].items():
            # Ensure Quantity and Price are valid
            try:
                quantity = int(details.get("Quantity", 0))  # Convert quantity to integer
                price_per_unit = details.get("Price", 0)  # Ensure price is numeric
                if isinstance(price_per_unit, (int, float)) and quantity > 0:
                    total_cost += quantity * price_per_unit
                    total_units += quantity
                    print(f"  - {device}: {quantity} units")
            except (ValueError, TypeError):
                print(f"  - {device}: Quantity or Price missing/invalid")

        # Total Estimated Cost
        print(f"\nTotal Estimated Cost: ${total_cost}")

        # Overall Installation Complexity
        # Installation complexity is based on the number of devices and scenarios selected
        complexity_score = len(summary_plan["Devices"]) + len(summary_plan["Scenarios"])
        print(f"Overall Installation Complexity: {complexity_score}/5")
    else:
        print("\nNo devices configured.")

    print("===============================================================")



def configure_smart_system():
    summary_plan = {"Scenarios": [], "Devices": {}, "Installation Complexity": 0, "Estimated Cost": 0}
    
    # Step 1: Ask about scenarios
    scenarios = [
        "Remote indoor Monitoring and Motion Detection",
        "Two-Way Communication and Smart Locks",
        "Integrated Alarms and Environmental Hazard Monitoring",
        "Package and Activity Monitoring",
        "Smart Lighting Integration",
        "Health Emergencies"
    ]
    selected_scenarios = ask_question("Which scenarios would you like to set up? (Choose all that apply)", scenarios, multi_select=True)
    for scenario in selected_scenarios:
        summary_plan["Scenarios"].append(scenarios[scenario - 1])

    if 1 in selected_scenarios:
        scenario_1(summary_plan)
    if 2 in selected_scenarios:
        scenario_2(summary_plan)
    if 3 in selected_scenarios:
        scenario_3(summary_plan)
    if 4 in selected_scenarios:
        scenario_4(summary_plan)
    if 5 in selected_scenarios:
        scenario_5(summary_plan)
    if 6 in selected_scenarios:
        scenario_6(summary_plan)

    # Call the summary function
    print_final_summary(summary_plan)

# Run the configuration
configure_smart_system()

