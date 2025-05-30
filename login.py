import os
import pandas as pd
from ui import clear_screen

def login():
    clear_screen()
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")
    print("=====   SELAMAT    DATANG  DI   =====")
    print("=====   PERPUSTAKAAN    JEMBER  =====")
    print("=========== SILAKAN  LOGIN ==========")
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    df = pd.read_csv("akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if ambil_role.empty:
        print("Username atau password salah. Silakan coba lagi.")
        opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali ke menu utama> ")
        if opsi == "0":
            return None, None
        return login()
    else:
        role = ambil_role.iloc[0]['role']
        print(f"Login berhasil.\nSelamat datang {username}.")
        print(f"Anda masuk sebagai {role.capitalize()}.")
        input("Tekan ENTER untuk melanjutkan")

    return username, role

def registrasi():
    '''registrasi'''
    username = input("username: ").strip()
    password = input("password: ").strip()
    role = "peminjam"

    if not username:
        print("Username tidak boleh kosong")
        opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali> ")
        if opsi == "0":
            return
        return registrasi()
    if not password:
        print("Password tidak boleh kosong")
        opsi = input("Tekan ENTER untuk mengulang atau 0 untuk kembali> ")
        if opsi == "0":
            return
        return registrasi()
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
            return registrasi()

        df = pd.read_csv('akun_pengguna.csv')

        if username in df["username"].values:
            print("username sudah ada, buatlah username yang berbeda")
            opsi = input("tekan ENTER untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            return registrasi()

    user_baru = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])

    df = pd.concat([df, user_baru], ignore_index=True)
    df.to_csv('akun_pengguna.csv', index=False)
