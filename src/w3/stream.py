import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    base_url=os.environ.get("ANTHROPIC_BASE_URL"),
    api_key=os.environ["OPENCODE_API_KEY"],
)
model = os.environ.get("ANTHROPIC_MODEL")

messages = []

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
print(f"与 {model} 对话中（输入 exit 或 Ctrl+C 退出）")

while True:
    try:
        user_input = input("\n你: ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit"):
        break

    add_user_message(messages, user_input)

    with client.messages.stream(
        model=model,
        max_tokens=100000,
        messages=messages,
        system=system_prompt,
    ) as stream:
        print(f"AI: ")
        chunks = []
        for text in stream.text_stream:
            print(text, end="")
            chunks.append(text)

    add_assistant_message(messages, "".join(chunks))
