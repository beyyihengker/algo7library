def interface_peminjam():
    while True:
        print("\n======˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊=======")
        print("====  Selamat  Datang!  ====")
        print("=====   Menu Peminjam  =====")
        print("========˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊========")
        menu_petugas =[
            ["1", "Melihat daftar buku"],
            ["2", "Meminjam buku"],
            ["3", "Logout"],
            ["4", "Keluar Aplikasi"]
        ]
    
        pilihan = int(input("Pilih menu: "))
        
        if pilihan == "1":


        elif pilihan == "2":


        elif pilihan == "3":
            os.system("cls")
            main()
        
        elif pilihan == "4":
            os.system("cls")
            print("Keluar dari aplikasi...")
            exit()
        
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
            os.system("cls")
            interface_peminjam()