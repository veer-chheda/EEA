import unsloth
from unsloth import FastLanguageModel

class ModelLoader:

    def load_model(self, model_name="unsloth/phi-4-unsloth-bnb-4bit", max_seq_length=16000, load_in_4bit=True):
        """
        Load and configure a language model for summarization.
        
        Args:
            model_name (str): Name of the model to load
            max_seq_length (int): Maximum sequence length
            load_in_4bit (bool): Whether to load model in 4-bit quantization
            
        Returns:
            tuple: Model and tokenizer
        """
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            dtype=None,
            load_in_4bit=load_in_4bit,
        )
        return model, tokenizer