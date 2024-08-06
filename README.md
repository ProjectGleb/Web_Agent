# Duality: An AI employee that can control your computer.
![Duality-demo](https://github.com/user-attachments/assets/3d9fa8c5-fd6a-4cac-b392-f817ebab7481)

## Overview 🔎
Duality is an AI agent crew that can take over your browser and complete tasks for you. 

This repo contains two types of agent logic:
1. **Semi-Autonomus (main branch): An AI gent that can learn to complete computer tasks through a simple video recording of a task.** 
2. **Autonomus (full_brnach): An AI agent that can autonomousely complete computer tasks with no demonstration. (STILL IN CONSTRUCTION)**

---

## Features 🧰:
### Semi-Autonomus Logic:
1. **Create a Screen Recording:**
    - Record how you complete a task
2. **Transcription:**
    - The recording is transcribed into actionable steps using GPT4o.
3. **Parsing and Interaction:**
    - The steps are parsed through the agent logic, which initiates a browser session and parses through HTML elements that it deems relevant.
    - The agent then interacts with these elements to perform the task.

### Autonomus Logic:
1. **Constructing a Plan:**
    - Based on the provided text query, the agent constructs a plan to achieve the specified goal.
2. **Browser Session and Transcription:**
    - The agent begins a browser session and transcribes its screenshots using GPT4o.
3. **Parsing to Memory:**
   - The agent then saves the screen content into episodic and simantic memory, and takes action based on the context.
5. **Analysis & Action:**
    - The agent analyzes the web state against the goal + memory and takes itterative actions until the goal is achieved.
   

---

## Set-up 🔧
Create anaconda environment
```
conda create -n agent_env python=3.10 -y 

conda activate agent_env
```

Install dependencies
```
pip install -r requirements.txt
```

Set up the api keys
```
AGENTQL_API_KEY=...
OPENAI_API_KEY=...
```

## Run 💥🏃‍♂️🔥
To run the script you have two options.
1. Run the main.py script to host a local server and then open then use the frontent app to record and execute tasks.
2. Run the recording script in the Backend/Recording_Logic folder and then use the agent logic in the same folder to test it.

P.S: Autonomus Logic is extremely novel and thereby experimental. It makes mistakes, so please use at your own peril.
