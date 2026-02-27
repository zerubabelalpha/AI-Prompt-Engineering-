"""
*
* Testing ai model from openrouter 
* interact with the model inside terminal for query and rendered response
*
"""
from openai import OpenAI
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import json
# import requests
# from bs4 import BeautifulSoup
import re
import os 
import subprocess

WORKSPACE = "agent_workspace"

if not os.path.exists(WORKSPACE):
    os.mkdir(WORKSPACE)

console = Console()

conversation_history =[]
PROMPT_TEMPLATE = """
Task:
{task}
if the task is releted to coding follow the instructions.
Instructions:
Assume you are proessional software engineer, which builds project in organied, simplified and consise way.
1. provide the idea in organized and structured way,
2. provide file structure
3. generate task and implementation plan for the project
4. implement the tasks according to the implementation plan that you provided.
5. write and provide a command for the test cases.
6. provide a setup.md file which help the user to understand and execute the project in his machine.
"""
# load environment variable
load_dotenv()

# Configure the model

def setup_model():

    API_KEY=os.getenv("API_KEY")

    if not API_KEY:
        print("please setup api key inside .env")
        return
    
    client = OpenAI(
                    base_url = "https://openrouter.ai/api/v1",
                    api_key = API_KEY,
                    )
    return client

def simple_chat(client, prompt,model_name="arcee-ai/trinity-large-preview:free", show_output=True):

    try:
        response =  client.responses.create(
        model=model_name,
        input=prompt
        )

        reply = response.output_text or "_(No response)_"
        
        #print("AI :",reply)

        if show_output:

            md=Markdown(reply)
            console.print(md)
            print()

        return reply

    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None

def generate_with_parameters(
        client,   
        temp, 
        max_token,
        template, 
        model_name="arcee-ai/trinity-large-preview:free",
        role="user",
        **kwargs
        ):

    try:

        try:
            prompt = template.format(**kwargs)
        except KeyError as e:
            console.print(f"[bold red]Template missing variable:[/bold red] {e}")
            return None
        
        conversation_history.append({
            'role':role,
            'content': prompt
        })

        MAX_HISTORY = 20
        if len(conversation_history) > MAX_HISTORY:
            conversation_history[:] = conversation_history[-MAX_HISTORY:]

        stream = client.responses.create(
            model=model_name,
            input=conversation_history,
            temperature = temp,
            max_output_tokens = max_token,
            stream=True
        )

        full_reply=""


        for event in stream:
            if event.type == "response.output_text.delta":
                delta = event.delta
                full_reply += delta
                print(delta, end="", flush=True)

        print("\n")
        
         # Save assistant reply to memory
        conversation_history.append({
            "role": role,
            "content": full_reply
        })
        return full_reply


    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None   

def calculator(expression:str)->str:
    try:
        allowed_chars = "1234567890-+*/. "  # there is no factorial in the allowed chars
        if any(c not in allowed_chars for c in expression):
            return "Error: invalid chars in expression."
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
""""def web_search(query:str)->str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.google.com/search?q={query}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
        if results:
            print(f"search results: {results[0].get_text()}")

            return results[0].get_text()
        
        return "no results found"

    except Exception as e:
        return f"Error: {e}"""""
  
def execute_python(code):
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        return f"Error: {e}"
    
def file_write(filename, content):
    try:
        workspace_path = os.path.abspath(WORKSPACE)
        file_path = os.path.abspath(os.path.join(workspace_path, filename))

        if not file_path.startswith(workspace_path):
            return "Error: invalid file path."
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"file: {filename} written successfuly.\nContent:\n{content}"
    except Exception as e:
        return f"Error: {e}"
    
def file_read(filename):
    try:
        workspace_path = os.path.abspath(WORKSPACE)
        file_path = os.path.abspath(os.path.join(workspace_path, filename))

        if not file_path.startswith(workspace_path):
            return "Error: Invalid file path."

        if not os.path.exists(file_path):
            return f"file: {file_path} dosnt exixt"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"
    
def code_tester(filename):
    try:
        workspace_path = os.path.abspath(WORKSPACE)
        file_path = os.path.abspath(os.path.join(workspace_path, filename))

        if not file_path.startswith(workspace_path):
            return "Error: Invalid file path."

        if not os.path.exists(file_path):
            return f"Error: File '{filename}' not found."

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.stderr:
            return f"Execution Error:\n{result.stderr}"

        return f"Execution Output:\n{result.stdout}"

    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out."
    except Exception as e:
        return f"Error running code: {e}"
    
TOOLS = {
    "calculator": calculator,
    # "web_search": web_search,
    "code_executor": execute_python,
    "file_write": file_write,
    "file_read": file_read,
    "code_tester": code_tester,
}

def agentic_ai(client, task, max_steps=10):

    system_prompt = """
    You are an AI coding agent.

    You can use tools to complete the task.

    Available tools:
    - calculator(expression)
    - code_executor(code)
    - file_write(filename, content)
    - file_read(filename)
    - code_tester(filename)

    RULES:
    1. If a tool is needed, respond ONLY in JSON:
    {"tool": "tool_name", "input": value}

    2. For file_write use:
    {"tool": "file_write", 
        "input": {"filename": "name.py", "content": "file content here"}}

    3. If the task is complete, respond with:
    {"final": "your final answer here"}

    Do NOT explain anything outside JSON.
    """

    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task}
    ]

    for step in range(max_steps):

        response = client.responses.create(
            model="arcee-ai/trinity-large-preview:free",
            input=conversation
        )

        reply = response.output_text.strip()
        print(f"\nStep {step+1} RAW MODEL OUTPUT:\n{reply}\n")

        
        match = re.search(r'\{.*\}', reply, re.DOTALL)
        if not match:
            return "Failed to parse JSON from model."

        try:
            action = json.loads(match.group())
        except Exception:
            return "JSON parsing failed."

        
        if "final" in action:
            return action["final"]

        
        tool_name = action.get("tool")
        tool_input = action.get("input")

        if tool_name not in TOOLS:
            return f"Unknown tool: {tool_name}"

        try:
            if tool_name == "file_write":
                result = file_write(
                    tool_input["filename"],
                    tool_input["content"]
                )
            else:
                result = TOOLS[tool_name](tool_input)
        except Exception as e:
            result = f"Tool execution error: {e}"

        print(f"Tool Result:\n{result}\n")

        
        conversation.append({"role": "assistant", "content": reply})
        conversation.append({
            "role": "system",
            "content": f"Tool result:\n{result}"
        })

    return "Max steps reached without final answer."


if __name__=="__main__":
    console.print("[bold cyan]==== Model Testing ==== [/bold cyan]\n")

    client = setup_model()
    if not client:
        exit(1)


    while True:
        user_input = input("Ask me anything...  (quit to exit).\n> ")
        if user_input.lower()=='quit':
            break
        #simple_chat(client, user_input)
        # generate_with_parameters(
        #     client, 
        #     temp=0.7, 
        #     max_token=5000, 
        #     template=PROMPT_TEMPLATE, 
        #     role="developer", 
        #     task=user_input)
        final_output = agentic_ai(client, user_input)
        console.print(f"Finl output:\n{final_output}")

        

