# PubMed Searcher - Upgrade Roadmap

This document outlines enhancements to make the project more capable without using LLMs or embeddings.

## Phase 1: Core Enhancement (Priority: High)

### 1.1 Advanced Query Processing

Implement query parsing with support for:

**Boolean Operators:**
- AND, OR, NOT logic
- Parenthetical grouping
- Field-specific searches: `TITLE:term`, `AUTHOR:name`, `JOURNAL:name`

**Query Syntax Support:**
```python
# Examples
"(machine learning OR deep learning) AND (clinical OR diagnosis)"
"AUTHOR:Smith AND TITLE:diagnosis"
"2020-2024[PDAT]"  # Date range
```

### 1.2 Advanced Ranking Strategies

Replace simple BM25 with composite ranking:

**Multi-Signal Ranking:**
```python
final_score = (
    w1 * bm25_score +
    w2 * recency_score +
    w3 * author_score +
    w4 * journal_score
)
```

### 1.3 Result Filtering & Refinement

Implement post-retrieval filtering by:
- Date range
- Article type
- Language
- Abstract availability

### 1.4 Deduplication

Remove duplicates using:
- Exact PMID matching
- Jaccard similarity on token sets
- Title similarity (Levenshtein distance)

## Phase 2: Data Analysis & Understanding (Priority: High)

### 2.1 TF-IDF Analysis

Corpus-level term analysis using scikit-learn.

### 2.2 Statistical Text Analysis

Extract publication patterns:
- Term frequency distribution
- Temporal distribution
- Author productivity
- Journal distribution

### 2.3 Clustering & Topic Detection

Group semantically related results using:
- TF-IDF vectorization
- Cosine similarity
- Hierarchical clustering

## Phase 3: Data Persistence & Export (Priority: Medium)

### 3.1 Local Caching

SQLite database for offline access.

### 3.2 Export Formats

Support: BibTeX, RIS, JSON, CSV, Markdown

### 3.3 Deduplication & Merging

Handle duplicate results across searches.

## Phase 4: Advanced Analytics (Priority: Medium)

### 4.1 Author Network Analysis

Build collaboration networks using NetworkX.

### 4.2 Temporal Analysis

Analyze publication trends over time.

### 4.3 Journal Impact Analysis

Rank results by journal prominence.

## Dependencies

```
requests==2.31.0
rank-bm25==0.2.2
scikit-learn>=1.0.0
networkx>=2.6
nltk>=3.6
matplotlib>=3.3
seaborn>=0.11
pandas>=1.2
python-Levenshtein>=0.12
```
