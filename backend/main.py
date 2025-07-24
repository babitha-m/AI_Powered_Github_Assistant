from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse

from github_fetch import fetch_github_issue
from llm_parser import generate_issue_analysis

#Web Server using FastAPI
app = FastAPI()

#Middleware for communication between backend and frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Request Body Schema
class IssueInput(BaseModel):
    repo_url: str
    issue_number: int

#Parsing the URL
def parse_url(repo_url: str):
    path_parts = urlparse(repo_url).path.strip("/").split("/")
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    return None, None

#Checking if its woriking
@app.get("/")
async def root():
    return {"message": "GitHub Issue Assistant is running"}

#Triggering analysis
@app.post("/analyze_issue")
async def analyze_issue(payload: IssueInput):
    owner, repo = parse_url(payload.repo_url)  #Getting owner and repo details from url
    if not owner or not repo:
        return {"error": "Invalid GitHub repository URL"}

    try:
        issue_data, comments_data = await fetch_github_issue(owner, repo, payload.issue_number)
    except ValueError as e:
        return {"error": str(e)}

    title = issue_data.get("title", "")
    body = issue_data.get("body", "")
    comments = [comment.get("body", "") for comment in comments_data]

    llm_analysis = await generate_issue_analysis(title, body, comments)

    return {
        "title": title,
        "body": body,
        "comments": comments,
        "llm_analysis": llm_analysis,
    }
