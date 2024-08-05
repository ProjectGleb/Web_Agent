# Duality: Your AI employee 🤖
This repo contains autonomus and semi-autonomus logic for a multi-agent crew that can automate digital labour.

Demo: https://drive.google.com/file/d/1myGTO42d8zqeMZ1tbs-yQwYAo5JAf3wQ/view?usp=sharing

The system has two paths for operating:
1. **Learning to complete a task through your desktop recording, as if a child. And then being able to complete it without help.** 
2. **Automatically zero-shotting tasks based on a query.**

## How It Works:
### Function 1: Learning Tasks From Your Recordings (Semi-autonomus)
1. **Create a Screen Recording:**
    - Record how you complete a task
2. **Transcription:**
    - The recording is transcribed into actionable steps using GPT4o.
3. **Parsing and Interaction:**
    - The steps are parsed through the agent logic, which initiates a browser session and parses through HTML elements that it deems relevant.
    - The agent then interacts with these elements to perform the task.

### Function 2: Automating Tasks from Text Prompts (Autonomus)
1. **Constructing a Plan:**
    - Based on the provided text query, the agent constructs a plan to achieve the specified goal.
2. **Browser Session and Transcription:**
    - The agent begins a browser session and transcribes its screenshots using GPT.
3. **Parsing and Interaction:**
    - The transcription is parsed by the LLM into an AgentQL query, which then interacts with the webpage.
4. **Re-Analysis and Iteration:**
    - The agent continuously re-analyzes the changing web state against the goal and iterates the process until the goal is achieved.
   
P.S: Autonomus Logic is extremely novel and thereby experimental. It makes mistakes, so please use at your own risk.
