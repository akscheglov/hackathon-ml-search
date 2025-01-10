from core import vector_store, embed_model, llm, vector_store_type, VectorStoreType
from prompts import update_prompts

from llama_index.core import VectorStoreIndex, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore

node_postprocessors = []

if vector_store_type == VectorStoreType.INMEMORY or vector_store_type == VectorStoreType.FAISS:
    dir = './store_'+vector_store_type.name.lower()
    vector_store = FaissVectorStore.from_persist_dir(dir)
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=dir, embed_model=embed_model)
    index = load_index_from_storage(storage_context=storage_context)
else:
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

query_engine = index.as_query_engine(llm=llm, similarity_top_k=10, node_postprocessors=node_postprocessors)

update_prompts(query_engine)

queries = [
    'сколько богатырей выходят из моря?',
]

print('Q&A')

for query in queries:
    response = query_engine.query(query)
    print(f'Q: {query}')
    print(f'A: {response}\n\n')
