import os
import json
import random

class SmartAirSystem:
    def __init__(self):
        self.space_objects = []
        self.smart_plan_summary = {}
        self.product_prices = {
            "smart_variable_speed_controller": 60,  # Example price in euros
            "matter_compatible_fan": 150,
            "smart_binary_switch": 25,
            "hunter_smart_fan_with_light": 200,
            "hunter_smart_fan": 180,
            "aqara_dual_relay_module_t2": 40,
            "aqara_single_switch_module_t1": 30,
            "smartmi_matter_standing_fan": 120,
            "smart_plug": 20,
            "in_wall_smart_switch_module": 50,
            "air_quality_sensor": 80,
            "Aqara_presence_sensor_FP2": 100,
            "Aqara_presence_sensor_FP1E": 60,
            "gas_leak_detector": 70,
            "smart_air_purifier": 250
        }
        self.total_cost = 0
        self.processed_spaces = set()
        self.total_devices = 0
        self.conversation = []
        self.all_conversations = []

    def random_choice(self, options, allow_multiple=False):
        if allow_multiple:
            return random.sample(options, k=random.randint(1, len(options)))
        return random.choice(options)

    def add_to_conversation(self, role, text):
        self.conversation.append({"role": role, "text": text})
    
    def ask_scenarios(self):
        self.add_to_conversation("AI", "Which scenarios are you interested in? (Enter numbers separated by commas)")
        self.add_to_conversation("AI", "1. Automated Climate Control\n2. Air Quality Monitoring\n3. Energy Efficiency\n"
              "4. Integration with Smart Home Devices\n5. Scheduled Ventilation\n"
              "6. Safety Features\n7. Filter Maintenance")
        scenarios = self.random_choice([1,2,3,4,5,6,7], allow_multiple=True)
        self.add_to_conversation("User", ",".join(map(str, scenarios)))
        return scenarios

    def configure_spaces(self, scenarios):
        self.add_to_conversation("AI", "In which spaces do you want to implement the smart venting/air system?")
        self.add_to_conversation("AI", "1. Bedroom\n2. Kitchen\n3. Living Room\n4. Bathroom\n5. Studio\n6. Hallway\n7. Toilet\n8. Storage Room")
        spaces = {
            1: "Bedroom",
            2: "Kitchen",
            3: "Living Room",
            4: "Bathroom",
            5: "Studio",
            6: "Hallway",
            7: "Toilet",
            8: "Storage Room"
        }
        selected_spaces = self.random_choice(list(spaces.keys()), allow_multiple=True)
        self.add_to_conversation("User", ",".join(map(str, selected_spaces)))
        for choice in selected_spaces:
            space_name = spaces[int(choice)]
            self.add_to_conversation("AI", f"How many {space_name}s do you have? ")
            count = random.randint(1, 3)
            self.add_to_conversation("User", str(count))
            for i in range(count):
                unique_space = f"{space_name}{i + 1}"
                self.space_objects.append(unique_space)
                self.smart_plan_summary[unique_space] = {"products": []}

    def add_product_to_summary(self, space, product, quantity=1):
        # Check if the product already exists in the space
        for existing_product in self.smart_plan_summary[space]["products"]:
            if existing_product["product"] == product:
                # If it exists, update the quantity and cost
                existing_product["quantity"] += quantity
                existing_product["cost"] += self.product_prices.get(product, 0) * quantity
                self.total_cost += self.product_prices.get(product, 0) * quantity
                self.total_devices += quantity
                return  # Exit the function to avoid duplicate additions

        # If the product does not exist, add it as a new entry
        price = self.product_prices.get(product, 0)
        total_price = price * quantity
        self.smart_plan_summary[space]["products"].append({"product": product, "quantity": quantity, "cost": total_price})
        self.total_cost += total_price
        self.total_devices += quantity


    def add_non_smart_ventilator(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space)
        self.add_to_conversation("AI", f"Do you want to add a non-smart ventilator in {space} into smart venting system? (1. Yes, 2. No)")
        answer = random.randint(1, 2)
        self.add_to_conversation("User", str(answer))
        
        if answer == 1:
            self.add_to_conversation("AI", f"What kind of ventilator do you have in {space}?")
            self.add_to_conversation("AI", "1. Ceiling Ventilator\n2. Standing Ventilator\n3. Wall Ventilator")
            ventilator_type = random.randint(1, 3)
            self.add_to_conversation("User", str(ventilator_type))
            if ventilator_type == 1:
                self.add_to_conversation("AI", f"Is the Ceiling fan in {space} AC-powered or DC-powered? (1. AC, 2. DC)")
                power_type = random.randint(1, 2)
                self.add_to_conversation("User", str(power_type))
                if power_type == 1:
                    self.add_to_conversation("AI", "We recommend you to replace the switch to a smart variable speed controller switch")
                    self.add_product_to_summary(space, "smart_variable_speed_controller")
                else:
                    self.add_to_conversation("AI", f"For DC-powered fan the variable speed control is not possible through smart controller, do you want to:\n1. Replace it with a matter-compatible fan\n"
                          "2. Replace the switch with a smart binary switch?")
                    choice = random.randint(1, 2)
                    self.add_to_conversation("User", str(choice))
                    if choice == 1:
                        self.add_to_conversation("AI", "Do you need a smart fan with light? (1. Yes, 2. No)")
                        choice = random.randint(1, 2)
                        self.add_to_conversation("User", str(choice))
                        if choice == 1:
                            self.add_to_conversation("AI", "we recommend you the hunter smart ceiling fan with light")
                            self.add_product_to_summary(space, "hunter_smart_fan_with_light")
                        else:
                            self.add_to_conversation("AI", "we recommend you the hunter smart ceiling fan")
                            self.add_product_to_summary(space, "hunter_smart_fan")
                    else:
                        self.add_to_conversation("AI", f"Do you need a separate light controll on the switch (1. Yes, 2. No)")
                        answer = random.randint(1, 2)
                        self.add_to_conversation("User", str(answer))
                        if answer == 1:
                            self.add_to_conversation("AI", "we recommend you the Aqara Dual Relay Module T2")
                            self.add_product_to_summary(space, "Aqara Dual Relay Module T2")
                        else:
                            self.add_to_conversation("AI", "we recommend you the Aqara Single Switch Module T1")
                            self.add_product_to_summary(space, "Aqara Single Switch Module T1")    
            elif ventilator_type == 2:
                self.add_to_conversation("AI", f"The variable speed control is not possible through add a smart power controller, Do you want to:\n1. Buy a new matter-compatible standing fan\n"
                      "2. Add a smart plug between the existing standing fan's plug and the socket?")
                choice = random.randint(1, 2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_to_conversation("AI", "we recommend you the smartmi matter-compatible standing fan")
                    self.add_product_to_summary(space, "smartmi_matter_standing_fan")
                else:
                    self.add_to_conversation("AI", "we recommend you to add a smart plug between the existing standing fan's plug and the socket. A smart_plug is added to Plan Summary")
                    self.add_product_to_summary(space, "smart_plug")
            elif ventilator_type == 3:
                self.add_to_conversation("AI", "we recommend to install the smart module in the cable box to convert it to smart wall ventilator (without variable speed control)")
                self.add_product_to_summary(space, "in_wall_smart_switch_module")

    def add_existing_exhaust_fan(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space) 
        
        self.add_to_conversation("AI", "Do you want to add existing exhaust fans into the smart venting system? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you want to convert the exhaust fan in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_to_conversation("AI", f"we recommend you to install in-wall smart switch module for exhaust fan in {space}")
                    self.add_product_to_summary(space, "in_wall_smart_switch_module")

    def add_purifier_or_humidifier(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space) 
        self.add_to_conversation("AI", "Do you want to add an existing purifier or humidifier into the smart ecosystem? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            self.add_to_conversation("AI", "We recommend you to use smart plug between the device's plug and the socket to realize smart control.")
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you want to install a smart plug for the purifier/humidifier in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_product_to_summary(space, "smart_plug")

    def add_air_quality_sensor(self):
        self.add_to_conversation("AI", "In order to improve the indoor air quality, we recommend you to set up automation of air purifier or air exhaust fan together with air quality sensor. Do you want to continue set up? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you need an air quality sensor in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))                
                if choice == 1:
                    self.add_to_conversation("AI", f"The air quality sensor is added to {space}.")
                    self.add_product_to_summary(space, "air_quality_sensor")

    def add_presence_sensor(self):
        self.add_to_conversation("AI", "In order to realize the automatic venting only when the user is in a certain zone, the presence sensor is needed. Do you want to add a presence sensor to improve energy efficiency? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you want a multi-zone presence sensor in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_to_conversation("AI", "we recommend you to use Aqara FP2 multi-zone sensor for detection")
                    self.add_product_to_summary(space, "Aqara_presence_sensor_FP2")
                else:
                    self.add_to_conversation("AI", "we recommend you to use Aqara FP1e AI sensor for detection")
                    self.add_product_to_summary(space, "Aqara_presence_sensor_FP1E")

    def scheduled_vent(self):
        self.add_to_conversation("AI", "We recommend you to set up the automation based on your GPS location and your regular time routine.")
    
    def add_safety_features(self):
        self.add_to_conversation("AI", "For ensure safty household environment, We recommend you to set up the auto-trigger of exhaust fan with gas leak detector. Do you want to setup safety feature for exhaust fan? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you want a gas detector in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_product_to_summary(space, "gas_leak_detector")

    def add_air_purifier(self):
        self.add_to_conversation("AI", "For more smart feature with air purifier, we recommend you to purchase originally matter-compatible air purifier, it unified the air quality sensor and filter alert. Do you need the smart air purifier? (1. Yes, 2. No)")
        choice = random.randint(1,2)
        self.add_to_conversation("User", str(choice))
        if choice == 1:
            for space in self.space_objects:
                self.add_to_conversation("AI", f"Do you want a smart air purifier in {space}? (1. Yes, 2. No)")
                choice = random.randint(1,2)
                self.add_to_conversation("User", str(choice))
                if choice == 1:
                    self.add_product_to_summary(space, "smart_air_purifier")

    def calculate_summary(self, scenarios):
        # Map scenario indices to names
        scenario_names = {
            1: "Automated Climate Control",
            2: "Air Quality Monitoring",
            3: "Energy Efficiency",
            4: "Integration with Smart Home Devices",
            5: "Scheduled Ventilation",
            6: "Safety Features",
            7: "Filter Maintenance"
        }

        # Get the names of the chosen scenarios
        chosen_scenarios = [scenario_names[scenario] for scenario in scenarios]

        # Initialize the summary text
        summary_text = "============= Smart Venting Plan Summary =============\n\n"

        # Add chosen scenarios
        summary_text += f"Scenarios Chosen: {', '.join(chosen_scenarios)}\n\n"

        # Add the device summary for each space
        summary_text += "Devices Summary by Space:\n"
        for space, details in self.smart_plan_summary.items():
            summary_text += f"{space}:\n"
            for product in details["products"]:
                summary_text += f"  - {product['product']} (Quantity: {product['quantity']}, Cost: €{product['cost']})\n"

        # Calculate total cost
        summary_text += f"\nTotal Estimated Cost: €{self.total_cost:.2f}\n"

        # Calculate installation complexity and ecological rating
        num_scenarios = len(scenarios)
        installation_complexity = min(5, (self.total_devices + num_scenarios) / 5)  # Scaled 1-5
        ecological_rating = max(1, 5 - (num_scenarios / 2))  # Scaled 1-5
        summary_text += f"Installation Complexity: {installation_complexity:.1f}/5\n"
        summary_text += f"Ecological Rating: {ecological_rating:.1f}/5\n"

        # Add the formatted summary as a single entry to the conversation
        self.add_to_conversation("AI", summary_text)

    def generate_dataset_venting(self, num_samples, output_file="smart_home_dialogues.json"):
        # Check if the file already exists
        if os.path.exists(output_file):
            # Load existing data from the file
            with open(output_file, "r") as f:
                existing_data = json.load(f)
        else:
            # If the file doesn't exist, initialize an empty list
            existing_data = []

        # Generate new dialogues and append them to the existing data
        for i in range(num_samples):
            self.space_objects = []  # Reset spaces for each simulation
            self.smart_plan_summary = {}  # Reset summary for each simulation
            self.processed_spaces = set()  # Reset processed spaces
            self.total_cost = 0  # Reset total cost
            self.total_devices = 0  # Reset total devices
            self.conversation = []  # Reset conversation for each simulation
            
            # Run the simulation
            scenarios = self.ask_scenarios()
            self.configure_spaces(scenarios)
            for scenario in scenarios:
                if scenario in [1, 5]:
                    for space in self.space_objects:
                        self.add_non_smart_ventilator(space)
                if scenario in [1, 2, 6]:
                    for space in self.space_objects:
                        self.add_existing_exhaust_fan(space)
                if scenario in [1, 2, 5, 7]:
                    for space in self.space_objects:
                        self.add_purifier_or_humidifier(space)  
                if scenario == 2:
                    self.add_air_quality_sensor()
                if scenario == 3:
                    self.add_presence_sensor()
                if scenario == 5:
                    self.scheduled_vent()
                if scenario == 6:
                    self.add_safety_features()
                if scenario == 7:
                    self.add_air_purifier()
            
            self.calculate_summary(scenarios)
            self.all_conversations.extend(self.conversation)
            
            # Add the generated conversation to the dataset
            existing_data.append(self.conversation)

        # Save the updated dataset to the JSON file
        with open(output_file, "w") as f:
            json.dump(existing_data, f, indent=4)
        
        print(f"Generated {num_samples} venting dialogues and saved to '{output_file}'.")



smart_air_system = SmartAirSystem()
smart_air_system.generate_dataset_venting(num_samples=10)
