import os
import requests
import openai

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

def review_code(diff):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = f"Review the following Java code changes and suggest improvements:\n\n{diff}"

    response = openai.ChatCompletion.create(
        model="text-davinci-004",    # Use GPT-4 model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    diff = get_diff()
    review = review_code(diff)
    print("### Code Review by GPT-4 ###")
    print(review)
