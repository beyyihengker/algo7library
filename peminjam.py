import fitur as ft
from ui import header, footer

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
            ft.menu_daftar_buku(user_id)

        elif pilihan == "2":
            header("PERPUSTAKAAN JEMBER", "PINJAM BUKU")
            ft.pinjam_buku(user_id)
            input("Tekan enter untuk melanjutkan...")

        elif pilihan == "3":
            pass
        
        elif pilihan == "4":
            pass
    
        elif pilihan == "5":
            return

        elif pilihan == "6":
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
