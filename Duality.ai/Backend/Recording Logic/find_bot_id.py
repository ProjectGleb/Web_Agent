import requests 
from config_reader import ConfigReader

cr = ConfigReader()
section_header = "TELEGRAM"
bot_token = cr.read_prop(section_header, "bot_token")

print('bot token : ', bot_token)
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

print('JSON : ', requests.get(url).json())

