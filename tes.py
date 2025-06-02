import pandas as pd
from datetime import datetime, timedelta
import os

# File database
DB_FILES = {
    'akun_pengguna': 'akun_pengguna.csv',
    'books': 'books.csv',
    'genres': 'genres.csv',
    'transaksi_peminjaman': 'transaksi_peminjaman.csv'
}

# Inisialisasi database jika belum ada
def init_db():
    for file in DB_FILES.values():
        if not os.path.exists(file):
            pd.DataFrame().to_csv(file, index=False)

    # Inisialisasi struktur tabel jika kosong
    if os.path.getsize(DB_FILES['akun_pengguna']) == 0:
        pd.DataFrame(columns=['user_id', 'username', 'password', 'role']).to_csv(DB_FILES['akun_pengguna'], index=False)
    
    if os.path.getsize(DB_FILES['books']) == 0:
        pd.DataFrame(columns=['book_id', 'title', 'author', 'genre_id', 'quantity', 'publication_year', 'isbn']).to_csv(DB_FILES['books'], index=False)
    
    if os.path.getsize(DB_FILES['genres']) == 0:
        pd.DataFrame(columns=['genre_id', 'genre_name']).to_csv(DB_FILES['genres'], index=False)
    
    if os.path.getsize(DB_FILES['transaksi_peminjaman']) == 0:
        pd.DataFrame(columns=['loan_id', 'book_id', 'user_id', 'loan_date', 'due_date', 'return_date', 'status']).to_csv(DB_FILES['transaksi_peminjaman'], index=False)

# Fungsi baca database
def read_db(table_name):
    return pd.read_csv(DB_FILES[table_name])

# Fungsi tulis database
def write_db(table_name, df):
    df.to_csv(DB_FILES[table_name], index=False)

# Fungsi untuk peminjaman buku
def pinjam_buku(user_id):
    books = read_db('books')
    print("\nDaftar Buku Tersedia:")
    print(books[['book_id', 'title', 'author', 'quantity']].to_string(index=False))
    
    book_id = input("Masukkan ID buku yang ingin dipinjam: ")
    
    if int(book_id) not in books['book_id'].values:
        print("Buku tidak ditemukan!")
        return
    
    book = books[books['book_id'] == int(book_id)].iloc[0]
    
    if book['quantity'] <= 0:
        print("Buku tidak tersedia!")
        return
    
    # Buat transaksi peminjaman
    transaksi = read_db('transaksi_peminjaman')
    loan_id = transaksi['loan_id'].max() + 1 if not transaksi.empty else 1
    
    today = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    new_transaksi = pd.DataFrame([{
        'loan_id': loan_id,
        'book_id': book_id,
        'user_id': user_id,
        'loan_date': today,
        'due_date': due_date,
        'return_date': None,
        'status': 'menunggu'
    }])
    
    transaksi = pd.concat([transaksi, new_transaksi], ignore_index=True)
    write_db('transaksi_peminjaman', transaksi)
    
    print(f"Peminjaman buku {book['title']} berhasil diajukan. Menunggu konfirmasi petugas.")

# Fungsi untuk konfirmasi peminjaman oleh petugas
def konfirmasi_peminjaman():
    transaksi = read_db('transaksi_peminjaman')
    books = read_db('books')
    
    menunggu_transaksi = transaksi[transaksi['status'] == 'menunggu']
    
    if menunggu_transaksi.empty:
        print("Tidak ada transaksi yang menunggu konfirmasi.")
        return
    
    print("\nDaftar Peminjaman Menunggu Konfirmasi:")
    print(menunggu_transaksi.to_string(index=False))
    
    loan_id = input("Masukkan ID peminjaman yang akan dikonfirmasi: ")
    action = input("Konfirmasi (1. Setujui, 2. Tolak): ")
    
    idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
    
    if action == '1':
        transaksi.loc[idx, 'status'] = 'aktif'
        
        # Kurangi stok buku
        book_id = transaksi.loc[idx, 'book_id'].values[0]
        book_idx = books[books['book_id'] == book_id].index
        books.loc[book_idx, 'quantity'] -= 1
        
        write_db('books', books)
        print("Peminjaman disetujui. Status berubah menjadi aktif.")
    elif action == '2':
        transaksi.loc[idx, 'status'] = 'ditolak'
        print("Peminjaman ditolak.")
    
    write_db('transaksi_peminjaman', transaksi)

# Fungsi untuk pengembalian buku oleh peminjam
def kembalikan_buku(user_id):
    transaksi = read_db('transaksi_peminjaman')
    aktif_transaksi = transaksi[(transaksi['user_id'] == user_id) & (transaksi['status'] == 'aktif')]
    
    if aktif_transaksi.empty:
        print("Tidak ada buku yang sedang dipinjam.")
        return
    
    print("\nDaftar Buku yang Dipinjam:")
    print(aktif_transaksi[['loan_id', 'book_id', 'loan_date', 'due_date']].to_string(index=False))
    
    loan_id = input("Masukkan ID peminjaman yang akan dikembalikan: ")
    
    idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
    transaksi.loc[idx, 'status'] = 'menunggu_pengecekan'
    
    write_db('transaksi_peminjaman', transaksi)
    print("Buku berhasil diajukan untuk dikembalikan. Menunggu konfirmasi petugas.")

# Fungsi untuk konfirmasi pengembalian oleh petugas
def konfirmasi_pengembalian():
    transaksi = read_db('transaksi_peminjaman')
    books = read_db('books')
    
    menunggu_transaksi = transaksi[transaksi['status'] == 'menunggu_pengecekan']
    
    if menunggu_transaksi.empty:
        print("Tidak ada pengembalian yang menunggu konfirmasi.")
        return
    
    print("\nDaftar Pengembalian Menunggu Konfirmasi:")
    print(menunggu_transaksi.to_string(index=False))
    
    loan_id = input("Masukkan ID peminjaman yang akan dikonfirmasi: ")
    
    idx = transaksi[transaksi['loan_id'] == int(loan_id)].index
    transaksi.loc[idx, 'status'] = 'dikembalikan'
    transaksi.loc[idx, 'return_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Tambah stok buku
    book_id = transaksi.loc[idx, 'book_id'].values[0]
    book_idx = books[books['book_id'] == book_id].index
    books.loc[book_idx, 'quantity'] += 1
    
    write_db('books', books)
    write_db('transaksi_peminjaman', transaksi)
    print("Pengembalian dikonfirmasi. Status berubah menjadi dikembalikan.")

# Fungsi untuk melihat riwayat peminjaman
def lihat_riwayat():
    transaksi = read_db('transaksi_peminjaman')
    books = read_db('books')
    
    # Cek dan update status yang terlambat
    today = datetime.now().date()
    aktif_transaksi = transaksi[transaksi['status'] == 'aktif']
    
    for _, row in aktif_transaksi.iterrows():
        due_date = datetime.strptime(row['due_date'], '%Y-%m-%d').date()
        if today > due_date:
            transaksi.loc[transaksi['loan_id'] == row['loan_id'], 'status'] = 'terlambat'
    
    write_db('transaksi_peminjaman', transaksi)
    
    print("\nRiwayat Transaksi Peminjaman:")
    print(transaksi.to_string(index=False))

# Fungsi login
def login():
    akun_pengguna = read_db('akun_pengguna')
    
    username = input("Username: ")
    password = input("Password: ")
    
    user = akun_pengguna[(akun_pengguna['username'] == username) & (akun_pengguna['password'] == password)]
    
    if user.empty:
        print("Login gagal. Username atau password salah.")
        return None
    
    return user.iloc[0]['user_id'], user.iloc[0]['role']

# Menu utama
def main():
    init_db()
    
    print("=== Sistem Perpustakaan ===")
    
    user_info = login()
    if not user_info:
        return
    
    user_id, role = user_info
    
    while True:
        print("\nMenu Utama:")
        if role == 'peminjam':
            print("1. Pinjam Buku")
            print("2. Kembalikan Buku")
            print("3. Keluar")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                pinjam_buku(user_id)
            elif choice == '2':
                kembalikan_buku(user_id)
            elif choice == '3':
                break
            else:
                print("Pilihan tidak valid!")
                
        elif role == 'petugas':
            print("1. Konfirmasi Peminjaman")
            print("2. Konfirmasi Pengembalian")
            print("3. Lihat Riwayat Peminjaman")
            print("4. Keluar")
            
            choice = input("Pilih menu: ")
            
            if choice == '1':
                konfirmasi_peminjaman()
            elif choice == '2':
                konfirmasi_pengembalian()
            elif choice == '3':
                lihat_riwayat()
            elif choice == '4':
                break
            else:
                print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()