import pandas as pd
import re
import unicodedata

RE_BAD_ENCODING = re.compile(r'[ÐÑŸÐ­ÐÐžÐ¨Ð±Ð²Ð°ÐµÐ¶Ð¸ÐºÐ»Ð¼Ð½Ð¾Ð¿Ñ€ÑÑ‚ÑƒÑ„Ñ…]')

def contains_gibberish(text):
    if not isinstance(text, str):
        return True
    return bool(RE_BAD_ENCODING.search(text))

def remove_bad_unicode(text):
    if not isinstance(text, str):
        return ""
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != "C")
    return re.sub(r'\s+', ' ', text).strip()

def clean_lyrics(text):
    if not isinstance(text, str):
        return ""

    text = remove_bad_unicode(text)

    text = re.sub(r'\d+\s+Contributors?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bLyrics\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[.*?\]', '', text)
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    result = ' '.join(lines)
    result = re.sub(r'[^\w\s\']', '', result)
    result = re.sub(r'\d+', '', result)

    return result.lower().strip()

def preprocess_lirik_file(file1, file2=None, output_file='hasil_bersih.csv'):
    df1 = pd.read_csv(file1)
    if file2:
        df2 = pd.read_csv(file2)
        df = pd.concat([df1, df2], ignore_index=True)
    else:
        df = df1

    if 'lirik' not in df.columns:
        raise ValueError("Dataset harus memiliki kolom 'lirik'.")

    df = df[~df['lirik'].apply(contains_gibberish)].reset_index(drop=True)
    df['lirik'] = df['lirik'].apply(clean_lyrics)

    df.to_csv(output_file, index=False)
    print(f"✅ Data berhasil dibersihkan dan disimpan sebagai: {output_file}")

preprocess_lirik_file('dataset/Daftar_Lagu.csv', 'dataset/lirik_550.csv', 'dataset/data.csv')