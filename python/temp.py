import re


# Open the file for reading
with open('D:\Ronak\Python\questions_text.txt', 'r') as file:
    text = file.read()

# Define a regular expression pattern to split the text into sentences
sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'

# Split the text into sentences
sentences = re.split(sentence_pattern, text)

# Print each sentence
for sentence in sentences:
    print(sentence)
