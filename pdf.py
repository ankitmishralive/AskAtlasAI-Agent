import os 
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from llama_index.llms.mistralai import MistralAI       
from dotenv import load_dotenv 

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.ollama import Ollama

from llama_index.core.embeddings import resolve_embed_model

from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

load_dotenv()  # Load environment variables from .env file

MISTRAL_TOKEN = os.getenv("MISTRAL_TOKEN")


# HF_TOKEN= os.getenv("HF_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")


# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5",token=HF_TOKEN)

def get_index(data, index_name):
    index = None 
    if not os.path.exists(index_name):
        print("Building Index ", index_name)
        embed_model = resolve_embed_model("local:BAAI/bge-m3")
        index = VectorStoreIndex.from_documents(data, show_progress=True,embed_model=embed_model)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )
    
    return index 

# Initialize the LLM
# llm = MistralAI(api_key=MISTRAL_TOKEN, model="mistral-8b-latest")

# Load PDF data
pdf_path = os.path.join('data', 'Demographics_of_the_world.pdf')
demographics_pdf = PDFReader().load_data(pdf_path)

# Create or load the index
demographics_index = get_index(demographics_pdf, "demographics")

# llm = MistralAI(api_key=MISTRAL_TOKEN,model="Mistral-7B-instruct-v0.1 4bit")


llm = MistralAI(api_key=MISTRAL_TOKEN,model="mistral-medium")

# llm = Ollama(model="llama3.1:latest", request_timeout=120.0)

# llm = HuggingFaceInferenceAPI(
#     model_name="mistralai/Mistral-7B-Instruct-v0.2", token=HF_TOKEN
# )

# Create a query engine with the LLM
demographics_engine = demographics_index.as_query_engine(llm=llm)

# Example query
# response = demographics_engine.query("What are the key demographics of the world?")
# print(response)