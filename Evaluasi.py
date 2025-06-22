import pandas as pd
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

def clean_lyrics(text):
    text = re.sub(r'\[.*?\]', '', str(text))  
    text = re.sub(r'\d+ Contributors.*Lyrics', '', text)
    text = re.sub(r'[^\w\s]', '', text) 
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()
df = pd.read_csv("dataset/data.csv")

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['lirik'])
bm25_corpus = [doc.split() for doc in df['lirik']]
bm25 = BM25Okapi(bm25_corpus)

def save_history_to_file(history_item, filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(history_item, ensure_ascii=False) + "\n")

def search_tfidf(query, top_n=1):
    q_clean = clean_lyrics(query)
    q_vec = tfidf_vectorizer.transform([q_clean])
    sim = cosine_similarity(q_vec, tfidf_matrix).flatten()
    indices = sim.argsort()[-top_n:][::-1]
    return [
        {
            "judul": df.iloc[i]["judul"],
            "skor": round(float(sim[i]), 3)
        }
        for i in indices
    ]

def search_bm25(query, top_n=1):
    q_clean = clean_lyrics(query)
    q_tokens = q_clean.split()
    scores = bm25.get_scores(q_tokens)
    indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    max_score = max(scores) if max(scores) != 0 else 1
    return [
        {
            "judul": df.iloc[i]["judul"],
            "skor": round(scores[i] / max_score, 3)
        }
        for i in indices
    ]

def evaluate_from_file(file_path, k=1):
    correct_at_k = 0
    reciprocal_ranks = []
    total = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            data = json.loads(line.strip())
            ground_truth = data['ground_truth'].strip().lower()
            found = False
            for rank, item in enumerate(data['results'][:k]):
                if item['judul'].strip().lower() == ground_truth:
                    correct_at_k += 1
                    reciprocal_ranks.append(1 / (rank + 1))
                    found = True
                    break
            if not found:
                reciprocal_ranks.append(0)

    top_k = correct_at_k / total * 100
    mrr = sum(reciprocal_ranks) / total
    return {
        "Top-{} Accuracy".format(k): round(top_k, 2),
        "MRR": round(mrr, 3)
    }

if __name__ == "__main__":
    print("=== Sistem Pencarian Judul Lagu ===")

    while True:
        query = input("\nMasukkan potongan lirik (atau 'eval' / 'exit'): ").strip()
        if query.lower() == "exit":
            break
        elif query.lower() == "eval":
            print("\n📊 Evaluasi TF-IDF:")
            print(evaluate_from_file("tfidf_history.txt"))
            print("\n📊 Evaluasi BM25:")
            print(evaluate_from_file("bm25_history.txt"))
        else:
            ground_truth = input("Masukkan judul lagu yang benar: ").strip()

            tfidf_results = search_tfidf(query)
            bm25_results = search_bm25(query)

            save_history_to_file({
                "query": query,
                "ground_truth": ground_truth,
                "results": tfidf_results
            }, "database/tfidf_history.txt")

            save_history_to_file({
                "query": query,
                "ground_truth": ground_truth,
                "results": bm25_results
            }, "database/bm25_history.txt")

            print("\n🎧 TF-IDF:")
            for i, r in enumerate(tfidf_results, 1):
                print(f"{i}. Judul: {r['judul']} | Skor: {r['skor']}")

            print("\n🎧 BM25:")
            for i, r in enumerate(bm25_results, 1):
                print(f"{i}. Judul: {r['judul']} | Skor: {r['skor']}")
