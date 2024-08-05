from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent, Task
from dotenv import load_dotenv
import os
import warnings
from ocr_agent import OCR_Tool, ocr_agent, ocr_task
from planning_agent import planner, plan

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'

# Define warnings
warnings.filterwarnings("ignore")

planner = Agent(
    role="Web Guide",
    goal="Given a user_goal:and web screenshots_interactive_elements passed from the previous agent, create a step-by-step plan that a computer will execute to accomplish the user's goal.",
    backstory="You're an AI planning agent trying to help a user navigate the web-browser based on their query.",
    allow_delegation=False,
    verbose=True
)


plan = Task(
    description=(
        "Navigate through the web given an element provided' \n"),
    expected_output="'Type1': {{'google_search_box': 'github.com'}}",
    agent=planner,
	async_execution=False,
)

# Initialize Crew
project_crew = Crew(
    tasks=[plan],
    agents=[planner],
    memory=True,  # Enable memory usage for enhanced task execution
)

# Kickoff the crew
result = project_crew.kickoff(inputs={"user_goal": 'Explain to me what you can see on the screen using the ocr tool',
                                      "past_actions": "PAST ACTIONS [Click0: accept_browser_cookies_btn, Type: {{google_search_box : github.com}}, Click1: github_link_btn, Type1: {{github_username_box : Gleb}}, Type2: {{github_password_box : 123}, ERROR ENCOUNTERED: AUTHENTICATION REQUIRED, CODE SENT TO gleb.studios@gmail.com]}"})

# print(result)


# class Web_Navigating_Tool(BaseTool):
#     name: str = "Web_Navigating_Tool"
#     description: str = """This tool makes 1 navigation action, click or type, based on the provided interactive element on the page and how to interract with it.\n
#     Args:\n
#         - interactive_element: interactive element of the screen.\n
#     Returns:\n
#         - Screen context."""
#     def _run(self, element: str)->str:
	


# 	def research_task(self, agent, participants, context):
# 		return Task(
