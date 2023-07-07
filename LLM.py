from PyPDF2 import PdfReader
import os
import re
from cleantext import clean
import openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS, Pinecone, Chroma
from nltk.corpus import wordnet
from langchain.embeddings import  OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet


nltk.download("wordnet")
nltk.download("punkt")
nltk.download('omw-1.4')
nltk.download("averaged_perceptron_tagger")

# Load environment variables from .env
load_dotenv()
open_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = open_api_key


def cleaning_of_text(x):
  pattern = re.compile("<.*?>")
  x =  pattern.sub(r" ", x)
  pattern = re.compile("r'https?://\S+|www.\.\S+")
  x = pattern.sub(r" ", x)
  x = clean(x)
  x = x.replace("\n"," ")
  x = x.replace("!"," ")
  x = x.replace("?"," ")
  return x



def get_wordnet_part_of_speech(tag):

  if tag.startswith("J"):
    return wordnet.ADJ

  elif tag.startswith("V"):
    return wordnet.VERB

  elif tag.startswith("N"):
    return wordnet.NOUN

  elif tag.startswith("R"):
    return wordnet.ADV

  else:
    return wordnet.NOUN



def lemmatize(x):
  text = []
  tokens = word_tokenize(x)
  words_tags = nltk.pos_tag(tokens)
  for word, tag in words_tags:
    num =  WordNetLemmatizer().lemmatize(word, pos=get_wordnet_part_of_speech(tag))
    text.append(num)
  return " ".join(text)



def get_data(file_names):

  # Collecting data
  all_text = ""

  for file_ in file_names:
    reader = PdfReader("./pdf_data/"+file_)

    for n in range(len(reader.pages)):
      page = reader.pages[n]
      text = page.extract_text()
      all_text+=text

  #Splitting into chunks
  text_splitter = CharacterTextSplitter(separator="\n",chunk_size=2000, chunk_overlap=200, length_function = len)
  chunks = text_splitter.split_text(all_text)


  # Cleaning of our data
  new_data_chunks=[]
  for n in chunks:
    new_data_chunks.append(cleaning_of_text(n))


  #Lemmatizing
  lemmatized_data = []
  for n in new_data_chunks:
    lemmatized_data.append(lemmatize(n))

  return lemmatized_data


file_names = os.listdir("./pdf_data/")


data = get_data(file_names)


#get embeddings
embdings =  OpenAIEmbeddings(model="text-embedding-ada-002")

#store in chroma
#db = Chroma.from_texts(data, embdings)
db = Chroma(persist_directory= "./db-20230704T094838Z-001/db",embedding_function=embdings)

# Creating LLM for our model
model_name = "gpt-3.5-turbo-16k"
llm = OpenAI(model_name=model_name)

chain = load_qa_chain(llm, chain_type="stuff")


# generate answers
def give_keywords(query):
  db = Chroma(persist_directory= "./db-20230704T094838Z-001/db",embedding_function=embdings)
  search = db.similarity_search(query,k=3)
  return search

def get_answer(query, similar_docs):
  # 
  answer = chain.run(input_documents=similar_docs, question=query)
  return answer


# query = "tell me about CRISPR & Gene Editing?"
# similar_docs = give_keywords(query)
# answer = get_answer(query, similar_docs)
# print(answer)


