# Recording logic

Recording demo video: https://www.youtube.com/watch?v=7KqTQCBoYMg

## Running the code
    
Record yourself performing a task as well as speaking through it by running: 
```
 python screen_record.py
```

Feed frames of the recorded video and transcribed audio to GPT-4 by running: 
```
 python gpt4_feed.py
```

To check everythin is working as intended use AgentQL to perform the task. 
```
python agentql_executor.py 
```
If all works well you can append task to memory folder and whala! Your task is fully automated.

