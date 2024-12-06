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

1.2 The next step is to transform it into a structured conditional logical questionaire. 
Create Dialogue Scenarios: For each of the smart system scenario like listed above, create a decision tree containing the conditional logical questions which necessites the configuration.


####Firstly the smart system related dialogue are generated seperating according to listed 6 different smart system:
1: Smart Lighting System
2: Smart Heating System
3: Smart AV (Audio-Visual) System
4: Smart security/surveillance system
5: Smart Shade/Shutter System
6: Smart Air/Venting System

At the beginning of the dialogue, the general preferene questions and the dempgraphic question as well as their legacy system are solicited. After that the user are asked for their interested smart system. 
Based on their choice of smart systems, a set of conditional logical questions structured on the usage scenarios of that system is created. This has been done through seperate python script (please find in the main branch) but being triggered by simulated user dialogue logic which is in [main_dialogue.py](main_dialogue.py). 
For each questionair, based on the user's choice for scenarios, their household dimension and their personal tastes for home appliances and systems, it will propose a final smart implementation plan for the chosen smart system. As well as 3 metrics of the total estiamted cost, the ecological rating as well as the installation complexity. 
All those dialogues are output to a single json file called "smart_home_dialogues.json", that is reserved for later reformatting and model fine-tuning.

##2. Format Data for Training: Each json file contains moltipal of dialogues, which are generated through random simulation (using random library). Each dialogue is comprise of the above elaborated content but with nested list structure also with assiging the question the role "AI" and the answer the role "User".
In order to fit the data for fine-tunning using fundamental model "Mistral series":
###2.1. Flattened the data to remove the nested structure:
   def flatten_data(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    # Flatten the data if it's nested (as seen in your dataset)
    flattened_data = [turn for conversation in data for turn in conversation if isinstance(conversation, list)]
    return flattened_data
###2.2. Furthur transfer the class lists into the disctionary
   def extract_dialogues(data):
    processed_data = []
    def recursive_extraction(entry):
        if isinstance(entry, dict):
            processed_data.append(entry) 
        elif isinstance(entry, list):
            for sub_entry in entry:
                recursive_extraction(sub_entry)   
    recursive_extraction(data)
    return processed_data
###2.3. Reassign each line the Mistral given key name:
   def format_prompts(examples):
    return {
        "text": [
            f"{role}: {text}" for role, text in zip(examples["role"], examples["text"])
        ]
    } 
###2.4. Nest all processing procedure together to generate dataset and divide that using "dataset" library into training and evaluation dataset;
   def reformat_and_split(input_file, output_dir, test_size=.2, seed=42): 
    global dataset  # Declare that we're modifying the global variable
    flattened_data = flatten_data(input_file)   
    processed_data = extract_dialogues(flattened_data)
    
    dataset = Dataset.from_dict({
    "role": [entry["role"] for entry in processed_data],
    "text": [entry["text"] for entry in processed_data]
    })
    dataset = dataset.map(format_prompts, batched=True)

    # Split the dataset into training and evaluation sets
    split_data = dataset.train_test_split(test_size=test_size, seed=seed)
    train_data = split_data["train"]
    eval_data = split_data["test"]

    # Save the split datasets
    train_output_path = os.path.join(output_dir, "train_data.json")
    eval_output_path = os.path.join(output_dir, "eval_data.json")
    
    train_data.to_json(train_output_path)
    eval_data.to_json(eval_output_path)
  
    print(f"Example from training data: {train_data['text'][0]}")
    print(f"Example from evaluation data: {eval_data['text'][0]}")
    
    return train_data, eval_data



##3. Fine-Tune the Mistral model with synthesized Dataset
1 Prepare the Dataset for Fine-Tuning
To fine-tune the Mistral-7B-Instruct model, the synthesized dataset from the previous step must be used. This dataset, structured into train_data.json and eval_data.json, contains flattened and formatted dialogues for causal language modeling.
Here are the key steps:

from datasets import load_dataset

train_dataset = load_dataset("json", data_files="output_data/train_data.json")["train"]
eval_dataset = load_dataset("json", data_files="output_data/eval_data.json")["train"]

2 Inspect the Dataset:
Ensure the datasets are correctly loaded and formatted. Use the following snippet to check a sample:

print(train_dataset[0])  # Check a single training example
print(eval_dataset[0])   # Check a single evaluation example

###3.2 Configure Parameter-Efficient Fine-Tuning (PEFT)
To fine-tune the model with minimal computational resources, the LoRA (Low-Rank Adaptation) technique is utilized. This approach modifies only a small number of model parameters while keeping the base model weights frozen, optimizing the fine-tuning process.
Set LoRA Configuration:
LoRA is configured to update specific target modules in the model.
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj", "lm_head",
    ],
    bias="none",
    lora_dropout=0.1,
    task_type="CAUSAL_LM",  # Task type for causal language modeling
)

model = get_peft_model(model, config)
Enable Gradient Checkpointing:
Reduces memory usage during training.
model.gradient_checkpointing_enable()

###3.3 Define Training Arguments
The TrainingArguments class from transformers is used to configure the fine-tuning process. Key parameters include batch sizes, learning rate, evaluation strategy, and the number of epochs.
from transformers import TrainingArguments

args = TrainingArguments(
    output_dir="smart_home_chatbot",  # Directory to save model checkpoints
    overwrite_output_dir=True,
    logging_dir="./logs",             # Directory for logs
    logging_steps=50,                 # Log interval
    evaluation_strategy="steps",      # Evaluate at regular intervals
    eval_steps=500,                   # Interval for evaluation
    save_steps=500,                   # Interval for saving checkpoints
    save_total_limit=1,               # Retain only the latest checkpoint
    num_train_epochs=3,               # Number of epochs
    per_device_eval_batch_size=4,     # Evaluation batch size
    per_device_train_batch_size=4,    # Training batch size
    gradient_accumulation_steps=32,   # Accumulate gradients over several steps
    learning_rate=1e-4,               # Learning rate
    optim="adamw_8bit",               # Optimizer with 8-bit weights
    fp16=True,                        # Use 16-bit floating-point precision
    report_to=["tensorboard"],        # Report training metrics to TensorBoard
    dataloader_pin_memory=True,
    tf32=True                         # Enable TF32 on NVIDIA GPUs
)

###3.4 Initialize the Trainer and Start Fine-Tuning
The SFTTrainer from trl (transformers reinforcement learning) is used for fine-tuning. This library is optimized for tasks like causal language modeling.
Initialize the Trainer:
Configure the trainer with the model, training arguments, and datasets.
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    max_seq_length=256,          # Maximum sequence length
    dataset_text_field="text",   # Text field in the dataset
    eval_dataset=eval_dataset
)
Train the Model:
Start the fine-tuning process.
trainer.train()

###3.5 Monitor Training
Logs: Training metrics such as loss and evaluation accuracy are logged in TensorBoard. Run the following command to view them:
tensorboard --logdir=./logs
Checkpoints: The model checkpoints are saved in the smart_home_chatbot directory.

###3.6 Output
After training, the fine-tuned model is saved and ready for deployment. The following files will be generated:

adapter_model = trainer.model
merged_model = adapter_model.merge_and_unload()

trained_tokenizer = trainer.tokenizer

Fine-tuned model weights in smart_home_chatbot/.
Logs for monitoring training progress.
The final trained model can now be used for downstream tasks like answering queries or generating responses for smart home systems.


##4. Combine with Retrieval-Augmented Generation (RAG) for Domain Knowledge
To handle domain-specific queries about smart home and IoT:
	• Add a Retrieval Component: Use a RAG pipeline, where the model can query a knowledge base for smart home/IoT information. This can be implemented with an open-source solution like Haystack or by integrating a document search API to retrieve relevant information.
	• Hybrid Pipeline: Combine the decision-tree-guided questioning with RAG-based answering. When a client asks a general question, the model can retrieve relevant information and provide a well-informed response.
![image](https://github.com/user-attachments/assets/48c2d7d1-d16d-4e7b-b064-3d3523dac571)

