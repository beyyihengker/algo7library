def main():
    print("\n===========˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊===========")
    print("=====   SELAMAT    DATANG  DI   =====")
    print("=====   PERPUSTAKAAN    JEMBER  =====")
    print("====== SILAKAN  LOGIN  SEBAGAI: =====")
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")

    menu_utama= [
        ["1", "petugas"],
        ["2", "Peminjam"],
        ["3", "Keluar Aplikasi"]
    ]

    try:
        role_pilihan = int(input("Silakan Pilih Opsi Antara 1/2/3: "))

        if role_pilihan == 1:
            role = "petugas"
            nama = input("Silakan Masukkan Username : ")
            password = input("Silakan Masukkan Password: ")
            
        elif role_pilihan == 2:
            role = "peminjam"
            nama = input("Silakan Masukkan Username : ")
            password = input("Silakan Masukkan Password: ")
            
        elif role_pilihan == 3:
            os.system("cls")
            print("Terima kasih telah menggunakan aplikasi kami!!")
            exit()  

        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
            os.system("cls")
            main()

    except ValueError:
        print("Masukkan pilihan yang valid!")
        input("Tekan enter untuk melanjutkan.")
        os.system("cls")
        main()

    while True:
        for account in akun:
            if account["role"] == role and account["username"] == username and account["password"] == password:
                print(f"Login berhasil! Selamat datang, {nama}.")
                os.system("cls")
                interface_petugas() if role == "petugas" else interface_peminjam()
                return
            
        print("Login gagal. Silakan coba lagi.")
        input("Tekan enter untuk kembali")
        os.system("cls")
        main()