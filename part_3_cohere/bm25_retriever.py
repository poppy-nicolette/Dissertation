# BM25s pre-retriever function
from typing import Tuple
import numpy as np

def bm25_retriever(query:str)->Tuple[np.array, np.array]:
    """
    Inputs:
        query: str
    Outputs:
        Tuple of two np.arrays, one for results and one for scores
    """
    global results, scores,query_tokens
    #you can also add a stemmer here as an arg: stemmer=stemmer
    query_tokens = bm25s.tokenize(query,stopwords=True,lower=True)

    #note: if you pass a new corpus here, it must have the same length as your indexed corpus
    #in this case, I am passing the new list 'identifier_list' - it contains just the DOI and title
    # you can also pass 'corpus', or 'corpus_list'
    if len(corpus_list)!=len(identifier_list):
        raise ValueError("The len of the corpus_list does not equal the len of the identifier_list")

    # retrieve indices
    results, scores = retriever.retrieve(query_tokens, corpus=identifier_list, k=top_k, return_as="tuple")

    # check if no results found
    if all(score == 0.00 for score in scores[0]):
        print("Nothing found, please try another query.")
        return [],[] # returning empty lists if 0 for scores, one for results, one for scores

    return results[0],scores[0]