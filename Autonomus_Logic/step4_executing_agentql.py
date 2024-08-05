import agentql
import time
from playwright.sync_api import sync_playwright
import json
from dotenv import load_dotenv
import os
load_dotenv()

# Agent = LLM + memory(?) + planning skills(PDF?) + tool use(AgentQL)
def agentql_logic():
    session = agentql.start_session("https://www.google.com")
    page = session # This is the main page

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    elements = {
        'Click0': 'accept_all_btn',
        'Type0': {'google_search_box': 'github.com'},
        'Click1': 'google_search_btn',
        "Click2": "github_lets_build_from_here_link",
        "Click3": "github_sign_in_btn",
        "Type2": {'github_signin_username_box': username},
        "Type3": {'github_signin_password_box': password},
        "Click4": "sign_in_btn",
        "Type4": {'new_repo_name_box': 'Automated QL Repo Test'},
        "Click5": "public_btn",
        "Click6": "create_new_repository_btn"
    }

    for action, value in elements.items():
        if 'Click' in action:
            Query = f"""
            {{
                {value}
            }}
            """
            response = page.query(Query)
            element = getattr(response, value)
            element.click(force=True)

        elif 'Type' in action:
            for item, text in value.items():
                print(f"Typing '{text}' into: {item}")
                Query = f"""
                {{
                    {item}
                }}
                """
                response = page.query(Query)
                element = getattr(response, item)
                element.type(text)



    time.sleep(5)

    session.stop()




