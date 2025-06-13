"""Aplikasi Utama Pengelolaan Perpustakaan"""

# Third-Party Library
import pandas as pd

# Local imports
import modules.fitur as ft
import modules.peminjam as pj
import modules.petugas as pt
from modules.login import login, registrasi
from ui.ui import header, footer

def main():
    '''Main Menu'''
    users = pd.read_csv("data/akun_pengguna.csv")
    ft.refresh_transkasi_peminjaman()
    header("SELAMAT DATANG DI", "PERPUSTAKAAN JEMBER")
    print("Pilih opsi:")
    print("1. Login\n2. Registrasi\n0. Keluar")
    opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
    if opsi == "1":
        user_id = login()
        if user_id is not None:
            role = users.loc[users['user_id'] == user_id, 'role'].values[0]
            if role == "petugas":
                pt.interface_petugas()
                input("Tekan ENTER untuk kembali ke menu utama")
                main()
            elif role == "peminjam":
                pj.interface_peminjam(user_id)
                input("Tekan ENTER untuk kembali ke menu utama")
                main()
        else:
            main()
    elif opsi == "2":
        registrasi()
        print("Akun berhasil dibuat. Silahkan login ulang!")
        input("Tekan ENTER untuk melanjutkan")
        main()

    elif opsi == "0":
        exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
        if exit_choice == 'y':
            footer()
            exit()
        elif exit_choice == 'n':
            input("Tekan enter untuk kembali ke menu utama.")
        else:
            input("Pilihan tidak valid. Tekan enter untuk kembali ke menu utama.")
        main()
    else:
        print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
        input("Tekan ENTER untuk mengulang")
        main()

if __name__ == "__main__":
    main()
