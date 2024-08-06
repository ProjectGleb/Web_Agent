import agentql
import time
from playwright.sync_api import sync_playwright
import json
import os

def agentql_logic(session_url, elements):
    session = agentql.start_session(session_url)
    page = session 

#Action format:
    # elements = {
    #     'Click0': 'accept_all_btn',
    #     'Type0': {'google_search_box': 'github.com'},
    #     'Click1': 'google_search_btn',
    #     "Click2": "github_lets_build_from_here_link",
    #     "Click3": "github_sign_in_btn",
    #     "Type2": {'github_signin_username_box': username},
    #     "Type3": {'github_signin_password_box': password},
    #     "Click4": "sign_in_btn",
    #     "Type4": {'new_repo_name_box': 'Automated QL Repo Test'},
    #     "Click5": "public_btn",
    #     "Click6": "create_new_repository_btn"
    # }

    for action, value in elements.items():
        print(action, value)
        if 'Click' in action:
            Query = f"""
            {{
                {value}
            }}
            """
            response = page.query(Query)
            element = getattr(response, value)
            element.click()

        elif 'Type' in action:
            print('Type : ', value)
            print(action)
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

        time.sleep(1)

    session.stop()


def parse_instructions_from_file(file_path):
    elements = {}
    type_count = 0
    click_count = 0
    # other_count = 0
    session_url = None

    with open(file_path, 'r') as file:
        instructions = file.readlines()

    for line in instructions:
        if line.strip():
            if line.startswith('Website:'):
                session_url = line.split(': ', 1)[1].strip().strip("'")
            else:
                action, detail = line.split(': ', 1)
                if action == 'Type':
                    action, key, detail = line.split(': ', 2)
                    elements[f'Type{type_count}'] = {key.strip(): detail.strip()}
                    type_count += 1
                elif action == 'Click':
                    elements[f'Click{click_count}'] = detail.strip().strip("'")
                    click_count += 1
                # else:
                #     elements[f'{action.capitalize()}{other_count}'] = detail.strip().strip("'")
                #     other_count += 1

    return session_url, elements


file_path = './golem_tasks.txt'
session_url, elements = parse_instructions_from_file(file_path)

print(elements)

if session_url:
    print(f"Session started with URL: {session_url}")
    agentql_logic(session_url, elements)
else:
    print("No website URL found in the instructions file.")

