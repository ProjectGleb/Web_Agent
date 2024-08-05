# #AGENT QL LOGIC
def agent_logic(user_inp):
    import agentql
    import time
    from dotenv import load_dotenv
    import os

    load_dotenv()

    def agentql_logic():
        time.sleep(4)
        session = agentql.start_session("https://www.google.com")
        page = session  # This is the main page

        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        
        elements = {}

        if "github" in user_inp:
            elements = {
                'Click0': 'accept_all_btn',
                'Type0': {'google_search_box': 'github.com'},
                'Click1': 'google_search_btn',
                "Click2": "github_lets_build_from_here_link",
                "Click3": "github_sign_in_btn",
                "Type2": {'github_signin_username_box': username},
                "Type3": {'github_signin_password_box': password},
                "Click4": "sign_in_btn",
                "Type4": {'new_repo_name_box': 'Agent_test'},
                "Click5": "public_btn",
                "Click6": "create_new_repository_btn"
            }
            output = "Successfully created a GitHub repository"

        elif "codeverse.uk" in user_inp:
            elements = {
                'Click0': 'accept_all_btn',
                'Type0': {'google_search_box': 'codeverse.uk'},
                'Click1': 'google_search_btn',
                "Click2": "CodeVerse",
                "Click3": "reach_out_btn",
                "Type2": {'Whats_your_name_box': "Bob Ross"},
                "Type3": {'whats_your_email_box': "bob.ross@gmail.com"},
                "Type4": {'phone_number_box': '07384860303'},
                "Click4": "something_else_btn",
                "Click5": "i_have_an_idea_btn",
                "Type5": {'Please_tell_us_about_your_project_box': "Project: Create AGI with passion"},
                "Type6": {'Anything_else_youd_like_us_to_know_box?': ''},
                "Click7": "submit_btn"
            }
            output = "Successfully submitted the Codeverse.uk form on behalf of Bob Ross"

        elif "captcha" in user_inp: 
            elements = {
                'Click0': 'accept_all_btn',
                'Type0': {'google_search_box': 'google captcha test'},
                'Click1': 'google_search_btn',
                "Click2": "ReCaptcha_demo",
                "Click3": "I'm_bot_a_robot_btn",
                "Click4": "submit",
            }
            output = "ReCaptcha test executed"

        else: 
            elements = {
                'Click0': 'accept_all_btn',
                'Type0': {'google_search_box': 'langchain'},
                'Click1': 'google_search_btn',
                "Click2": "Langchain",
                "Click3": "Sign_up_btn",
                "Click4": "Login_btn",
                "Click5": "Login_with_email_btn",
                "Type2": {'email_textbox': "gleb.studios@gmail.com"},
                "Type3": {'passoword_textbox': "ApeX030610+"},
                "Click6": "continue_btn",
                "Click7": "Playground_btn",
                "Click8": "Message_btn",
                "Click8": "Output_Schema_box",
                "Type4": {'Human_text_box': 'Fight for humans or machines? 1 for humans 0 for machines.'},
                "Type5": {'AI_text_box': 'You are an AI made by AI.'},
                "Click8": "Start",
                "Type6": {'API_key_text_box': 'XXX'},
            }
            output = "Successfully completed the Langchain interaction"

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
    return(result)


#API CRUD actions
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/")
def process_input(user_input: str = Form(...)):
    # Process the input data (e.g., start backend code execution)
    print(f"Received input: {user_input}")

    result = agent_logic(user_inp=user_input)  # Get the result from agent_logic

    # Replace this with your actual processing logic
    print(f"{user_input}")
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





