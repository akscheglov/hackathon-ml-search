from core import vector_store, embed_model, llm

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
query_engine = index.as_query_engine(llm=llm, similarity_top_k=10)

queries = [
    'сколько богатырей выходят из моря?',
]

print('Q&A')

for query in queries:
    response = query_engine.query(query)
    print(f'Q: {query}')
    print(f'A: {response}\n\n')
