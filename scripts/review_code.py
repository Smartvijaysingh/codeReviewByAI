import requests
import os
from github import Github

# Set up your Azure OpenAI and GitHub credentials
openai_api_key = 'cbaaa9bee6704ec3b136c7927e58e4d5'
# openai_endpoint = 'https://usa-decision-azureai-openai.openai.azure.com/openai/deployments/gpt4-turbo/completions?api-version=2023-07-01-preview'
#openai_endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
openai_endpoint = 'https://sapiens-decision-openai.openai.azure.com/openai/deployments/Decision-GPT35/completions?api-version=2023-03-15-preview'

github_token = os.getenv('GITHUB_TOKEN')
pr_number = os.getenv('PR_NUMBER')

print(f"PR_NUMBER: {os.getenv('PR_NUMBER')}")
print(f"GITHUB_REPOSITORY: {os.getenv('GITHUB_REPOSITORY')}")
print(f"GITHUB_Token: {os.getenv('GITHUB_TOKEN')}")
# Replace with your pull request number


g = Github(github_token)
repo_name = os.getenv('GITHUB_REPOSITORY')
print(f"myTest: {g.get_repo(repo_name)}")
repo = g.get_repo(repo_name)  # Get the repository object
pr = repo.get_pull(int(pr_number))
files = pr.get_files()

def review_code(file_content):
    file_content = str(file_content)
    headers = {
        'Content-Type': 'application/json',
        'api-key': openai_api_key,
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an expert code reviewer."},
            {"role": "user", "content": f"Please review the following code:\n\n{file_content}"}
        ]
    }
    response = requests.post(openai_endpoint, headers=headers, json=data)
    print(f"response: {response}")
    if response.status_code != 200:
        print(f"Error: {response.content}")
        return "Error in processing the request."
    response_json = response.json()
    return response_json['choices'][0]['message']['content']


    # print("response_json: ", response_json)
    # choices = response_json.get('choices')
    #
    # if len(choices) > 0:
    #     return choices[0].get('text')
    # else:
    #     return "No review comments generated."

for file in files:
    if file.filename.endswith(('.java')):  # Add other file types as needed
        review_comments = review_code(file.patch)
        pr.create_issue_comment(f"**Review for {file.filename}:**\n\n{review_comments}")

print("Code review comments have been posted to the pull request.")
