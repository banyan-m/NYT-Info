import matplotlib.pyplot as plt
import sqlite3
from transformers import pipeline
from collections import defaultdict

# Establish a connection to the SQLite database
conn = sqlite3.connect('nyt_articles.db')

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch the data
cur.execute("SELECT snippet FROM articles WHERE snipembedding IS NOT NULL LIMIT 1000")
rows = cur.fetchall()

# Close the database connection
cur.close()
conn.close()

# Load the zero-shot classification pipeline
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

emotion_scores = defaultdict(int)

# Classify the sequences
for row in rows:
    sequence_to_classify = row[0]
    results = classifier(sequence_to_classify)
    # results is a list of lists of dictionaries, so we need to get the first list
    result_list = results[0]
    sorted_results = sorted(result_list, key=lambda x: x['score'], reverse=True)  # Sort results by score in descending order
    # If the highest score is 'neutral', use the second highest score
    if sorted_results[0]['label'] == 'neutral':
        label = sorted_results[1]['label']
        score = sorted_results[1]['score']
    else:
        label = sorted_results[0]['label']
        score = sorted_results[0]['score']
    emotion_scores[label] += score

print(plt.get_backend()) 

# Plot the scores for each emotion
plt.bar(emotion_scores.keys(), emotion_scores.values())
plt.xlabel('Emotion')
plt.ylabel('Total Score')
plt.title('NYT Snippet Emotion Scores from Roberta Model')
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig('graphs/roberta/Snippet_emotion_scores1000noneut.png')

plt.close()  # Close the figure