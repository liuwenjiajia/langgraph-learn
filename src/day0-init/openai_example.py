import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL"),
    api_key=os.environ["OPENAI_API_KEY"],
)
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

messages = []
print(f"与 {model} 对话中(输入 exit 或 Ctrl+C 退出)")

while True:
    try:
        user_input = input("你: ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    reply = response.choices[0].message.content
    print(f"AI: {reply}")
    messages.append({"role": "assistant", "content": reply})
