from ui import header, footer
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import fitur as ft

def interface_petugas():
    while True:
        header("PERPUSTAKAAN JEMBER", "MENU PETUGAS")
        
        print("1. Lihat Daftar Buku")
        print("2. Tambah Buku")
        print("3. Hapus Buku")
        print("4. Konfirmasi Peminjaman")
        print("5. Konfirmasi Pengembalian")
        print("6. lihat Riwayat Peminjaman")
        print("7. Logout")
        print("8. Keluar Aplikasi")

        pilihan = input("Pilih menu: ").strip()

        books = pd.read_csv("books.csv")
        genres = pd.read_csv("genres.csv")
        
        if pilihan == "1":
            ft.menu_daftar_buku()

        elif pilihan == "2":
            ft.tambah_buku(books,genres)

        elif pilihan == "3":
            ft.hapus_buku(books, genres)

        elif pilihan == "4":
            ft.konfirmasi_peminjaman()
        
        elif pilihan == "5":
            ft.konfirmasi_pengembalian()

        elif pilihan == "6":
            ft.lihat_riwayat_peminjaman()
            input("Tekan enter untuk melanjutkan...")
        
        elif pilihan == "7":
            return
        
        elif pilihan == "8":
            exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
            if exit_choice == 'y':
                footer()
                exit()
            elif exit_choice == 'n':
                input("Tekan enter untuk kembali ke menu utama.")
            else:
                input("Pilihan tidak valid. Tekan enter untuk kembali ke menu utama.")
        
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
