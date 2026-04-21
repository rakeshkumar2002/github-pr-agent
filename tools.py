import requests, os

BASE = "https://api.github.com"

def _headers():
    """Build headers lazily so GITHUB_TOKEN is read after load_dotenv() runs."""
    return {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }

def list_prs(owner, repo):
    res = requests.get(f"{BASE}/repos/{owner}/{repo}/pulls", headers=_headers())
    if not res.ok:
        return {"error": res.status_code, "message": res.json().get("message", res.text)}
    prs = res.json()
    if not isinstance(prs, list):
        return {"error": "unexpected_response", "message": str(prs)}
    return [{"number": p["number"], "title": p["title"], "user": p["user"]["login"]} for p in prs]

def get_diff(owner, repo, pr_number):
    headers = {**_headers(), "Accept": "application/vnd.github.v3.diff"}
    res = requests.get(f"{BASE}/repos/{owner}/{repo}/pulls/{pr_number}", headers=headers)
    if not res.ok:
        return {"error": res.status_code, "message": res.text}
    return res.text[:8000]  # trim large diffs

def post_comment(owner, repo, pr_number, comment):
    print(f"\n📝 Proposed comment on PR #{pr_number}:\n")
    print(comment)
    confirm = input("\nPost this? (y/n): ")
    if confirm.lower() != "y":
        return {"status": "skipped", "message": "User declined to post"}
    res = requests.post(
        f"{BASE}/repos/{owner}/{repo}/issues/{pr_number}/comments",
        headers=_headers(),
        json={"body": comment}
    )
    if not res.ok:
        return {"error": res.status_code, "message": res.json().get("message", res.text)}
    return {"status": res.status_code, "url": res.json().get("html_url")}

def execute_tool(name, inputs):
    if name == "list_prs":     return list_prs(**inputs)
    if name == "get_diff":     return get_diff(**inputs)
    if name == "post_comment": return post_comment(**inputs)
    return {"error": f"Unknown tool: {name}"}
