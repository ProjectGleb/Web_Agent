#Getting user input, and making a plan
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import requests
load_dotenv()
from step0_user_goal import get_user_input

user_goal = get_user_input()

def agent_planning(user_goal):
    # activate chatGPT agent
    import os

    api_key = os.getenv("OPENAI_API_KEY")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": """You are a web agent, designed to craft a plan to achieve the user's goal which a computer will then execute. The plan should detail EVERY SINGLE click, type or other interaction a computer needs to take to navigate through the web browser to achieve the user's goal. The plan should be outputing each step as concrete actions like "Click", "Enter" "Scrawl", "Return", etc. Dont add conclusions.(Assume google.com is already opened). You are not limited to the number of steps you should take.
                As an example, if the user's request is "Tell me if there is anything important in my email inbox," here is the plan and format you should craft would look like this:
                PLAN: 1. Search :
                1. Type in search gmail.com in the search box.
                2. Click on the search button.
                3. Click on the first link.
                4. Type in email and password.
                5. Click on the sign in button.
                6. Click on the inbox.
                7. Read the first email.
                8. Extract the important information.
                9. Repeat step 5-9 for any unread emails.
                10. Return the important information to the user.
                11. End.
                 """

            },
            {
                "role": "user",
                "content": f"user goal:{user_goal}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Response from OpenAI:", response.json())
        # print('\n')
        print(response.json()['choices'][0]['message']['content'])
    else:
        print("Error:", response.status_code, response.text)


agent_planning(user_goal)





# Planning output:
"""
PLAN:
1. Type "github.com" into the search box.
2. Click on the search button.
3. Click on the first search result to navigate to GitHub.
4. Click on the "Sign in" button.
5. Type in the GitHub username.
6. Type in the GitHub password.
7. Click on the "Sign in" button to log into GitHub.
8. Click on the "+" icon at the top right corner of the GitHub homepage.
9. Click on "New repository" from the dropdown menu.
10. Type "Name" for the repository in the repository name field.
11. Type "Description" for the repository in the description field (optional).
12. Click on "Public" to set the repository visibility to public (or click on “Private” if preferred).
13. Scroll to the "Initialize this repository with:" section.
14. Click on the checkbox next to "Add a README file" (optional).
15. Click on the checkbox next to "Add .gitignore" and select "Python" from the dropdown.
16. Click on the checkbox next to "Choose a license" and select a license from the dropdown (optional).
17. Click on the "Create repository" button.
18. End."""

# Take a step, logg it, in steps completed, and mark as complete in the plan

