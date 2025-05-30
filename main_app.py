import os
from ui import clear_screen
from login import login, registrasi

def main():
    '''Main Menu'''
    clear_screen()
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")
    print("=====   SELAMAT    DATANG  DI   =====")
    print("=====   PERPUSTAKAAN    JEMBER  =====")
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")
    print("Pilih opsi:")
    print("1. Login\n2. Registrasi\n0. Keluar")
    opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
    if opsi == "1":
        username, role = login()
        if role == "petugas":
            # interface_petugas()
            pass
        elif role == "peminjam":
            # interface_peminjam()
            pass
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
            print("Keluar dari aplikasi...")
            exit()
        else:
            main()
    else:
        print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
        input("Tekan ENTER untuk mengulang")
        main()

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()