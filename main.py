import agentql
import time
from playwright.sync_api import sync_playwright
import json
from dotenv import load_dotenv
import os
load_dotenv()
from Autonomus_Logic.step0_user_goal import get_user_input
from Autonomus_Logic.step1_planning import agent_planning
from Autonomus_Logic.step2_ocr import screenshot_ocr
from Autonomus_Logic.step3_planning_crew import crew_planning



user_goal = get_user_input() #Get user query
plan = agent_planning(user_goal) #Make a step by step plan 
screenshot_content = screenshot_ocr(user_goal) #Transcribe the screenshot
# crew_script = crew_planning(user_goal, screenshot_content, past_actions???)


'''
1. GOAL (create github repo) √
2. CONSTRUCT A STEP BY STEP PLAN 
3. TRANSCRIBE THE SCREENSHOT {outline interactive elements} √
    3.2 SAVE TO MEMORY
4.1 CHECK ACTION MEMORY,
    4.2  MAKE 1 ACTION PLAN
5. EXECUTE (USE AGENTQL)
6. SAVE TO MEMORY {goal, action, outcome}

'''



# Agent = LLM + memory(?) + planning skills(PDF?) + tool use(AgentQL)
session = agentql.start_session("https://www.google.com")

time.sleep(1)

session.current_page.screenshot(path='screenshot.png')
time.sleep(1)


session.stop()
