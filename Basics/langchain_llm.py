from langchain.chat_models import init_chat_model

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
llm_endpoint = os.getenv("llm_endpoint")
llm = init_chat_model(
    "openai:gpt-5-mini",
    api_key=os.getenv("API_KEY"),
    base_url=llm_endpoint,
)

print(llm.invoke("What is the capital of France?").content)