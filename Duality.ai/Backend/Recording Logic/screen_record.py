import pyautogui
import cv2
import numpy as np
import os
import time
import sounddevice as sd
import soundfile as sf
import threading

duration = 1000  
end_time = time.time() + duration

output_folder = "frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)

# Initialize audio recording parameters
audio_output_file = f"{output_folder}/output_audio.wav"
samplerate = 44100
chunk = 1024  # Number of frames per buffer

# Shared flag to stop the recording
stop_recording = threading.Event()

def record_audio():
    global stop_recording
    print("Recording audio...")
    try:
        # Determine the number of input channels
        device_info = sd.query_devices(sd.default.device[0], 'input')
        channels = device_info['max_input_channels']
        
        # Initialize an empty list to store audio frames
        audio_frames = []
        
        # Start the stream
        with sd.InputStream(samplerate=samplerate, channels=channels) as stream:
            while not stop_recording.is_set():
                audio_frames.append(stream.read(chunk)[0])
        
        print("Audio recording finished.")
        
        # Convert list of audio frames to a numpy array
        audio_frames = np.concatenate(audio_frames, axis=0)
        
        # Save the recorded audio to a file
        sf.write(audio_output_file, audio_frames, samplerate)
    except Exception as e:
        print(f"An error occurred while recording audio: {e}")

# Start audio recording in a separate thread
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

no_of_frames = 0

try:
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_filename = os.path.join(output_folder, f"frame_{no_of_frames:04d}.png")
        cv2.imwrite(frame_filename, frame[:, :, :3])

        no_of_frames += 1

        if time.time() > end_time:
            stop_recording.set()
            break
except KeyboardInterrupt:
    print('Recording interrupted by user.')
    stop_recording.set()

print('Number of frames:', no_of_frames)

audio_thread.join()
cv2.destroyAllWindows()


from openai import OpenAI
import json 

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

audio_file= open(audio_output_file, "rb")
transcription = openai_client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  language="en"
)
print('transcribed text : ')
print(transcription.text)

with open(f'{output_folder}/transcription.txt', "w") as text_file:
    text_file.write(transcription.text)
