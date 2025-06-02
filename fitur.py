import pandas as pd
from ui import header
from tabulate import tabulate

def lihat_buku(books, genres, isbn=False):
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

            if isbn:
                kolom_view.append('isbn')
                rename_kolom['isbn'] = 'ISBN'

            df = books_with_genres[kolom_view]
            df = df.rename(columns=rename_kolom)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', numalign='left', showindex=False))
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
    """Fungsi sorting menggunakan Merge Sort yang dioptimalkan untuk dataset kecil."""
    if len(df) <= 15:  # Gunakan Insertion Sort untuk dataset kecil
        return insertion_sort(df, key, ascending)
    
    mid = len(df) // 2
    left = optimized_merge_sort(df.iloc[:mid], key, ascending)
    right = optimized_merge_sort(df.iloc[mid:], key, ascending)
    
    return merge(left, right, key, ascending)

def merge(left, right, key, ascending):
    result = pd.DataFrame(columns=left.columns)
    i = j = 0

    while i < len(left) and j < len(right):
        if ascending:
            condition = left.iloc[i][key] <= right.iloc[j][key]
        else:
            condition = left.iloc[i][key] >= right.iloc[j][key]
        
        if condition:
            result = pd.concat([result, left.iloc[[i]]], ignore_index=True)
            i += 1
        else:
            result = pd.concat([result, right.iloc[[j]]], ignore_index=True)
            j += 1

    result = pd.concat([result, left.iloc[i:], right.iloc[j:]], ignore_index=True)
    return result


def insertion_sort(df, key, ascending):
    df = df.copy()
    for i in range(1, len(df)):
        j = i
        while j > 0:
            if ascending:
                condition = df.iloc[j - 1][key] > df.iloc[j][key]
            else:
                condition = df.iloc[j - 1][key] < df.iloc[j][key]
                
            if condition:
                # Swap rows
                df.iloc[j - 1], df.iloc[j] = df.iloc[j], df.iloc[j - 1]
                j -= 1
            else:
                break
    return df

def find_books_by_genre(books, genre_id):
    # Sort the books by 'genre_id' in ascending order
    books_sorted = optimized_merge_sort(books, key='genre_id', ascending=True)
    low = 0
    high = len(books_sorted) - 1
    result_indices = []

    while low <= high:
        mid = (low + high) // 2
        current_genre = books_sorted.iloc[mid]['genre_id']

        if current_genre == genre_id:
            # Expand to the left to find all matching genres
            left = mid - 1
            while left >= 0 and books_sorted.iloc[left]['genre_id'] == genre_id:
                result_indices.append(left)
                left -= 1

            # Include the mid index
            result_indices.append(mid)

            # Expand to the right to find all matching genres
            right = mid + 1
            while right < len(books_sorted) and books_sorted.iloc[right]['genre_id'] == genre_id:
                result_indices.append(right)
                right += 1
            break

        if current_genre < genre_id:
            low = mid + 1
        else:
            high = mid - 1

    # Return the found books or an empty DataFrame if none found
    if result_indices:
        return len(result_indices), books_sorted.iloc[result_indices].copy()
    else:
        return 0, pd.DataFrame(columns=books.columns)

def cari_buku_berdasarkan_keyword(books, keyword):
    """Fungsi untuk mencari buku berdasarkan judul atau pengarang."""
    keyword = keyword.lower()
    matching_indices = []
    
    for idx, row in books.iterrows():
        title = row['title'].lower()
        author = row['author'].lower()
        if keyword in title or keyword in author:
            matching_indices.append(idx)
            
    if matching_indices:
        found_books = books.loc[matching_indices].copy()
        return found_books
    else:
        print(f"Tidak ditemukan buku dengan kata kunci '{keyword}'")
        return pd.DataFrame(columns=books.columns)
