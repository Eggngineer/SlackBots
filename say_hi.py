import os

from slack_sdk.web import WebClient

client = WebClient(token=os.environ["SLACK_API_TOKEN"])
response = client.chat_postMessage(text=":wave: <https://www.notion.so/Home-af2607e0197a44a89acb804c74d94b4a|SlackBotリポジトリが更新されました！>", channel="#random")
print(response)
