import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.prompts import ChatPromptTemplate
from functions import (
    convert_and_store,
    txt_to_vector,
    load_vectors,
    split_text_into_chunks,
    retrieve_question_from_vectors
)
from config import ai_model, embedding_model, Source_Documents, commands #, model_google

# KI-Modell initialisieren
model = OllamaLLM(model=ai_model)
#model_google = ChatGoogleGenerativeAI(model="gemini-pro")

template = '''Hi there! I'm your AI Assistant, ready to help you with your documents. All my responses are based solely on the information you provide.

---

**Conversation History:** {conversation_history}
**Source Material (Database):** {database}
**Your Question:** {question}
'''

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


conversation_history = []

while True:
    question = input(f"Hi there, how can I help you?\n You: ").strip().lower()
    if question == "exit":
        print("Goodbye")
        exit()
    elif question == "sync":
        pass

