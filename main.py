import os, sys, re

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

try:
    input = sys.argv[1]
except IndexError:
    sys.exit(1)

match = False
for i in sys.argv:
    match = re.search(r"\-\-verbose", i)
messages = [# To be used Later to store the entire conversation with the LLM
    types.Content(role="user", parts=[types.Part(text=input)]),
]
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
print(response.text)
x = response.usage_metadata.prompt_token_count
y = response.usage_metadata.candidates_token_count
if match:
    print(f"User prompt: {input}")
    print(f"Prompt tokens: {x}\nResponse tokens: {y}")