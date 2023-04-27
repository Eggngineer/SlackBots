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
    info = search_arXiv(keyward='point cloud',rankMax=5)

    for paper in info.results():
        paper_info = {
            "title_en": paper.title,
            "title_ja": translator.translate(text=paper.title, dest="ja").text,
            "summary_en": paper.summary,
        }

        paper_info["summary_en"] = format_summary(paper_info["summary_en"])
        paper_info["summary_ja"] = translator.translate(
            text=paper_info["summary_en"], dest="ja"
        ).text

        print(f'{paper_info["title_en"]} ( {paper_info["title_ja"]} )')
        print('"""\n')
        print(paper_info["summary_en"])
        print('"""\n')
        print(paper_info["summary_ja"])
        print('"""')


if __name__ == "__main__":
    main()
