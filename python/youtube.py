# importing all the necessary model , libraries etc into programe

from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer, BertTokenizer, BertModel, AutoTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import spacy
from transformers import BertTokenizer, BertModel
from warnings import filterwarnings as filt
import csv 
import re


# To downloading the "punkt" dataset, which contains data used for tokenization
# nltk.download('punkt')


filt('ignore')

# Creating a BERT tokenizer
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Loaging the pre-trained BERT model "bert-base-uncased"
bert_model = BertModel.from_pretrained("bert-base-uncased")

# Selecting the SentenceTransformer model 
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# loading the "en_core_web_sm" model (pre-trained model for processing English text)
nlp = spacy.load("en_core_web_sm")


# Function For Generation Of Question Provided {Sentence,Keyword}
def get_question(sentence, answer):

  mdl = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
  tknizer = AutoTokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')

  text = "context: {} answer: {}".format(sentence,answer)
  max_len = 256
  encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = mdl.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=5,
                                  num_return_sequences=1,
                                  no_repeat_ngram_size=2,
                                  max_length=300)


  dec = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]


  Question = dec[0].replace("question:","")
  Question= Question.strip()
  return Question

# Takes a Document or Text as Input and returns the Embeddings of that Text Using the BERT

def get_embedding(doc):

  bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  bert_model = BertModel.from_pretrained("bert-base-uncased")
  
  # txt = '[CLS] ' + doc + ' [SEP]'
  tokens = bert_tokenizer.tokenize(txt)
  token_idx = bert_tokenizer.convert_tokens_to_ids(tokens)
  segment_ids = [1] * len(tokens)

  torch_token = torch.tensor([token_idx])
  torch_segment = torch.tensor([segment_ids])

  return bert_model(torch_token, torch_segment)[-1].detach().numpy()


# For part-of-speech (POS) tagging of a given text "context"
def get_pos(context):
  doc = nlp(context)
  docs = [d.pos_ for d in doc]
  return docs, context.split()

# Process the Text and Split it into Sentences
def get_sent(context):
  doc = nlp(context)
  return list(doc.sents)

# Takes a Docuent as Input and Returns a List of the Feature Names Based on the Document's Text
def get_vector(doc):
  stop_words = "english"
  n_gram_range = (1,1)
  df = CountVectorizer(ngram_range = n_gram_range, stop_words = stop_words).fit([doc])
  return df.get_feature_names()

# Generating the KeyWord of the "Context" For the get_question Function
def get_key_words(context, module_type = 't'):
  keywords = []
  top_n = 5
  for txt in get_sent(context):
    keywd = get_vector(str(txt))
    print(f'vectors : {keywd}')
    if module_type == 't':
      doc_embedding = get_embedding(str(txt))
      keywd_embedding = get_embedding(' '.join(keywd))
    else:
      doc_embedding = model.encode([str(txt)])
      keywd_embedding = model.encode(keywd)
    
    distances = cosine_similarity(doc_embedding, keywd_embedding)
    print(distances)
    keywords += [(keywd[index], str(txt)) for index in distances.argsort()[0][-top_n:]]

  return keywords

# Load the spaCy English tokenizer
nlp = spacy.load("en_core_web_sm")

# File Path Where Sentence From which Question is to Be Generated is Stored.
file_path = "D:\Ronak\Python\questions_text.txt"

# File Path Where the Question generated from the Sentences is to be Store.
file_path1 = "D:\Ronak\Python\question.txt"

# opening and reading the file_path file
with open(file_path, 'r') as file:
    text = file.read()

sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'

sentences = re.split(sentence_pattern, text)

# Reading not the line but the full sentence.
counter = 0
temp_text = ""

def remove_punctuation_except_full_stop(sentence):
    # Define a regular expression pattern to match all punctuation except full stop
    pattern = r'[^\w\s.]'
    
    # Use re.sub() to remove the matched characters
    cleaned_sentence = re.sub(pattern, '', sentence)
    
    return cleaned_sentence

extra_temp = ""

# Iterate through the sentences
for sentence in sentences:
    print(sentence)
    # extra_temp = remove_punctuation_except_full_stop(sentence)
    # print(extra_temp)
    counter = -1
    # counter = counter + 1
    for ans, context in get_key_words(sentence, 'st'):
         counter = counter + 1
         print(counter)
         if counter % 5 == 0:
            with open(file_path1, "a") as file:
            # Write Generated Question into file_path1
               temp_text = get_question(context, ans) + "\n"
               file.write(temp_text)
               print(temp_text)
         else :
            continue
         
 