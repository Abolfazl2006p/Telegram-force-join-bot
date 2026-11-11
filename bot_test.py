import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = 'YOUR_TOKEN_HERE'
URL = f"https://api.telegram.org/bot{TOKEN}/"

CHANNEL_ID = '-1003975532129'
INVITE_LINK = 'YOUR_INVITE_LINK_HERE'

PROXY_PORT = "12334" 
PROXIES = {
    'http': f'http://127.0.0.1:{PROXY_PORT}',
    'https': f'http://127.0.0.1:{PROXY_PORT}'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_updates(offset=None):
    url = URL + "getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        response = requests.get(url, params=params, timeout=40, proxies=PROXIES, headers=HEADERS, verify=False)
        return response.json()
    except Exception:
        return {}

def send_message(chat_id, text, reply_markup=None):
    url = URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
        
    try:
        requests.post(url, json=payload, timeout=10, proxies=PROXIES, headers=HEADERS, verify=False)
    except Exception as e:
        print("Error sending message:", e)

def check_membership(chat_id):
    url = URL + "getChatMember"
    payload = {"chat_id": CHANNEL_ID, "user_id": chat_id}
    try:
        response = requests.post(url, json=payload, proxies=PROXIES, verify=False)
        result = response.json()
        
        if result.get("ok"):
            status = result["result"]["status"]
            if status in ["member", "administrator", "creator"]:
                return True
        return False
    except Exception:
        return False

print("Bot is running...")
last_update_id = None

while True:
    updates = get_updates(last_update_id)
    if updates and updates.get("ok"):
        for update in updates["result"]:
            last_update_id = update["update_id"] + 1
            
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                if text == "/start":
                    keyboard = {
                        "inline_keyboard": [
                            [
                                {"text": "Join Channel", "url": INVITE_LINK},
                                {"text": "I Joined", "callback_data": "check_join"}
                            ]
                        ]
                    }
                    send_message(chat_id, "Hello! Please join our private channel to use this bot:", reply_markup=keyboard)
                else:
                    send_message(chat_id, f"You said: {text}")
            
            elif "callback_query" in update:
                callback_query = update["callback_query"]
                chat_id = callback_query["message"]["chat"]["id"]
                callback_id = callback_query["id"]
                data = callback_query["data"]
                
                if data == "check_join":
                    requests.post(URL + "answerCallbackQuery", json={"callback_query_id": callback_id}, proxies=PROXIES, verify=False)
                    
                    if check_membership(chat_id):
                        send_message(chat_id, "Welcome! Your membership is verified. You can now use the bot.")
                    else:
                        send_message(chat_id, "You haven't joined the channel yet! Please join and try again.")
                    
    time.sleep(1)