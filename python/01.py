from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer
import torch
  
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
  
context = "burj khalifa is the tallest biulding in the whole world."
input_text = f"Generate a question from the following context: \'{context}\'"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)
  
output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, pad_token_id=50256, attention_mask=attention_mask)
  
generated_question = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_question)