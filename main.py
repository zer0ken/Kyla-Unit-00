import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory

if "GOOGLE_API_KEY" not in os.environ:
    load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

messages = [
    (
        "system",
        "You are a helpful assistant that can answer questions and help with tasks.",
    ),
    ("user", "What is the weather in Tokyo?"),
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)
