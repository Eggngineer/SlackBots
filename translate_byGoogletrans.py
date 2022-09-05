import arxiv
from googletrans import Translator
import os
from slack_sdk.web import WebClient

client = WebClient(token=os.environ["G_TRANS_TOKEN"])

translator = Translator()

RANK = 5

search = arxiv.Search(
  query = "point cloud",
  max_results = RANK,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

i=1
for paper in search.results():
    title_en = paper.title
    summary_en = paper.summary
    
    title_en = title_en.replace('\n', ' ')
    summary_en = summary_en.replace('\n', ' ')

    summary_ja = translator.translate(summary_en,dest='ja').text
    response = client.chat_postMessage(text=summary_ja, channel="#random")
    print(i,'.'+'"'+title_en+'"')
    print(summary_ja)
    print("---")

    i += 1

    