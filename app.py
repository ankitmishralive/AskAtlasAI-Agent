
import warnings

# Suppress UserWarnings from the pydantic module
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from dotenv import load_dotenv 
import os 
import pandas as pd 

from llama_index.experimental.query_engine import PandasQueryEngine

from prompts import new_prompt,instruction_str,context

# from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI


from note_engine import note_engine

from llama_index.core.tools import QueryEngineTool,ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.mistralai import MistralAI

from llama_index.llms.gemini import Gemini

from pdf import demographics_engine
from llama_index.llms.ollama import Ollama


# from llama_index.llms.ollama import Ollama


load_dotenv()  # Load environment variables from .env file

# HF_TOKEN= os.getenv("HF_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN").strip()

MISTRAL_TOKEN= os.getenv("MISTRAL_TOKEN")

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Or you can skip providing a token, using Hugging Face Inference API anonymously
remotely_run = HuggingFaceInferenceAPI(
     model_name="mistralai/Mistral-7B-Instruct-v0.3",
    # model_name="mistralai/Ministral-8B-Instruct-2410",
     token=HF_TOKEN,
    #   model_config={"protected_namespaces": ()} 
)


population_path = os.path.join('data','population.csv')
population_df= pd.read_csv(population_path)

population_query_engine = PandasQueryEngine(df=population_df, verbose=True,
                                            instruction_str=instruction_str,llm=remotely_run)


population_query_engine.update_prompts({
    'pandas_prompt':new_prompt
})




# Define the tools list
tools = [

    note_engine, 


    QueryEngineTool(
        query_engine=population_query_engine,

        metadata=ToolMetadata(
            name="population_data",
            description="this gives information at the world population."
        )
    ),


    QueryEngineTool(
        query_engine=demographics_engine,
        metadata=ToolMetadata(
            name="demographics_data",
            description="this gives information at the world's demographics."
        )
    )


]



# Mistal Models:
# mistral-tiny, mistral-small, mistral-medium, mistral-large, open-mixtral-8x7b, open-mistral-7b, 
# open-mixtral-8x22b, mistral-small-latest, mistral-medium-latest, mistral-large-latest,
#  codestral-latest, open-mistral-nemo-latest, ministral-8b-latest, ministral-3b-latest

# llm = MistralAI(api_key=MISTRAL_TOKEN,model="Mistral-7B-instruct-v0.1 4bit")

# llm = Gemini(
#     model="models/gemini-1.5-flash",
# )



llm = MistralAI(api_key=MISTRAL_TOKEN,model="ministral-8b-latest")

agent = ReActAgent.from_tools(tools, llm=llm,verbose=True,context=context)


while (prompt := input("Enter  a prompt (q to quit):  ")) != "q":
    result = agent.query(prompt)
    print(result)






