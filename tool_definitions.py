tools = [
    {
        "type": "function",
        "function": {
            "name": "list_prs",
            "description": "List open pull requests in a GitHub repo",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "GitHub repo owner/org name"},
                    "repo":  {"type": "string", "description": "GitHub repo name"}
                },
                "required": ["owner", "repo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_diff",
            "description": "Get the code diff for a specific PR",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner":     {"type": "string", "description": "GitHub repo owner/org name"},
                    "repo":      {"type": "string", "description": "GitHub repo name"},
                    "pr_number": {"type": "integer", "description": "PR number"}
                },
                "required": ["owner", "repo", "pr_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "post_comment",
            "description": "Post a review comment on a PR",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner":     {"type": "string", "description": "GitHub repo owner/org name"},
                    "repo":      {"type": "string", "description": "GitHub repo name"},
                    "pr_number": {"type": "integer", "description": "PR number"},
                    "comment":   {"type": "string", "description": "Review comment text"}
                },
                "required": ["owner", "repo", "pr_number", "comment"]
            }
        }
    }
]