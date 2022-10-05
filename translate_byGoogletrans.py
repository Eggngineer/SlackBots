import arxiv
from googletrans import Translator
import os
from slack_sdk.web import WebClient

client = WebClient(token=os.environ["G_TRANS_TOKEN"])

translator = Translator()

RANK = 5

search = arxiv.Search(
  query = 'abs:"point cloud registration"',
  max_results = RANK,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

i=1
for paper in search.results():
    title_en = paper.title
    summary_en = paper.summary.replace('\n', ' ')
    url = paper.pdf_url

    summary_ja = str(i)+". "+title_en+"\n"+translator.translate(summary_en,dest='ja').text+"\n"+url+"\n---"

    response = client.chat_postMessage(text=summary_ja, channel="#todays_paper")

    i += 1

    