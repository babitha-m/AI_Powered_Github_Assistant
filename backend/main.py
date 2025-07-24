from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from urllib.parse import urlparse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request body schema
class IssueInput(BaseModel):
    repo_url: str
    issue_number: int

#Function to parse URL and get the details of the owner and repo
def parse_url(repo_url: str):
    """
    Extracts owner and repo name from a URL like https://github.com/facebook/react
    """
    path_parts = urlparse(repo_url).path.strip("/").split("/")
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]  # owner, repo
    return None, None

# Root endpoint to check if its working
@app.get("/")
async def root():
    return {"message": "GitHub Issue Assistant is running"}

# POST endpoint with correct body model
@app.post("/analyze_issue")
async def analyze_issue(payload: IssueInput):
    owner, repo = parse_url(payload.repo_url) #parsing url
    issue_number = payload.issue_number       #issune number is given directly

    if not owner or not repo:
        return {"error": "Invalid GitHub repository URL"}

    #Using GitHub API to fetch the data
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"    
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"

    async with httpx.AsyncClient() as client:
        issue_res = await client.get(issue_url)
        comments_res = await client.get(comments_url)

    if issue_res.status_code != 200:
        return {"error": f"Issue not found or error fetching issue: {issue_res.text}"}

    issue_data = issue_res.json()
    comments_data = comments_res.json()

    return {
        "title": issue_data.get("title"),
        "body": issue_data.get("body"),
        "comments": [c["body"] for c in comments_data],
    }