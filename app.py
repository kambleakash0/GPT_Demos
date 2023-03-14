import os
import openai
import gradio as gr

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are an helpful and kind AI Assistant."},
]


def predict(input, document=None):
    global messages
    if input:
        if document:
            with open(document.name, "r") as f:
                data = f.read()
            messages.append(
                {
                    "role": "system",
                    "content": "Read the given document and answer user's question. This is the document that user is referring to: {}".format(
                        data
                    ),
                }
            )
            messages.append({"role": "assistant", "content": "Ok. I have read the text."})

        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        if document:
            messages.pop(-3)
            messages.pop(-3)
        reply = [
            (messages[i]["content"], messages[i + 1]["content"])
            for i in range(1, len(messages) - 1, 2)
        ]
        return reply


with gr.Blocks(
    css=""" 
        footer { display: none !important; } 
        .gradio-container { min-height: 0px !important; } 
        #doc { height: 84px !important; } 
    """
) as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    # state = gr.State([])

    with gr.Row(elem_id="inputs"):
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Input text here and press Shift+Enter or click Send to get a response from the chatbot.",
                lines=3,
                elem_id="txt",
            ).style(container=False)
        with gr.Column(scale=0.15):
            doc = gr.File(type="file", show_label=False, elem_id="doc").style(
                container=False,
            )
    send_btn = gr.Button("Send", label="Send")
    send_btn.click(predict, [txt, doc], chatbot)
    send_btn.click(lambda: "", None, txt)  # Pythonic way of clearing text after submit
    txt.submit(predict, [txt, doc], chatbot)
    txt.submit(None, None, txt, _js="() => {''}") # Javascript way of clearing text after submit, faster than Pythonic way

demo.launch()
