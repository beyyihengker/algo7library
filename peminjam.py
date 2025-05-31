import pandas as pd
from ui import header, footer

def lihat_buku():
    """Fungsi untuk melihat daftar buku."""
    header("PERPUSTAKAAN JEMBER", "DAFTAR BUKU")
    
    try:
        df = pd.read_csv("buku.csv")
        if df.empty:
            print("Tidak ada buku yang tersedia.")
        else:
            print(df.to_string(index=False))
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    
    input("Tekan enter untuk kembali ke menu peminjam...")

def pinjam_buku(username):
    """Fungsi untuk meminjam buku."""
    header("PERPUSTAKAAN JEMBER", "MEMINJAM BUKU")
    
    try:
        df = pd.read_csv("buku.csv")
        if df.empty:
            print("Tidak ada buku yang tersedia untuk dipinjam.")
            input("Tekan enter untuk kembali ke menu peminjam...")
            return
        
        print(df.to_string(index=False))
        judul_buku = input("Masukkan judul buku yang ingin dipinjam: ").strip()
        
        if judul_buku not in df['judul'].values:
            print("Buku tidak ditemukan. Silakan coba lagi.")
            input("Tekan enter untuk kembali ke menu peminjam...")
            return
        
        # Simpan peminjaman ke file
        with open("peminjaman.txt", "a") as f:
            f.write(f"{username} meminjam buku: {judul_buku}\n")
        
        print(f"Buku '{judul_buku}' berhasil dipinjam oleh {username}.")
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    
    input("Tekan enter untuk kembali ke menu peminjam...")

def interface_peminjam(username):
    """Antarmuka peminjam untuk melihat daftar buku dan meminjam buku."""
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
        lihat_buku()
        interface_peminjam(username)

    elif pilihan == "2":
        pinjam_buku(username)
        interface_peminjam(username)

    elif pilihan == "3":
            return
        
    elif pilihan == "4":
        exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
        if exit_choice == 'y':
            footer()
            exit()
        interface_peminjam(username)
        
    else:
        print("Pilihan tidak valid.")
        input("Tekan enter untuk kembali")
        interface_peminjam(username)

# interface_peminjam()