
from datetime import datetime
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from anthropic.types import ToolParam
from anthropic.types import Message

# .env 优先于已有环境变量：宿主环境（如 Claude 桌面应用）可能已设 ANTHROPIC_BASE_URL，不覆盖会把 key 发错端点
HERE = Path(__file__).resolve().parent  # 脚本所在目录，数据文件放这里，与运行时的工作目录无关
load_dotenv(HERE.parents[1] / ".env", override=True)

client = anthropic.Anthropic(
    base_url=os.environ.get("ANTHROPIC_BASE_URL"),
    api_key=os.environ["OPENCODE_API_KEY"],
)
model = os.environ.get("ANTHROPIC_MODEL")

messages = []


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)

def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant", 
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)


def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
        # 不关闭时该模型先思考：耗尽 max_tokens、content[0] 变成 thinking 块，思考里的 ``` 还会误触发 stop_sequences
        "thinking": {"type": "disabled"},
    }
    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system
        
    message = client.messages.create(**params)
    return message

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

def run_conversation(messages):
    while True:
        response = chat(messages)

        add_assistant_message(messages, response)

        # 伪代码
        if response.stop_reason != "tool_use":
            break

        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)
        
    return messages

def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []
    
    for tool_request in tool_requests:
        if tool_request.tool_name == "get_current_datetime":
            return get_current_datetime(**tool_request.tool_input)
