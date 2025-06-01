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

def optimized_merge_sort(df, key, ascending=True):
    if len(df) <= 15:  # Gunakan Insertion Sort untuk dataset kecil
        return insertion_sort(df, key, ascending)
    
    mid = len(df) // 2
    left = optimized_merge_sort(df.iloc[:mid], key, ascending)
    right = optimized_merge_sort(df.iloc[mid:], key, ascending)
    
    return merge(left, right, key, ascending)

def insertion_sort(df, key, ascending):
    df = df.copy()
    for i in range(1, len(df)):
        j = i
        while j > 0 and (
            (df.iloc[j-1][key] > df.iloc[j][key] if ascending else 
             df.iloc[j-1][key] < df.iloc[j][key])):
            # Swap rows
            df.iloc[j-1], df.iloc[j] = df.iloc[j], df.iloc[j-1]
            j -= 1
    return df

def merge(left, right, key, ascending):
    result = pd.DataFrame(columns=left.columns)
    i = j = 0
    
    while i < len(left) and j < len(right):
        if (left.iloc[i][key] <= right.iloc[j][key] if ascending else 
            left.iloc[i][key] >= right.iloc[j][key]):
            result = pd.concat([result, left.iloc[[i]]], ignore_index=True)
            i += 1
        else:
            result = pd.concat([result, right.iloc[[j]]], ignore_index=True)
            j += 1
    
    result = pd.concat([result, left.iloc[i:], right.iloc[j:]], ignore_index=True)
    return result