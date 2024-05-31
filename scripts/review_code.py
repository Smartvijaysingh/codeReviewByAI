import os
import openai
from github import Github

openai.api_type = "azure"
openai.api_base = "https://sapiens-decision-openai.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = os.getenv('OPENAI_API_KEY')

github_token = os.getenv('GITHUB_TOKEN')
pr_number = os.getenv('PR_NUMBER')

g = Github(github_token)
repo_name = os.getenv('GITHUB_REPOSITORY')
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_number))
files = pr.get_files()

def review_code(file_content):
    prompt = f"Review the following Java code changes and suggest improvements with code if code changes requires:\n\n{file_content}"
    try:
        response = openai.ChatCompletion.create(
            engine="Decision-GPT35",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return "Error in processing the request."

for file in files:
    if file.filename.endswith('.java'):  # Add other file types as needed
        review_comments = review_code(file.patch)
        pr.create_issue_comment(f"**Review for {file.filename}:**\n\n{review_comments}")

print("Code review comments have been posted to the pull request.")
