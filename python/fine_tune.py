from transformers import BertForQuestionAnswering, BertTokenizer, AdamW
import torch

# Load the pre-trained model and tokenizer
model = BertForQuestionAnswering.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Define and load your training data
training_data = [
    {"question": "What is the capital of France?", "context": "Paris is the capital of France.", "start_positions": 12, "end_positions": 17},
    {"question": "Who wrote Hamlet?", "context": "William Shakespeare is the author of Hamlet.", "start_positions": 0, "end_positions": 18},
    # Add more data here
]

# Define training configuration
optimizer = AdamW(model.parameters(), lr=1e-5)
num_epochs = 3

# Fine-tuning loop
for epoch in range(num_epochs):
    for batch in training_data:
        inputs = tokenizer(batch["question"], batch["context"], return_tensors="pt", padding=True, truncation=True)
        start_positions = torch.tensor(batch["start_positions"])
        end_positions = torch.tensor(batch["end_positions"])
        
        outputs = model(**inputs, start_positions=start_positions, end_positions=end_positions)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

# Evaluate your fine-tuned model

# Use the fine-tuned model for inference
