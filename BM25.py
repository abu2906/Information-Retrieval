import pandas as pd
import re
from rank_bm25 import BM25Okapi


df = pd.read_csv("dataset/data.csv")

corpus = [lirik.split() for lirik in df['lirik']]
bm25 = BM25Okapi(corpus)

def search_with_bm25(query, top_n=5):
    query_tokens = query.split()
    scores = bm25.get_scores(query_tokens)
    max_score = max(scores) if max(scores) > 0 else 1
    normalized_scores = [s / max_score for s in scores]

    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    
    results = []
    for i in top_indices:
        results.append({
            "judul": df.iloc[i]['judul'],
            "artis": df.iloc[i].get('artis', 'Unknown'),
            "skor": round(normalized_scores[i], 3)
        })
    return results

if __name__ == "__main__":
    print("=== Pencarian Judul Lagu dengan BM25 ===")
    while True:
        query = input("\nMasukkan potongan lirik (atau ketik 'exit' untuk keluar): ").strip()
        if query.lower() == "exit":
            break

        hasil = search_with_bm25(query)
        print("\nHasil Pencarian:")
        for i, lagu in enumerate(hasil, 1):
            print(f"{i}. Judul: {lagu['judul']} | Artis: {lagu['artis']} | Skor: {lagu['skor']}")
