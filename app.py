import os
import openai
import gradio as gr

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are an helpful and kind AI Assistant."},
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

css = "footer {display: none !important;} .gradio-container {min-height: 0px !important;}"

with gr.Blocks(css=css) as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    # state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)

    txt.submit(predict, txt, chatbot)
    # txt.submit(lambda: "", None, txt) # Pythonic way of clearing text after submit
    txt.submit(None, None, txt, _js="() => {''}") # Javascript way of clearing text after submit, faster than Pythonic way

demo.launch()
