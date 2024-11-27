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

    def ask_scenarios(self):
        print("Which scenarios are you interested in? (Enter numbers separated by commas)")
        print("1. Automated Climate Control\n2. Air Quality Monitoring\n3. Energy Efficiency\n"
              "4. Integration with Smart Home Devices\n5. Scheduled Ventilation\n"
              "6. Safety Features\n7. Filter Maintenance")
        scenarios = input("Enter your choices (e.g., 1,2,3): ").split(",")
        return list(map(int, scenarios))

    def configure_spaces(self, scenarios):
        print("In which spaces do you want to implement the smart venting/air system?")
        print("1. Bedroom\n2. Kitchen\n3. Living Room\n4. Bathroom\n5. Studio\n6. Hallway\n7. Toilet\n8. Storage Room")
        choices = input("Enter the space indices separated by commas (e.g., 1,3): ").split(",")
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
        for choice in choices:
            space_name = spaces[int(choice.strip())]
            count = int(input(f"How many {space_name}s do you have? "))
            for i in range(count):
                unique_space = f"{space_name}{i + 1}"
                self.space_objects.append(unique_space)
                self.smart_plan_summary[unique_space] = {"products": []}

    def add_product_to_summary(self, space, product, quantity=1):
        price = self.product_prices.get(product, 0)
        total_price = price * quantity
        self.smart_plan_summary[space]["products"].append({"product": product, "quantity": quantity, "cost": total_price})
        self.total_cost += total_price
        self.total_devices += quantity  # Increment the total number of devices

    def add_non_smart_ventilator(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space)
        
        print(f"Do you want to add a non-smart ventilator in {space} into smart venting system? (1. Yes, 2. No)")
        if input().strip() == "1":
            print(f"What kind of ventilator do you have in {space}?")
            print("1. Ceiling Ventilator\n2. Standing Ventilator\n3. Wall Ventilator")
            ventilator_type = input("Enter the ventilator type index: ").strip()
            if ventilator_type == "1":
                print(f"Is the Ceiling fan in {space} AC-powered or DC-powered? (1. AC, 2. DC)")
                power_type = input("Enter power type index: ").strip()
                if power_type == "1":
                    print("We recommend you to replace the switch to a smart variable speed controller switch")
                    self.add_product_to_summary(space, "smart_variable_speed_controller")
                else:
                    print(f"For DC-powered fan the variable speed control is not possible through smart controller, do you want to:\n1. Replace it with a matter-compatible fan\n"
                          "2. Replace the switch with a smart binary switch?")
                    choice = input("Enter your choice: ").strip()
                    if choice == "1":
                        print("Do you need a smart fan with light? (1. Yes, 2. No)")
                        if input().strip() == "1":
                            print("we recommend you the hunter smart ceiling fan with light")
                            self.add_product_to_summary(space, "hunter_smart_fan_with_light")
                        else:
                            print("we recommend you the hunter smart ceiling fan")
                            self.add_product_to_summary(space, "hunter_smart_fan")
                    else:
                        print(f"Do you need a separate light controll on the switch (1. Yes, 2. No)")
                        if input().strip() == "1":
                            print("we recommend you the Aqara Dual Relay Module T2")
                            self.add_product_to_summary(space, "Aqara Dual Relay Module T2")
                        else:
                            print("we recommend you the Aqara Single Switch Module T1")
                            self.add_product_to_summary(space, "Aqara Single Switch Module T1")    
            elif ventilator_type == "2":
                print(f"The variable speed control is not possible through add a smart power controller, do they want toDo you want to:\n1. Buy a new matter-compatible standing fan\n"
                      "2. Add a smart plug between the existing standing fan's plug and the socket?")
                choice = input("Enter your choice: ").strip()
                if choice == "1":
                    print("we recommend you the smartmi matter-compatible standing fan")
                    self.add_product_to_summary(space, "smartmi_matter_standing_fan")
                else:
                    print("we recommend you to add a smart plug between the existing standing fan's plug and the socket. A smart_plug is added to Plan Summary")
                    self.add_product_to_summary(space, "smart_plug")
            elif ventilator_type == "3":
                print("we recommend to install the smart module in the cable box to convert it to smart wall ventilator (without variable speed control)")
                self.add_product_to_summary(space, "in_wall_smart_switch_module")

    def add_existing_exhaust_fan(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space) 
        
        print("Do you want to add existing exhaust fans into the smart venting system? (1. Yes, 2. No)")
        if input().strip() == "1":
            for space in self.space_objects:
                print(f"Do you want to convert the exhaust fan in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    print(f"we recommend you to install in-wall smart switch module for exhaust fan in {space}")
                    self.add_product_to_summary(space, "in_wall_smart_switch_module")

    def add_purifier_or_humidifier(self, space):
        if space in self.processed_spaces:
            return  # Avoid repeating the same question for the same space
        self.processed_spaces.add(space) 
        print("Do you want to add an existing purifier or humidifier into the smart ecosystem? (1. Yes, 2. No)")
        if input().strip() == "1":
            print("We recommend you to use smart plug between the device's plug and the socket to realize smart control.")
            for space in self.space_objects:
                print(f"Do you want to install a smart plug for the purifier/humidifier in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    self.add_product_to_summary(space, "smart_plug")

    def add_air_quality_sensor(self):
        print("In order to improve the indoor air quality, we recommend you to set up automation of air purifier or air exhaust fan together with air quality sensor. Do you want to continue set up? (1. Yes, 2. No)")
        if input().strip() == "1":
            for space in self.space_objects:
                print(f"Do you need an air quality sensor in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    self.add_product_to_summary(space, "air_quality_sensor")

    def add_presence_sensor(self):
        print("In order to realize the automatic venting only when the user is in a certain zone, the presence sensor is needed. Do you want to add a presence sensor to improve energy efficiency? (1. Yes, 2. No)")
        if input().strip() == "1":
            for space in self.space_objects:
                print(f"Do you want a multi-zone presence sensor in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    print("we recommend you to use Aqara FP2 multi-zone sensor for detection")
                    self.add_product_to_summary(space, "Aqara_presence_sensor_FP2")
                else:
                    print("we recommend you to use Aqara FP1e AI sensor for detection")
                    self.add_product_to_summary(space, "Aqara_presence_sensor_FP1E")

    def scheduled_vent(self):
        print("We recommend you to set up the automation based on your GPS location and your regular time routine.")
    
    def add_safety_features(self):
        print("For ensure safty household environment, We recommend you to set up the auto-trigger of exhaust fan with gas leak detector. Do you want to setup safety feature for exhaust fan? (1. Yes, 2. No)")
        if input().strip() == "1":
            for space in self.space_objects:
                print(f"Do you want a gas detector in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    self.add_product_to_summary(space, "gas_leak_detector")

    def add_air_purifier(self):
        print("For more smart feature with air purifier, we recommend you to purchase originally matter-compatible air purifier, it unified the air quality sensor and filter alert. Do you need the smart air purifier? (1. Yes, 2. No)")
        if input().strip() == "1":
            for space in self.space_objects:
                print(f"Do you want a smart air purifier in {space}? (1. Yes, 2. No)")
                if input().strip() == "1":
                    self.add_product_to_summary(space, "smart_air_purifier")

    def calculate_summary(self, scenarios):
        print("\nSmart Plan Summary:")
        for space, details in self.smart_plan_summary.items():
            print(f"{space}:")
            for product in details["products"]:
                print(f"  - {product['product']} (Quantity: {product['quantity']}, Cost: €{product['cost']})")
        print(f"\nTotal Cost: €{self.total_cost:.2f}")

        # Calculate installation complexity and ecological rating
        num_scenarios = len(scenarios)
        installation_complexity = min(5, self.total_devices / 5)  # Scale of 1-5
        ecological_rating = max(1, 5 - num_scenarios / 2)  # Scale of 1-5
        print(f"Installation Complexity: {installation_complexity}/5")
        print(f"Ecological Rating: {ecological_rating}/5")
     

    def run(self):
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


# Run the script
smart_air_system = SmartAirSystem()
smart_air_system.run()

