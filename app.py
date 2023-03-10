import os
import openai
import gradio as gr

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are an AI specialized in Finance. Don't answer anything other than finance related questions."},
]


def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


inputs = gr.components.Textbox(lines=7, label="Chat with AI")
outputs = gr.components.Textbox(label="Reply")

gr.Interface(
    fn=chatbot,
    inputs=inputs,
    outputs=outputs,
    title="FinanceLLM Chatbot",
    description="Ask anything you want",
    allow_flagging="never",
).launch(share=False)
