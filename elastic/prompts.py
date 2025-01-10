from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType
from llama_index.core.base.base_query_engine import BaseQueryEngine

qa_prompt_tmpl = PromptTemplate(
    (
        "Тебе дана информация ниже.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Учитывая приведенную информацию, но не другие знания, "
        "ответь на вопрос.\n"
        "Будь краток и разговаривай на русском.\n"
        "Вопрос: {query_str}\n"
        "Ответ: "
    ),
    prompt_type=PromptType.QUESTION_ANSWER
)

refine_template = PromptTemplate(
    (
        "Исходный запрос выглядит следующим образом: {query_str}\n"
        "Мы предоставили существующий ответ: {existing_answer}\n"
        "У нас есть возможность уточнить существующий ответ "
        "(только при необходимости), добавив дополнительный контекст ниже.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Учитывая новый контекст, уточни исходный ответ, чтобы лучше "
        "ответить на запрос. "
        "Если контекст бесполезен, верните исходный ответ."
        "При ответе раговаривай только на руссом.\n"
        "Уточненный ответ: "
    ),
    prompt_type=PromptType.REFINE
)

def update_prompts(query_engine: BaseQueryEngine):
    query_engine.update_prompts(
        {
            "response_synthesizer:text_qa_template": qa_prompt_tmpl,
            "response_synthesizer:refine_template": refine_template,
        },
    )
