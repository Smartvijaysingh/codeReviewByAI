import os
import requests
import openai


# Azure OpenAI configuration
api_base = "https://usa-decision-azureai-openai.openai.azure.com/"
api_version = "2024-05-13"
deployment_name = "gpt4o"  # Replace with your deployment name

# Set the Azure OpenAI endpoint and API key
openai.api_base = api_base
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create an instance of the OpenAI API client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Debug statements to verify environment variables
print("API Base:", openai.api_base)
print("API Key:", openai.api_key[:4] + "..." + openai.api_key[-4:])  # Print partial key for verification

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

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=deployment_name,  # This is your model deployment name in Azure
        messages=messages,
        max_tokens=1500,
        temperature=0.5 # This specifies the API version to use
    )
    return response['choices'][0]['message']['content']

def review_code(diff):
    prompt = f"Review the following Java code changes and suggest improvements:\n\n{diff}"
    return get_completion(prompt)

if __name__ == "__main__":
    diff = get_diff()
    review = review_code(diff)
    print("### Code Review by GPT-4 ###")
    print(review)
