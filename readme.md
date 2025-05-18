# Extract-Explain-Abstract Framework

This repository provides a pipeline for generating and evaluating extractive and abstractive summaries on legal datasets using LLMs. It supports chunked text processing, multiple summary types (EEA, EA, and abstract), and evaluation using ROUGE, BERTScore, and domain-specific semantic similarity using InLegalBERT.

---

## Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA 11.7+
- `transformers`, `nltk`, `pandas`, `scikit-learn`, `bert-score`

Ensure that `punkt` is downloaded for NLTK:

```bash
python -m nltk.downloader punkt
