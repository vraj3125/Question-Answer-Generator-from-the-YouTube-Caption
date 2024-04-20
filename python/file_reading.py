import spacy

# Load the spaCy English tokenizer
nlp = spacy.load("en_core_web_sm")

# Open and read the text file
file_path = "D:\Ronak\Python\questions_text.txt"
with open(file_path, "r") as file:
    text = file.read()

# Process the text with spaCy
doc = nlp(text)
counter = 0
# Iterate through the sentences
for sentence in doc.sents:
    print(sentence.text)
    print(counter)
    counter = counter + 1
