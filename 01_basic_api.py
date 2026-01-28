"""
*
* Testing Gemini ai api 
* interact with the model inside terminal for query and rendered response
*
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

from rich.console import Console
from rich.markdown import Markdown


console=Console()

#load environment variable
load_dotenv()

#gonfigure the api
def setup_gemini():
    api_key=os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("please set api key in .env")
        print("get the key from the api")
        return
    genai.configure(api_key=api_key)
    print("api key configured succussfully")
    return genai

def simple_chat(prompt, model_name="deep-research-pro-preview-12-2025"):
    try:
        model=genai.GenerativeModel(model_name)
        response=model.generate_content(prompt)

        print(f"You asked {prompt}")
        print(f"{'*'*4}")

        md=Markdown(response.text)
        console.print(md)
        return response
    
    except Exception as e:
        print("error occured :",e)
        return 
    
if __name__=="__main__":
    print("====  google api testing  ====")

    genai=setup_gemini()
    if not genai:
        exit()
    
    print("available models")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"{m.name}")
    
    while True:
        user_input=input("am here to help,Ask me anything...   (Q) to exit \n")
        if user_input.lower()=='quit':
            break
        simple_chat(user_input)
