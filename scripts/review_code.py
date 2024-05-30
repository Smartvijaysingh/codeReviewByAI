import os
import openai

# Function to get diff from the pull request
def get_diff():
    # This is a simplified placeholder. You might need to use GitHub API or CLI to get actual diff.
    diff = os.popen('git diff HEAD~1 HEAD').read()
    return diff

# Function to review code with GPT-4
def review_code(diff):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = f"Review the following Java code changes and suggest improvements:\n\n{diff}"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Assuming GPT-4 is under the 'text-davinci-003' engine
        prompt=prompt,
        max_tokens=1500,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

if __name__ == "__main__":
    diff = get_diff()
    review = review_code(diff)
    print("### Code Review by GPT-4 ###")
    print(review)
