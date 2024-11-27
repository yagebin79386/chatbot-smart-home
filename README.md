# Chatbot-Smart-Home
Create a chatbot to automatically collect the basic info and specific requirement from clients for creating a smart home solution, the chatbot can also help with general Q&A around this topic

##1. Convert the Decision Tree into Training Data
1.1 Firsty construct a clear decision tree based on scenarios for each smart system. 
Here below are the scenarios for different smart systems:

Smart lighting system:
1 Sleep/Wake-Up 
2 Security Enhancement
3 Energy Efficiency
4 Personalized Scenes
5 Voice-Controlled Operation
6 Health and Well-being
7 Outdoor Safety
8 Entertainment Sync

Smart heating system:
1. Scheduled Heating (attributes: Time Scheduling)
2. Geo-Fencing (attributes: Location-Based Control)
3. Zonal Heating (attributes: Room-Specific Control)
4. Energy Monitoring (attributes: Usage Tracking)
5. Voice Control (attributes: Voice Commands)
6. Adaptive Learning (attributes: Self-Learning Adjustments)
7. Weather Responsive (attributes: Weather-Adaptive Heating)

Smart security system:
1. Remote indoor Monitoring and Motion Detection
2. Two-Way Communication and Smart Locks
3. Integrated Alarms and Environmental Hazard Monitoring
4. Package and Activity Monitoring
5. Smart Lighting Integration
6. Health Emergencies

Smart AV(audio/video) system:
1. Home Theater Experience
2. Multi-Room Audio
3. Video Conferencing
4. Gaming
5. Learning and Education
6. Fitness and Health
7. Accessibility Features
8. Smart Alarms and Notifications

Smart shutter system:
1. Automated environment light control
2. Privacy management
3. Energy efficiency
4. Sleep quality improvement
5. Voice-controlled convenience

Smart venting system:
1. Automated Climate Control
2. Air Quality Monitoring
3. Energy Efficiency
4. Integration with Smart Home Devices
5. Scheduled Ventilation
6. Safety Features
7. Filter Maintenance

1.2 The next step is to transform it into a structured conditional logical questionaire. Here’s how:
Create Dialogue Scenarios: Convert each path in your decision tree into a series of question-answer pairs or dialogue sequences that represent an ideal conversation flow.
use the [generate_dialogue_template.py](https://github.com/yagebin79386/chatbot-smart-home/blob/357afb54df7613f55e4d610b32bd3be5b10078f7/generate_dialogue_template.py) to generate the dialogue template for general individual information in json formate. 


	• Include Relevant Q&A Data for Smart Home and IoT: Gather or create Q&A pairs about smart home and IoT topics to supplement the training data. This will help the model answer relevant questions it encounters during the conversation.
	• Format Data for Training: Each dialogue can be represented as input-output pairs in a JSON or CSV format, such as:
		○ Input: "User: I’m interested in setting up a smart thermostat. AI: Great! Do you already have any existing smart devices?"
		○ Output: "User: Yes, I have a smart speaker."
####Firstly the smart system related dialogue are generated seperating according to listed 6 different smart system:
1: Smart Lighting System
2: Smart Heating System
3: Smart AV (Audio-Visual) System
4: Smart security/surveillance system
5: Smart Shade/Shutter System
6: Smart Air/Venting System

For each of the above system there is a conditional logical questionair based on the user's preference for use scenarios in that system. This has been done through seperate python script (please find in the main branch) but being triggered by simulated user dialogue logic which is in [main_dialogue.py](main_dialogue.py). For each questionair, based on the user's choice for scenario, the products and their choice for brands for legecy home appliances and systems, it will propose a final smart implementation plan for the chosen smart system. As well as 3 metrics of the total estiamted cost, the ecological rating as well as the installation complexity. 
All those dialogues are output to a single json file called "smart_home_dialogues.json", that is reserved for later model fine-tuning.


##2. Fine-Tune GPT-2 with the Custom Dataset
Once the dataset is ready, you can proceed with fine-tuning the model:
	• Prepare the Training Environment: Use libraries like Hugging Face’s Transformers, which make it easy to fine-tune models with custom datasets. Install the necessary libraries and set up your environment.
	• Tokenize the Data: Preprocess the dataset by tokenizing the text to prepare it for training. The Transformers library has tokenizers that work well with GPT-2.
	• Fine-Tune the Model: Use the Trainer API in Hugging Face to fine-tune GPT-2 on your dataset. Set appropriate training parameters like batch size, learning rate, and number of epochs to optimize performance. Monitor training to avoid overfitting.


##3. Implement the Decision Tree Logic in Post-Processing
LLMs may not always follow strict decision paths, so you can enhance control by implementing the decision tree as a post-processing layer:
	• Custom Logic Layer: Wrap the model’s outputs in custom logic that enforces the decision tree. For instance, after each response, check the user’s answer and decide the next question based on your decision tree.
	• Dynamic Question Flow: Based on the response, dynamically adjust the next question rather than relying entirely on the model. This ensures that the decision tree structure is strictly followed.


##4. Combine with Retrieval-Augmented Generation (RAG) for Domain Knowledge
To handle domain-specific queries about smart home and IoT:
	• Add a Retrieval Component: Use a RAG pipeline, where the model can query a knowledge base for smart home/IoT information. This can be implemented with an open-source solution like Haystack or by integrating a document search API to retrieve relevant information.
	• Hybrid Pipeline: Combine the decision-tree-guided questioning with RAG-based answering. When a client asks a general question, the model can retrieve relevant information and provide a well-informed response.
![image](https://github.com/user-attachments/assets/48c2d7d1-d16d-4e7b-b064-3d3523dac571)

