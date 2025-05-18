import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer
from bert_score import BERTScorer


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TextDataset(Dataset):
    def __init__(self, texts):
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx]


def embed_texts(texts, tokenizer, model, device, batch_size=8):
    embeddings = []
    dataloader = DataLoader(TextDataset(texts), batch_size=batch_size)
    with torch.no_grad():
        for batch in dataloader:
            batch = list(batch)
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
            outputs = model(**inputs)
            attention_mask = inputs['attention_mask'].unsqueeze(-1)
            hidden_states = outputs.last_hidden_state * attention_mask
            summed = hidden_states.sum(dim=1)
            counts = attention_mask.sum(dim=1).clamp(min=1e-9)
            mean_pooled = summed / counts
            embeddings.append(mean_pooled.cpu())
    return torch.cat(embeddings, dim=0).numpy()


def compute_semantic_similarity(
    generated_summaries, reference_summaries, model_name="law-ai/InLegalBERT", batch_size=8
):
    assert len(generated_summaries) == len(reference_summaries), "Input lists must match length"
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    model.eval()
    gen_emb = embed_texts(generated_summaries, tokenizer, model, device, batch_size)
    ref_emb = embed_texts(reference_summaries, tokenizer, model, device, batch_size)
    scores = [cosine_similarity([g],[r])[0][0] for g, r in zip(gen_emb, ref_emb)]
    return scores


def compute_rouge_scores_batch(generated_summaries, reference_summaries):
    assert len(generated_summaries) == len(reference_summaries), "Input lists must match length"
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    results = []
    for g, r in zip(generated_summaries, reference_summaries):
        scores = scorer.score(r, g)
        results.append({
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        })
    return results


def compute_bertscore_batch(
    generated_summaries,
    reference_summaries,
    model_name="roberta-large",
    batch_size=8,
    idf=False,
    lang="en"
):
    assert len(generated_summaries) == len(reference_summaries), "Input lists must match length"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    scorer = BERTScorer(
        model_type=model_name,
        lang=lang,
        device=device,
        idf=idf,
        batch_size=batch_size,
        rescale_with_baseline=False
    )
    P, R, F1 = scorer.score(generated_summaries, reference_summaries, batch_size=batch_size, verbose=True)
    return {
        "precision": P.cpu().numpy().tolist(),
        "recall": R.cpu().numpy().tolist(),
        "f1": F1.cpu().numpy().tolist()
    }


# def main():

#     generated_summaries = [
#         "The Supreme Court held that the eviction was valid under Section 14.",
#         "The accused was acquitted due to lack of evidence."
#     ]
#     reference_summaries = [
#         "Under Section 14, the eviction was ruled lawful by the apex court.",
#         "Owing to insufficient proof, the court exonerated the defendant."
#     ]

#     print("Semantic Similarity (LegalBERT Cosine):")
#     sim_scores = compute_semantic_similarity(generated_summaries, reference_summaries)
#     for i, score in enumerate(sim_scores):
#         print(f"Pair {i+1}: {score:.4f}")

#     print("\nROUGE Scores:")
#     rouge_scores = compute_rouge_scores_batch(generated_summaries, reference_summaries)
#     for i, res in enumerate(rouge_scores):
#         print(f"Pair {i+1}: {res}")

#     print("\nBERTScore (Precision, Recall, F1):")
#     bert_scores = compute_bertscore_batch(generated_summaries, reference_summaries)
#     for i, (p, r, f1) in enumerate(zip(bert_scores["precision"], bert_scores["recall"], bert_scores["f1"])):
#         print(f"Pair {i+1}: P={p:.4f} R={r:.4f} F1={f1:.4f}")


# # if __name__ == "__main__":
# #     main()