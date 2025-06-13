from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import fitz  # Converts PDF files to TXT.
import docx  # Converts Docx files to TXT.
import pandas as pd  # Converts Excel files to TXT.
import shutil
import spacy # Industrial-Strength Natural Language Processing https://spacy.io/
from config import ai_model, embedding_model, Source_Documents, Converted_TXT, Vectors, Chunk_size

# Embedding Model
embeddings = OllamaEmbeddings(model=embedding_model)

# Vector Store with Chrome DB
def load_vectors(vVectors):
    global vector_store
    vector_store = Chroma(
        collection_name="database", 
        persist_directory= Vectors,
        embedding_function=embeddings
    )
    return vector_store

def retrieve_question_from_vectors(question):
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(question)
    database_text = "\n".join([doc.page_content for doc in docs])
    return database_text

# ----Converting documents to TXT format----

def read_pdf(Source_Documents):
    text = ""
    with fitz.open(Source_Documents) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

def read_word(Source_Documents):
    doc = docx.Document(Source_Documents)
    return "\n".join([para.text for para in doc.paragraphs])

def read_excel(Source_Documents):
    df = pd.read_excel(Source_Documents)
    return df.to_string()  # Tabellen-Daten als Text

def convert_and_store(Source_Documents, Converted_TXT):  
    for file_name in os.listdir(Source_Documents):
        file_path = os.path.join(Source_Documents, file_name)
        converted_path = os.path.join(Converted_TXT, f"{os.path.splitext(file_name)[0]}.txt")

        if os.path.exists(converted_path):  
            continue

        if file_name.endswith(".pdf"):
            content = read_pdf(file_path)
        elif file_name.endswith(".docx"):
            content = read_word(file_path)
        elif file_name.endswith(".xlsx"):
            content = read_excel(file_path)
        elif file_name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as txt_file:
                content = txt_file.read()
        else:
            continue

        with open(converted_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(content)
         print("Task completed successfully.") 


# ---- Natural Language Processing with spaCy ----

# For additional language support, please visit https://spacy.io/.
#nlp = spacy.load("de_core_news_sm") # For German language support
nlp = spacy.load("en_core_web_sm") # For English language support

def split_text_into_chunks(text, max_tokens= Chunk_size):
    doc = nlp(text)
    sentences = [sentence.text.strip() for sentence in doc.sents if sentence.text.strip()]
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        combined_text = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
        token_count = len(combined_text.split())

        if token_count > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk = combined_text

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# ---- Converting TXT to Vectors ----

def txt_to_vector(Converted_TXT):
    documents = []
    for file_name in os.listdir(Converted_TXT):
        file_path = os.path.join(Converted_TXT, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        text_chunks = split_text_into_chunks(text)

        for chunk in text_chunks:
            document = Document(
                page_content=chunk,
                metadata={"file_name": file_name}
            )
            documents.append(document)

    if documents:
        vector_store.add_documents(documents)
        print("Task completed successfully.")


    # Deletes all TXT files from the Converted_TXT folder.
    if os.path.exists(Converted_TXT):
        try:
            for file_name in os.listdir(Converted_TXT):
                file_path = os.path.join(Converted_TXT, file_name)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting files: {e}")


