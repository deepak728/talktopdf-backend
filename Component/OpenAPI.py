import time
import requests
import json

# Define the API endpoint and your API key
url = "https://api.pawan.krd/v1/chat/completions"
api_key = "pk-"

# Create the headers for the request
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
system_content = "You have to make the summary of given input in a story format."

# Global variables to track requests
request_count = 0
start_time = time.time()


def rate_limit():
    global request_count, start_time
    if request_count >= 3:
        elapsed_time = time.time() - start_time
        if elapsed_time < 16:
            time.sleep(16 - elapsed_time)
        request_count = 0
        start_time = time.time()
    request_count += 1


async def make_request(prompt):
    rate_limit()
    payload = {
        "model": "pai-001-light",
        "max_tokens": 1000,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_json = response.json()
        print("Response received successfully:")
        # print(json.dumps(response_json, indent=4))
        return response_json["choices"][0]["message"]["content"]
    else:
        print(f"Failed to get response, status code: {response.status_code}")
        print("Response body:", response.text)
        return "Failed to get response"


async def get_summary(content):
    output = await make_request(content)
    print(output)
    return output


async def get_summary_with_word_limit(content, words):
    prompt = (
        "give me the summary of given story in paragraph format and like a story around "
        + str(words)
        + " words. story: "
        + content
    )
    try:
        output = await make_request(prompt)
        return output
    except Exception as e:
        print(f"Failed to get summary: {e}")

    return ""
