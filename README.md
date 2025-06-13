Here is a corrected and more polished version of your text:

# AI-RAG-Toolkit

A versatile Retrieval-Augmented Generation (RAG) toolkit designed for exploring and integrating various AI models, including local LLMs (via Ollama) and API-based services (such as Gemini and ChatGPT). This project aims to be a flexible platform for experimenting with advanced RAG architectures and other AI functionalities.

## How to Use It:

1. **Install Anaconda or Miniconda**
   [https://www.anaconda.com/](https://www.anaconda.com/)

2. **Create a New Environment**

   ```bash
   conda create -n my_rag_env python=3.12
   ```

3. **Install the Required Libraries via Conda-Forge and/or Pip**

   ```bash
   conda install -c conda-forge langchain
   conda install -c conda-forge pandas
   conda install -c conda-forge spacy
   pip install PyMuPDF
   pip install python-docx
   ```

4. **Download the SpaCy Language Model(s)**

   ```bash
   python -m spacy download en_core_web_sm  # English model  
   python -m spacy download de_core_news_sm  # German model
   ```

5. **If You Encounter Issues, Try Installing LangChain via Pip Instead**

   ```bash
   pip install langchain-ollama
   pip install langchain-chroma
   ```
6. **Depending on your AI model, either insert your API key in config.py or download Ollama and select an AI model and embedding model there.**
https://ollama.com/
