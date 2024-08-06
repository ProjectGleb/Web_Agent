# #AGENT QL LOGIC

# get an agent to compare the memory to the user query, and execute the most resemblant one. 
import json
import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import agentql
import time

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to load JSON files based on keywords in the user query
def load_json_file(user_inp):
    memory_path = 'memory'
    for filename in os.listdir(memory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(memory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                if any(keyword in user_inp.lower() for keyword in filename.lower().replace('.json', '').split('_')):
                    return data
    return None

def agent_logic(user_inp):
    def agentql_logic():
        # Load the JSON file based on the user query
        elements = load_json_file(user_inp)
        if elements is None:
            return "No matching action found for the query."

        time.sleep(4)
        session = agentql.start_session("https://www.google.com")
        page = session  # This is the main page

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        # Update elements with actual username and password
        for key, value in elements.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_value == "username":
                        elements[key][sub_key] = username
                    elif sub_value == "password":
                        elements[key][sub_key] = password

        output = "Successfully executed the actions."

        # Execute actions
        for action, value in elements.items():
            if 'Click' in action:
                Query = f"""
                {{
                    {value}
                }}
                """
                print(f"Executing Click Query: {Query}")
                try:
                    response = page.query(Query)
                    element = getattr(response, value)
                    element.click(force=True)
                except Exception as e:
                    print(f"Error during clicking {value}: {e}")

            elif 'Type' in action:
                for item, text in value.items():
                    print(f"Typing '{text}' into: {item}")
                    Query = f"""
                    {{
                        {item}
                    }}
                    """
                    print(f"Executing Type Query: {Query}")
                    try:
                        response = page.query(Query)
                        element = getattr(response, item)
                        element.type(text)
                    except Exception as e:
                        print(f"Error during typing {text} into {item}: {e}")

        time.sleep(5)  # Wait before stopping the session
        session.stop()
        return output

    result = agentql_logic()
    return result

@app.post("/process/")
def process_input(user_input: str = Form(...)):
    # Process the input data (e.g., start backend code execution)
    print(f"Received input: {user_input}")

    result = agent_logic(user_inp=user_input)  # Get the result from agent_logic

    # Replace this with your actual processing logic
    print(f"{user_input}")
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
