"""Login dan Registrasi Pengguna Perpustakaan"""

import pandas as pd
from ui.ui import header

def login():
    """Fungsi login pengguna perpustakaan"""
    header("PERPUSTAKAAN JEMBER", "LOGIN AKUN PENGGUNA")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    df = pd.read_csv("data/akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if ambil_role.empty:
        print("Username atau password salah. Silakan coba lagi.")
        opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali ke menu utama> ")
        if opsi == "0":
            return None
        return login()
    else:
        user_id = ambil_role.iloc[0]['user_id']
        role = ambil_role.iloc[0]['role']
        print(f"Login berhasil.\nSelamat datang {username}.")
        print(f"Anda masuk sebagai {role.capitalize()}.")
        input("Tekan ENTER untuk melanjutkan")

    return user_id

def registrasi():
    """Fungsi registrasi sebagai peminjam perpustakaan"""

    df = pd.read_csv('data/akun_pengguna.csv')

    while True:
        header("PERPUSTAKAAN JEMBER", "REGISTRASI AKUN PENGGUNA")
        username = input("username: ").strip()
        password = input("password: ").strip()
        role = "peminjam"
        user_id = df['user_id'].max() + 1 if not df.empty else 1

        if not username:
            print("Username tidak boleh kosong")
            opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        if not password:
            print("Password tidak boleh kosong")
            opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        if password:
            huruf = False
            angka = False
            for karakter in password:
                if karakter.isalpha():
                    huruf = True
                if karakter.isnumeric():
                    angka = True

            if not (huruf and angka):
                print("Password harus berupa huruf dan angka")
                opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

            if username in df["username"].values:
                print("username sudah ada, buatlah username yang berbeda")
                opsi = input("tekan ENTER untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

            break

    user_baru = pd.DataFrame([[user_id, username, password, role]],
                             columns=["user_id", "username", "password", "role"])

    df = pd.concat([df, user_baru], ignore_index=True)
    df.to_csv('akun_pengguna.csv', index=False)
