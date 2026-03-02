
# 🗣️ English Communication Practice ChatBot Project

## 🚀 Project Overview
English Communication Practice Bot is an AI-powered chatbot designed to help users improve their English communication skills through interactive conversations. The chatbot provides grammar correction, simple explanations, and follow-up questions to encourage continuous English practice.  

The system uses Groq Large Language Model (LLM) for intelligent responses and MongoDB Atlas to store conversation history. The chatbot backend is developed using FastAPI.

## Objectives
- Develop an AI-based English communication assistant
- Provide grammar correction and sentence improvement
- Maintain conversation memory using MongoDB
- Build REST API using FastAPI
- Enable real-time conversational interaction
- Deploy chatbot for online access


---


## 🧠 System Architecture


User → FastAPI → LangChain → Groq LLM → MongoDB Atlas → Response

---

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **LangChain**
- **Groq API**
- **MongoDB Atlas**
- **Natural Language Processing (NLP)**
- **Uvicorn**
- **Pydantic**
- **GitHub**
- **Render**

---

## NLP Usage
Natural Language Processing (NLP) is used in this project to:
- Understand user input in natural English
- Perform grammar correction
- Maintain conversational context
- Generate human-like responses
- Support interactive English communication practice

---

## Memory Implementation
The chatbot stores user conversations in MongoDB using a unique `user_id`.  
When a new question is asked:
1. Previous conversation history is retrieved.
2. History is passed to the LLM using LangChain.
3. The chatbot generates context-aware responses.
4. New conversations are stored back into MongoDB.

This enables memory-based conversational interaction.

## 📡 API Endpoint

### POST /chat

#### Example Request
- {
  "user_id": "user123",
  "question": "How can I improve my English?"
}
### Example Response
- {
  "response": "You can improve your English by practicing daily conversations..."
}

## 📂 Project Structure

English _Bot

- **app.py**
- **requirements.txt**
- **.env.example**
- **README.md**
- **English_Communication_Practice_Bot_Report.pdf** 
- **screenshots**

### Deployment Link
---
### GitHub Repository Link
https://github.com/Hyma27/english_bot

