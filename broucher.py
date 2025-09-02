import requests
import gradio as gr
import json
from bs4 import BeautifulSoup
from gptOss import gptOss
from qwen import qwen
import time

    
system_message = "You are an assistant that analyzes the contents of a company website landing page \
and creates a short brochure about the company for prospective customers, investors and recruits. Always Respond in markdown."

def gradio_gpt(user_input):
  return g.chat(system_message, user_input)

def gradio_qwen(user_input):
  return q.chat(system_message, user_input)

class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
  

def stream_brochure(company_name, url, model):
    yield "⏳ Generating your brochure, please wait..."

    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += Website(url).get_contents()

    if model == "GPT":
        result = g.chat(system_message, prompt)
    elif model == "Qwen":
        result = q.chat(system_message, prompt)
    else:
        raise ValueError("Unknown model")

    yield result


def main():
    global g, q
    g = gptOss()
    q = qwen()

    with gr.Blocks(title="AI Brochure Generator") as demo:
        gr.Markdown(
            """
            # 🧠 AI-Powered Company Brochure Generator
            Paste a landing page URL and choose a model to instantly generate a concise brochure for investors, customers, or new hires.
            """
        )

        with gr.Row():
            company_name = gr.Textbox(label="🏢 Company Name", placeholder="e.g. OpenAI", scale=1)
            url = gr.Textbox(label="🔗 Website URL", placeholder="https://www.example.com", scale=2)
        
        model = gr.Dropdown(["GPT", "Qwen"], label="🤖 Choose a Language Model")

        submit_btn = gr.Button("🚀 Generate Brochure")
        output = gr.Markdown(label="📄 Generated Brochure")

        submit_btn.click(
        fn=stream_brochure,
        inputs=[company_name, url, model],
        outputs=output)


    demo.launch(share=True, inbrowser=True)


if __name__ == "__main__":
    main()

