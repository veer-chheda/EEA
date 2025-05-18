import os
import pandas as pd
from config import MODELS, DATASETS
from dataset import DatasetHandler
from evaluate import (
    compute_rouge_scores_batch,
    compute_bertscore_batch,
    compute_semantic_similarity
)
from summarise import generate_summary
from extractive import extraction
from .preprocess import chunk_text_by_word_limit
from config import MODELS, MAX_SEQ_LEN, DATASET_INDEX, DATASET_DOC, DATASETS, SUMMARY_NAME, THRESHOLD
from model import ModelLoader

def chunked_generate_summary(input_text, model_name, summary_type, dataset_name, max_len, model, tokenizer):

    chunks = chunk_text_by_word_limit(input_text, word_limit=max_len)
    chunk_summaries = [
        generate_summary(chunk, model, tokenizer, model_name=model_name, type=summary_type, dataset=dataset_name)
        for chunk in chunks
    ]
    combined_summary = " ".join(chunk_summaries)

    final_summary = generate_summary(combined_summary, model, tokenizer, model_name=model_name, type=summary_type, dataset=dataset_name)
    return final_summary

def process_dataset(
    dataset_name: str,
    model_key: str,
    output_csv: str,
    split: str = "test"
):
    index = DATASET_INDEX[dataset_name]
    max_length = MAX_SEQ_LEN[model_key]
    doc_name = DATASET_DOC[dataset_name]
    summary_name = SUMMARY_NAME[dataset_name]
    threshold = THRESHOLD[dataset_name]
    model_name = MODELS[model_key]
    print(f"Loading {dataset_name} ...")
    
    model_loader = ModelLoader()
    model, tokenizer = model_loader.load_model(model_name, max_length)
    
    if dataset_name not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    dataset_handler = DatasetHandler()
    train_df, test_df = dataset_handler.dataset_loader(dataset_name)
    df = test_df if split == "test" else train_df

    print("Generating chunked summaries and references...")
    results = []
    for i, row in df.iterrows():
        doc_id = row[index]
        input_text = row[doc_name]
        reference_summary = row[summary_name]

        _, extractive_summary = extraction(input_text, threshold)
        eea_summary = chunked_generate_summary(extractive_summary, model_key, "eea", dataset_name, max_length, model, tokenizer)
        ea_summary  = chunked_generate_summary(extractive_summary, model_key, "ea",  dataset_name, max_length, model, tokenizer)
        abstract    = chunked_generate_summary(input_text, model_key, "abstract", dataset_name, max_length, model, tokenizer)

        results.append({
            "dataset": dataset_name,
            "model": model_key,
            "doc_id": doc_id,
            "reference_summary": reference_summary,
            "eea_summary": eea_summary,
            "ea_summary": ea_summary,
            "abstract": abstract
        })

    results_df = pd.DataFrame(results)

    print("Computing ROUGE...")
    for summ_type in ["eea_summary", "ea_summary", "abstract"]:
        rouges = compute_rouge_scores_batch(
            results_df[summ_type].tolist(),
            results_df["reference_summary"].tolist()
        )
        results_df[f"{summ_type}_rouge1"] = [r["rouge1"] for r in rouges]
        results_df[f"{summ_type}_rouge2"] = [r["rouge2"] for r in rouges]
        results_df[f"{summ_type}_rougeL"] = [r["rougeL"] for r in rouges]

    print("Computing BERTScore...")
    for summ_type in ["eea_summary", "ea_summary", "abstract"]:
        berts = compute_bertscore_batch(
            results_df[summ_type].tolist(),
            results_df["reference_summary"].tolist()
        )
        results_df[f"{summ_type}_bertscore_p"] = berts["precision"]
        results_df[f"{summ_type}_bertscore_r"] = berts["recall"]
        results_df[f"{summ_type}_bertscore_f1"] = berts["f1"]

    print("Computing InLegalBERT similarity...")
    for summ_type in ["eea_summary", "ea_summary", "abstract"]:
        sims = compute_semantic_similarity(
            results_df[summ_type].tolist(),
            results_df["reference_summary"].tolist()
        )
        results_df[f"{summ_type}_inlegalbert_sim"] = sims

    results_df.to_csv(output_csv, index=False)
    print(f"Saved all results to {output_csv}")


# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("--dataset", type=str, required=True)
#     parser.add_argument("--model", type=str, required=True)
#     parser.add_argument("--output_csv", type=str, required=True)
#     parser.add_argument("--split", type=str, default="test")
#     args = parser.parse_args()

#     process_dataset(
#         dataset_name=args.dataset,
#         model_key=args.model,
#         output_csv=args.output_csv,
#         split=args.split
#     )