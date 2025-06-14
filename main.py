import os
import time
from datetime import datetime
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from functions import txt_to_vector, load_vectors, convert_and_store, sync_and_delete, retrieve_database_from_vector
from config import ai_model, Source_Documents, Vectors


model = OllamaLLM(model=ai_model)
template = """
Hi there! I'm your AI Assistant, ready to help you with your documents. All my responses are based solely on the information you provide.

---

**Conversation History:** {conversation_history}
**Source Material (Database):** {database}
**Your Question:** {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


commands = ["exit", "sync", "new", "n"]
conversation_history = []

while True:
    current_hour = datetime.now().hour
    if current_hour % 4 == 0:
        sync_and_delete()

    question = input(f"{ai_model}: Hi there, how can I help you?\nYou: ").strip().lower()

    if question in commands:
        if question == "exit":
            print("Goodbye")
            break
        elif question == "sync":
            convert_and_store(Source_Documents)
            txt_to_vector()
            load_vectors()
        elif question == "new" or question == "n":
            conversation_history.clear()
    else:
        database = retrieve_database_from_vector(question)
        conv_str = "\n".join([f"User: {entry['question']}\nBot: {entry['response']}" 
                              for entry in conversation_history])
        result = chain.invoke({
            "database": database,
            "question": question,
            "conversation_history": conv_str
        })
        conversation_history.append({"question": question, "response": result})
        print(result)
