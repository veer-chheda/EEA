import pandas as pd
from datasets import load_dataset
import os
from config import DATASETS

class DatasetHandler:
    """Handles dataset loading and preprocessing."""
    
    def dataset_loader(self, dataset_name=""):
        dataset_name_hf = DATASETS[dataset_name]
        if dataset_name_hf == 'civilsum':
            test_set = pd.read_csv('path to civilsum')
            return test_set
        dataset = load_dataset(dataset_name_hf)
        train_set = pd.DataFrame(dataset['train'])
        test_set = pd.DataFrame(dataset['test'])
        return train_set, test_set
    
    def load_documents_from_directory(self, directory_path):
        documents = {}
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents[filename] = f.read()
        
        return documents