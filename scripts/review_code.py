import os
import openai
import requests
from github import Github

# Set up your Azure OpenAI and GitHub credentials
openai.api_type = "azure"
openai.api_base = "https://sapiens-decision-openai.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = "42f7029b82624b29acae4e096991d80d"

github_token = os.getenv('GITHUB_TOKEN')
pr_number = os.getenv('PR_NUMBER')

# Debugging prints
print(f"PR_NUMBER: {pr_number}")
print(f"GITHUB_REPOSITORY: {os.getenv('GITHUB_REPOSITORY')}")
print(f"GITHUB_TOKEN: {github_token}")

# Initialize GitHub client
g = Github(github_token)
repo_name = os.getenv('GITHUB_REPOSITORY')
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_number))
files = pr.get_files()

def review_code(file_content):
    prompt = f"Review the following Java code changes and suggest improvements:\n\n{file_content}"
    try:
        response = openai.Completion.create(
            engine="Decision-GPT35",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1500,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {str(e)}")
        return "Error in processing the request."

for file in files:
    if file.filename.endswith('.java'):  # Add other file types as needed
        review_comments = review_code(file.patch)
        pr.create_issue_comment(f"**Review for {file.filename}:**\n\n{review_comments}")

print("Code review comments have been posted to the pull request.")
