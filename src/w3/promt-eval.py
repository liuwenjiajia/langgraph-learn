import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# .env 优先于已有环境变量：宿主环境（如 Claude 桌面应用）可能已设 ANTHROPIC_BASE_URL，不覆盖会把 key 发错端点
HERE = Path(__file__).resolve().parent  # 脚本所在目录，数据文件放这里，与运行时的工作目录无关
load_dotenv(HERE.parents[1] / ".env", override=True)

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

def chat(messages, system=None, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        # 不关闭时该模型先思考：耗尽 max_tokens、content[0] 变成 thinking 块，思考里的 ``` 还会误触发 stop_sequences
        "thinking": {"type": "disabled"},
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    response = client.messages.create(**params)
    return response.content[0].text

def generate_dataset():
    prompt = r"""
        Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

        Example output:
        ```json
            [
            \{
                "task": "Description of task",
            \},
            ...additional
            ]
        ```

        * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
        * Focus on tasks that do not require writing much code

        Please generate 3 objects.
        """
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)


## 运行生成测试数据时打开
# dataset = generate_dataset()
# print(dataset)
# with open(HERE / 'dataset.json', 'w') as f:
#     json.dump(dataset, f, indent=2)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output

def grade_by_model(test_case, output):
    # 创建评估提示
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {test_case['task']}
    Solution: {output}
    
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """
    
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)

def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)
    
    # TODO - 评分
    score = grade_by_model(test_case, output)
    
    return {
        "output": output,
        "test_case": test_case,
        "score": score["score"]
    }
    
def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    return results

with open(HERE / "dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
print(json.dumps(results, indent=2))