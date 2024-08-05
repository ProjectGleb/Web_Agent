from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent
from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
from ocr_agent import OCR_Tool, ocr_agent, ocr_task
from planning_agent import planner, plan 
from executing_agent import Web_Navigating_Tool, web_navigator_agent, web_navigation
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'


'''
Agents:
CEO AGENT
PLANNING AGENT
EXECUTING AGENT
'''

web_navigator_agent_tool = Web_Navigating_Tool()

ceo = Agent(
    role="CEO",
    goal="Help the user accolimplish their goal by delegating tasks to other agents.",
    backstory="An AI agent trying to help a user navigate the web-browser based on their query by using other specialized agents that have specialized tools at your disposal.",
    verbose=True,
    delete=True
)

ceoing = Task(
    description=(
        " You are the CEO. Your role is to use ai web-agents at your disposal to help accomplish the users goal. Take into consideration the USER_GOAL: {user_goal}, and PAST_ACTIONS: {past_actions}."),
    expected_output="'Employee task request''",
    agent=ceo
)

warnings.filterwarnings("ignore")

project_crew = Crew(
    tasks=[ceoing, plan,  web_navigation, ocr_task],
    agents=[ceo, web_navigator_agent, planner, ocr_agent],
    manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),  # Mandatory for hierarchical process
    process=Process.hierarchical, 
    memory=True, 
)

# Kickoff the crew
result = project_crew.kickoff(inputs={"user_goal": 'Navigate through browser and get to github.com',
                                      "past_actions": "PAST ACTIONS [Click0: accept_browser_cookies_btn, Type: {{google_search_box : github.com}}, Click1: github_link_btn, Type1: {{github_username_box : Gleb}}, Type2: {{github_password_box : 123}, ERROR ENCOUNTERED: AUTHENTICATION REQUIRED, CODE SENT TO gleb.studios@gmail.com]}"})

print(result)

"""
Clic0 : 

"""