#  AI-Powered GitHub Issue Assistant

This project analyzes GitHub issues using OpenAI's language models to generate structured summaries, helping developers quickly understand and triage issues.

---

##  Features

-  Analyzes GitHub issues using LLMs
-  Returns structured JSON summaries (summary, type, priority, labels, impact)
-  Simple Streamlit UI for input and visualization
-  Supports optional GitHub token for private repositories

---

##  Architecture Overview

### 1. **Backend (FastAPI + OpenAI)**
Handles core logic: fetches GitHub issue data, processes it using OpenAI, and returns structured output.

- **`main.py`** – FastAPI endpoint: `/analyze_issue`
- **`github_fetch.py`** – Fetches issue title, body, and comments
- **`llm_parser.py`** – Sends content to OpenAI and parses the response

### 2. **Frontend (Streamlit)**
User-facing interface to input GitHub repo info and view AI-generated summaries.

- **`frontend/app.py`**
  - Inputs: GitHub repo URL, issue number, optional token
  - Loading spinner during analysis
  - JSON-style output display

### 3. **API Communication**
- Streamlit sends a `POST` request to the FastAPI server
- FastAPI:
  - Fetches the issue + comments
  - Sends to OpenAI
  - Returns structured analysis

---

##  Installation & Running Locally
Follow these steps to run the AI-Powered GitHub Issue Assistant on your local machine:
### 1. Clone the Repository

```bash
git clone https://github.com/babitha-m/AI_Powered_Github_Assistant.git
cd AI_Powered_Github_Assistant
```

###  2. Install the required Python packages:
```bash pip install -r requirements.txt ```

### 3. Create a .env file in the root directory and add your OpenAI API key:
```bash OPENAI_API_KEY=your_openai_api_key_here ```
 You can optionally provide a GitHub personal access token in the UI for accessing private repositories. 

### 4. Start the backend server using Uvicorn:
```bash 
cd backend
uvicorn main:app --reload

The API will be available at: http://127.0.0.1:8000

Explore the API via Swagger UI: http://127.0.0.1:8000/docs
```

### 5. Run the Streamlit Frontend
In a new terminal, navigate to the frontend directory and launch the app:
```bash 
cd frontend
streamlit run app.py
```
### 🔧 Prerequisites

- Python 3.10+
- OpenAI API Key
- GitHub token (optional, for private repos)

