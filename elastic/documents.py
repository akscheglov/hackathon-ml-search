from config import conversations_file_path, text_files_path, html_files_path, urls_list

import json
from os import listdir
from os.path import isfile, join
from typing import List
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.file import HTMLTagReader
from llama_index.readers.web import SimpleWebPageReader

def _combine(docs: List[List[Document]]) -> List[Document]:
    result = []
    for doc in docs:
        result.extend(doc)

    return result

def _files(path: str) -> List[str]:
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def _get_conversations() -> List[Document]:
    print('Loading conversations')
    with open(file=conversations_file_path, mode='rt') as f:
        conversations_dict = json.loads(f.read())

    documents = [Document(text=item['conversation'], metadata={"conversation_id": item['conversation_id']})
                    for item in conversations_dict]

    return documents

def _get_html_files() -> List[Document]:
    print('Loading html files')
    reader = HTMLTagReader(tag="section", ignore_no_id=True)
    docs = [reader.load_data(f) for f in _files(html_files_path)]

    return _combine(docs)

def _get_data_documents() -> List[Document]:
    reader = SimpleDirectoryReader(input_dir=text_files_path)
    documents = reader.load_data(show_progress=True)

    return documents

def _get_web_data() -> List[Document]:
    print('Loading web resources')
    web_reader = SimpleWebPageReader(html_to_text=True)
    documents = web_reader.load_data(urls_list)

    return documents

def get_documents() -> List[Document]:
    docs = [
        _get_conversations(),
        _get_web_data(),
        _get_html_files(),
        _get_data_documents(),
    ]

    return _combine(docs)


