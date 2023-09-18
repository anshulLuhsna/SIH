from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import openai
import pinecone
import os
import requests

url_summarize = "https://api.worqhat.com/api/ai/content/v2"
headers_summarize = {
    "x-api-key": "sk-95ac67907ba94319a3d6a6c7e3907421",
    "Authorization": "Bearer sk-95ac67907ba94319a3d6a6c7e3907421",
    "Content-Type": "application/json"
}


load_dotenv()
open_key = os.environ.get("OPENAI_API_KEY")
pine_key = os.environ.get("PINECONE_API_KEY")
openai.api_key = open_key

# loader = UnstructuredPDFLoader("6 Consumer rights.pdf")
# data = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0)
# texts=text_splitter.split_documents(data)

# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002",openai_api_key=open_key)
pinecone.init(api_key = pine_key,
     environment="gcp-starter")
     
index_name= "laws"

# docsearch = Pinecone.from_texts([t.page_content for t in texts],embeddings,index_name=index_name)


index = pinecone.Index(index_name)
query = "How to file a complaint?"

xq = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
docs=index.query([xq],top_k=1,include_metadata=True)

print(docs)

training_data = docs["matches"][0]["metadata"]["text"]

data = {
    "question":query,
    "training_data": training_data, 
    "randomness": 0.1
    }

response = requests.post(url_summarize, headers=headers_summarize, json=data)
print(response.json()["content"])