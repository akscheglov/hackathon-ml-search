from config import ModelType, VectorStoreType, model_type, vector_store_type, ollama_model_name, request_timeout, llamafile_port

from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core.vector_stores.simple import SimpleVectorStore

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.llms.llamafile import Llamafile
from llama_index.embeddings.llamafile import LlamafileEmbedding

index_name = model_type.name.lower()+'_idx'

match model_type:
    case ModelType.OLLAMA:
        llm = Ollama(model=ollama_model_name, request_timeout=request_timeout)
        embed_model = OllamaEmbedding(ollama_model_name)
        index_name = ollama_model_name + '' + index_name
    case ModelType.LLAMAFILE:
        server_url = 'http://localhost:'+llamafile_port
        llm = Llamafile(base_url=server_url, request_timeout=request_timeout, temperature=0, seed=0)
        embed_model = LlamafileEmbedding(base_url=server_url, request_timeout=request_timeout)
    case _:
        raise Exception('unknown model type' + model_type.name)



match vector_store_type:
    case VectorStoreType.INMEMORY:
        # SimpleVectorStore.from_persist_dir(persist_dir='mydir')
        vector_store = SimpleVectorStore()
    case VectorStoreType.ELASTICSEARCH:
        vector_store = ElasticsearchStore(
            index_name=index_name,
            vector_field='model_vector',
            text_field='model_text',
            es_url='http://localhost:9200',
        )
    case _:
        raise Exception('unknown vector store type' + vector_store_type.name)
