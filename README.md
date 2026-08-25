# PubMed Searcher

A Python utility for searching PubMed articles and ranking them using the BM25 relevance algorithm.

## Overview

This tool provides programmatic access to the [PubMed public API](https://www.ncbi.nlm.nih.gov/home/develop/api/) for querying biomedical literature and implements the **BM25 (Best Matching 25)** algorithm for ranking retrieved documents by relevance. BM25 is a probabilistic ranking function that incorporates term frequency, inverse document frequency, and document length normalization—standard in modern information retrieval systems.

## Features

- **PubMed API Integration**: Query millions of biomedical literature articles via NCBI Entrez services
- **BM25 Ranking Algorithm**: Probabilistic relevance ranking with IDF weighting and document length normalization
- **Metadata Extraction**: Retrieves titles, abstracts, author lists, publication dates, and PubMed URLs
- **Error Handling**: Comprehensive exception handling for network errors and API failures
- **Logging**: Structured logging for debugging and performance monitoring

## Requirements

- Python 3.7 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aaravsedja/pubmed-searcher.git
cd pubmed-searcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Dependencies:
- `requests` (2.31.0+): HTTP client library for API requests
- `rank-bm25` (0.2.2+): BM25 ranking implementation

## Usage

### Command Line

Run the script with default parameters:

```bash
python pubmed_search.py
```

To modify search parameters, edit the `main()` function in `pubmed_search.py`:

```python
def main():
    query = "machine learning healthcare"  # Search query
    max_results = 30                       # Max articles to fetch
    top_k = 10                             # Results to display
```

### Programmatic API

```python
from pubmed_search import search_pubmed, fetch_pubmed_articles, rank_articles_bm25, display_results

# Query PubMed
query = "artificial intelligence clinical diagnosis"
pmids = search_pubmed(query, max_results=50)

# Fetch article metadata
articles = fetch_pubmed_articles(pmids)

# Rank articles using BM25
ranked_articles = rank_articles_bm25(articles, query)

# Display formatted results
display_results(ranked_articles, top_k=10)
```

## API Reference

### search_pubmed(query, max_results=20, rettype='json')

Searches PubMed and returns article identifiers.

**Parameters:**
- `query` (str): Search query string using PubMed query syntax
- `max_results` (int): Maximum number of results to retrieve (default: 20)
- `rettype` (str): Return format, typically 'json' (default: 'json')

**Returns:**
- `list[str]`: List of PubMed IDs (PMIDs)

**Raises:**
- `requests.exceptions.RequestException`: Network or API errors

### fetch_pubmed_articles(pmids)

Retrieves detailed metadata for specified articles.

**Parameters:**
- `pmids` (list[str]): List of PubMed IDs

**Returns:**
- `list[dict]`: Article records with fields:
  - `pmid` (str): PubMed identifier
  - `title` (str): Article title
  - `abstract` (str): Article abstract
  - `authors` (list[dict]): Author records with 'name' field
  - `pubdate` (str): Publication date
  - `source` (str): Journal/source name
  - `url` (str): Direct PubMed link

**Raises:**
- `requests.exceptions.RequestException`: Network or API errors

### rank_articles_bm25(articles, query)

Ranks articles using the BM25 relevance algorithm.

**Parameters:**
- `articles` (list[dict]): Article records from `fetch_pubmed_articles()`
- `query` (str): Original search query for relevance computation

**Returns:**
- `list[tuple]`: List of (article, score) tuples sorted by BM25 score (descending)

### display_results(ranked_articles, top_k=10)

Formats and prints ranked results.

**Parameters:**
- `ranked_articles` (list[tuple]): Output from `rank_articles_bm25()`
- `top_k` (int): Number of top results to display (default: 10)

## Algorithm Details

### BM25 Ranking

The BM25 algorithm computes relevance scores as:

```
BM25(D, Q) = Σ IDF(qi) * (f(qi, D) * (k1 + 1)) / (f(qi, D) + k1 * (1 - b + b * |D| / avgdl))
```

Where:
- `D` is the document (article)
- `Q` is the query
- `qi` are query terms
- `f(qi, D)` is term frequency in document
- `IDF(qi)` is inverse document frequency
- `k1` and `b` are tuning parameters (default: k1=2.0, b=0.75)
- `|D|` is document length
- `avgdl` is average document length in corpus

The implementation uses:
- Document = concatenation of title and abstract
- Tokenization: whitespace splitting with lowercasing
- IDF computation: logarithm-based with standard smoothing

### Processing Pipeline

1. **Search**: Query PubMed via NCBI Entrez esearch endpoint
2. **Fetch**: Retrieve article metadata via efetch endpoint
3. **Tokenize**: Split title and abstract into tokens
4. **Rank**: Compute BM25 scores for each document
5. **Sort**: Order results by descending score
6. **Display**: Format and output top-k results

## NCBI API Specifications

### Endpoints

- **esearch**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- **efetch**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

### Parameters

- `db`: Database name (pubmed)
- `term`: Search query with PubMed query syntax
- `retmax`: Maximum results per request
- `rettype`: Return format (json)
- `tool`: Application name (required by NCBI)
- `email`: Contact email (required by NCBI)

### Rate Limiting

- Public access: 3 requests per second maximum
- Recommended: Implement request throttling for batch operations
- API key authentication: Available for higher rate limits

### Query Syntax

PubMed supports field-specific searches:
- `term[TIAB]`: Search in title and abstract
- `term[AUTH]`: Search by author
- `term[PDAT]`: Search by publication date
- `term[JOUR]`: Search by journal

## Implementation Notes

- **Tokenization**: Simple whitespace splitting; does not use stemming or lemmatization
- **Language**: English-focused (no multilingual support)
- **Scoring**: BM25 scores are unbounded; absolute values are not comparable across queries
- **Fetching**: Batch requests limited to practical sizes due to API response sizes
- **Caching**: No built-in result caching; repeated queries trigger new API calls

## Limitations

- Rate-limited by NCBI (3 requests/second for public access)
- Requires internet connectivity for API access
- BM25 ranking based on title and abstract only (full text not available)
- Query support limited to standard PubMed query syntax
- No built-in citation or reference following

## Performance Considerations

For optimal performance with large result sets:
- Fetch articles in batches (API limits ~100 PMIDs per request)
- Implement request throttling to respect rate limits
- Cache results locally to avoid redundant API calls
- Consider indexing frequently searched queries

## Extending the Implementation

### Custom BM25 Parameters

Modify `rank_articles_bm25()` to adjust BM25 tuning:
```python
bm25 = BM25Okapi(documents, k1=1.5, b=0.75)
```

### Adding Full-Text Ranking

Extend metadata retrieval to include full article text where available.

### Query Optimization

Implement query expansion and synonym detection for improved recall.

### Parallel Processing

Use ThreadPoolExecutor for concurrent API requests to improve throughput.

## Error Handling

The script implements error handling for:
- Network connectivity issues (requests.exceptions.RequestException)
- API response errors (HTTP error codes)
- Empty result sets
- Malformed API responses

Errors are logged via Python's standard logging module at appropriate levels (INFO, WARNING, ERROR).

## Dependencies

See `requirements.txt` for exact versions. Core dependencies:

- **requests**: HTTP client for API communication
- **rank-bm25**: BM25 ranking implementation using Okapi variant

## References

- Okapi BM25: [Wikipedia](https://en.wikipedia.org/wiki/Okapi_BM25)
- NCBI Entrez Programming Utilities: [Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25499/)
- PubMed Help: [https://pubmed.ncbi.nlm.nih.gov/help/](https://pubmed.ncbi.nlm.nih.gov/help/)
- rank-bm25 Implementation: [GitHub](https://github.com/dorianbrown/rank_bm25)
- Robertson, S. (2004). Understanding Inverse Document Frequency. Journal of Documentation, 60(5), 503-520.

## License

Open source - MIT License

## Contributing

Pull requests and issue reports are welcome.
