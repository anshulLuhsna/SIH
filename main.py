# Libraries
import openai
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st




load_dotenv()
open_key = st.secrets["OPENAI_API_KEY"]
pine_key = st.secrets["PINECONE_API_KEY"]
openai.api_key = open_key

pinecone.init(api_key = pine_key,
     environment="gcp-starter")
     
index_name= "laws"
index = pinecone.Index(index_name)


url_summarize = "https://api.worqhat.com/api/ai/content/v2"
headers_summarize = {
    "x-api-key": "sk-95ac67907ba94319a3d6a6c7e3907421",
    "Authorization": "Bearer sk-95ac67907ba94319a3d6a6c7e3907421",
    "Content-Type": "application/json"
}


# Functions
# def get_response(question, history):
#     st.session_state["history"].append(question)
    
    
    
#     for i,message in enumerate(st.session_state["history"]):
#         if(i % 2 == 0):
#             with st.chat_message("user"):
#                 st.write(st.session_state["history"][-2] )
#         else: 
#             with st.chat_message("assistant"):
#                 st.write(st.session_state["history"][-1])


    
if "history" not in st.session_state:
    st.session_state["history"]=[]
if "conversation" not in st.session_state:
    st.session_state["conversation"]=[]
if "voiceinp" not in st.session_state:
     st.session_state.voiceinp = False





# if st.session_state.voiceinp:    
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#                 st.write("Listening...")
#                 audio = recognizer.listen(source)
#     user_voice_question = recognizer.recognize_google(audio)
#     xqq = openai.Embedding.create(input=user_voice_question, engine="text-embedding-ada-002")['data'][0]['embedding']
#     docss=index.query([xqq],top_k=3,include_metadata=True)
#     training_dataa=""
#     for i in range(3):
#         training_dataa+=docss["matches"][i]["metadata"]["text"]
#     print(training_dataa)
#     dataa = {
#     "question":"Only answer on the basis of data provided, otherwise refuse to answer"+user_voice_question,
#     "preserve_history": True,
#     "history_object":st.session_state["history"],
#     "training_data": training_dataa,
#     "randomness": 0.1
#     }


#     response = requests.post(url_summarize, headers=headers_summarize, json=dataa)
#     message = response.json()["content"]
#     st.session_state["history"].append(user_voice_question)
#     st.session_state["history"].append(message)
#     st.session_state["conversation"].append({"role": "user", "content": user_voice_question})
#     st.session_state["conversation"].append({"role": "assistant", "content": message})
#     for msg in st.session_state["conversation"]:
#         st.chat_message(msg["role"]).write(msg["content"])

# Session state keys declaration


# UI starts here
st.title("Hello!")
# st.button("Take voice input", on_click=get_voice())


# for i,message in enumerate(st.session_state["history"]):
#         if(i % 2 == 0):
#             with st.chat_message("user"):
#                 st.write(st.session_state["history"][-2] )
#         else: 
#             with st.chat_message("assistant"):
#                 st.write(st.session_state["history"][-1])

    

if prompt := st.chat_input():
    st.session_state.voiceinp = False
    xq = openai.Embedding.create(input=prompt, engine="text-embedding-ada-002")['data'][0]['embedding']
    docs=index.query([xq],top_k=3,include_metadata=True)
    training_data=""
    for i in range(3):
        training_data+=docs["matches"][i]["metadata"]["text"]
    print(training_data)
    data = {
    "question":"Only answer on the basis of data provided, otherwise refuse to answer"+prompt,
    "preserve_history": True,
    "history_object":st.session_state["history"],
    "training_data": training_data,
    "randomness": 0.1
    }


    response = requests.post(url_summarize, headers=headers_summarize, json=data)
    message = response.json()["content"]
    st.session_state["history"].append(prompt)
    st.session_state["history"].append(message)
    st.session_state["conversation"].append({"role": "user", "content": prompt})
    st.session_state["conversation"].append({"role": "assistant", "content": message})
    for msg in st.session_state["conversation"]:
        st.chat_message(msg["role"]).write(msg["content"])
