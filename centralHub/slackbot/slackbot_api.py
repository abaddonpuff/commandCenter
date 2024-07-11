import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SLACK_APP_TOKEN = os.getenv("SLACKBOT_OAUTH")
SLACk_WEBHOOK = os.getenv("SLACK_C2NOTIFIER")


def post_slack_message(text: str) -> bool:
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(SLACk_WEBHOOK, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return True
    else:
        return False


def main():
    text = "Bread and milk"
    post_slack_message(text)
    pass


if __name__ == "__main__":
    main()
