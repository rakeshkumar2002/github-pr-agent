import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from tools import execute_tool
from tool_definitions import tools

load_dotenv()  # Must be called before OpenAI() reads OPENAI_API_KEY
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM = """You are a code review agent. When asked to review PRs:
1. List open PRs first
2. Get the diff for each PR
3. Analyze code quality, bugs, style issues
4. Post a constructive review comment
Be concise and specific in reviews."""

def run_agent(user_message):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.chat.completions.create(
            model="openrouter/free",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        choice = response.choices[0]

        # Append assistant response
        messages.append(choice.message)

        if choice.finish_reason == "stop":
            # Extract final text
            if choice.message.content:
                print("\nAgent:", choice.message.content)
            break

        if choice.finish_reason == "tool_calls":
            for tool_call in choice.message.tool_calls:
                func = tool_call.function
                args = json.loads(func.arguments)
                print(f"  → Calling {func.name}({args})")
                result = execute_tool(func.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })