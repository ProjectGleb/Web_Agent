import os
from openai import OpenAI
import json 
import cv2
import base64

api_keys_file = os.path.join(os.path.dirname(__file__), 'api_keys.json')

if os.path.exists(api_keys_file):
    with open(api_keys_file, 'r') as f:
        api_keys = json.load(f)
else:
    api_keys = {}

if 'openai_api_key' in api_keys:
    openai_client = OpenAI(api_key=api_keys['openai_api_key'])
else:
    exit('Please enter API key')

def describe_descriptions(frames, transcribed_text, iterations=3, skip_frames=10):

    # system_prompt = "Come up with a detailed description of what the user is doing in the video, but convert it to commands that can be fed to an agent like 'click_submit_button', 'take_screenshot', 'open_browser_window', and so on. If typing is involved mention which field or textbox associated. Don't say much in natural language. Only use the commands. format it as a dictionary like so: 'Click0': 'accept_all_btn', 'Type0': {'google_search_box': 'github.com'}, 'Click1': 'google_search_btn', 'Click2': 'github_lets_build_from_here_link', 'Click3': 'github_sign_in_btn', 'Type2': {'github_signin_username_box': username}, 'Type3': {'github_signin_password_box': password}, 'Click4': 'sign_in_btn', 'Type4': {'new_repo_name_box': 'Automated QL Repo Test'}, 'Click5': 'public_btn', 'Click6': 'create_new_repository_btn'"
    
    # system_prompt = "Come up with a detailed description of what the user is doing in the video, but convert it to commands that can be fed to an agent like 'click_submit_button', 'take_screenshot', 'open_browser_window', and so on. If typing is involved mention which field or textbox is associated in the same context. Don't say much in natural language. Only use the commands."

    system_prompt = f"You're an AI agent trying to help a user navigate the web-browser based on their queries to achieve a specific goal by interacting with the browser one action at a time. If it's a 'Type' action, it must be in the format of 'Type': 'element_to_be_interacted_with': 'text_to_be_typed_in'.\n If it's a 'Click' action, it must be in the format of 'Click': 'element_to_be_interacted_with'.\n The element_to_be_interacted_with must end with '_btn' if it's a button or '_box' if it's a text box.\n Always start with 'Website: ' as the first line, followed by the website of focus. The second task is almost always accept all cookies button.  Here is the user explaining what they're doing, use this to make sense of the video as well: {transcribed_text}. Don't use natural language. Don't provide any other explanation."

    PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            system_prompt,
            *map(lambda x: {"image": x, "resize": 500}, frames[0::skip_frames]),
        ],
        },
    ]
    
    last_response = None 

    for _ in range(iterations):     
        params = {
            "model": "gpt-4o",
            "messages": PROMPT_MESSAGES,
            "max_tokens": 200,
        }
        result = openai_client.chat.completions.create(**params)
        last_response = result.choices[0].message.content

        print('Intermediate Response : ')
        print(last_response)
        print('##########################################')

        # Feed the model's output back into itself
        PROMPT_MESSAGES.append({"role": "assistant", "content": last_response})
        PROMPT_MESSAGES.append({"role": "user", "content": 'The above are your previous attempts. Please analyze them to make your new answer even better. Try to identify mistakes and rectify them.'})

    return last_response


def process_frames_from_folder(folder_path):
    # Get list of image files from the folder
    frame_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))])
    base64Frames = []
    for frame in frame_files[5:-5]:
        img_frame = cv2.imread(frame)
        _, buffer = cv2.imencode(".png", img_frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    with open(f'{folder_path}/transcription.txt', "r") as text_file:
        transcribed_text = text_file.read()
    
    print('transcribed text : ', transcribed_text)

    # Summarize descriptions
    summary = describe_descriptions(base64Frames, transcribed_text, iterations=1, skip_frames=20)
    
    with open(f'./golem_tasks.txt', "w") as text_file:
        text_file.write(summary)

if __name__ == "__main__":
    folder_path = "frames"  # Path to the folder containing the frames
    process_frames_from_folder(folder_path)
