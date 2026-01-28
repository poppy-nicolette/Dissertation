def retrieve_documents_2(query:str, threshold:float) -> List[Dict[str,str]]:
    """
    Dense retriever: retrieves documents from the embedded documents and performs cosine similarity for similarities score

    Args:
        query: this is the query passed
        threshold: value for similarity cutoff
    Returns:
        List of dictionaries containing strings as key/value pairs
    """
    global top_indices, filtered_indices, similarities,toppy_top,query_embedding,document_embeddings # for debugging
    query_embedding = generate_embeddings(query)
    document_embeddings = generate_embeddings(documents)
    #cosine similarity
    similarities = [
        np.dot(query_embedding, doc_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
        for doc_emb in document_embeddings
    ]

    #test_tuple = (i,float(sim) for i,sim in enumerate(similarities) if sim >= threshold)
    test_tuple = []
    for i,sim in enumerate(similarities):
        if sim >= threshold:
            a = (i,sim)
            test_tuple.append(a)
    toppy_top = sorted(test_tuple,key=lambda score: score[1], reverse=True)
    filtered_list = toppy_top[:5]
    top_indices = [idx for idx,score in filtered_list]
    try:
        return [documents_with_doi[i] for i in top_indices]
    except:
        return None
