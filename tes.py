import pandas as pd

# Load data
def load_data():
    books = pd.read_csv('books.csv')
    genres = pd.read_csv('genres.csv')
    return books, genres

# Optimized Merge Sort dengan Insertion Sort untuk elemen kecil
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

# Binary Search untuk mencari range genre
def find_books_by_genre(books, genre_id):
    books_sorted = books.sort_values('genre_id')
    low = 0
    high = len(books_sorted) - 1
    result_indices = []
    
    while low <= high:
        mid = (low + high) // 2
        current_genre = books_sorted.iloc[mid]['genre_id']
        
        if current_genre == genre_id:
            # Expand ke kiri dan kanan untuk temukan semua dengan genre yang sama
            left = mid - 1
            while left >= 0 and books_sorted.iloc[left]['genre_id'] == genre_id:
                result_indices.append(left)
                left -= 1
            
            result_indices.append(mid)
            
            right = mid + 1
            while right < len(books_sorted) and books_sorted.iloc[right]['genre_id'] == genre_id:
                result_indices.append(right)
                right += 1
            break
        elif current_genre < genre_id:
            low = mid + 1
        else:
            high = mid - 1
    
    return books_sorted.iloc[result_indices].copy() if result_indices else pd.DataFrame(columns=books.columns)

# Fungsi untuk menampilkan buku
def display_books(books_df, genres_df):
    if books_df.empty:
        print("\nTidak ada buku yang ditemukan.")
        return
    
    # Merge dengan genre untuk dapatkan nama genre
    merged_df = pd.merge(books_df, genres_df, left_on='genre_id', right_on='genre_id', how='left')
    
    # Format output
    display_cols = ['book_id', 'title', 'author', 'genre_name', 'quantity', 'publication_year']
    renamed_cols = ['ID', 'Judul', 'Penulis', 'Genre', 'Stok', 'Tahun']
    
    formatted_df = merged_df[display_cols].rename(columns=dict(zip(display_cols, renamed_cols)))
    
    print("\nDaftar Buku:")
    print("=" * 100)
    print(formatted_df.to_string(index=False))
    print("=" * 100)

# Menu utama lihat daftar buku
def view_books_menu(books_df, genres_df):
    current_books = books_df.copy()
    
    while True:
        print("\n=== MENU DAFTAR BUKU ===")
        print("1. Tampilkan semua buku")
        print("2. Urutkan buku")
        print("3. Filter berdasarkan genre")
        print("4. Cari buku")
        print("5. Kembali ke menu utama")
        
        choice = input("Pilih menu (1-5): ")
        
        if choice == '1':
            display_books(current_books, genres_df)
        elif choice == '2':
            print("\nUrutkan berdasarkan:")
            print("1. Judul (A-Z)")
            print("2. Judul (Z-A)")
            print("3. Tahun Terbit (Terbaru)")
            print("4. Tahun Terbit (Terlama)")
            sort_choice = input("Pilihan (1-4): ")
            
            if sort_choice == '1':
                sorted_books = optimized_merge_sort(current_books, 'title', True)
            elif sort_choice == '2':
                sorted_books = optimized_merge_sort(current_books, 'title', False)
            elif sort_choice == '3':
                sorted_books = optimized_merge_sort(current_books, 'publication_year', False)
            elif sort_choice == '4':
                sorted_books = optimized_merge_sort(current_books, 'publication_year', True)
            else:
                print("Pilihan tidak valid!")
                continue
            
            display_books(sorted_books, genres_df)
            current_books = sorted_books.copy()
        elif choice == '3':
            print("\nDaftar Genre Tersedia:")
            print(genres_df[['genre_id', 'genre_name']].to_string(index=False))
            
            try:
                genre_id = int(input("Masukkan ID genre: "))
                genre_books = find_books_by_genre(current_books, genre_id)
                
                if not genre_books.empty:
                    genre = genres_df.loc[genres_df['genre_id'] == genre_id, 'genre_name'].values[0]
                    print(f"\nBuku dengan genre '{genre}':")
                    display_books(genre_books, genres_df)
                    current_books = genre_books.copy()
                else:
                    print("Tidak ditemukan buku dengan genre tersebut.")
            except ValueError:
                print("ID genre harus berupa angka!")
        elif choice == '4':
            query = input("Masukkan kata kunci pencarian (judul/penulis): ").lower()
            
            mask = (current_books['title'].str.lower().str.contains(query) | 
                   current_books['author'].str.lower().str.contains(query))
            
            found_books = current_books[mask]
            
            if not found_books.empty:
                print(f"\nHasil pencarian untuk '{query}':")
                display_books(found_books, genres_df)
                current_books = found_books.copy()
            else:
                print(f"Tidak ditemukan buku dengan kata kunci '{query}'")
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid!")

# Main program
def main():
    books_df, genres_df = load_data()
    
    print("\n=== APLIKASI PERPUSTAKAAN ===")
    print("Anda login sebagai Peminjam")
    
    while True:
        print("\nMenu Utama:")
        print("1. Lihat Daftar Buku")
        print("2. Pinjam Buku")
        print("3. Keluar")
        
        main_choice = input("Pilih menu (1-3): ")
        
        if main_choice == '1':
            view_books_menu(books_df, genres_df)
        elif main_choice == '2':
            print("Fitur peminjaman buku akan diimplementasikan di sini")
        elif main_choice == '3':
            print("Terima kasih telah menggunakan sistem perpustakaan.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()