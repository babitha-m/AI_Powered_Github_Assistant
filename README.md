# AI_Powered_Github_Assistant
This system acts as a Github Issue assistant and provides a summarised issue analysis given the repo and the issue number.
Major Components:
1.  LLM-Powered Backend (FastAPI)
Purpose: Acts as the core engine that fetches, processes, and analyzes GitHub issue data.

Key Files:

main.py: Exposes a FastAPI endpoint (/analyze_issue) that takes repo URL, issue number, and optional token.

github_fetch.py: Fetches issue title, body, and comments from GitHub using httpx.

llm_parser.py: Sends the combined text to OpenAI to generate a structured summary in the form of json.

2.  Frontend UI (Streamlit)
Purpose: Simple user interface for entering GitHub repo name and issue number and viewing AI-generated output.

Key Features:

Input fields: repo URL, issue number, and optional GitHub token.

Submit button with loading spinner animation.

Displays AI-generated output in JSON-like code block.

File: frontend/app.py

3. API Communication
Streamlit frontend sends a POST request to FastAPI backend using httpx.

Backend processes the issue and returns a response.