import pandas as pd
import fitur as ft
from ui import header, footer
from datetime import datetime, timedelta
from tabulate import tabulate

def pinjam_buku(user_id):
    books = pd.read_csv("books.csv")
    while True:
        try:
            book_id = int(input("Masukkan ID buku yang ingin dipinjam: "))
        except ValueError:
            print("ID buku harus berupa angka. Silakan coba lagi.")
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

        today = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        new_transaksi = pd.DataFrame([{
            'loan_id': loan_id,
            'book_id': book_id,
            'user_id': user_id,
            'loan_date': today,
            'due_date': due_date,
            'return_date': None,
            'status': 'menunggu'
        }])

        transaksi = pd.concat([transaksi, new_transaksi], ignore_index=True)
        transaksi.to_csv("transaksi_peminjaman.csv", index=False)

        print(f"Peminjaman buku {book['title']} berhasil diajukan. Menunggu konfirmasi petugas.")
        break

def kembalikan_buku(user_id):
    transaksi = pd.read_csv("transaksi_peminjaman.csv")
    transaksi_aktif = transaksi[(transaksi['user_id'] == user_id) & (transaksi['status'] == 'aktif')]
    
    if transaksi_aktif.empty:
        print("Tidak ada buku yang sedang dipinjam.")
        return
    
    print("\nDaftar Buku yang Dipinjam:")
    daftar_buku = transaksi_aktif[['loan_id', 'book_id', 'loan_date', 'due_date']]
    print(tabulate(daftar_buku, headers='keys', tablefmt='fancy_grid', showindex=False))
    
    loan_id = input("Masukkan ID peminjaman yang akan dikembalikan: ")
    
    idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
    transaksi.loc[idx, 'status'] = 'menunggu_pengecekan'
    
    transaksi.to_csv("transaksi_peminjaman.csv", index=False)
    print("Buku berhasil diajukan untuk dikembalikan. Menunggu konfirmasi petugas.")

def lihat_riwayat_peminjaman(user_id):
    transaksi = pd.read_csv("transaksi_peminjaman.csv")
    books = pd.read_csv("books.csv")
    transaksi_buku = transaksi.merge(books, on='book_id', how='left')
    riwayat = transaksi_buku[transaksi_buku['user_id'] == user_id]
    riwayat = riwayat[['loan_id', 'title', 'loan_date', 'due_date', 'return_date', 'status']]
    riwayat = riwayat.rename(columns={
        'loan_id': 'ID Peminjaman',
        'title': 'Judul Buku',
        'loan_date': 'Tanggal Pinjam',
        'due_date': 'Tanggal Batas Pengembalian',
        'return_date': 'Tanggal Pengembalian',
        'status': 'Status'
    })

    if riwayat.empty:
        print("Tidak ada riwayat peminjaman.")
        return
    
    print("\nRiwayat Peminjaman:")
    print(tabulate(riwayat, headers='keys', tablefmt='fancy_grid', showindex=False))

def menu_urutkan_buku(books, genres, user_id):
    """Fungsi untuk mengurutkan buku berdasarkan pilihan pengguna."""
    header("PERPUSTAKAAN JEMBER", "URUTKAN BUKU")
    print("Pilih kriteria pengurutan:")
    print("1. Judul (A-Z)")
    print("2. Judul (Z-A)")
    print("3. Tahun Terbit (Terbaru)")
    print("4. Tahun Terbit (Terlama)")
    
    sort_choice = input("Pilihan (1-4): ")
    
    if sort_choice == '1':
        sorted_books = ft.optimized_merge_sort(books, key='title', ascending=True)
    elif sort_choice == '2':
        sorted_books = ft.optimized_merge_sort(books, key='title', ascending=False)
    elif sort_choice == '3':
        sorted_books = ft.optimized_merge_sort(books, key='publication_year', ascending=False)
    elif sort_choice == '4':
        sorted_books = ft.optimized_merge_sort(books, key='publication_year', ascending=True)
    else:
        print("Pilihan tidak valid!")
        return
    
    ft.lihat_buku(sorted_books, genres)

def menu_daftar_buku(user_id):
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
            ft.lihat_buku(books, genres)
            opsi = input("Tekan enter untuk kembali ke menu daftar buku atau ketik 1 untuk meminjam buku: ")
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")

        elif choice == '2':
            menu_urutkan_buku(books, genres, user_id)
            opsi = input("Tekan enter untuk kembali ke menu daftar buku atau ketik 1 untuk meminjam buku: ")
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")
        
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

            genre_books = ft.find_books_by_genre(books, genre_id)
            ft.lihat_buku(genre_books, genres)
            opsi = input("Tekan enter untuk kembali ke menu daftar buku atau ketik 1 untuk meminjam buku: ")
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")
        
        elif choice == '4':
            while True:
                keyword = input("Masukkan kata kunci untuk mencari buku: ").strip()
                if not keyword:
                    print("Kata kunci tidak boleh kosong. Silakan coba lagi.")
                    continue
                break

            search_results = ft.cari_buku_berdasarkan_keyword(books, keyword)
            ft.lihat_buku(search_results, genres)
            opsi = input("Tekan enter untuk kembali ke menu daftar buku atau ketik 1 untuk meminjam buku: ")
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")
        
        elif choice == '5':
            return
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan enter untuk melanjutkan...")
            continue

def interface_peminjam(user_id):
    """Antarmuka peminjam untuk melihat daftar buku dan meminjam buku."""
    while True:
        header("PERPUSTAKAAN JEMBER", "MENU PEMINJAM")
        print("1. Lihat Daftar Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. Lihat Riwayat Peminjaman")
        print("5. Logout")
        print("6. Keluar Aplikasi")       

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            menu_daftar_buku(user_id)

        elif pilihan == "2":
            header("PERPUSTAKAAN JEMBER", "PINJAM BUKU")
            pinjam_buku(user_id)
            input("Tekan enter untuk melanjutkan...")

        elif pilihan == "3":
            header("PERPUSTAKAAN JEMBER", "KEMBALIKAN BUKU")
            kembalikan_buku(user_id)
            input("Tekan enter untuk melanjutkan...")
        
        elif pilihan == "4":
            header("PERPUSTAKAAN JEMBER", "RIWAYAT PEMINJAMAN")
            lihat_riwayat_peminjaman(user_id)
            input("Tekan enter untuk melanjutkan...")
    
        elif pilihan == "5":
                return

        elif pilihan == "6":
            exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
            if exit_choice == 'y':
                footer()
                exit()
            input("Pilihan tidak valid. Tekan enter untuk kembali ke menu utama.")

        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
