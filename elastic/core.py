from config import ModelType, VectorStoreType, model_type, vector_store_type, ollama_model_name, request_timeout, llamafile_port

from llama_index.vector_stores.elasticsearch import ElasticsearchStore, AsyncBM25Strategy, AsyncDenseVectorStrategy
from elasticsearch import AsyncElasticsearch

from llama_index.core.vector_stores.simple import SimpleVectorStore

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.llms.llamafile import Llamafile
from llama_index.embeddings.llamafile import LlamafileEmbedding

# import faiss
from llama_index.vector_stores.faiss import FaissVectorStore

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
            es_client=AsyncElasticsearch(hosts=['http://localhost:9200'], request_timeout=request_timeout),
            # retrieval_strategy=AsyncBM25Strategy(),
            retrieval_strategy=AsyncDenseVectorStrategy(hybrid=True),
        )
    case VectorStoreType.FAISS:
        d = 1536 # dimensions of text-ada-embedding-002, the embedding model that we're going to use
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
    case _:
        raise Exception('unknown vector store type' + vector_store_type.name)
