import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SLACK_APP_TOKEN = os.getenv("SLACKBOT_OAUTH")


def post_slack_message(text: str) -> bool:
    url = "https://hooks.slack.com/services/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"
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(url, headers=headers, data=json.dumps(data))
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
