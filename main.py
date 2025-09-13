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



"""You’re almost there. Let me clarify the moving pieces in simple terms:

What are “tools” and “tool results” here?

Tools: the functions you expose to the model via config.tools (your available_functions from call_function.py). Examples: get_files_info, get_file_content, run_python, write_file_content.
Tool call: when the model returns a part with function_call=name+args.
Tool result: what your Python code returns after you actually execute that function_call via call_function(...). You must add that result back into messages so the model can see the outcome and decide the next step.
Concretely in your loop:

Model says “I want to call get_files_info” (function_call in response).
You run call_function(function_call_part, verbose) in Python.
That returns a types.Content with a function_response inside. You need to append a message to messages that represents the tool’s output so the next model turn has the data.
Right now you’re extracting only ['result'] into plaintext:
messages.append(Content(role='user', parts=[Part(text=...)]))
That’s acceptable for the lesson, but guard it so you don’t crash if the structure changes.

Guarding your function response (simple, robust check):

Your current line assumes parts[0].function_response.response['result'] always exists.
Safer:
Ensure parts exists and has index 0.
Ensure function_response and response exist.
Ensure 'result' key exists and is a string.
Example pattern (keep your current approach, just safer):

# python
tool_msg = function_call_result
res_text = None
try:
    fr = tool_msg.parts[0].function_response.response
    if isinstance(fr, dict):
        res_text = fr.get("result")
except Exception:
    res_text = None

if res_text:
    messages.append(types.Content(role="user", parts=[types.Part(text=res_text)]))
else:
    messages.append(types.Content(role="user", parts=[types.Part(text="Tool returned no result")]))

Verbose flag detail

re.search returns a match object or None, not a boolean. You’re overwriting verbose each loop iteration.
Make it a real bool:
verbose = any("--verbose" in arg for arg in sys.argv)

Why you saw “Final response” early

response.text concatenates only the text parts and ignores non-text parts. If the candidate contains both text and a function_call part, response.text will still be non-empty, so you printed and broke early before executing tools.
Fix: prioritize function calls when present. If response.function_calls exists and non-empty, handle them first, append tool results, then continue the loop without printing final text. Only when there are no function calls should you treat response.text as final.
Suggested control flow

Call generate_content
Append candidate.content to messages
If response.function_calls: run them, append tool results, continue
Else if response.text: print final response and break
Else: break
That prevents premature “Final response” when the model is in the middle of a tool plan.

Putting it together, adjust just the order and guards in your loop:

Check function_calls first.
Only print response.text when there are no function calls.
Try that change and re-run. If you hit 429, wait ~1 minute and retry."""