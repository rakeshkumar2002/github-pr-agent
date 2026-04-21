# 🤖 GitHub PR Review Agent

An AI-powered agent that automatically reviews open GitHub Pull Requests — listing PRs, reading diffs, and posting detailed code review comments, all without human intervention.

Built using the **ReAct (Reasoning + Acting)** agentic pattern with OpenAI's tool-calling API and the GitHub REST API.

---

## ✨ How It Works

The agent follows a ReAct loop — it thinks, acts, observes, and repeats until the task is done:

```
[THINK]  "I need to list open PRs first"
[ACT]    → list_prs(owner, repo)
[OBS]    [{ number: 1, title: "feat: add typing animation..." }]

[THINK]  "Now I'll fetch the diff for PR #1"
[ACT]    → get_diff(owner, repo, pr_number=1)
[OBS]    <code diff>

[THINK]  "Now I'll post a review comment"
[ACT]    → post_comment(owner, repo, pr_number=1, comment="...")
[OBS]    { status: 201 }

[RESPOND] "Here's the review summary..."
```

---

## 🗂️ Project Structure

```
github-pr-agent/
├── main.py              # Entry point
├── agent.py             # ReAct agent loop (OpenAI tool-calling)
├── tools.py             # GitHub API functions (list, diff, comment)
├── tool_definitions.py  # OpenAI-compatible tool schemas
├── .env                 # API keys (never commit this!)
├── .gitignore
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM       | OpenAI GPT-4o / OpenRouter |
| Agent Pattern | ReAct (Reasoning + Acting) |
| GitHub Integration | GitHub REST API v3 |
| Env Management | python-dotenv |
| Language | Python 3.14 |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/github-pr-agent.git
cd github-pr-agent
```

### 2. Create a virtual environment

```bash
/opt/homebrew/bin/python3.14 -m venv ~/.venvs/github-pr-agent
~/.venvs/github-pr-agent/bin/pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=ghp_your_github_personal_access_token
OPENAI_API_KEY=sk-your_openai_or_openrouter_api_key
```

- **GitHub Token**: Generate at [github.com/settings/tokens](https://github.com/settings/tokens) with `repo` scope
- **OpenAI API Key**: Get from [platform.openai.com](https://platform.openai.com) or use [OpenRouter](https://openrouter.ai)

### 4. Configure the target repo

Edit `main.py` to point to your repository:

```python
run_agent("Review all open PRs in owner/repo-name")
```

### 5. Run the agent

```bash
~/.venvs/github-pr-agent/bin/python main.py
```

---

## 🔧 Tools Available

| Tool | Description |
|------|-------------|
| `list_prs` | Lists all open pull requests in a GitHub repo |
| `get_diff` | Fetches the code diff for a specific PR (trimmed to 8000 chars) |
| `post_comment` | Posts a review comment on a PR |

---

## 🧠 Agent Pattern: ReAct

This project implements the **ReAct** agent pattern — a loop where the LLM:
1. **Reasons** about the current state
2. **Acts** by calling a tool
3. **Observes** the result
4. **Repeats** until the task is complete (`stop_reason == "stop"`)

The core loop lives in `agent.py`:

```python
while True:
    response = client.chat.completions.create(...)

    if choice.finish_reason == "stop":
        print(choice.message.content)
        break

    if choice.finish_reason == "tool_calls":
        # execute tools and feed results back
        ...
```

---

## ⚙️ Configuration

### Switching Models

In `agent.py`, change the `model` parameter:

```python
# OpenAI
model="gpt-4o"

# OpenRouter (free tier)
model="meta-llama/llama-3.3-8b-instruct:free"
```

### Using OpenRouter

Update `agent.py` to point to OpenRouter's base URL:

```python
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
```

---

## 🔒 Security Notes

- **Never commit your `.env` file** — it's listed in `.gitignore`
- Rotate your GitHub token if it's ever exposed
- Use tokens with minimal required scopes (`repo` is sufficient)

---

## 📦 Dependencies

```
python-dotenv>=1.0.0
anthropic>=0.96.0
requests>=2.33.0
openai>=2.0.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 📄 License

MIT License — feel free to use, fork, and build on this project.
