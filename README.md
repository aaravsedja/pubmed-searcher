# PubMed Searcher

A Python utility for searching PubMed articles and ranking them using the BM25 relevance algorithm.

## Overview

This tool searches the [PubMed public API](https://www.ncbi.nlm.nih.gov/home/develop/api/) for scientific articles matching your query and ranks them by relevance using the **BM25 (Best Matching 25)** algorithm—a probabilistic ranking function widely used in information retrieval.

## Features

- 🔍 **PubMed Integration**: Search millions of biomedical literature articles
- 📊 **BM25 Ranking**: Intelligent relevance ranking based on term frequency and document length normalization
- 📄 **Rich Metadata**: Retrieve article titles, abstracts, authors, publication dates, and direct PubMed links
- 📝 **Formatted Output**: Clean, readable display of ranked results with summaries
- 🛡️ **Error Handling**: Graceful handling of API errors and network issues
- 📋 **Logging**: Comprehensive logging for debugging and monitoring

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/aaravsedja/pubmed-searcher.git
cd pubmed-searcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP library for API calls
- `rank-bm25` - BM25 ranking implementation

## Usage

### Basic Usage

Edit the search query in `pubmed_search.py` and run:

```bash
python pubmed_search.py
```

### Programmatic Usage

```python
from pubmed_search import search_pubmed, fetch_pubmed_articles, rank_articles_bm25, display_results

# Search for articles
query = "artificial intelligence clinical diagnosis"
pmids = search_pubmed(query, max_results=30)

# Fetch detailed information
articles = fetch_pubmed_articles(pmids)

# Rank using BM25
ranked_articles = rank_articles_bm25(articles, query)

# Display results
display_results(ranked_articles, top_k=10)
```

### Customization

Modify these parameters in `main()`:

```python
query = "your search terms here"  # Change the search query
max_results = 30                  # Number of articles to fetch (default: 20)
top_k = 10                        # Number of results to display
```

## How It Works

### 1. PubMed Search
The script uses the NCBI Entrez API to search PubMed's database with your query. This returns a list of PubMed IDs (PMIDs) for matching articles.

### 2. Article Fetching
For each PMID, the script retrieves:
- Article title
- Abstract
- Author information
- Publication date
- Journal/source
- PubMed URL

### 3. BM25 Ranking
The BM25 algorithm ranks articles based on:
- **Term Frequency (TF)**: How often query terms appear in each document
- **Inverse Document Frequency (IDF)**: How rare the term is across all documents
- **Document Length Normalization**: Prevents bias toward longer documents

Higher scores indicate better relevance to your query.

### 4. Display Results
Results are formatted with key metadata and sorted by BM25 score.

## Output Example

```
================================================================================
PubMed Search Results (Ranked by BM25 Relevance)
================================================================================

Rank #1 (BM25 Score: 8.45)
Title: Deep Learning Applications in Clinical Diagnosis
PMID: 35123456
URL: https://pubmed.ncbi.nlm.nih.gov/35123456/
Published: 2023 Jan 15
Journal: Nature Medicine
Authors: Smith J, Johnson K, Williams R et al.
Abstract: Deep learning has revolutionized clinical diagnostics...
```

## API Notes

- **Rate Limiting**: NCBI requests a maximum of 3 requests per second for public users
- **Email Required**: The script includes an email parameter (required by NCBI)
- **Documentation**: [NCBI Entrez API Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25499/)

## Limitations

- Free NCBI API access has rate limits
- Requires internet connection to access PubMed
- BM25 ranking is based on titles and abstracts only
- Large result sets may take time to fetch

## Future Enhancements

- [ ] Filter by publication date range
- [ ] Filter by article type (reviews, research, etc.)
- [ ] Export results to CSV/JSON
- [ ] Advanced query operators support
- [ ] Caching to reduce API calls
- [ ] Parallel fetching for improved performance
- [ ] Integration with citation networks
- [ ] Custom BM25 parameter tuning

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open a GitHub issue on the [repository](https://github.com/aaravsedja/pubmed-searcher).

## References

- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
- [NCBI Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25499/)
- [PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/)
- [rank-bm25 Documentation](https://github.com/dorianbrown/rank_bm25)
