import re
import nltk

"""Handles text preprocessing tasks."""

# Abbreviation patterns to handle sentence splitting
ABBREVIATIONS = set([
    "e.g.", "i.e.", "etc.", "vs.", "cf.", "Dr.", "Mr.", "Ms.", "Mrs.", "Co.",
    "Inc.", "Ltd.", "Corp.", "Prof.", "Sr.", "Jr.", "A.M.", "P.M.", "St.", 
    "no.", "No.", "E.g.", "Nos.", "v."
])

def preprocess_text(text):
    # Remove control characters and normalize spaces
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\b\d+\.\s', '', text)

    sentences = nltk.sent_tokenize(text)
    sentences = merge_abbreviated_sentences(sentences)
    
    return sentences, list(range(len(sentences)))

def merge_abbreviated_sentences(sentences):
    merged_sentences = []
    buffer = ""

    for sent in sentences:
        if any(sent.strip().endswith(abbr) for abbr in ABBREVIATIONS):
            buffer += " " + sent.strip()
        elif re.match(r".*\b[A-Z]\.[A-Z]\.\s[A-Z][a-z]+,\s[J|C]\.?$", sent.strip()):
            # Merge judicial names like "D.S. Sinha, J."
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
    sentence = re.sub(r'[^a-zA-Z0-9\s\.\,]', '', sentence)
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence.lower()

def extract_summary(text):
    match = re.search(r"summary:assistant\s*(.*)", str(text), re.IGNORECASE | re.DOTALL)
    return match.group(1) if match else text

def chunk_text_by_word_limit(text, word_limit=128000):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_word_count + sentence_word_count <= word_limit:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks