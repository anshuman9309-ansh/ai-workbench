"""
Prompt engineering experiment module.
Demonstrates: how promot shapes respones, temperature, and other parameters affect the output of a language model.

Run individual experiments:

python prompt_experiment.py 1 # Specificity only
python prompt_experiment.py 2 # Persona only
python prompt_experiment.py 1 # Format only
python prompt_experiment.py 1 # Temperature only
python prompt_experiment.py # All experiements combined

"""

import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SAMPLE_TEXT = """Generative artificial intelligence (generative AI) is a type of AI that can create new content 
and ideas, including conversations, stories, images, videos, and music. It can learn human language, 
programming languages, art, chemistry, biology, or any complex subject matter. It reuses what it knows to solve
new problems. For example, it can learn English vocabulary and create a poem from the words it processes. Your 
organization can use generative AI for various purposes, like chatbots, media creation, product development, and 
design.""".strip()

total_tokens = 0
total_calls = 0

def call_llm(prompt: str, temperature: float = 0.7) -> tuple[str, int]:
    global total_tokens, total_calls
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=300
        )
        total_calls += 1
        tokens = response.usage.total_tokens
        total_tokens += tokens

        end = time.time()
        text = response.choices[0].message.content
        print(f"  [{tokens} tokens, {end - start:.1f} seconds")
        return text, tokens
    
    except AuthenticationError as e:
        print(f"Authentication error: {e}. Check your API key.")
    except APIConnectionError as e:
        print(f"API connection error: {e}. Check your internet connection or the OpenAI service status.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def experiment_specificity():
    """Variable 1: Instruction specificity (vague -> precise)"""
    print("\n" + "=" * 60)
    print("Experiment 1: Instruction Specificity")
    print("Question: How does prompt precision affect output quality?")
    print("=" * 60)

    levels = [
        ("Vague", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("Specific", f"Summarize this text in exactly 3 bullet points:\n{SAMPLE_TEXT}"),
        ("Highly Specific", f"Summarize this text in 3 bullet points, each under 15 bullet points, foucssing only on business impact:\n{SAMPLE_TEXT}")
    ]

    for level, prompt in levels:
        print(f"\n---Level: {level} ---")
        print(f"  Prompt: {prompt}")
        result, tokens = call_llm(prompt)
        print(f"  Output:\n{result}")

def experiment_persona():
    """Variable 2: Instruction Persona/audience (general -> expert)"""
    print("\n" + "=" * 60)
    print("Experiment 2: Instruction Persona")
    print("Question: How does the target audienece change the output?")
    print("=" * 60)

    personas = [
        ("General Audience", f"Explain generative AI to a general audience in simple terms:\n{SAMPLE_TEXT}"),
        ("Technical Audience", f"Explain generative AI to a technical audience, including key algorithms and models:\n{SAMPLE_TEXT}"),
        ("Business Audience", f"Explain generative AI to a business audience, focusing on ROI and market impact:\n{SAMPLE_TEXT}")
    ]
    for persona, prompt in personas:
        print(f"\n---Persona: {persona} ---")
        print(f"  Prompt: {prompt}")
        result, tokens = call_llm(prompt)
        print(f"  Output:\n{result}")   

def experiment_format():
    """Variable 3: Output format(free text -> structured)"""
    print("\n" + "=" * 60)
    print("Experiment 3: Output Format control")
    print("Question: Can you control the structure of AI output?")
    print("=" * 60)

    formats = [
        ("Free Text", f"Explain generative AI in your own words:\n{SAMPLE_TEXT}"),
        ("JSON", f"Explain generative AI in JSON format with specific keys:\n{SAMPLE_TEXT}"),
        ("Markdown Table", f"Explain generative AI in a markdowntable format with columns: Theme | Key Points | Impact:\n{SAMPLE_TEXT}")    
    ]
    for format_type, prompt in formats:
        print(f"\n---Format: {format_type} ---")
        print(f"  Prompt: {prompt}")
        result, tokens = call_llm(prompt)
        print(f"  Output:\n{result}")   

def experiment_temperature():
    """Variable 4: Temperature (creativity)"""
    print("\n" + "=" * 60)
    print("Experiment 4: Temperature")
    print("Question: How does the temperature setting affect the creativity of the output?")
    print("=" * 60)

    prompt = f"Explain generative AI in a creative way:\n{SAMPLE_TEXT}"
    temperatures = [ 0.0, 0.7, 1.0 ]

    for temp_level in temperatures:
        print(f"\n---Temperature: {temp_level} ---")
        print(f"  Prompt: {prompt}")
        print(f"  Running the same prompt twice to compare consistency...")

        results = []
        for i in range(2):
            result, tokens = call_llm(prompt, temperature=temp_level)
            results.append(result)
            print(f"  Run {i+1} Output:\n{result}")

        if results[0] == results[1]:
            print("  The outputs are identical, indicating low creativity.")
        else:
            print("  The outputs differ, indicating higher creativity.")

def print_summary():
    """Print experiment summary with total usage."""
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE — Summary")
    print("=" * 60)
    print(f"  Total API calls made: {total_calls}")
    print(f"  Total tokens used:    {total_tokens}")
    print(f"  Estimated cost:       ${total_tokens * 0.00000015:.4f} (approx)")
    print()
    print("  Key Findings:")
    print("  1. SPECIFICITY: More precise prompts → more useful outputs")
    print("  2. PERSONA: Audience framing changes vocabulary and depth")
    print("  3. FORMAT: LLMs can output structured data (JSON, tables)")
    print("  4. TEMPERATURE: Controls randomness vs consistency")
    print()
    print("  → The prompt IS the program. Master prompts = master AI.")
    print("=" * 60)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set. See .env.example")
        sys.exit(1)

    print("=" * 60)
    print("Lab 1B: Prompt Engineering Experiment")
    print(f"Model: {MODEL}")
    print(f"Sample text: {len(SAMPLE_TEXT)} chars")
    print("=" * 60)

    experiments = {
        "1": experiment_specificity,
        "2": experiment_persona,
        "3": experiment_format,
        "4": experiment_temperature,
    }

    if len(sys.argv) > 1 and sys.argv[1] in experiments:
        experiments[sys.argv[1]]()
    else:
        for exp in experiments.values():
            exp()

    print_summary()

