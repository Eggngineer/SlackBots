import os

import arxiv
from googletrans import Translator
from slack_sdk.web import WebClient


def _init_translator() -> Translator:
    return Translator()


def _init_client() -> WebClient:
    token = os.environ["G_TRANS_TOKEN"]

    return WebClient(token=token)


def search_arXiv(keyward: str=None, rankMax: int=None) -> arxiv.Search:
    if keyward is None:
        keyward = input("Search for: ")
    if rankMax is None:
        rankMax = int(input("Top N: "))
    query = f'abs:"point cloud registration"'
    max_results = rankMax

    info = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    return info


def format_summary(summary: str) -> str:
    summary = summary.replace("\n", " ")
    summary = summary.replace(". ", ".\n\n")

    return summary


def main() -> None:
    translator = _init_translator()
    client = _init_client()
    info = search_arXiv(keyward='Point Cloud',rankMax=5)

    for rank, paper in enumerate(info.results()):
        paper_info = {
            "title_en": paper.title,
            "title_ja": translator.translate(text=paper.title, dest="ja").text,
            "summary_en": paper.summary,
        }

        paper_info["summary_en"] = format_summary(paper_info["summary_en"])
        paper_info["summary_ja"] = translator.translate(
            text=paper_info["summary_en"], dest="ja"
        ).text
        paper_info['url'] = paper.pdf_url

        content = f"""
> {rank+1}.  <{paper_info['url']}|{paper_info['title_en']}> ( {paper_info['title_ja']} )

```
{paper_info['summary_ja']}
```

        """

        _ = client.chat_postMessage(
            text=content,
            channel="#todays_paper",
        )




if __name__ == "__main__":
    main()
