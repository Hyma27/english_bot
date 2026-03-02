import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from datetime import datetime, UTC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


 
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
mongo_uri = os.getenv("MONGO_URI")



client = MongoClient(mongo_uri)
db = client["englishbot"]
collection = db["chats"]

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    question: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

prompts = ChatPromptTemplate.from_messages([
    ("system",
     """You are an English Communication Practice Assistant.
      Correct grammar politely.
      Explain mistakes simply.
      Ask follow-up questions.
      Keep answers short and beginner friendly.
"""),
    ("placeholder", "{history}"),
    ("user", "{question}")
])


chat = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama-3.1-8b-instant"
    
    )
chain = prompts | chat



def get_history(user_id):
    chats = collection.find(
        {"user_id":user_id}
    ).sort("time",1)
    
    history = []
    
    for chat in chats:
        history.append(
            (chat["role"], chat["message"])
        )
    return history
    
@app.get("/")
def home():
    return {"message": "Welcome to the English Practice Bot!"}

@app.post("/chat")
def chat(request: ChatRequest):
    history = get_history(request.user_id)
    response = chain.invoke({"history": history, "question": request.question})
    collection.insert_one({
                       "user_id":request.user_id,
                       "role": "user",
                       "message": request.question,
                       "time": datetime.now(UTC)
    })

    collection.insert_one({
                       "user_id": request.user_id,
                       "role": "assistant",
                       "message": response.content,
                        "time": datetime.now(UTC)
    })
 
    return {"response": response.content}

    