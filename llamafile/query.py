from config import server_url, persist_dir, request_timeout

from llama_index.llms.llamafile import Llamafile
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.core import StorageContext, load_index_from_storage

llm = Llamafile(base_url=server_url, request_timeout=100, temperature=0, seed=0)
embed_model = LlamafileEmbedding(base_url=server_url, request_timeout=request_timeout)

storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
index = load_index_from_storage(storage_context, embed_model=embed_model)

node_postprocessors=[]
query_engine = index.as_query_engine(llm=llm, node_postprocessors=node_postprocessors)

response = query_engine.query('сколько витязей выходят из моря?')
print(response)
