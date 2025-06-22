import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data(filepath):
    df = pd.read_csv(filepath)
    if 'judul' not in df.columns or 'lirik' not in df.columns:
        raise ValueError("Dataset harus memiliki kolom 'judul' dan 'lirik'.")
    return df['judul'].tolist(), df['lirik'].fillna("").tolist(), df['artis'].tolist()

def search_by_lyrics(query, artis, titles, lyrics, top_n=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lyrics)
    query_vec = vectorizer.transform([query])

    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        results.append({
            "judul": titles[idx],
            "artis": artis[idx],
            "similarity": round(similarity[idx], 3),
            "lirik": lyrics[idx][:300] + "..." if len(lyrics[idx]) > 300 else lyrics[idx]
        })
    return results

if __name__ == "__main__":
    judul_list, lirik_list, artis = load_data("dataset/data.csv")

    print("=== Pencarian Lagu Berdasarkan Lirik (TF-IDF + Cosine Similarity) ===")
    while True:
        query = input("\nMasukkan potongan lirik (atau ketik 'exit' untuk keluar): ").strip()
        if query.lower() == "exit":
            break

        hasil = search_by_lyrics(query, artis, judul_list, lirik_list)
        print("\nHasil Rekomendasi Lagu Terdekat:")
        for i, res in enumerate(hasil, 1):
            print(f"{i}. Judul: {res['judul']} | Artis: {res['artis']} | Skor: {res['similarity']}")
