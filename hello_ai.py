import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Call LLM with a prompt

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Be concise and provide clear answers."},
            {"role": "user", "content": "What is generative AI in one sentence?"}
        ],
        temperature=0.7,
        max_tokens=100
    )

    # response

    print(f"Response: {response.choices[0].message.content}")
    print(f"Total tokens used: {response.usage.total_tokens}")

except AuthenticationError as e:
    print(f"Authentication error: {e}. Check your API key.")
except APIConnectionError as e:
    print(f"API connection error: {e}. Check your internet connection or the OpenAI service status.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")