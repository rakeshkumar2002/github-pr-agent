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


SYSTEM = """You are a code review assistant. Your job is to catch objective issues only.

REVIEW FOR:
- Bugs: null checks, off-by-one errors, unhandled exceptions, race conditions
- Security: hardcoded secrets, SQL injection, unvalidated inputs
- Correctness: logic errors, wrong return types, broken error handling

DO NOT COMMENT ON:
- Code style or formatting (that's the linter's job)
- Naming choices unless genuinely confusing
- Architecture or design decisions
- Whether a different approach "would be better"
- Anything you're not confident about

TONE RULES:
- Never use words like "should", "must", "always", "never" for subjective points
- If uncertain, say "worth double-checking:" instead of stating it as fact
- One issue = one comment. Don't pile on.
- If the PR looks good, say so briefly. Don't invent issues.
"""

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