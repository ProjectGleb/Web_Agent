import requests 
from config_reader import ConfigReader 
import logging 
import time 

class TelegramClient:
    def __init__(self):
        config_reader = ConfigReader()
        section_header = 'TELEGRAM'

        self.chat_id = config_reader.read_prop(section_header, 'chat_id')
        self.parse_mode = config_reader.read_prop(section_header, 'parse_mode')
        self.bot_token = config_reader.read_prop(section_header, 'bot_token')

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.offset = None 

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&parse_mode={self.parse_mode}&text={message}"

        try:
            # sends message
            response_json = requests.get(url).json()
            logging.debug(str(response_json))
        except Exception as e:
            print(f"Some problem occurred while sending message via telegram: {e}")

    def get_updates(self):
        url = f"{self.base_url}/getUpdates?timeout=100"
        if self.offset:
            url += f"&offset={self.offset}"

        try: 
            response_json = requests.get(url).json()
            logging.debug(str(response_json))
            return response_json
        except Exception as e: 
            logging.error(f"Some problem occured while getting updates from telegram : {e}")

    def process_updates(self):
        updates = self.get_updates()
        
        if updates and updates.get('ok'):
            for update in updates['result']:
                self.offset = update['update_id'] + 1

                if 'message' in update: 
                    message = update['message']['text']
                    chat_id = update['message']['chat']['id']
                    self.handle_message(chat_id, message)

    def handle_message(self, chat_id, message):
        response_message = f"Echo : {message}"
        self.send_message_to_chat(chat_id, response_message)

    def send_message_to_chat(self, chat_id, message):
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
        }
        logging.debug(f"Sending message to chat {chat_id}")
        try: 
            requests.post(url, json=payload)
            logging.debug('Message sent')
        except Exception as e: 
            logging.error(f"Some problem occured in sending message via telegram: {e}")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    client = TelegramClient()

    while True:
        client.process_updates()
        time.sleep(1)

