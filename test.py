import subprocess
import re
import datetime

def get_commits_from_year(year):
    # Get the list of commits
    result = subprocess.run(
        ['git', 'log', '--pretty=format:%H %cd', '--date=short'],
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Filter commits from the specified year
    commits = result.stdout.splitlines()
    commits_from_year = [line.split()[0] for line in commits if line.split()[1].