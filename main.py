import os, sys, re

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        input = sys.argv[1]
    except IndexError:
        sys.exit(1)

    verbose = False
    for i in sys.argv:
        verbose = re.search(r"\-\-verbose", i)
    messages = [# To be used Later to store the entire conversation with the LLM
        types.Content(role="user", parts=[types.Part(text=input)]),
    ]
    try:
        for i in range(20):
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    ),
                )
            if response.candidates:
                print(response.candidates)
                for candidate in response.candidates:
                    messages.append(candidate.content)
            if response.text:
                print("Final response:")
                print(response.text)
                break
            elif response.function_calls:
                print(response.function_calls)
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    if function_call_result.parts[0].function_response.response:
                        messages.append(types.Content(role='user', parts=[types.Part(text=function_call_result.parts[0].function_response.response['result'])]))
                    else:
                        raise Exception("Error: Fatal error when calling function.")
            else:
                break
        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(f"Error: Fatal error as {e}")

if __name__ == "__main__":
    main()