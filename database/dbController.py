import openai
import ollama
import astrapy
import json
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from llama_index.core import SimpleDirectoryReader

class ProcessDocuments: 
    def __init__(self):
        self.markdown_dir = "./data"

        pass
    
    def createDocs(self, something):
        pass

    def embedd(self, text: str):
        pass