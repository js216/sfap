import requests
import sys
from pathlib import Path
import re

GREEN = "\033[32m"
RESET = "\033[0m"

LLAMA_API_URL = "http://localhost:8080/v1/chat/completions"

SYSTEM_PROMPT = """You are a datasheet specification extraction agent. Your
only job is to extract specifications.

OUTPUT FORMAT:
{
  "Full parameter name (short name)": {
    "min": number or null,
    "typ": number or null,
    "max": number or null,
    "unit": "string"
  }
}

EXTRACTION RULES:
- Always include both the full and short spec name in the key.
- Full name goes first, and short name in brackets: "Operating Temperature (T)"
- If a typ value is a range like "-11.5 to 14.5", split it: min=-11.5, max=14.5
- Convert scientific notation: "10 12" → 1e12
- Convert ± values into min/max fields
- Omit parameters with no numeric values (all null)
- Omit footnotes like (1) and (2)
- If no specifications exist, return: {}

CRITICAL OUTPUT RULES:
- Return ONLY valid JSON
- NO explanations
- NO descriptions
- NO phrases like "this section", "no specifications", "I will skip"
- NO text before or after the JSON
- NO markdown code blocks
- Just the raw JSON object
"""

def get_chunks(filepath):
    """Return a list of Markdown tables as strings from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to match GitHub-style tables
    table_pattern = re.compile(
        r"(?:^\|.*\|\s*\n)"           # Header row
        r"(?:^\|[-:\s|]+\|\s*\n)"     # Separator row
        r"(?:^\|.*\|\s*\n?)+",        # Body rows
        re.MULTILINE
    )

    tables = table_pattern.findall(content)
    return [t.strip() for t in tables]

def process_datasheet(filepath):
    """Process datasheet by sending chunks to LLM and printing results."""
    chunks = get_chunks(filepath)

    for i, chunk in enumerate(chunks):
        # Skip chunks with no numbers or tables
        if not any(char.isdigit() for char in chunk) and "|" not in chunk:
            continue

        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": chunk}
            ],
            "temperature": 0.0,
        }

        if sys.stdout.isatty():
            print(chunk)

        response = requests.post(LLAMA_API_URL, json=payload, timeout=240)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content'].strip()

        # Strip markdown code blocks if present
        content = re.sub(r'^```(?:json)?\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        content = content.strip()

        if sys.stdout.isatty():
            print(f"{GREEN}")
        print(f"{content}")
        if sys.stdout.isatty():
            print(f"{RESET}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 2_run_llama.py <file.md>")
        sys.exit(1)

    for arg in sys.argv[1:]:
        process_datasheet(arg)
