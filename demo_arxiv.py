import arxiv

title = 'Dual Cross-Attention Learning for Fine-Grained Visual Categorization and Object Re-Identification'
search = arxiv.Search(
    query=f"ti:{title}",
    max_results=1,
    sort_by=arxiv.SortCriterion.Relevance,
)

for r in search.results():
    print(r.title)