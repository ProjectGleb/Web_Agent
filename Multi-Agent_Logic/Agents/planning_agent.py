from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
load_dotenv()

### MAKE SURE THE AGENT MAKES A PLAN BASED ON PAST ACTIONS AND FALIURES

"""
Notes:
- Agents should be results driven and hava a clear goal in mind/
- Role is their job title
- Goals should be actionable 
- Backstorry should be their resume
"""

warnings.filterwarnings("ignore")

get_openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'

#HISTORY LOG

planner = Agent(
    role="Web Guide",
    goal="Given a user_goal:{user_goal} and web screenshots_interactive_elements passed from the previouse agent, create a step-by-step plan that a computer will execute to acomplish the user's goal.",
    backstory="You're an AI planning agent trying to help a user navigate the web-browser based on their query.",
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        " BEFORE BEGGINING TO REASON, PRINT THE FOLLOWING FOR TEST PURPOSES: 'Hello, let me try to reason' \n"
        "1. Produce a step by step which should EVERY SINGLE click, type or other interaction a computer needs to take to navigate through the web browser to achieve the user's goal. The plan should be outputing each step as concrete actions like 'Click', 'Enter' 'Scrawl', 'Return', etc. Dont add conclusions.(Assume google.com is already opened). You are not limited to the number of steps you should take."
        "2. Take {past_actions} and {user_goal} into account to avoid repetition or falling into loops.\n"        
        """As an example, if the user's request is "Tell me if there is anything important in my email inbox," here is the plan and format you should craft would look like this:
        EXAMPLE PLAN:
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
        11. End."""),
    expected_output="'Type1': {{'google_search_box': 'github.com'}}",
    agent=planner
)

