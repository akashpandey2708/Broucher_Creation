import requests
import os
from dotenv import load_dotenv
load_dotenv('put the path of your env file here') 
API_KEY = os.getenv("API_KEY") 

class gptOss:
    def __init__(self):
        self.url="https://openrouter.ai/api/v1/chat/completions"
        self.headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
          }
        self.model="openai/gpt-oss-20b:free"

    def chat(self,system_prompt,user_prompt):
        data={
        "model": self.model,
        "messages": [{"role": "system", "content": system_prompt},
                 {"role": "user", "content": user_prompt}]
        }
        response = requests.post(url=self.url,headers=self.headers,json=data) 
        return response.json()["choices"][0]["message"]["content"]