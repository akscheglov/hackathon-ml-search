from core import vector_store, embed_model
from documents import get_documents

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

# LlamaIndex Pipeline configured to take care of chunking, embedding
# and storing the embeddings in the vector store.
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=350, chunk_overlap=50),
        embed_model,
    ],
    vector_store=vector_store,
)

documents = get_documents()

print(".....Starting pipeline.....")

pipeline.run(show_progress=True, documents=documents)

print(".....Done running pipeline.....")
