from config import server_url, persist_dir, input_dir_path, request_timeout

from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

reader = SimpleDirectoryReader(input_dir=input_dir_path)
documents = reader.load_data(show_progress=True)

transformations=[
    SentenceSplitter(
	    chunk_size=256,
	    chunk_overlap=5
    ),
]
embed_model = LlamafileEmbedding(base_url=server_url, request_timeout=request_timeout)

index = VectorStoreIndex.from_documents(
	documents,
	show_progress=True,
    transformations=transformations,
    embed_model=embed_model,
)

index.storage_context.persist(persist_dir=persist_dir)
