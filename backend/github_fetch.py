import httpx

async def fetch_github_issue(owner: str, repo: str, issue_number: int, token: str = None):
    #Using Github API to fetch deets
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    # Optional Authorization header
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as http_client:
        issue_res = await http_client.get(issue_url)
        comments_res = await http_client.get(comments_url)

    if issue_res.status_code != 200:
        raise ValueError(f"Issue fetch failed: {issue_res.text}")

    return issue_res.json(), comments_res.json()
