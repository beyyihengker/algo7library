import pandas as pd
import fitur as ft
from ui import header, footer
from datetime import datetime, timedelta

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
            ft.find_books_by_genre(books, genres) # jgn lupa
            opsi = input("Tekan enter untuk kembali ke menu daftar buku atau ketik 1 untuk meminjam buku: ")
            if opsi == '1':
                pinjam_buku(user_id)
                input("Tekan enter untuk melanjutkan...")

def interface_peminjam(user_id):
    """Antarmuka peminjam untuk melihat daftar buku dan meminjam buku."""
    while True:
        header("PERPUSTAKAAN JEMBER", "MENU PEMINJAM")

        menu_petugas =[
            ["1", "Melihat daftar buku"],
            ["2", "Meminjam buku"],
            ["3", "Logout"],
            ["4", "Keluar Aplikasi"]
        ]
        for menu in menu_petugas:
            print(f"{menu[0]}. {menu[1]}")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            menu_daftar_buku(user_id)

        elif pilihan == "2":
            pinjam_buku(user_id)
    
        elif pilihan == "3":
                return

        elif pilihan == "4":
            exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
            if exit_choice == 'y':
                footer()
                exit()

        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")

# interface_peminjam()