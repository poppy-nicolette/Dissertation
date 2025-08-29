#function to generate embeddings using SciBERT
from typing import List
import numpy as np


def generate_embeddings(texts: List[str]) -> List[np.ndarray]:
    """
    converts raw text to numerical representations using a pretrained model, in this case, SciBERT.
    Currently this is applied to both the document text and the query. 
    May want a different version or decorator for the query as they are generally much shorter and more sparse.

    Input: text from tokenizer step above as a list of strings
    Output: np.array
    """
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        max_length=512,
        padding="max_length",
        truncation=True,
        return_attention_mask=True)# return the attention mask - need to learn more)
    
    # this passes the tokenized inputs through the model
    outputs = model(**inputs)
    #this uses mean pooling - may want to investigate other methods
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings

def main():
    generate_embeddings(texts)

if __name__ == "__main__":
    main()

    