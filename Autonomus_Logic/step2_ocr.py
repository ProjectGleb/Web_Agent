import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def screenshot_ocr(user_goal):

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path = "/Users/gleb/Desktop/CS/Projects/AI_Web_Agent/Autonomus_Logic/Web_Screenshots/screenshot.jpg"

    base64_image = encode_image(image_path)

    # User's action
    # Prompt text with user's action
    prompt_text = f"""
    You are a web-scraper, Your job is to extract information based on the screenshot of a webpage and user_action:{user_goal} and format it appropreately.
    In addition describe what are the key interactive elements seen in this web page screenshot (such as buttons and text boxes) in the following format:
    interactive_elements = 
    'accept_all_btn',
    'google_search_box',
    'google_search_btn',
    'github_signin_username_box'
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 400
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Parse the JSON response to extract the useful content
    response_json = response.json()
    screenshot_content = response_json['choices'][0]['message']['content']

    # Access and print the specific parts of the response
    if 'choices' not in response_json:
        print("Error: No content found in the response.")