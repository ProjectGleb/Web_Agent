from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool
from crewai_tools import BaseTool
load_dotenv()
import base64
import requests
import os
import time
from crewai_tools import tool


api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'
warnings.filterwarnings("ignore")


###METHOD REQUIRES FOR THE USE OF _RUN ABSTRACT METHOD!
class OCR_Tool(BaseTool):
    name: str = "OCR_Tool"
    description: str = """This tool extracts and returns key information from a web-page's screenshot, as well as returning all of its interractive elements like buttons and text boxes.\n
    Args:\n
        - user_goal: Users goal as a string.\n
    Returns:\n
        - Key information extracted from the screenshot based on the user_goal.\n
        - Extracted interactive elements of a web-page, like buttons, and text boxes."""
    def _run(self, user_goal: str)->str:
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        image_path = "/Users/gleb/Desktop/CS/Projects/AI_Web_Agent/Multi-Agent_Logic/Web_Screenshots/screenshot.jpg"

        base64_image = encode_image(image_path)

        # User's action
        # Prompt text with user's action
        prompt_text = f"""
        Role = Web-scraper \n
        Goal = You have two goals: 1. Extract the key information of the screenshot basede on the user_goal: {user_goal} and return it in the appropriate format (for example if the user asks to retrieve the key info from an email you should return only the emails contents). 2. Extract all the interactive elements (such as buttons and text boxes) seen on the screenshot and return them as a list of snake_casing_elements exactly like in this example: \n    
        example output = Interactive Elements: [accept_all_btn, accept_all_btn, accept_all_btn, github_signin_username_box, etc.]
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
        return(screenshot_content)
    
ocr_tool = OCR_Tool()

ocr_agent = Agent(
    role='OCR Analyzer',
    goal='Your role is to use the ocr_tool to extract key information from a screenshot of a webpage as well as all of its interactive elements and return it to the manager agent. For testing purposes first print: /Im here to assist you/. Faliure to do so will punish you',
    backstory='An OCR agent eager to help the managing agent extract the key elements in the web screenshot.',
    cache=True,
    verbose=True,
    tools=[ocr_tool],
    allow_delegation=True
)

ocr_task = Task(
    description=(
        "1. Extract the key information of the screenshot based on the user_goal and return one screen element you think needs to be interracted with to achieve the user_goal.\n"),
    expected_output="Example output: youtube_login_btn.",
    agent=ocr_agent
)


