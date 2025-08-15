from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load SciBERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
model = BertModel.from_pretrained('allenai/scibert_scivocab_uncased')

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def plot_heatmap(embedding1, embedding2, title):
    # Calculate the difference between the two embeddings
    diff = embedding1 - embedding2
    # Reshape the difference to a 2D array for the heatmap
    diff_2d = diff.reshape(1, -1)
    # Create a heatmap
    plt.figure(figsize=(12, 2))
    sns.heatmap(diff_2d, cmap='coolwarm', annot=False, cbar=True)
    plt.title(title)
    plt.show()

# Original and typo-infested text
original_text = "The quick brown fox jumps over the lazy dog."
typo_text = "The quick brown fox jumps over the lazzy dog."

# Get embeddings
original_embedding = get_embeddings(original_text)
typo_embedding = get_embeddings(typo_text)

# Calculate cosine similarity
similarity = cosine_similarity(original_embedding, typo_embedding)
print(f"Cosine Similarity: {similarity[0][0]}")

# Plot heatmap
plot_heatmap(original_embedding, typo_embedding, "Difference Between Original and Typo-Infested Text Embeddings")
