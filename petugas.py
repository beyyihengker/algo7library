from ui import header, footer

def interface_petugas(user_id):
    while True:
        header("PERPUSTAKAAN JEMBER", "MENU PETUGAS")
        menu_petugas =[
            ["1", "Registrasi akun peminjam"],
            ["2", "Menambahkan buku"],
            ["3", "Melihat daftar buku"],
            ["4", "Peminjaman"]
            ["5", "Pengembalian"]
            ["6", "Logout"],
            ["7", "Keluar Aplikasi"]
        ]
        for menu in menu_petugas:
            print(f"{menu[0]}. {menu[1]}")
    
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            pass


        elif pilihan == "2":
            # lihat_buku()
            interface_petugas(user_id)

        elif pilihan == "3":
            # tambah_buku()
            interface_petugas(user_id)

        elif pilihan == "4":
            # lihat_peminjaman()
            interface_petugas(user_id)
        
        elif pilihan == "5":
            # konfirmasi_pengembalian()
            interface_petugas(user_id)
        
        elif pilihan == "6":
            return
        
        elif pilihan == "6":
            exit_choice = input("Apakah Anda yakin ingin keluar? (y/n): ").strip().lower()
            if exit_choice == 'y':
                footer()
                exit()
            interface_petugas(user_id)
        
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")
            interface_petugas(user_id)
