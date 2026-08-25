#!/usr/bin/env python3
"""
PubMed Article Search and BM25 Ranking

This script searches the PubMed API for articles matching a query and ranks
them using the BM25 algorithm based on relevance to the search terms.
"""

import requests
import json
from typing import List, Dict, Tuple
from urllib.parse import urlencode
import logging
from rank_bm25 import BM25Okapi

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# PubMed API endpoints
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(query: str, max_results: int = 20, rettype: str = "json") -> List[str]:
    """
    Search PubMed for articles matching the query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to fetch (default: 20)
        rettype: Return type (json or xml)
    
    Returns:
        List of PubMed IDs (PMIDs)
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "rettype": rettype,
        "tool": "pubmed-searcher",
        "email": "user@example.com",  # NCBI requests an email
    }
    
    try:
        logger.info(f"Searching PubMed for: {query}")
        response = requests.get(PUBMED_SEARCH_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        pmids = data.get("result", {}).get("uids", [])
        logger.info(f"Found {len(pmids)} articles")
        
        return pmids
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching PubMed: {e}")
        return []


def fetch_pubmed_articles(pmids: List[str]) -> List[Dict]:
    """
    Fetch detailed information about articles from PubMed.
    
    Args:
        pmids: List of PubMed IDs
    
    Returns:
        List of article dictionaries with metadata
    """
    if not pmids:
        return []
    
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "json",
        "tool": "pubmed-searcher",
        "email": "user@example.com",
    }
    
    try:
        logger.info(f"Fetching details for {len(pmids)} articles")
        response = requests.get(PUBMED_FETCH_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("result", {}).get("uids", [])
        
        # Build article list with relevant metadata
        article_list = []
        for uid in articles:
            if uid == "uids":
                continue
            
            article_data = data["result"][uid]
            article_info = {
                "pmid": uid,
                "title": article_data.get("title", ""),
                "abstract": article_data.get("abstract", ""),
                "authors": article_data.get("authors", []),
                "pubdate": article_data.get("pubdate", ""),
                "source": article_data.get("source", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
            }
            article_list.append(article_info)
        
        logger.info(f"Successfully fetched {len(article_list)} articles")
        return article_list
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching articles: {e}")
        return []


def rank_articles_bm25(articles: List[Dict], query: str) -> List[Tuple[Dict, float]]:
    """
    Rank articles using BM25 algorithm based on relevance to query.
    
    Args:
        articles: List of article dictionaries
        query: Original search query
    
    Returns:
        List of (article, score) tuples sorted by BM25 score (descending)
    """
    if not articles:
        return []
    
    # Prepare documents for BM25
    # Combine title and abstract for ranking
    documents = []
    for article in articles:
        # Tokenize by whitespace and lowercase
        text = (article.get("title", "") + " " + article.get("abstract", "")).lower()
        tokens = text.split()
        documents.append(tokens)
    
    # Initialize BM25
    bm25 = BM25Okapi(documents)
    
    # Tokenize query
    query_tokens = query.lower().split()
    
    # Score all documents
    scores = bm25.get_scores(query_tokens)
    
    # Pair articles with scores and sort
    ranked = list(zip(articles, scores))
    ranked.sort(key=lambda x: x[1], reverse=True)
    
    logger.info(f"Ranked {len(ranked)} articles using BM25")
    return ranked


def display_results(ranked_articles: List[Tuple[Dict, float]], top_k: int = 10):
    """
    Display ranked results in a readable format.
    
    Args:
        ranked_articles: List of (article, score) tuples
        top_k: Number of top results to display
    """
    print("\n" + "=" * 80)
    print("PubMed Search Results (Ranked by BM25 Relevance)")
    print("=" * 80 + "\n")
    
    for idx, (article, score) in enumerate(ranked_articles[:top_k], 1):
        print(f"Rank #{idx} (BM25 Score: {score:.2f})")
        print(f"Title: {article['title']}")
        print(f"PMID: {article['pmid']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['pubdate']}")
        print(f"Journal: {article['source']}")
        
        if article.get("authors"):
            authors_str = ", ".join([a.get("name", "") for a in article["authors"][:3]])
            print(f"Authors: {authors_str}" + (" et al." if len(article["authors"]) > 3 else ""))
        
        if article.get("abstract"):
            abstract_preview = article["abstract"][:300] + "..." if len(article["abstract"]) > 300 else article["abstract"]
            print(f"Abstract: {abstract_preview}")
        
        print("-" * 80 + "\n")


def main():
    """Main function to run the PubMed search."""
    # Example search query
    query = "machine learning healthcare"
    max_results = 30
    top_k = 10
    
    print(f"\nSearching PubMed for: '{query}'")
    print(f"Maximum results: {max_results}, Top results to display: {top_k}\n")
    
    # Step 1: Search PubMed
    pmids = search_pubmed(query, max_results=max_results)
    
    if not pmids:
        logger.warning("No articles found")
        return
    
    # Step 2: Fetch article details
    articles = fetch_pubmed_articles(pmids)
    
    if not articles:
        logger.warning("Could not fetch article details")
        return
    
    # Step 3: Rank articles using BM25
    ranked_articles = rank_articles_bm25(articles, query)
    
    # Step 4: Display results
    display_results(ranked_articles, top_k=top_k)


if __name__ == "__main__":
    main()
