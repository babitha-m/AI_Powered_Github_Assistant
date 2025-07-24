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


# Root endpoint
@app.get("/")
async def root():
    return {"message": "GitHub Issue Assistant is running"}

# POST endpoint with correct body model
@app.post("/analyze_issue")
async def analyze_issue(payload: IssueInput):
    repo_url = payload.repo_url
    issue_number = payload.issue_number

    return {
        "summary": "This is a placeholder summary.",
        "type": "feature_request",
        "priority_score": "3 - Seems moderately urgent.",
        "suggested_labels": ["enhancement", "API"],
        "potential_impact": "Users may face limited functionality."
    }
