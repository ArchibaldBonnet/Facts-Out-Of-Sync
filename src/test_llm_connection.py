import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["EURECOM_LLM_URL"],
    api_key=os.environ["EURECOM_LLM_KEY"],
)

response = client.chat.completions.create(
    model=os.environ["EURECOM_LLM_MODEL"],
    temperature=0,
    messages=[{"role": "user", "content": "Reply with exactly: connection ok"}],
)

print(response.choices[0].message.content)
