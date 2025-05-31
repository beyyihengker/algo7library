from ui import header, footer
from login import login, registrasi
import peminjam as pj
import petugas as pt

def main():
    '''Main Menu'''
    header("SELAMAT DATANG DI", "PERPUSTAKAAN JEMBER")
    print("Pilih opsi:")
    print("1. Login\n2. Registrasi\n0. Keluar")
    opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
    if opsi == "1":
        username, role = login()
        if role == "petugas":
            pt.interface_petugas(username)
        elif role == "peminjam":
            pj.interface_peminjam(username)
            input("Tekan ENTER untuk kembali ke menu utama")
            main()
        elif role is None:
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
        else:
            main()
    else:
        print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
        input("Tekan ENTER untuk mengulang")
        main()

if __name__ == "__main__":
    main()