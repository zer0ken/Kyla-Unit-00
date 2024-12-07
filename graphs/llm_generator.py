from langchain_groq import ChatGroq
from langchain_together import ChatTogether
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)


def generate_llm(**kwargs):
    default_kwargs = {
        'model': 'gemini-1.5-flash',
        'temperature': 0.7,
        'max_tokens': None,
        'timeout': None,
        'max_retries': 2,
        'safety_settings': {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
        }
    }
    return ChatGoogleGenerativeAI(
        **{**default_kwargs, **kwargs}
    )


def generate_groq_llm(**kwargs):
    default_kwargs = {
        'model': 'llama3-8b-8192',
        'temperature': 0.3,
        'max_tokens': None,
        'timeout': None,
        'max_retries': 2,
    }
    return ChatGroq(
        **{**default_kwargs, **kwargs}
    )


def generate_together_llm(**kwargs):
    default_kwargs = {
        'model': 'meta-llama/Meta-Llama-3.1-8B-Instruct',
    }
    return ChatTogether(**{**default_kwargs, **kwargs})

