import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import sqlite3
from transformers import AutoModelForSequenceClassification, AutoTokenizer

nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')

# Assume embeddings is a list of your embeddings
embeddings = [embedding1, embedding2, ...]

# Use PCA to reduce the dimensionality to 50 dimensions
pca = PCA(n_components=50)
embeddings_pca = pca.fit_transform(embeddings)

# Use t-SNE to reduce the dimensionality to 2 dimensions
tsne = TSNE(n_components=2)
embeddings_tsne = tsne.fit_transform(embeddings_pca)

# Plot the embeddings
plt.scatter(embeddings_tsne[:, 0], embeddings_tsne[:, 1])
plt.show()

