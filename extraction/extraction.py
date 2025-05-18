import re
from collections import OrderedDict
from math import log
import json
import nltk
from nltk.corpus import stopwords
from rouge_score import rouge_scorer
from categorical_corpus import categorical_pairs, categorical_phrases
from datasets import load_dataset
import pandas as pd

# nltk.download('punkt')
# nltk.download('stopwords')

# Abbreviation patterns
abbreviations = set([
    "e.g.", "i.e.", "etc.", "vs.", "cf.", "Dr.", "Mr.", "Ms.", "Mrs.", "Co.",
    "Inc.", "Ltd.", "Corp.", "Prof.", "Sr.", "Jr.", "A.M.", "P.M.", "St.", "no.", "No.", "E.g.", "Nos.", "v."
])

# Summary division percentages based on categories
summary_division = {'Introduction': 10, 'Context': 24, 'Analysis': 60, 'Conclusion': 6}

def preprocess_text(file):
    """
    Reads a file and applies preprocessing steps to clean and tokenize text.
    """
    with open(file, 'r') as f:
        text = f.read()
    
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)  # Remove control characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

    text = re.sub(r'\b\d+\.\s', '', text)

    sentences = nltk.sent_tokenize(text)
    sentences = merge_abbreviated_sentences(sentences)
    
    return sentences, list(range(len(sentences)))

def merge_abbreviated_sentences(sentences):
    """
    Merges sentences improperly split due to abbreviations.
    """
    merged_sentences = []
    buffer = ""

    for sent in sentences:
        if any(sent.strip().endswith(abbr) for abbr in abbreviations):
            buffer += " " + sent.strip()
        elif re.match(r".*\b[A-Z]\.[A-Z]\.\s[A-Z][a-z]+,\s[J|C]\.?$", sent.strip()):
            # Merge judicial names like "D.S. Sinha, J."
            buffer += " " + sent.strip()
        else:
            # Append buffer if not empty before adding the current sentence
            if buffer:
                buffer += " " + sent.strip()
                merged_sentences.append(buffer.strip())
                buffer = ""
            else:
                merged_sentences.append(sent.strip())

    if buffer:
        merged_sentences.append(buffer.strip())

    return merged_sentences


def clean_and_normalize(sentence):
    """
    Cleans and normalizes a sentence by handling punctuation, removing extra spaces, 
    and converting to lowercase.
    """
    sentence = re.sub(r'[^a-zA-Z0-9\s\.\,]', '', sentence)  # Keep only alphanumerics and some punctuation
    sentence = re.sub(r'\s+', ' ', sentence).strip()  # Normalize whitespace
    return sentence.lower()

def calculate_tf_idf(text):
    """
    Calculate TF-IDF scores for words in the entire text.
    """
    text = ' '.join(text)
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))


    total_sentences = len(nltk.sent_tokenize(text))
    tf_idf_scores = {}
    for word in set(words):
        if word.lower() not in stop_words:
            tf = text.lower().count(word.lower())
            di = sum(1 for sent in nltk.sent_tokenize(text) if word.lower() in sent.lower())
            di = di if di != 0 else 0.5  # Avoid division by zero
            idf = log(total_sentences / di)
            tf_idf_scores[word.lower()] = tf * idf

    return tf_idf_scores

def calculate_sentence_tf_idf(sentence, tf_idf_scores):
    """
    Calculate the TF-IDF score for a sentence by summing the TF-IDF values of words in it.
    """
    words = sentence.split()
    score = sum(tf_idf_scores.get(word.lower(), 0) for word in words)
    return score

def rank_by_categories(sentence):
    """
    Rank the sentence based on matching cue phrases and pairs in different categories.
    """
    scores_categories = {
        'F': {'score': 0, 'phrases': []}, 'I': {'score': 0, 'phrases': []},
        'A': {'score': 0, 'phrases': []}, 'LR': {'score': 0, 'phrases': []},
        'SS': {'score': 0, 'phrases': []}, 'SP': {'score': 0, 'phrases': []},
        'R': {'score': 0, 'phrases': []}
    }
    scores = {'Introduction': 0, 'Context': 0, 'Analysis': 0, 'Conclusion': 0}

    for category, phrases in categorical_phrases.items():
        mapped_category = map_to_category(category)
        for phrase in phrases:
            if phrase in sentence:
                scores[mapped_category] += 1
                scores_categories[category]['score'] += 1
                scores_categories[category]['phrases'].append(phrase)

    for category, pairs in categorical_pairs.items():
        mapped_category = map_to_category(category)
        for start_phrase, end_phrases in pairs.items():
            if start_phrase in sentence:
                start_index = sentence.find(start_phrase)
                sentence_after_start = sentence[start_index + len(start_phrase):]
                matched_end_phrases = [end_phrase for end_phrase in end_phrases if end_phrase in sentence_after_start]
                scores[mapped_category] += len(matched_end_phrases)
                scores_categories[category]['score'] += len(matched_end_phrases)
                scores_categories[category]['phrases'].extend(matched_end_phrases)

 
    print("\nDetailed Scores by Categories:")
    for category, details in scores_categories.items():
        print(f"Category: {category}, Score: {details['score']}, Phrases: {details['phrases']}")

    return scores


def map_to_category(code):
    """
    Maps the code to the corresponding summary category.
    """
    mapping = {'F': 'Introduction', 'I': 'Introduction', 'A': 'Context', 'LR': 'Context',
               'SS': 'Analysis', 'SP': 'Analysis', 'R': 'Conclusion'}
    return mapping.get(code, 'Context')

def generate_summary_by_category(category_scores, total_words, max_percent_summary=34):
    """
    Generate a summary by selecting top sentences from each category according to summary division.
    """
    summary = []
    max_summary_words = min(4096, int((max_percent_summary / 100) * total_words))
    word_count = 0
    used_sentences = set()  

    for category, percent in summary_division.items():
        words_in_summary = int((percent / 100) * max_summary_words)
        category_sentences = category_scores[category]

        for sentence, score in category_sentences:
            if sentence not in used_sentences: 
                summary.append(sentence)
                used_sentences.add(sentence)  
                word_count += len(sentence.split())
                if word_count >= words_in_summary:
                    break

    return ' '.join(summary)

def save_sentences_to_json(category_scores, output_file='category_sentences.json'):
    """
    Saves the ranked sentences for each category to a JSON file.
    """
    category_dict = {category: [sentence for sentence, score in sentences] for category, sentences in category_scores.items()}
    
    with open(output_file, 'w') as json_file:
        json.dump(category_dict, json_file, indent=4)

def compute_rouge_scores(generated_summary, reference_summary):
    """
    Computes ROUGE scores for the generated summary against a reference summary.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_summary, generated_summary)

    return scores

def rank_sentences_by_category(file):
    """
    Reads a file and ranks sentences into different categories, considering preprocessing.
    """
    text, indices = preprocess_text(file)
    total_words = sum(len(sent.split()) for sent in text)
    tf_idf_scores = calculate_tf_idf(text)

    category_scores = {'Introduction': [], 'Context': [], 'Analysis': [], 'Conclusion': []}

    for para_idx, para in enumerate(text):
        sentences = nltk.sent_tokenize(para)
        for sent_idx, sentence in enumerate(sentences):

            cleaned_sentence = clean_and_normalize(sentence)

            scores = rank_by_categories(cleaned_sentence)

            tf_idf_score = calculate_sentence_tf_idf(cleaned_sentence, tf_idf_scores)

            for category in scores:
                category_scores[category].append((sentence, scores[category] + tf_idf_score))

    for category in category_scores:
        category_scores[category] = sorted(category_scores[category], key=lambda x: x[1], reverse=True)

    summary = generate_summary_by_category(category_scores, total_words)


    save_sentences_to_json(category_scores)

    return summary


def analyze_first_sentence(file):
    text, indices = preprocess_text(file)  # Preprocess text
    first_sentence = text[0] if text else ""  # Extract the first sentence
    if not first_sentence:
        print("No text found in the file.")
        return

    print(f"First Sentence: {first_sentence}")

    cleaned_sentence = clean_and_normalize(first_sentence)  
    words = nltk.word_tokenize(cleaned_sentence) 
    scores = rank_by_categories(cleaned_sentence)  

    word_analysis = []
    for word in words:
        word_score = {'word': word, 'categories': {}}
        for category, phrases in categorical_phrases.items():
            mapped_category = map_to_category(category)
            if any(phrase in word for phrase in phrases):
                word_score['categories'][mapped_category] = word_score['categories'].get(mapped_category, 0) + 1
        word_analysis.append(word_score)

    # Display results
    print("\nWord-Level Analysis:")
    for entry in word_analysis:
        print(f"Word: {entry['word']}, Categories: {entry['categories']}")

    # Display final sentence score
    print("\nFinal Sentence Score by Categories:")
    for category, score in scores.items():
        print(f"{category}: {score}")

    return scores


def tag_sentences_with_categories(file):
    """
    Tags each sentence in the text with its corresponding category using HTML-like tags
    based on the categorical phrases.
    """
    sentences, _ = preprocess_text(file)
    
    tf_idf_scores = calculate_tf_idf(sentences)

    tagged_sentences = []
    categorized_sentences = {}
    for idx, sentence in enumerate(sentences):
        cleaned_sentence = clean_and_normalize(sentence)
        scores = rank_by_categories(cleaned_sentence)
        best_category = max(scores, key=scores.get)
        tagged_sentence = f"<{best_category}>{sentence}</{best_category}>"
        tagged_sentences.append(tagged_sentence)
        if best_category not in categorized_sentences:
            categorized_sentences[best_category] = []
                
        categorized_sentences[best_category].append(sentence)

    return ' '.join(i for i in tagged_sentences)

tag_fullform_mapping = {
    'F': 'Fact',
    'I': 'Issue',
    'A': 'Argument',
    'LR': 'Ruling by lower court',
    'SS': 'Statute',
    'SP': 'Precedent',
    'R': 'Ruling by present court',
}




# if __name__ == "__main__":
#     dataset = load_dataset("Ashreen/dataset-IN-Abs")

#     train_set = pd.DataFrame(dataset['train'])
#     test_set = pd.DataFrame(dataset['test'])
#     file = test_set["document"][12] # Replace with your file path
    
#     # Tag sentences with categories and print the result
#     tagged_text = tag_sentences_with_original_categories(file)
#     print("Tagged Text:\n", tagged_text)


