import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_issue_analysis(title: str, body: str, comments: list[str]):
    prompt = f"""You are an expert GitHub issue assistant, the best in the industry. 
    Yout task is to

Here's a GitHub issue titled: "{title}"

Issue description:
{body}

Comments:
{chr(10).join(comments)}

Please analyze this and provide:

a JSON in the following format exactly:

{{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "A score from 1 (low) to 5 (critical), with a brief justification.",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "A brief sentence on potential user impact if it's a bug."
}}

Ensure the output is valid JSON. Do not include any extra explanation. Only return the JSON.
Return the output clearly and concisely.
"""

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful GitHub issue analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content
