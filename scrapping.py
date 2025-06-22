import requests
import time
import csv

from bs4 import BeautifulSoup
from tqdm import tqdm

ACCESS_TOKEN = "SJ7HcXQTcD8WPOOMqzroL82AIpV670tSWDxlGd9p5QuR61zyOHWR0IZiRIpuwL69"  # ← Ganti dengan token Genius-mu
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
SEARCH_URL = "https://api.genius.com/search"

def mencari_kata_kunci(query):
    response = requests.get(SEARCH_URL, params={"q": query}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["response"]["hits"]
    return[]

def mencari_lirik(url_lagu):
    halaman = requests.get(url_lagu)
    pecahan = BeautifulSoup(halaman.text, "html.parser")
    lirik_div = pecahan.find("div", class_="Lyrics_Container-sc-1ynbvzw-6")
    if not lirik_div:
        lirik_div = pecahan.find_all("div", class_=lambda c: c and "Lyrics__Container" in c)
        return "\n".join([div.get_text(separator="\n") for div in lirik_div])
    
    baris = lirik_div.split("\n")
    bersih = []
    for b in baris:
        if any(kata in b.lower() for kata in ["contributors", "translations", "english", "embed"]):
            continue
        bersih.append(b.strip())

    return "\n".join(bersih).strip() if bersih else "Lirik tidak ditemukan"

def mencari_lagu():
    hasil = []
    keywords = [
        "Chrisye", "Iwan Fals", "Nike Ardilla", "Dewa 19", "Sheila On 7", "Padi", "Peterpan", "Ungu",
        "Ruth Sahanaya", "Titi DJ", "Slank", "Gigi", "Cokelat", "Seventeen", "Yovie & Nuno", "Rossa",
        "Afgan", "Ari Lasso", "Glenn Fredly", "Naif", "Melly Goeslaw", "D'Masiv", "Nidji", "Ada Band",
        "Kotak", "Kerispatih", "Five Minutes", "Geisha", "Judika", "Samsons", "Yura Yunita", "Tulus",
        "Isyana Sarasvati", "Maudy Ayunda", "Sal Priadi", "Pamungkas", "The Groove", "Kahitna",
        "Reza Artamevia", "Andien", "Once Mekel", "Vina Panduwinata", "Bunga Citra Lestari",
        "Broery Marantika", "Hetty Koes Endang", "Evie Tamala", "Iis Dahlia", "Inul Daratista",
        "Zaskia Gotik", "Via Vallen", "Nella Kharisma", "Happy Asmara", "Ayu Ting Ting", "Cita Citata",
        "Rhoma Irama", "Elvy Sukaesih", "Mansyur S", "Jamal Mirdad", "Lilis Suryani", "Ernie Djohan",
        "Yuni Shara", "Krisdayanti", "Anang Hermansyah", "Ashanty", "Syahrini", "Agnez Mo", "Anggun",
        "Melanie Subono", "Once", "Dian Pramana Poetra", "Fariz RM", "Deddy Dores", "Deddy Dhukun",
        "Deddy Mizwar", "Ikang Fawzi", "Harvey Malaiholo", "Tompi", "Barry Likumahuwa", "Indra Lesmana",
        "Rieka Roeslan", "Radja", "Drive", "Letto", "Jikustik", "GAC", "Maliq & D’Essentials", "HiVi!",
        "Fourtwnty", "Payung Teduh", "Fiersa Besari", "Kunto Aji", "Danilla", "Nadin Amizah", "Hindia",
        "Banda Neira", "Efek Rumah Kaca", "The Rain", "Last Child", "Yovie Widianto", "RAN", "Dua Mata",
        "Soulvibe", "The Overtunes", "CJR", "SM*SH", "Cherrybelle", "Blink", "JKT48",
        "Gamaliel Audrey Cantika", "Alexa", "The Changcuters", "Netral", "Superglad", "Burgerkill",
        "Saint Loco", "Steven and Coconut Treez", "Tony Q Rastafara", "Shaggydog", "Tipe-X",
        "Endank Soekamti", "Rocket Rockers", "The Sigit", "White Shoes & The Couples Company",
        "Mocca", "Sore", "Goodnight Electric", "The Upstairs", "The Adams", "Killing Me Inside", "Noah",
        "Govinda", "Sammy Simorangkir", "Marcell", "Rio Febrian", "Andra and The Backbone", "Utopia",
        "Element", "Base Jam", "Caffeine", "J-Rocks", "Dygta", "Zivilia", "ST12", "Wali", "The Potter’s",
        "Armada", "Dadali", "Kangen Band", "Hijau Daun", "Repvblik", "Papinka", "D’Bagindas", "Vagetoz",
        "Astrid", "Shanty", "D’Cinnamons", "Ten 2 Five", "Glen Fredly", "Yovie Widianto", "Once",
        "Kahitna", "Krisdayanti", "Gigi", "Slank", "Iwan Fals", "Dewa 19", "Chrisye", "Peterpan", "Ungu",
        "ST12", "D'Masiv", "Letto", "Padi", "Sheila On 7", "Seventeen", "Radja", "Samsons", "Kerispatih",
        "Five Minutes", "Wali", "Repvblik", "Armada", "Kangen Band", "Hijau Daun", "Drive", "Geisha",
        "Zivilia", "Dygta", "Papinka", "The Potter’s", "Jikustik", "Alexa", "Base Jam", "Caffeine",
        "D'Bagindas", "Vagetoz", "Last Child", "Govinda", "Nidji", "Element", "Superglad", "Tipe-X",
        "Burgerkill", "Endank Soekamti", "Steven and Coconut Treez", "Tony Q Rastafara", "Shaggydog",
        "The Sigit", "Rocket Rockers", "The Upstairs", "White Shoes & The Couples Company"
    ]


    urls = set()

    for keyword in tqdm(keywords * 20):
        if len(hasil) >= 4000 :
            break

        hasil_kata_kunci = mencari_kata_kunci(keyword)
        for hsil in hasil_kata_kunci:
            url = hsil["result"]["url"]
            title = hsil["result"]["title"]
            artist = hsil["result"]["primary_artist"]["name"]
            
            if url in urls:
                continue
 
            try:
                lirik = mencari_lirik(url)
                hasil.append({
                    "judul": title,
                    "artis": artist,
                    "lirik":lirik
                })
                urls.add(url)
                time.sleep(1)
            
            except Exception as e:
                print(f"Gagal mengambil lirik untuk {title} - {artist}: {e}")
                continue

            if len(hasil) >= 4000:
                break
    
    return hasil

def simpan_csv(data, filename="Dataset/Daftar_Lagu.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["judul", "artis", "lirik"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    result = mencari_lagu()
    simpan_csv(result)
    print("Selesai| Data Berhasil Disimpan")

