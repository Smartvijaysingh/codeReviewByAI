import requests
import os
from github import Github

# Set up your Azure OpenAI and GitHub credentials
openai_api_key = 'd06eb40c833a49a4829f079d1ddbfc14'
openai_endpoint = 'https://usa-decision-azureai-openai.openai.azure.com/'
github_token = os.getenv('GITHUB_TOKEN')
pr_number = os.getenv('PR_NUMBER')  # Replace with your pull request number


g = Github(github_token)
repo_name = os.getenv('GITHUB_REPOSITORY')
repo = g.get_repo(repo_name)  # Get the repository object
pr = repo.get_pull(int(pr_number))

def review_code(file_content):
    headers = {
        'Content-Type': 'application/json',
        'api-key': openai_api_key,
    }
    data = {
        "prompt": f"Please review the following code:\n\n{file_content}",
        "max_tokens": 2000,
        "temperature": 0.5,
        "stop": ["\n\n"]
    }
    response = requests.post(openai_endpoint, headers=headers, json=data)
    return response.json().get('choices')[0].get('text')

for file in files:
    if file.filename.endswith(('.py', '.js', '.java', '.go')):  # Add other file types as needed
        review_comments = review_code(file.patch)
        pr.create_issue_comment(f"**Review for {file.filename}:**\n\n{review_comments}")

print("Code review comments have been posted to the pull request.")
