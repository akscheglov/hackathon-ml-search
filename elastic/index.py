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
Контекст: {context_str}. Назови заголовок, который суммирует все \
уникальные объекты, названия или темы, найденные в контексте. Будь краток и используй только русский язык. Заголовок: """,
        combine_template="""\
{context_str}. На основании вышеуказанных заголовков и контекста, \
каково полное название этого документа? Будь краток и используй только русский язык. Заголовок: """,
    ),
    SummaryExtractor(
        summaries=["self"],
        llm=llm,
        prompt_template="""\
Вот содержимое раздела:
{context_str}

Кратко изложи основные темы и сущности раздела. Для итогового резюме используй русский язык. \

Краткое содержание: """,
    ),
    KeywordExtractor(
        keywords=10,
        llm=llm,
        prompt_template="""\
Контекст: {context_str}. Приведи до {keywords} уникальных ключевых слов для приведенного контекста. \
В ответе используй только русский язык и выведи ключевые слова через запятую. Ключевые слова: """,
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

from config import VectorStoreType, vector_store_type

if vector_store_type == VectorStoreType.INMEMORY or vector_store_type == VectorStoreType.FAISS:
    vector_store.persist('./store_'+vector_store_type.name.lower())
