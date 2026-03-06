import datetime
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient 
from datetime import datetime,UTC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

## Connect to MongoDB and create database & collection
client = MongoClient(mongo_uri)
db = client["engllish2"]
collection = db["chat"]

#Initialize FastAPI application
app = FastAPI(
    title="English Chatbot",
    description="AI-powered English Communication Practice Assistant",
    version="1.0"
)

## Define request structure for the chat API
class ChatRequest(BaseModel):
    user_id: str
    question: str

## Enable CORS so frontend applications can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # can assess from any origin
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

## Define the AI prompt template to guide the English practice assistant
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an English Communication Practice Assistant. "
     "Help users improve grammar, speaking, vocabulary, and sentence formation. "
     "Correct mistakes and explain simply."
     "Help users convert their ideas into correct English sentences. "
     "If the user is preparing for interviews or daily communication, guide them with proper answers and suggestions. "
        "Provide feedback on their English usage and suggest improvements."
    ),
    ("placeholder", "{history}"),
    ("user", "{input}")
])


## Initialize Groq language model and create processing chain
chat = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.1-8b-instant")
chain = prompt | chat


## Function to retrieve previous conversation history from MongoDB
def get_history(user_id):
    chats = collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []
    
    for chat in chats:
        history.append((chat["role"], chat["message"]))
    return history

#Home endpoint to check if the API is running
@app.get("/")
def home():
    return {"message": "Welcome to the English Communication Practice Assistant!"}

# Chat endpoint to process user questions and return AI responses
@app.post("/chat")
def chat(request: ChatRequest):
    
    
    # Get previous conversation history
    history = get_history(request.user_id)
    
    # Generate AI response using the conversation history and user input
    response = chain.invoke({"history": history, "input": request.question})
    
    
    # Store user message in MongoDB
    collection.insert_one({
        "user_id": request.user_id,
        "role": "user",
        "message": request.question,
        "timestamp": datetime.now(UTC)
    })
    
     # Store AI response in MongoDB
    
    collection.insert_one({
        "user_id": request.user_id,
        "role": "assistant",
        "message": response.content,
        "timestamp": datetime.now(UTC)
    })
    
     # Return response to the client
    return {"response": response.content}

    
