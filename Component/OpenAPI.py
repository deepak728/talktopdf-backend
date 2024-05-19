import requests

API_URL = "https://api-inference.huggingface.co/models/pszemraj/led-large-book-summary"
headers = {"Authorization": "Bearer <token>"}


async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


async def get_summary(content):
    output = await query({"inputs": content})
    print(output)
    return output[0]["summary_text"]
