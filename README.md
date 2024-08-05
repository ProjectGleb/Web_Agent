# Duality: An AI employee that can control your computer.
![Duality-demo](https://github.com/user-attachments/assets/3d9fa8c5-fd6a-4cac-b392-f817ebab7481)

## Overview
Duality is an AI agent crew that can take over your browser and complete tasks for you. 

This repo contains two types of agent logic:
1. **Semi-Autonomus: An AI gent that can learn to complete computer tasks through a simple video recording of a task.** 
2. **Autonomus: An AI agent that can autonomousely complete computer tasks with no demonstration. (EXPERIMENTAL)**

## Features:
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
    - The agent begins a browser session and transcribes its screenshots using GPT.
3. **Parsing and Interaction:**
    - The transcription is parsed by the LLM into an AgentQL query, which then interacts with the webpage.
4. **Re-Analysis and Iteration:**
    - The agent continuously re-analyzes the changing web state against the goal and iterates the process until the goal is achieved.
   
P.S: Autonomus Logic is extremely novel and thereby experimental. It makes mistakes, so please use at your own risk.
