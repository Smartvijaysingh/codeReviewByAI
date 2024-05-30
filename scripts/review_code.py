import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_diff():
    pr_number = os.getenv('PR_NUMBER')
    repo = os.getenv('GITHUB_REPOSITORY')
    token = os.getenv('GITHUB_TOKEN')

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    files = response.json()

    diff = ""
    for file in files:
        filename = file['filename']
        patch = file.get('patch', '')
        diff += f"File: {filename}\n{patch}\n\n"
    return diff

def get_completion(prompt, client_instance, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = client_instance.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1500,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content']

def review_code(diff, client_instance):
    prompt = f"Review the following Java code changes and suggest improvements:\n\n{diff}"
    return get_completion(prompt, client_instance)

if __name__ == "__main__":
    diff = get_diff()
    review = review_code(diff, client)
    print("### Code Review by GPT-4 ###")
    print(review)
