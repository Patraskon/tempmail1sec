import requests
import random
import string
import time

API_ENDPOINT = "https://www.1secmail.com/api/v1/"

def generate_random_mailbox():
    response = requests.get(API_ENDPOINT + "?action=genRandomMailbox")
    data = response.json()
    
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    else:
        raise Exception("Failed to generate a random mailbox. Response: " + str(data))

def check_mailbox(email):
    username, domain = email.split('@')
    url = f"{API_ENDPOINT}?action=getMessages&login={username}&domain={domain}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Failed to retrieve messages. Status Code: {response.status_code}")
        return
    
    try:
        data = response.json()
        if isinstance(data, list):
            for message in data:
                message_id = message.get('id')
                message_details = get_message_details(email, message_id)
                if message_details:
                    print("Received code:", message_details['body'])
                    return
        else:
            raise ValueError
    except (json.JSONDecodeError, ValueError):
        print(f"Error: Invalid JSON response. Unable to retrieve messages. Response Text: {response.text}")

def get_message_details(email, message_id):
    username, domain = email.split('@')
    url = f"{API_ENDPOINT}?action=readMessage&login={username}&domain={domain}&id={message_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Failed to read the message. Status Code: {response.status_code}")
        return None
    
    try:
        data = response.json()
        return {
            'body': data.get('body'),
            'subject': data.get('subject'),
            'date': data.get('date'),
            'attachments': data.get('attachments')
        }
    except (json.JSONDecodeError, ValueError):
        print(f"Error: Invalid JSON response. Unable to read the message. Response Text: {response.text}")
        return None

def main():
    email = generate_random_mailbox()
    print("Generated email:", email)
    print("Waiting for code...")
    while True:
        check_mailbox(email)
        time.sleep(5)

if __name__ == '__main__':
    main()