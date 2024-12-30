import os
from enum import Enum
from dotenv import load_dotenv

class ModelType(Enum):
    OLLAMA = 1
    LLAMAFILE = 2

class VectorStoreType(Enum):
    INMEMORY = 1
    ELASTICSEARCH = 2

load_dotenv('../.settings')

ollama_model_name = os.getenv('OLLAMA_MODEL')
llamafile_port = os.getenv('LLAMAFILE_PORT')
model_type_string = os.getenv('MODEL_TYPE')

request_timeout = 300

conversations_file_path = '../data/conversations/conversations.json'
text_files_path = '../data/texts'
html_files_path = '../data/html'
urls_list = [
    'https://habr.com/ru/articles/751714/',
    'https://habr.com/ru/articles/755186/',
    'https://habr.com/ru/articles/760944/',
    'https://habr.com/ru/companies/tochka/articles/809493/',
]

model_type = ModelType[model_type_string]
vector_store_type = VectorStoreType.ELASTICSEARCH
