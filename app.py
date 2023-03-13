import os
import openai
import gradio as gr

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are an AI specialized in Healthcare. Don't answer anything other than health and healthcare related questions."},
]


def predict(input):
    global messages
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        reply = [(messages[i]["content"], messages[i+1]["content"]) for i in range(1, len(messages)-1, 2)]
        return reply

with gr.Blocks(css="#chatbot .overflow-y-auto{height:700px}") as demo:
    demo.title="HealthcareLLM Chatbot"
    gr.Markdown("## FinanceLLM Chatbot demo")

    chatbot = gr.Chatbot(elem_id="chatbot", label="HealthcareLLM").style(container=False)
    # state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type a message and press enter").style(container=False)

    txt.submit(predict, txt, chatbot)
    # txt.submit(lambda: "", None, txt) # Pythonic way of clearing text after submit
    txt.submit(None, None, txt, _js="() => {''}") # Javascript way of clearing text after submit, faster than Pythonic way

demo.launch()
