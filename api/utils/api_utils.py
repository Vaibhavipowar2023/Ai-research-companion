# api_utils.py
import requests
import xmltodict

ARXIV_BASE = "http://export.arxiv.org/api/query"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_arxiv(query, max_results=10):
    url = f"{ARXIV_BASE}?search_query=all:{query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    res = requests.get(url, timeout=20)
    res.raise_for_status()
    try:
        data = xmltodict.parse(res.text)
    except Exception:
        return []
    entries = data.get("feed", {}).get("entry", [])
    if isinstance(entries, dict):
        entries = [entries]
    papers = []
    for e in entries:
        authors = e.get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        papers.append({
            "title": (e.get("title", "") or "").strip(),
            "abstract": (e.get("summary", "") or "").strip(),
            "link": e.get("id", ""),
            "source": "arXiv",
            "authors": [a.get("name", "") for a in authors if isinstance(a, dict)]
        })
    return papers

def fetch_pubmed(query, retmax=10):
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}
    res = requests.get(PUBMED_ESEARCH, params=params, timeout=20)
    res.raise_for_status()
    ids = res.json().get("esearchresult", {}).get("idlist", [])
    papers = []
    for pid in ids:
        try:
            res2 = requests.get(PUBMED_EFETCH, params={"db": "pubmed", "id": pid, "retmode": "xml"}, timeout=20)
            doc = xmltodict.parse(res2.text)
            art = doc.get("PubmedArticleSet", {}).get("PubmedArticle", {})
            if not art:
                continue
            article = art.get("MedlineCitation", {}).get("Article", {})
            abstract = ""
            if "Abstract" in article and article["Abstract"]:
                abs_text = article["Abstract"].get("AbstractText")
                abstract = " ".join(abs_text) if isinstance(abs_text, list) else (abs_text or "")
            papers.append({
                "title": article.get("ArticleTitle", ""),
                "abstract": abstract,
                "link": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
                "source": "PubMed",
                "authors": []
            })
        except Exception:
            # skip any single failure but continue
            continue
    return papers
