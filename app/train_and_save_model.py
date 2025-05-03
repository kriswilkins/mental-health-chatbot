from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer # type: ignore
from datasets import load_dataset # type: ignore

chatbot = ChatBot(
    'TherapistBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)
trainer = ListTrainer(chatbot)

ds = load_dataset("RishiKompelli/TherapyDataset")

batch_size = 100000  # Adjust the batch size as needed
training_data = []
for i, example in enumerate(ds['train']):
    input_text = example['input']
    output_text = example['output']
    if input_text and output_text:
        training_data.append(input_text)
        training_data.append(output_text)
    
    if (i + 1) % batch_size == 0:
        print(f"Training batch {i // batch_size + 1}")
        trainer.train(training_data)
        training_data = []

if training_data:
    print("Training final batch")
    trainer.train(training_data)