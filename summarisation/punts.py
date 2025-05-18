import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from collections import Counter
from nltk.tokenize import sent_tokenize
import nltk

# Helper for model and generic punts setup
def load_punt_detection_model_and_embeddings(model_name="sentence-transformers/paraphrase-mpnet-base-v2"):
    model = SentenceTransformer(model_name)
    generic_punts = [
        "I cannot provide legal advice.",
        "Please consult a professional.",
        "I'm unable to answer that.",
        "I cannot generate a summary.",
        "I cannot generate a summary of a legal judgment.",
        "Please provide text to summarise.",
        "Provide text that you require for me to summarise",
        "Please consult a lawyer.",
        "I cannot provide a summary of the judgment in words or less."
    ]
    generic_embeddings = model.encode(generic_punts)
    return model, generic_embeddings, generic_punts

def is_punt_response(response, model, generic_embeddings, threshold=0.65):
    """
    Checks whether the response is a generic 'punt', using cosine similarity.
    """
    try:
        response_embedding = model.encode([response])
        similarities = cosine_similarity(response_embedding, generic_embeddings)[0]
        return any(sim > threshold for sim in similarities)
    except Exception:
        return True  # Treat encoding errors as punts

def has_ngram_repetition(text, n=3):
    tokens = text.split()
    ngrams = [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    count = Counter(ngrams)
    return any(c > 1 for c in count.values())

def has_jaccard_repetition(text, threshold=0.95):
    sentences = sent_tokenize(text)
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            set1 = set(sentences[i].lower().split())
            set2 = set(sentences[j].lower().split())
            if len(set1 | set2) == 0:
                continue
            sim = len(set1 & set2) / len(set1 | set2)
            if sim > threshold:
                return True
    return False

def analyze_punts_and_repetitions(
    df: pd.DataFrame,
    model=None,
    generic_embeddings=None,
    summary_cols=None
):

    if summary_cols is None:
        summary_cols = ['abstract_summary', 'ea_summary', 'eea_summary']

    if model is None or generic_embeddings is None:
        model, generic_embeddings, _ = load_punt_detection_model_and_embeddings()
    results = {}

    for col in summary_cols:
        punts = 0
        ngram_repeats = 0
        jaccard_repeats = 0
        total = 0

        for _, row in df.iterrows():
            response = str(row.get(col, ""))
            total += 1
            if is_punt_response(response, model, generic_embeddings):
                punts += 1
            if has_ngram_repetition(response):
                ngram_repeats += 1
            if has_jaccard_repetition(response):
                jaccard_repeats += 1

        results[col] = {
            "punt_count": punts,
            "ngram_repetition_count": ngram_repeats,
            "jaccard_repetition_count": jaccard_repeats,
            "total": total
        }

    return results

def analyze_punts_and_repetitions_from_csv(csv_path, model=None, generic_embeddings=None, summary_cols=None):
    """
    Loads a CSV and analyzes punts and repetitions.
    """
    df = pd.read_csv(csv_path, encoding="utf-8")
    return analyze_punts_and_repetitions(df, model=model, generic_embeddings=generic_embeddings, summary_cols=summary_cols)