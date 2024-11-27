## import json

def get_user_input(prompt, options=None, multi_select=False):
    """Get user input from console."""
    print(prompt)
    if options:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
    if multi_select:
        response = input("Select all that apply (e.g., 1,3,4): ").split(",")
        return [int(r.strip()) for r in response if r.strip().isdigit()]
    else:
        return int(input("Enter your choice: ").strip())

def configure_smart_curtain_and_shutter():
    """Main function to configure the smart curtain and shutter system."""
    spaces = []
    summary_plan = {"Devices": {}, "Scenarios": []}

    # Step 1: Select Smart Curtain/Shutter/Both
    print("Do you want to configure a Smart Curtain System, Smart Shutter System, or Both?")
    options = ["Smart Curtain System", "Smart Shutter System", "Both"]
    selected_option = get_user_input("Select one option:", options)
    summary_plan["Scenarios"].append(options[selected_option - 1])

    # Step 2: Configure Smart Curtain System
    if selected_option in [1, 3]:
        print("In which spaces do you want a smart curtain system?")
        spaces_options = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
        selected_spaces = get_user_input("Select all spaces:", spaces_options, multi_select=True)
        for space_index in selected_spaces:
            space_name = spaces_options[space_index - 1]
            num_units = get_user_input(f"How many {space_name}s do you want to install smart curtains in?")
            for i in range(num_units):
                spaces.append(f"{space_name} {i + 1}")

        for space in spaces:
            print(f"What type of curtain do you have in {space}?")
            curtain_types = ["Roller", "Double Roller", "Venetian", "Honeycomb", "Curtain", "Pleated", "Vertical", "Roman"]
            selected_types = get_user_input("Select all that apply:", curtain_types, multi_select=True)
            for curtain_type_index in selected_types:
                curtain_type = curtain_types[curtain_type_index - 1]
                quantity = get_user_input(f"How many {curtain_type} curtains do you have in {space}?")
                for unit in range(1, quantity + 1):
                    length = float(input(f"Enter the length of this {curtain_type} curtain (Unit {unit}) in meters: "))
                    product_name = f"MotionBlind {curtain_type} Motor"
                    price = 100 + int(length * 50)  # Example pricing logic
                    if product_name in summary_plan["Devices"]:
                        summary_plan["Devices"][product_name]["Quantity"] += 1
                    else:
                        summary_plan["Devices"][product_name] = {"Quantity": 1, "Price": price, "Complexity": 1}
    # Step 3: Configure Smart Shutter System
    if selected_option in [2, 3]:
        # Option 2 logic: Ask spaces and save them with incremental indices
        if selected_option == 2:
            print("In which spaces do you want a smart shutter system?")
            spaces_options = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
            selected_spaces = get_user_input("Select all spaces:", spaces_options, multi_select=True)
            space_count = {space: 0 for space in spaces_options}  # Track counts for each space type
            for space_index in selected_spaces:
                space_name = spaces_options[space_index - 1]
                num_units = get_user_input(f"How many {space_name}s do you want to install smart shutters in?")
                for i in range(num_units):
                    space_count[space_name] += 1
                    spaces.append(f"{space_name} {space_count[space_name]}")

        # Option 3 logic: Ask for each space installed curtain if they need smart shutter
        if selected_option == 3:
            add_more_spaces = get_user_input("For the Smart SHUTTER System, except the spaces you have mentioned, do you want to add other spaces?", ["Yes", "No"])
            if add_more_spaces == 1:
                print("What type of additional spaces do you want to add shutters to?")
                spaces_options = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office", "Hallway", "Outdoor"]
                selected_spaces = get_user_input("Select all spaces:", spaces_options, multi_select=True)
                space_count = {space: sum(1 for s in spaces if s.startswith(space)) for space in spaces_options}  # Get current count
                for space_index in selected_spaces:
                    space_name = spaces_options[space_index - 1]
                    num_units = get_user_input(f"How many {space_name}s do you want to install smart shutters in?")
                    for i in range(num_units):
                        space_count[space_name] += 1
                        spaces.append(f"{space_name} {space_count[space_name]}")

        # Common configuration logic for both options 2 and 3
        for space in spaces:
            need_shutter = get_user_input(f"Do you want a smart shutter system in {space}?", ["Yes", "No"])
            if need_shutter == 1:
                # Ask the type of shutter system
                shutter_types = ["Electric Motor", "Manual Belt Winder"]
                shutter_type = get_user_input(f"What type of shutter system do you have in {space}?", shutter_types)
            
                # If Electric Motor
                if shutter_type == 1:
                    print("We recommend you to install Aqara Smart Shutter Switch.")
                    quantity = get_user_input(f"How many Aqara Smart Shutter Switches do you need in {space}?")
                    if "Aqara Smart Shutter Switch" in summary_plan["Devices"]:
                        summary_plan["Devices"]["Aqara Smart Shutter Switch"]["Quantity"] += quantity
                    else:
                        summary_plan["Devices"]["Aqara Smart Shutter Switch"] = {"Quantity": quantity, "Price": 40, "Complexity": 2}
            
                # If Manual Belt Winder
                elif shutter_type == 2:
                    print("We recommend you to install HomePilot Smart Belt Winder System.")
                    # Add gateway if not already present
                    if "HomePilot Premium Gateway" not in summary_plan["Devices"]:
                        summary_plan["Devices"]["HomePilot Premium Gateway"] = {"Quantity": 1, "Price": 120, "Complexity": 1}
                    quantity = get_user_input(f"How many HomePilot Smart Belt Winders do you need in {space}?")
                    if "HomePilot Smart Belt Winder" in summary_plan["Devices"]:
                        summary_plan["Devices"]["HomePilot Smart Belt Winder"]["Quantity"] += quantity
                    else:
                        summary_plan["Devices"]["HomePilot Smart Belt Winder"] = {"Quantity": quantity, "Price": 80, "Complexity": 2}

  
    
    # Step 4: Scenario-Specific Questions
    print("\nDo you want to configure additional automation based on specific scenarios?")
    scenarios = [
        "Automated environment light control",
        "Privacy management",
        "Energy efficiency",
        "Sleep quality improvement",
        "Voice-controlled convenience"
    ]
    selected_scenarios = get_user_input("Select all that apply:", scenarios, multi_select=True)

    if any(scenario in [1, 2, 3] for scenario in selected_scenarios):
        print("If you want to achieve the best effect of the light control and view shuttering or warmth sheltering, it's better to add also the light/temperature sensor.")
        add_temp_sensor = get_user_input("Do you need the light/temperature sensor for any spaces?", spaces, multi_select=True)
        for space_index in add_temp_sensor:
            space_name = spaces[space_index - 1]
            sensor_name = f"Light/Temperature Sensor for {space_name}"
            if sensor_name not in summary_plan["Devices"]:
                summary_plan["Devices"][sensor_name] = {"Quantity": 1, "Price": 30, "Complexity": 1}

    # Scenario 2: Recommend automation for absence/presence
    if 2 in selected_scenarios:
        print("We recommend setting up automation based on your absence/presence and outdoor/indoor light contrast.")
        summary_plan["Scenarios"].append("Presence-based automation (Complexity added)")

    # Scenario 3: Weather and temperature sensor configuration
    if 3 in selected_scenarios:
        print("We suggest setting up automation depending on weather conditions and interior temperature sensors.")
        need_temp_sensor = get_user_input("Do you need temperature sensors for any spaces?", spaces, multi_select=True)
        for space_index in need_temp_sensor:
            space_name = spaces[space_index - 1]
            sensor_name = f"Light/Temperature Sensor for {space_name}"
            if sensor_name not in summary_plan["Devices"]:
                summary_plan["Devices"][sensor_name] = {"Quantity": 1, "Price": 30, "Complexity": 1}

    if 4 in selected_scenarios:
        print("For sleep quality improvement, we suggest automating shutters with sunrise/sunset schedules.")
        summary_plan["Scenarios"].append("Sleep automation (additional complexity added)")

    if 5 in selected_scenarios:
        print("Do you need smart speakers in any spaces?")
        speaker_spaces = get_user_input("Select all spaces:", spaces, multi_select=True)
        for space_index in speaker_spaces:
            space_name = spaces[space_index - 1]
            speaker_name = f"Smart Speaker in {space_name}"
            if speaker_name in summary_plan["Devices"]:
                summary_plan["Devices"][speaker_name]["Quantity"] += 1
            else:
                summary_plan["Devices"][speaker_name] = {"Quantity": 1, "Price": 50, "Complexity": 1}

    # Step 5: Summary
    print("\n============= Smart Curtain and Shutter Plan Summary =============")
    total_cost = 0
    total_device_complexity = 0
    scenario_weight = len(summary_plan["Scenarios"])  # Number of scenarios chosen
    device_count = len(summary_plan["Devices"])  # Total number of device types
    max_possible_complexity = 5  # Maximum possible complexity score

    print(f"Selected Scenarios: {', '.join(summary_plan['Scenarios'])}")
    print("\nDevices Configured by Space:")

    # Group devices by spaces
    space_summary = {space: [] for space in spaces}  # Initialize space summary
    for device, details in summary_plan["Devices"].items():
        # Parse the space name from the device name, assuming it's attached to a space
        for space in spaces:
            if space in device:
                space_summary[space].append(f"{details['Quantity']} x {device} (€{details['Price']} each)")

    # Print devices grouped by space
    for space, device_list in space_summary.items():
        if device_list:
            print(f"  - {space}:")
            for device in device_list:
                print(f"      • {device}")
        else:
            print(f"  - {space}: No devices configured")

    # Calculate total cost and complexity
    for device, details in summary_plan["Devices"].items():
        total_cost += details['Quantity'] * details['Price']
        total_device_complexity += details['Complexity'] * details['Quantity']

    # Normalize the complexity score
    complexity_from_scenarios = scenario_weight / 5 * 2.5  # Scenarios contribute up to 2.5 points
    complexity_from_devices = min(total_device_complexity / max(1, device_count), 2.5)  # Devices contribute up to 2.5 points
    installation_complexity = min(max_possible_complexity, complexity_from_scenarios + complexity_from_devices)

    # Calculate ecological rating based on the normalized complexity score
    ecological_rating = round(5 - installation_complexity, 1)

    # Print the total summary
    print(f"\nTotal Estimated Cost: €{total_cost}")
    print(f"Ecological Rating: {ecological_rating}/5")
    print(f"Installation Complexity: {round(installation_complexity, 1)}/5")
    print("==================================================================")


# Run the function
configure_smart_curtain_and_shutter()

