def interface_petugas():
    while True:
        print("\n==========˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊==========")
        print("==== Selamat  Datang,  Petugas ====")
        print("========    Menu  Petugas   =======")
        print("===========˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊===========")
        menu_petugas =[
            ["1", "Registrasi akun peminjam"],
            ["2", "Menambahkan buku"],
            ["3", "Melihat daftar buku"],
            ["4", "Peminjaman"]
            ["5", "Pengembalian"]
            ["6", "Logout"],
            ["7", "Keluar Aplikasi"]
        ]
    
        pilihan = int(input("Pilih menu: "))
        
        if pilihan == "1":


        elif pilihan == "2":


        elif pilihan == "5":
            os.system("cls")
            main()
        
        elif pilihan == "6":
            os.system("cls")
            print("Keluar dari aplikasi...")
            exit()
        
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
            os.system("cls")
            interface_petugas()