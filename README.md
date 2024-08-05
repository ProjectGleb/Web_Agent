# Duality: An AI agent that can use your computer to complete tasks.

Demo: https://drive.google.com/file/d/1pmI5eN391Of5rykucSi6S011g5t8Gykd/view?usp=drive_link

The system has two paths for operating:
1. **An AI gent that can learn to complete computer tasks through a simple video recording of one.** 
2. **An AI agent that can autonomousely complete computer tasks with no demonstration. (EXPERIMENTAL)**

## How It Works:
### Function 1: Semi-autonomus task completion
1. **Create a Screen Recording:**
    - Record how you complete a task
2. **Transcription:**
    - The recording is transcribed into actionable steps using GPT4o.
3. **Parsing and Interaction:**
    - The steps are parsed through the agent logic, which initiates a browser session and parses through HTML elements that it deems relevant.
    - The agent then interacts with these elements to perform the task.

### Function 2: Autonomus task completion
1. **Constructing a Plan:**
    - Based on the provided text query, the agent constructs a plan to achieve the specified goal.
2. **Browser Session and Transcription:**
    - The agent begins a browser session and transcribes its screenshots using GPT.
3. **Parsing and Interaction:**
    - The transcription is parsed by the LLM into an AgentQL query, which then interacts with the webpage.
4. **Re-Analysis and Iteration:**
    - The agent continuously re-analyzes the changing web state against the goal and iterates the process until the goal is achieved.
   
P.S: Autonomus Logic is extremely novel and thereby experimental. It makes mistakes, so please use at your own risk.
