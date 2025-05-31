import pandas as pd
from tabulate import tabulate

def lihat_buku(df):
    """Fungsi untuk melihat daftar buku."""
    try:
        if df.empty:
            print("Tidak ada buku yang tersedia.")
        else:
            print("Daftar Buku:")
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    
    input("Tekan enter untuk kembali ke menu...")

books = pd.read_csv("books.csv")
genres = pd.read_csv("genres.csv")

# lihat_buku(books)
lihat_buku(genres)