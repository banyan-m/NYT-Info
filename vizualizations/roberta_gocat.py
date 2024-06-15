import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import sqlite3
from transformers import pipeline
from collections import defaultdict

# Establish a connection to the SQLite database
conn = sqlite3.connect('nyt_articles.db')

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch the data
cur.execute("SELECT snippet, news_desk FROM articles LIMIT 2000")
rows = cur.fetchall()

# Close the database connection
cur.close()
conn.close()

# Load the zero-shot classification pipeline
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# Group rows by news_desk
news_desk_groups = defaultdict(list)
for row in rows:
    news_desk_groups[row[1]].append(row[0])

# Classify the sequences for each news_desk
for news_desk, snippets in news_desk_groups.items():
    emotion_scores = defaultdict(int)
    for snippet in snippets:
        results = classifier(snippet)
        for result_list in results:  # Iterate over each inner list
            for result in result_list:  # Iterate over each dictionary in the inner list
                label = result['label']
                score = result['score']
                emotion_scores[label] += score

    # Plot the scores for each emotion
    plt.bar(emotion_scores.keys(), emotion_scores.values())
    plt.xlabel('Emotion')
    plt.ylabel('Total Score')
    plt.title(f'NYT Snippet Emotion Scores from Roberta Model for {news_desk}')
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig(f'graphs/roberta/roberta_news_desk/{news_desk}_Snippet_emotion_scores2000.png')

    plt.close()  # Close the figure