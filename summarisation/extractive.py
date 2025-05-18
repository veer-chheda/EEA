import re
from collections import OrderedDict
from math import log
import json
import nltk
from nltk.corpus import stopwords
from rouge_score import rouge_scorer
from ..extraction.categorical_corpus import categorical_pairs, categorical_phrases, add_case_variations, update_pairs_with_case_variations

# Make sure to download these resources once
# nltk.download('punkt')
# nltk.download('stopwords')

# Abbreviation patterns
abbreviations = set([
    "e.g.", "i.e.", "etc.", "vs.", "cf.", "Dr.", "Mr.", "Ms.", "Mrs.", "Co.",
    "Inc.", "Ltd.", "Corp.", "Prof.", "Sr.", "Jr.", "A.M.", "P.M.", "St.", "no.", "No.", "E.g.", "Nos.", "v.", "Rs.", 
])


def preprocess_text(text):
    """
    Read a file and applies preprocessing steps to clean and tokenize text
    """
    # Remove unwanted characters and noise
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)  # Remove control characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

    # Remove numbered lists like "1. "
    text = re.sub(r'\b\d+.\s', '', text)

    sentences = nltk.sent_tokenize(text)
    sentences = merge_abbreviated_sentences(sentences)

    return sentences, list(range(len(sentences)))


def merge_abbreviated_sentences(sentences):
    """
    Merge sentences improperly split due to abbreviations or single capital letters followed by a period
    """
    merged_sentences = []
    buffer = ""

    for sent in sentences:
        # Check if the sentence ends with an abbreviation or a single capital letter followed by a period
        if re.search(r'[A-Z].$', sent.strip()) or sent.strip()[-1] not in {".", "!", "?"}:
            buffer += " " + sent.strip()
        if any(sent.strip().endswith(abbr) for abbr in abbreviations):
            buffer += " " + sent.strip()
        else:
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
    clean and normalize a sentence by handling punctuation
    """
    sentence = re.sub(r'[^a-zA-Z0-9\s\.\,]', '', sentence)  # Keep only alphanumerics and some punctuation
    sentence = re.sub(r'\s+', ' ', sentence).strip()  # Normalize whitespace
    return sentence.lower()

def calculate_tf_idf(text):
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
        'SO': {'score': 0, 'phrases': []}, 'R': {'score': 0, 'phrases': []}
    }
    scores = {'Introduction': 0, 'Context': 0, 'Analysis': 0, 'Conclusion': 0}

    # Check for categorical phrases
    for category, phrases in categorical_phrases.items():
        mapped_category = map_to_category(category)
        for phrase in phrases:
            if phrase in sentence:
                scores[mapped_category] += 1
                scores_categories[category]['score'] += 1
                scores_categories[category]['phrases'].append(phrase)

    # Check for categorical pairs
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

    # Print the results for debugging purposes
    # print("\nDetailed Scores by Categories:")
    # for category, details in scores_categories.items():
    #     print(f"Category: {category}, Score: {details['score']}, Phrases: {details['phrases']}")

    return scores


def map_to_category(code):
    """
    Maps the code to the corresponding summary category.
    """
    mapping = {'F': 'Introduction', 'I': 'Introduction', 'A': 'Context', 'LR': 'Context',
               'SS': 'Analysis', 'SP': 'Analysis', 'SO': 'Analysis', 'R': 'Conclusion'}
    return mapping.get(code, 'Context')




tag_fullform_mapping = {
    'F': 'Fact',
    'I': 'Issue',
    'A': 'Argument',
    'LR': 'Ruling by lower court',
    'SS': 'Statute',
    'SP': 'Precedent',
    'SO': 'General standards',
    'R': 'Ruling by present court',
}


def extraction(file, threshold):
    # categorical_phrases = add_case_variations(categorical_phrases)
    # categorical_pairs = update_pairs_with_case_variations(categorical_pairs)
    sentences, _ = preprocess_text(file)
    
    tf_idf_scores = calculate_tf_idf(sentences)

    tagged_sentences = []
    categorized_sentences = {}
    
    for idx, sentence in enumerate(sentences):
        cleaned_sentence = clean_and_normalize(sentence)
        
        scores_categories = {category: 0 for category in categorical_phrases.keys()}
        
        for category, phrases in categorical_phrases.items():
            for phrase in phrases:
                if phrase in cleaned_sentence:
                    scores_categories[category] += (1 + tf_idf_scores.get(phrase.lower(), 0))

        for category, pairs in categorical_pairs.items():
            for start_phrase, end_phrases in pairs.items():
                if start_phrase in cleaned_sentence:
                    start_index = cleaned_sentence.find(start_phrase)
                    sentence_after_start = cleaned_sentence[start_index + len(start_phrase):]
                    matched_end_phrases = [end_phrase for end_phrase in end_phrases if end_phrase in sentence_after_start]
                    scores_categories[category] += sum((1 + tf_idf_scores.get(end_phrase.lower(), 0)) for end_phrase in matched_end_phrases)
        
        if any(score > threshold for score in scores_categories.values()):
            best_category = max(scores_categories, key=scores_categories.get)
            best_tag = tag_fullform_mapping.get(best_category, "Unknown")
            
            tagged_sentence = f"<{best_tag}>{sentence}</{best_tag}>"
            tagged_sentences.append(tagged_sentence)
            

            if best_tag not in categorized_sentences:
                categorized_sentences[best_tag] = []
            
            categorized_sentences[best_tag].append(sentence)
    

    formatted_output = "\n\n".join(
        f"{category}:\n" + "\n".join(sentences)
        for category, sentences in categorized_sentences.items() if sentences
    )
    
    return ' '.join(tagged_sentences), formatted_output