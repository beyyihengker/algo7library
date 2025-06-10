import pandas as pd
from ui import header
from tabulate import tabulate
from datetime import datetime, timedelta

# FITUR GENERAL
def lihat_buku(books, genres):
    """Fungsi untuk melihat daftar buku."""
    books_with_genres = books.merge(genres, on='genre_id', how='left')
    try:
        if books_with_genres.empty:
            print("Tidak ada buku yang tersedia.")
        else:
            print("Daftar Buku:")
            kolom_view = ['book_id', 'title', 'author', 'genre_name', 'quantity', 'publication_year', 'isbn']
            rename_kolom = {
                'book_id': 'ID Buku',
                'title': 'Judul',
                'author': 'Author',
                'genre_name': 'Genre',
                'quantity': 'Jumlah',
                'publication_year': 'Tahun Terbit',
                'isbn': 'ISBN'
            }

            df = books_with_genres[kolom_view]
            df = df.rename(columns=rename_kolom)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', numalign='left', showindex=False))
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")

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
    for i in range(1, len(df)):
        j = i
        while j > 0:
            if ascending:
                condition = df.iloc[j - 1][key] > df.iloc[j][key]
            else:
                condition = df.iloc[j - 1][key] < df.iloc[j][key]
                
            if condition:
                df.iloc[j - 1], df.iloc[j] = df.iloc[j], df.iloc[j - 1]
                j -= 1
            else:
                break
    return df

def find_books_by_genre(books, genre_id):
    '''implementasi binary search dengan range finding'''
    books_sorted = optimized_merge_sort(books, key='genre_id', ascending=True)
    low = 0
    high = len(books_sorted) - 1
    result_indices = []

    while low <= high:
        mid = (low + high) // 2
        current_genre = books_sorted.iloc[mid]['genre_id']

        if current_genre == genre_id:
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

        if current_genre < genre_id:
            low = mid + 1
        else:
            high = mid - 1

    if result_indices:
        return books_sorted.iloc[result_indices].copy()
    else:
        return pd.DataFrame(columns=books.columns)

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

def menu_urutkan_buku(books, genres):
    """Fungsi untuk mengurutkan buku berdasarkan pilihan pengguna."""
    header("PERPUSTAKAAN JEMBER", "URUTKAN BUKU")
    print("Pilih kriteria pengurutan:")
    print("1. Judul (A-Z)")
    print("2. Judul (Z-A)")
    print("3. Tahun Terbit (Terbaru)")
    print("4. Tahun Terbit (Terlama)")
    
    sort_choice = input("Pilihan (1-4): ")
    
    if sort_choice == '1':
        sorted_books = optimized_merge_sort(books, key='title', ascending=True)
    elif sort_choice == '2':
        sorted_books = optimized_merge_sort(books, key='title', ascending=False)
    elif sort_choice == '3':
        sorted_books = optimized_merge_sort(books, key='publication_year', ascending=False)
    elif sort_choice == '4':
        sorted_books = optimized_merge_sort(books, key='publication_year', ascending=True)
    else:
        print("Pilihan tidak valid!")
        return
    
    lihat_buku(sorted_books, genres)

def menu_daftar_buku(user_id=None):
    """Fungsi untuk menampilkan menu daftar buku."""
    while True:
        header("PERPUSTAKAAN JEMBER", "MENU DAFTAR BUKU")
        print("1. Tampilkan semua buku")
        print("2. Urutkan buku")
        print("3. Filter berdasarkan genre")
        print("4. Cari buku")
        print("5. Kembali ke menu utama")
        
        choice = input("Pilih menu (1-5): ")

        books = pd.read_csv("books.csv")
        genres = pd.read_csv("genres.csv")
        
        if choice == '1':
            lihat_buku(books, genres)

        elif choice == '2':
            menu_urutkan_buku(books, genres)

        elif choice == '3':
            print("\nDaftar Genre Tersedia:")
            print(tabulate(genres, headers='keys', tablefmt='fancy_grid', showindex=False))
            
            while True:
                try:
                    genre_id = int(input("Masukkan ID genre: "))
                    if genre_id not in genres['genre_id'].values:
                        print("ID genre tidak valid. Silakan coba lagi.")
                        continue
                    break
                except ValueError:
                    print("ID genre harus berupa angka. Silakan coba lagi.")
                    continue

            genre_books = find_books_by_genre(books, genre_id)
            lihat_buku(genre_books, genres)
        
        elif choice == '4':
            while True:
                keyword = input("Masukkan kata kunci untuk mencari buku: ").strip()
                if not keyword:
                    print("Kata kunci tidak boleh kosong. Silakan coba lagi.")
                    continue
                break

            search_results = cari_buku_berdasarkan_keyword(books, keyword)
            lihat_buku(search_results, genres)
        
        elif choice == '5':
            return
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan enter untuk melanjutkan...")
            continue

        if user_id:
            opsi = input("Tekan enter untuk kembali ke menu utama atau ketik 1 untuk meminjam buku: ").strip()
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")
        else:
            input("Tekan enter untuk melanjutkan...")

def lihat_riwayat_peminjaman(user_id=None):
    transaksi = pd.read_csv("transaksi_peminjaman.csv")
    if user_id:
        books = pd.read_csv("books.csv")
        transaksi_buku = transaksi.merge(books, on='book_id', how='left')
        riwayat = transaksi_buku[transaksi_buku['user_id'] == user_id]
        riwayat = riwayat[['title', 'loan_date', 'due_date', 'return_date', 'status']]
        riwayat = riwayat.rename(columns={
            'title': 'Judul Buku',
            'loan_date': 'Tanggal Pinjam',
            'due_date': 'Tanggal Batas Pengembalian',
            'return_date': 'Tanggal Pengembalian',
            'status': 'Status'
        })
        transaksi = riwayat

    if transaksi.empty:
        print("Tidak ada riwayat peminjaman.")
        return
    
    print("\nRiwayat Peminjaman:")
    print(tabulate(transaksi, headers='keys', tablefmt='fancy_grid', showindex=False))

def refresh_transkasi_peminjaman():
    transaksi = pd.read_csv("transaksi_peminjaman.csv")
    
    transaksi_aktif = transaksi[transaksi['status'] == 'aktif']

    if not transaksi_aktif.empty:
        for index, row in transaksi_aktif.iterrows():
            due_date = row['due_date']
            today = datetime.now().strftime('%Y-%m-%d')
            if  today > due_date:
                transaksi.loc[index, 'status'] = 'terlambat'
    
    transaksi.to_csv("transaksi_peminjaman.csv", index=False)

refresh_transkasi_peminjaman()

# FITUR PEMINJAM
def pinjam_buku(user_id):
    books = pd.read_csv("books.csv")
    while True:
        try:
            book_id = int(input("Masukkan ID buku yang ingin dipinjam: "))
        except ValueError:
            print("ID buku harus berupa angka.")
            opsi = input("Tekan enter untuk mencoba lagi atau ketik 0 untuk kembali ke menu daftar buku: ")
            if opsi == '0':
                return
            continue

        if int(book_id) not in books['book_id'].values:
            print("Buku tidak ditemukan!")
            return

        book = books[books['book_id'] == int(book_id)].iloc[0]

        if book['quantity'] <= 0:
            print("Buku tidak tersedia!")
            return

        # Buat transaksi peminjaman
        transaksi = pd.read_csv("transaksi_peminjaman.csv")
        loan_id = transaksi['loan_id'].max() + 1 if not transaksi.empty else 1

        new_transaksi = pd.DataFrame([{
            'loan_id': loan_id,
            'book_id': book_id,
            'user_id': user_id,
            'loan_date': "-",
            'due_date': "-",
            'return_date': "-",
            'status': 'menunggu'
        }])

        transaksi = pd.concat([transaksi, new_transaksi], ignore_index=True)
        transaksi.to_csv("transaksi_peminjaman.csv", index=False)

        print(f"Peminjaman buku {book['title']} berhasil diajukan. Menunggu konfirmasi petugas.")
        break

def kembalikan_buku(user_id):
    transaksi = pd.read_csv("transaksi_peminjaman.csv")
    books = pd.read_csv("books.csv")
    transaksi_aktif = transaksi[(transaksi['user_id'] == user_id) & (transaksi['status'] == 'aktif')]
    
    if transaksi_aktif.empty:
        print("Tidak ada buku yang sedang dipinjam.")
        return
    
    print("\nDaftar Buku yang Dipinjam:")
    daftar_buku = transaksi_aktif.merge(books, on='book_id', how='left')
    daftar_buku = daftar_buku[['loan_id', 'title', 'loan_date', 'due_date']]
    daftar_buku = daftar_buku.rename(columns={
        'loan_id': 'ID Peminjaman',
        'title': 'Judul Buku',
        'loan_date': 'Tanggal Pinjam',
        'due_date': 'Tanggal Batas Pengembalian'
    })
    print(tabulate(daftar_buku, headers='keys', tablefmt='fancy_grid', showindex=False))
    
    while True:
        try:
            loan_id = int(input("Masukkan ID peminjaman yang akan dikembalikan: "))
            if loan_id not in transaksi_aktif['loan_id'].values:
                print("ID peminjaman tidak valid. Silakan coba lagi.")
                continue
            break
        except ValueError:
            print("ID peminjaman harus berupa angka. Silakan coba lagi.")
            continue
    
    idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
    transaksi.loc[idx, 'status'] = 'menunggu_pengecekan'
    
    transaksi.to_csv("transaksi_peminjaman.csv", index=False)
    print("Buku berhasil diajukan untuk dikembalikan. Menunggu konfirmasi petugas.")

# FITUR PETUGAS
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

def hapus_buku(books, genres):
    """Fungsi untuk menghapus buku."""
    while True:
        header("PERPUSTAKAAN JEMBER", "MENGHAPUS BUKU")
        print("Masukkan kata kunci buku yang ingin dihapus (judul/author)")
        keyword = input("(kosongkan inputan jika ingin melihat semua buku):").strip()
        search_results = cari_buku_berdasarkan_keyword(books, keyword)
        lihat_buku(search_results, genres)
        
        try:
            book_id = int(input("Masukkan ID Buku yang ingin dihapus: "))
            if book_id not in books['book_id'].values:
                print("Buku tidak ditemukan!")
                opsi = input("Tekan enter untuk mencoba lagi atau ketik 0 untuk kembali ke menu utama: ").strip()
                if opsi == '0':
                    return
                continue
            
            books = books[books['book_id'] != book_id]
            books.to_csv("books.csv", index=False)
            print(f"Buku dengan ID {book_id} berhasil dihapus.")
            
            opsi = input("Tekan enter untuk menghapus buku lain atau ketik 0 untuk kembali ke menu utama: ").strip()
            if opsi == '0':
                return
            
        except Exception:
            print("Input tidak valid atau terjadi kesalahan.")
            opsi = input("Tekan enter untuk mengulangi atau ketik 0 untuk kembali ke menu utama: ").strip()
            if opsi == '0':
                return

def konfirmasi_peminjaman():
    transaksi = pd.read_csv('transaksi_peminjaman.csv')
    books = pd.read_csv('books.csv')
    
    menunggu_transaksi = transaksi[transaksi['status'] == 'menunggu']
    
    while True:
        header("PERPUSTAKAAN JEMBER", "KONFIRMASI PEMINJAMAN")
        if menunggu_transaksi.empty:
            print("Tidak ada transaksi yang menunggu konfirmasi.")
            input("Tekan enter untuk kembali ke menu utama.")
            return

        print("\nDaftar Peminjaman yang Menunggu Konfirmasi:")
        print(tabulate(menunggu_transaksi, headers='keys', tablefmt='fancy_grid', showindex=False))
        
        loan_id = input("Masukkan ID peminjaman yang akan dikonfirmasi: ")
        
        if not loan_id.isdigit() or int(loan_id) not in menunggu_transaksi['loan_id'].values:
            input("ID peminjaman tidak valid. Silakan coba lagi.")
            continue
        
        confirm = input("Konfirmasi (1. Setujui, 2. Tolak): ")
        
        idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
        
        if confirm == '1':
            today = datetime.now().strftime('%Y-%m-%d')
            due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

            transaksi.loc[idx, 'loan_date'] = today
            transaksi.loc[idx, 'due_date'] = due_date
            transaksi.loc[idx, 'status'] = 'aktif'
            
            # Kurangi stok buku
            book_id = transaksi.loc[idx, 'book_id'].values[0]
            book_idx = books[books['book_id'] == book_id].index
            books.loc[book_idx, 'quantity'] -= 1
            
            books.to_csv('books.csv', index=False)
            print("Peminjaman disetujui. Status berubah menjadi aktif.")
            break  # Exit the loop after successful confirmation
        elif confirm == '2':
            transaksi.loc[idx, 'status'] = 'ditolak'
            print("Peminjaman ditolak.")
            break  # Exit the loop after processing rejection
        else:
            input("Pilihan tidak valid. Silakan coba lagi.")

    transaksi.to_csv('transaksi_peminjaman.csv', index=False)
    opsi = input("Tekan enter untuk mengkonfirmasi peminjaman lain atau ketik 0 untuk kembali ke menu utama: ").strip()
    if opsi == '0':
        return
    else:
        konfirmasi_peminjaman()  # Call the function again to allow further confirmations

def konfirmasi_pengembalian():
    transaksi = pd.read_csv('transaksi_peminjaman.csv')
    books = pd.read_csv('books.csv')

    menunggu_transaksi = transaksi[transaksi['status'] == 'menunggu_pengecekan']
    
    while True:
        header("PERPUSTAKAAN JEMBER", "KONFIRMASI PENGEMBALIAN")
        if menunggu_transaksi.empty:
            print("Tidak ada pengembalian yang menunggu konfirmasi.")
            input("Tekan enter untuk kembali ke menu utama.")
            return

        print("\nDaftar Pengembalian Menunggu Konfirmasi:")
        print(tabulate(menunggu_transaksi, headers='keys', tablefmt='fancy_grid', showindex=False))
    
        loan_id = input("Masukkan ID peminjaman yang akan dikonfirmasi: ")

        if not loan_id.isdigit() or int(loan_id) not in menunggu_transaksi['loan_id'].values:
            input("ID peminjaman tidak valid. Silakan coba lagi.")
            continue

        idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
        transaksi.loc[idx, 'status'] = 'dikembalikan'
        transaksi.loc[idx, 'return_date'] = datetime.now().strftime('%Y-%m-%d')

        # Tambah stok buku
        book_id = transaksi.loc[idx, 'book_id'].values[0]
        book_idx = books[books['book_id'] == book_id].index
        books.loc[book_idx, 'quantity'] += 1

        books.to_csv('books.csv', index=False)
        transaksi.to_csv('transaksi_peminjaman.csv', index=False)
        print("Pengembalian berhasil dikonfirmasi. Status berubah menjadi dikembalikan.")
        break
    
    opsi = input("Tekan enter untuk mengkonfirmasi pengembalian lain atau ketik 0 untuk kembali ke menu utama: ").strip()
    if opsi == '0':
        return
    else:
        konfirmasi_pengembalian()