# Chatbot-Smart-Home
Create a chatbot to automatically consult the user over setting up their smart home system. Based on the dempgraphic and preference questions for user the chatbot will help to create a smart home solution inlcuding the necessary smart devices as well the estimated purchase cost and installation complexity and ecological score.

##1. Generate scenario-based dialogue for each smart system
###1.1 Firstly construct a sequential questioning logic (decision tree) based on use scenarios for each smart system.
Here below are the relevant scenarios for each system and the thereupon constructed python script, which can interactively ask user different questions on condition of the user's previous answers:

Smart lighting system:
1. Sleep/Wake-Up 
2. Security Enhancement
3. Energy Efficiency
4. Personalized Scenes
5. Voice-Controlled Operation
6. Health and Well-being
7. Outdoor Safety
8. Entertainment Sync
File: [smart_lighting.py](smart_lighting.py)

Smart heating system:
1. Scheduled Heating (attributes: Time Scheduling)
2. Geo-Fencing (attributes: Location-Based Control)
3. Zonal Heating (attributes: Room-Specific Control)
4. Energy Monitoring (attributes: Usage Tracking)
5. Voice Control (attributes: Voice Commands)
6. Adaptive Learning (attributes: Self-Learning Adjustments)
7. Weather Responsive (attributes: Weather-Adaptive Heating)
File: [smart_heating.py](smart_heating.py)

Smart security system:
1. Remote indoor Monitoring and Motion Detection
2. Two-Way Communication and Smart Locks
3. Integrated Alarms and Environmental Hazard Monitoring
4. Package and Activity Monitoring
5. Smart Lighting Integration
6. Health Emergencies
File: [smart_security.py](smart_security.py)

Smart AV(audio/video) system:
1. Home Theater Experience
2. Multi-Room Audio
3. Video Conferencing
4. Gaming
5. Learning and Education
6. Fitness and Health
7. Accessibility Features
8. Smart Alarms and Notifications
File: [smart_AV.py](smart_AV.py)

Smart shutter system:
1. Automated environment light control
2. Privacy management
3. Energy efficiency
4. Sleep quality improvement
5. Voice-controlled convenience
File: [smart_shutter.py](smart_shutter.py)

Smart venting system:
1. Automated Climate Control
2. Air Quality Monitoring
3. Energy Efficiency
4. Integration with Smart Home Devices
5. Scheduled Ventilation
6. Safety Features
7. Filter Maintenance
File: [smart_venting.py](smart_venting.py)

###1.2 The next step is to transform it into fully automatic dialogue generator. 
Create Dialogue Scenarios: Following the same decision tree for questioning of the smart system like listed above, 
we imported the random library to simulate the user's answer to automatically generate random dialogues.
The scripts can be found for a specific smart system in the file [smart_SYSTEMNAME_generator.py] in the main branch.

##2. Construct the main dialogue structure
###2.1 In a complete consultaton sessoin, the first part should be the general question that comprise of "demographic questions", "users' preference questions" and "users' property-related questions".
After that the specific "smart system dialogue generator" are called depends on the users' chocie for the following smart systems:
1: Smart Lighting System
2: Smart Heating System
3: Smart AV (Audio-Visual) System
4: Smart security/surveillance system
5: Smart Shade/Shutter System
6: Smart Air/Venting System

###2.2 After the interactive dialogue for configuring specific smart system, to the end 3 metrics of the total estiamted cost, the ecological rating as well as the installation complexity will be calculated as well as necessary smart devices suggested will be summarized in the last part "Smart Plan Summary".
And the generated dialogues will be output to the json file for following reformat.
This main dialogue structure can be found in python script [main_dialogue.py](main_dialogue.py). The rounds of the dialogues can be controlled with paramter "num_rounds" in function smart_home_system().


##3. Format Data for Training: Each json file contains moltipal of dialogues, which are generated through random simulation (using random library). Each dialogue is comprise of the above elaborated content but with nested list structure also with assiging the question the role "AI" and the answer the role "User".
In order to fit the data for fine-tunning using fundamental model "Mistral series":
###3.1. Flattened the data to remove the nested structure:
   def flatten_data(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    # Flatten the data if it's nested (as seen in your dataset)
    flattened_data = [turn for conversation in data for turn in conversation if isinstance(conversation, list)]
    return flattened_data
###3.2. Furthur transfer the class lists into the disctionary
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
###3.3. Reassign each line the Mistral given key name:
   def format_prompts(examples):
    return {
        "text": [
            f"{role}: {text}" for role, text in zip(examples["role"], examples["text"])
        ]
    } 
###3.4. Nest all processing procedure together to generate dataset and divide that using "dataset" library into training and evaluation dataset;
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



##4. Fine-Tune the Mistral model with synthesized Dataset
###4.1 Prepare the Dataset for Fine-Tuning
To fine-tune the Mistral-7B-Instruct model, the synthesized dataset from the previous step must be used. This dataset, structured into train_data.json and eval_data.json, contains flattened and formatted dialogues for causal language modeling.
Here are the key steps:

from datasets import load_dataset

train_dataset = load_dataset("json", data_files="output_data/train_data.json")["train"]
eval_dataset = load_dataset("json", data_files="output_data/eval_data.json")["train"]

###4.2 Inspect the Dataset:
Ensure the datasets are correctly loaded and formatted. Use the following snippet to check a sample:

print(train_dataset[0])  # Check a single training example
print(eval_dataset[0])   # Check a single evaluation example

###4.3 Configure Parameter-Efficient Fine-Tuning (PEFT)
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

###4.4 Define Training Arguments
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

###4.5 Initialize the Trainer and Start Fine-Tuning
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

###4.6 Monitor Training
Logs: Training metrics such as loss and evaluation accuracy are logged in TensorBoard. Run the following command to view them:
tensorboard --logdir=./logs
Checkpoints: The model checkpoints are saved in the smart_home_chatbot directory.

##5. Output
After training, the fine-tuned model is saved and ready for deployment. The following files will be generated:

adapter_model = trainer.model
merged_model = adapter_model.merge_and_unload()

trained_tokenizer = trainer.tokenizer

Fine-tuned model weights in smart_home_chatbot/.
Logs for monitoring training progress.
The final trained model can now be used for downstream tasks like answering queries or generating responses for smart home systems.


