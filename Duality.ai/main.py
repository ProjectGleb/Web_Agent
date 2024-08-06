import json
import time
from pathlib import Path
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import agentql
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json_file(user_inp):
    # Using pathlib to construct the memory path
    memory_path = Path(__file__).resolve().parent / 'Backend' / 'Tasks_Memory'
    
    for file_path in memory_path.glob('*.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if any(keyword in user_inp.lower() for keyword in file_path.stem.split('_')):
                return data
    return None

def agent_logic(user_inp):
    def agentql_logic():
        elements = load_json_file(user_inp)
        if elements is None:
            return "No matching task found in memory for the query."

        time.sleep(4)
        session = agentql.start_session("https://www.google.com")
        page = session  # main page

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        for key, value in elements.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_value == "username":
                        elements[key][sub_key] = username
                    elif sub_value == "password":
                        elements[key][sub_key] = password

        output = "Successfully executed the actions."

        for action, value in elements.items():
            if 'Click' in action:
                Query = f"""
                {{
                    {value}
                }}
                """
                try:
                    response = page.query(Query)
                    element = getattr(response, value)
                    element.click(force=True)
                except Exception as e:
                    print(f"Error during clicking {value}: {e}")

            elif 'Type' in action:
                for item, text in value.items():
                    Query = f"""
                    {{
                        {item}
                    }}
                    """
                    try:
                        response = page.query(Query)
                        element = getattr(response, item)
                        element.type(text)
                    except Exception as e:
                        print(f"Error during typing {text} into {item}: {e}")

        time.sleep(5)  # Wait before stopping the session to see the task completed
        session.stop()
        return output

    result = agentql_logic()
    return result

@app.post("/process/")
def process_input(user_input: str = Form(...)):
    print(f"Received input: {user_input}")
    result = agent_logic(user_inp=user_input)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
