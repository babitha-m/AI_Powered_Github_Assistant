import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_issue_analysis(title: str, body: str, comments: list[str]):
    prompt = f"""You are an expert GitHub issue assistant, the best in the industry. 
There are lots of issues on GitHub repos and it is important for you to understand the issues as a GitHub issue assistant.

Your task is to analyze a GitHub issue in depth and understand the core of the issue in order to come to a conclusion.

I want you to learn from the following examples:

Example 1:
{{
  "summary": "App crashes immediately on launch after updating to Android 14 on Pixel 7.",
  "type": "bug",
  "priority_score": "4 - Causes complete app failure on a major OS update affecting active users.",
  "suggested_labels": ["bug", "android", "crash"],
  "potential_impact": "Users on Android 14 cannot use the app at all unless reinstalling, leading to frustration and potential churn."
}}

Example 2:
{{
  "summary": "Silent crash occurs when dereferencing a nil pointer struct in Odin nightly builds.",
  "type": "bug",
  "priority_score": "3 - Causes unexpected program termination without error feedback, affecting dev experience.",
  "suggested_labels": ["bug", "crash", "nil-pointer"],
  "potential_impact": "Developers get no diagnostics on crashes, making debugging difficult and reducing confidence."
}}


I want you to read the issue that is structured as follows:
Here's a GitHub issue titled: "{title}"

Issue description:
{body}

Comments:
{chr(10).join(comments)}

Please analyze this properly and provide a JSON in the following format exactly:

{{
"summary": "A one-sentence summary of the user's problem or request.It should be concise and precisely describe the problem",
"type": "bug | feature_request | documentation | question | other. You can classify the issue into one of the categories according to what suits it",
"priority_score": "A score from 1 (low) to 5 (critical), with a brief but strong justification for the score. Provide a concise and clean reason",
"suggested_labels": ["An array of 2-3 relevant GitHub labels (e.g.'Bug','UI','login-flow')"],
"potential_impact": "A brief sentence on potential user impact if the issue is a bug."
}}

Ensure the output is valid JSON. Do not include any extra explanation. Only return the JSON.
Return the output clearly and concisely.
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful GitHub issue analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    #Parsing the JSON Content
    return json.loads(response.choices[0].message.content)
