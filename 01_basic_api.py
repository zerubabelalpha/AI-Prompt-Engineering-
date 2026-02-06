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


console = Console()

# load environment variable
load_dotenv()

# Configure the model

def setup_model():

    api_key=os.getenv("API_KEY")

    if not api_key:
        print("please setup api key inside .env")
        return
    
    client = OpenAI(
                    base_url = "https://openrouter.ai/api/v1",
                    api_key = api_key,
                    )
    return client



def simple_chat(client, prompt,model_name="arcee-ai/trinity-mini:free"):

    try:
        response =  client.responses.create(
        model=model_name,
        input=prompt
        )

        reply = response.output_text or "_(No response)_"
        
        #print("AI :",reply)

        md=Markdown(reply)
        console.print(md)
        print()

        return reply



    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None


## 
#
# trying with diferent model parameters
#
##


def generate_with_parameters(client, prompt, temp, max_token, model_name="arcee-ai/trinity-mini:free"):

    try:

        response = client.responses.create(
            model=model_name,
            input=prompt,
            temperature = temp,
            max_output_tokens = max_token
        )

        reply = response.output_text or "_(No response)_"
        
        #print("AI :",reply)

        md=Markdown(reply)
        console.print(md)
        print()

        return reply


    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None



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
        generate_with_parameters(client, user_input, 0, 5000)