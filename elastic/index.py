from core import vector_store, embed_model, llm
from documents import get_documents

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import SummaryExtractor, TitleExtractor, KeywordExtractor

transformations = [
    SentenceSplitter(chunk_size=256, chunk_overlap=5),
    TitleExtractor(nodes=5, llm=llm),
    SummaryExtractor(summaries=["prev", "self"], llm=llm),
    KeywordExtractor(keywords=10, llm=llm),
    embed_model,
]

# LlamaIndex Pipeline configured to take care of chunking, embedding
# and storing the embeddings in the vector store.
pipeline = IngestionPipeline(
    transformations=transformations,
    vector_store=vector_store,
)

documents = get_documents()

print(".....Starting pipeline.....")

pipeline.run(show_progress=True, documents=documents)

print(".....Done running pipeline.....")
