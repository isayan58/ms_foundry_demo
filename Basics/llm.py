from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
llm_endpoint = os.getenv("llm_endpoint")
endpoint = llm_endpoint
deployment_name = "gpt-5-mini"
api_key = os.getenv("API_KEY")

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.responses.create(
    model=deployment_name,
    input="What is the capital of France?",
)

print(f"answer: {response.output[0]}")
