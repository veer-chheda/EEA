MODELS = {
"phi-4": "unsloth/phi-4-unsloth-bnb-4bit",
"llama3.2-1b": "unsloth/Llama-3.2-1B-Instruct-unsloth-bnb-4bit",
"llama3.2-3b": "unsloth/Llama-3.2-3B-Instruct-unsloth-bnb-4bit",
"qwen2.5-7b": "unsloth/Qwen2.5-7B-Instruct-bnb-4bit",
}

MAX_SEQ_LEN = {
    "phi-4": 16000,
    "llama3.2-1b": 128000,
    "llama3.2-3b": 128000,
    "qwen2.5-7b": 128000,
}

DATASET_INDEX = {
    "ilc": "Title",
    'civilsum': 'doc_id',
    'inabs': 'index'
}

DATASET_DOC = {
    "ilc": "Case",
    'civilsum': 'text',
    'inabs': 'document'
}

SUMMARY_NAME = {
    "ilc": "Summary",
    'civilsum': 'summary',
    'inabs': 'summary'
}

THRESHOLD = {
    "ilc": 20,
    'civilsum': 15,
    'inabs': 5
}

MAX_NEW_TOK = 5000

DATASETS = {
"ilc": "d0r1h/ILC",
"civilsum":"civilsum",#add locally by downloading the csv file from https://github.com/ra-MANUJ-an/CivilSum
"inabs": "Ashreen/dataset-IN-Abs",
}

