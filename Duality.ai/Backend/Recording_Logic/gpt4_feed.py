import os
from openai import OpenAI
import json 
import cv2
import base64
from dotenv import load_dotenv

load_dotenv()

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client without passing the API key
openai_client = OpenAI()

def describe_descriptions(frames, transcribed_text, iterations=3, skip_frames=10):
    system_prompt = f"You're an AI agent that based on a user web interaction video transcribes user actions one at a time. If it's a 'Type' action, it must be in the format of 'Type': 'element_to_be_interacted_with': 'text_to_be_typed_in'.\n If it's a 'Click' action, it must be in the format of 'Click': 'element_to_be_interacted_with'.\n The element_to_be_interacted_with must end with '_btn' if it's a button or '_box' if it's a text box.\n Always start with 'Website: ' as the first line, followed by the website of focus. The second task is almost always accept all cookies button.  Here is the user explaining what they're doing, use this to make sense of the video as well: {transcribed_text}. Don't use natural language. Don't provide any other explanation."

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
    
    with open(f'./new_task.txt', "w") as text_file:
        text_file.write(summary)

if __name__ == "__main__":
    folder_path = "frames"  # Path to the folder containing the frames
    process_frames_from_folder(folder_path)