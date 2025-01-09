from core import vector_store, embed_model, llm
from documents import get_documents

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import SummaryExtractor, TitleExtractor, KeywordExtractor

transformations = [
    SentenceSplitter(chunk_size=256, chunk_overlap=5),
    TitleExtractor(
        nodes=5,
        llm=llm,
        node_template="""\
Context: {context_str}. Give a title that summarizes all of \
the unique entities, titles or themes found in the context. Use russian for resulting title. Title: """,
        combine_template="""\
{context_str}. Based on the above candidate titles and content, \
what is the comprehensive title for this document? Use russian for resulting title. Title: """,
    ),
    SummaryExtractor(
        summaries=["self"],
        llm=llm,
        prompt_template="""\
Here is the content of the section:
{context_str}

Summarize the key topics and entities of the section. Use russian for resulting summary. \

Summary: """,
    ),
    KeywordExtractor(
        keywords=10,
        llm=llm,
        prompt_template="""\
{context_str}. Give {keywords} unique keywords for this \
document. Format as comma separated. Use russian for resulting keywords. Keywords: """,
    ),
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
