import os
from github import Github
from google import genai

gh = Github(os.environ["GITHUB_TOKEN"])
ai = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

repo = gh.get_repo(os.environ["REPO_NAME"])
pr = repo.get_pull(int(os.environ["PR_NUMBER"]))

code_changes = ""
for file in pr.get_files():
    code_changes += f"\nFile: {file.filename}\nChanges:\n{file.patch}\n"

prompt = f"""
You are an automated DevOps & Code Review Agent. Analyze this Pull Request:
Title: {pr.title}
Code Diff:
{code_changes}

Give a clear, short review with:
1. **Triage Category:** (Bug Fix / New Feature / Security Risk)
2. **Bugs & Security Check:** Point out any mistakes or leaked passwords.
3. **Action Needed:** Safe to merge, or needs fixes?
"""

response = ai.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

pr.create_issue_comment(f"🤖 **AutoDev AI Agent Review:**\n\n{response.text}")
