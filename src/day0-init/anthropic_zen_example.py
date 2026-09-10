import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://opencode.ai/zen/v1"),
    api_key=os.environ["OPENCODE_API_KEY"],
)
model = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")

messages = []
print(f"与 {model} 对话中（输入 exit 或 Ctrl+C 退出）")

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

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=messages,
    )

    reply = "".join(block.text for block in response.content if block.type == "text")
    print(f"AI: {reply}")
    messages.append({"role": "assistant", "content": reply})
