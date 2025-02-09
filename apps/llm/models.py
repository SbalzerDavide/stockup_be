from langchain_ollama.llms import OllamaLLM

from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

ollama_host = os.getenv("OLLAMA_HOST")
print(f"Ollama host: {ollama_host}")
model = OllamaLLM(model="llama3.2", base_url=ollama_host)
llm = ChatOpenAI(model="llama3.2", api_key="ollama", base_url=f"{ollama_host}/v1")


