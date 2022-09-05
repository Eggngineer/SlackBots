import os
from slack_sdk.web import WebClient
client = WebClient(token=os.environ["SLACK_API_TOKEN"])
response = client.chat_postMessage(text=":wave: SlackBotリポジトリが更新されました！", channel="#random")
print(response)
