import streamlit as st
import requests
import json

# Set FastAPI backend URL
BACKEND_URL = "http://localhost:8000/analyze_issue"

st.set_page_config(page_title=" GitHub Issue Assistant", layout="centered")

st.title(" GitHub Issue Assistant")
st.write("Analyze GitHub issues using LLM-powered backend.")

# Input form
with st.form("issue_form"):
    repo_url = st.text_input(" GitHub Repository URL", placeholder="e.g., https://github.com/facebook/react")
    issue_number = st.number_input(" Issue Number", min_value=1, step=1)
    submit_button = st.form_submit_button("Analyze")

# When the form is submitted
if submit_button:
    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL.")
    else:
        with st.spinner("Analyzing issue..."):
            try:
                payload = {"repo_url": repo_url, "issue_number": issue_number}
                response = requests.post(BACKEND_URL, json=payload)
                data = response.json()

                if "error" in data:
                    st.error(f" Error: {data['error']}")
                else:
                    st.subheader(" LLM Analysis Summary")
                    
                    
                    llm_data = data["llm_analysis"]

                    st.markdown(f"**Summary:** {llm_data['summary']}")
                    st.markdown(f"**Type:** `{llm_data['type']}`")
                    st.markdown(f"**Priority Score:** {llm_data['priority_score']}")
                    st.markdown("**Suggested Labels:** " + ", ".join(f"`{label}`" for label in llm_data["suggested_labels"]))
                    st.markdown(f"**Potential Impact:** {llm_data['potential_impact']}")

                    with st.expander(" Raw Issue Content"):
                        st.markdown(f"**Title:** {data['title']}")
                        st.markdown(f"**Body:**\n{data['body']}")
                        if data["comments"]:
                            st.markdown("**Comments:**")
                            for comment in data["comments"]:
                                st.markdown(f"- {comment}")
                        else:
                            st.markdown("_No comments on this issue._")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
