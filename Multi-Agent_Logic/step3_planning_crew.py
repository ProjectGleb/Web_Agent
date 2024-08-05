from dotenv import load_dotenv
import os
import warnings
from crewai import Agent, Task, Crew
load_dotenv()

# OCR TEXT OUTPUT. Needs to be taken and split into two parts, interractive elements and screen info, which could be then reused. 
def crew_planning(user_goal, interactive_elements, past_actions):

    warnings.filterwarnings("ignore")

    get_openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'

    #HISTORY LOG
    history_log = ["user_goal" "past_steps_taken", "browser_interractive elements", "", ]


    planner = Agent(
        role="Video Parser",
        goal="Given a {user_goal}, and {browser_screen_elements} and the {past_actions}, determine the next interaction",
        backstory="You're an AI agent trying to help a user navigate the web-browser based on their query§ to achieve a specific goal by interacting with the browser one action at a time.",
        allow_delegation=False,
        verbose=True
    )

    plan = Task(
        description=(
            "1. Make decisions based on past actions to avoid repetition or falling into loops.\n"
            "2. Produce only one action decision where the action must be either 'Click' or 'Type'.\n"
            "3. If it's a 'Type' action, it must be in the format of 'Type': 'element_to_be_interacted_with': 'text_to_be_typed_in'.\n"
            "4. If it's a 'Click' action, it must be in the format of 'Click1': 'element_to_be_interacted_with'.\n"
            "5. The element_to_be_interacted_with must end with '_btn' if it's a button or '_box' if it's a text box.\n"
            "6. Each action should have an index embedded into it based on the index of the past action. So if the past action was 'Click1', the next action should be 'Click2'.\n"
        ),
        expected_output="'Type1': {{'google_search_box': 'github.com'}}",
        agent=planner
    )


    edit = Task(
        description="Proofread the output of the previous agent and capitalize all the text.",
        expected_output="'TYPE1': {{'GOOGLE_SEARCH_BOX': 'GITHUB.COM'}}",
        agent=editor
    )

    crew = Crew(
        agents=[planner, editor],
        tasks=[plan, edit],
        verbose=2
    )

    # past_actions = {'action_history': {'Click0': 'accept_browser_cookies_btn', 'Type0': "{google_search_box : github.com}"}}
    result = crew.kickoff(inputs={"past_actions":"PAST ACTIONS [Click0: accept_browser_cookies_btn, Type: {{google_search_box : github.com}}]", 
                                "browser_screen_elements": "BROWSWER SCREEN ELEMENTS: [github_lets_build_from_here_link, github_blog_link, github_about_link]",
                                "user_goal": "USER GOAL: 'The user wants to create a new repository on Github'."})