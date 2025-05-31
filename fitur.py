import pandas as pd
from ui import header
from tabulate import tabulate

def lihat_buku(books, genres):
    """Fungsi untuk melihat daftar buku."""
    books_with_genres = books.merge(genres, on='genre_id', how='left')
    try:
        if books_with_genres.empty:
            print("Tidak ada buku yang tersedia.")
        else:
            print("Daftar Buku:")
            kolom_view = ['book_id', 'title', 'author', 'genre_name', 'quantity', 'publication_year']
            rename_kolom = {
                'book_id': 'ID Buku',
                'title': 'Judul',
                'author': 'Author',
                'genre_name': 'Genre',
                'quantity': 'Jumlah',
                'publication_year': 'Tahun Terbit'
            }
            df = books_with_genres[kolom_view]
            df = df.rename(columns=rename_kolom)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
            input("Tekan enter untuk kembali ke menu daftar buku...")
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")

def tambah_buku(books, genres):
    """Fungsi untuk menambahkan buku."""
    while True:
        header("PERPUSTAKAAN JEMBER", "MENAMBAHKAN BUKU")
    
        try:
            new_book = {
                'book_id': books['book_id'].max() + 1 if not books.empty else 1,
                'title': input("Masukkan Judul Buku: ").strip(),
                'author': input("Masukkan Pengarang Buku: ").strip(),
                # 'genre_id': input("Masukkan ID Genre: ").strip(),
                'quantity': int(input("Masukkan Jumlah Buku: ").strip()),
                'publication_year': int(input("Masukkan Tahun Terbit: ").strip()),
                'isbn': input("Masukkan ISBN Buku: ").strip()
            }

            genres = genres.rename(columns={'genre_id': 'id genre', 'genre_name': 'genre'})
            print("Daftar Genre:")
            print(tabulate(genres, headers='keys', tablefmt='fancy_grid', showindex=False))
            
            while True:
                new_book['genre_id'] = input("Masukkan ID Genre: ").strip()
                # Validasi genre_id
                if new_book['genre_id'] not in genres['id genre'].astype(str).values:
                    print("ID Genre tidak valid. Silakan coba lagi.")
                else:
                    break

            books = pd.concat([books, pd.DataFrame([new_book])], ignore_index=True)
            books.to_csv("books.csv", index=False)
            print(f"Buku '{new_book['title']}' berhasil ditambahkan.")
            opsi = input("Tekan enter untuk menambahkan buku lain atau ketik 0 untuk kembali ke menu utama: ").strip()
            if opsi == '0':
                return
            
        except Exception as e:
            print("Terjadi kesalahan")
            opsi = input("Tekan enter untuk mengulangi atau ketik 0 untuk kembali ke menu utama: ").strip()
            if opsi == '0':
                return
            continue
