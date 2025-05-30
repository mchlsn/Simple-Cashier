import time
import sys
import datetime
import getpass

Admin = {
    "rian": "ryan34",
    "indah": "In123",
    "ana": "an22"
}
batas = 3
login_berhasil = False  # inisialisasi login berhasil diluar fungsi
user = None

def login(admin, batas):
    global login_berhasil
    global user
    coba = 0
    while coba < batas:
        logs = input("Silahkan Input Username untuk menjalankan kasir : ")
        if not logs:
            print("Username Tidak Boleh Kosong")
            coba += 1
            print(f"Sisa Percobaan: {batas} - {coba}")
            continue
        if logs in admin:
            pas = getpass.getpass("Masukan Password: ")
            if not pas:
                print("Password Tidak Boleh Kosong !!")
                coba += 1
                print(f"Sisa Percobaan: {batas} - {coba}")
                continue

            if pas == admin[logs]:
                print("Login Berhasil")
                login_berhasil = True  # Set login_berhasil to True on successful login
                user = logs
                return True
            if not pas:
                print("password tidak boleh kosong")
            else:
                print("Password Salah")
        else:
            coba += 1
            print(f"username tidak ditemukan, Sisa percobaan = {batas} - {coba}")

    print("anda telah gagal login 3x.Akun akses ditolak")
    sys.exit()

login(Admin, batas)

if login_berhasil:
    print(f"Selamat Datang {user}")
    print("Aplikasi Kasir Dimulai...")

products = {
    "P001": {"nama": "Telur 1kg", "harga": 12000},
    "P002": {"nama": "Beras 5kg", "harga": 12000},
    "P003": {"nama": "gula 1kg", "harga": 17500},
    "P004": {"nama": "bumbu", "harga": 2000},
    "P005": {"nama": "garam", "harga": 6000},
    "P006": {"nama": "minyak 2L", "harga": 29000}
}
daftar_belanja = []

def show_products(products):
    print("\n=====Stock Barang=====")
    for pid, info in products.items():
        print(f"{pid}: Product = {info['nama']}, Harga = Rp{info['harga']:.2f}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def lihat_riwayat(data_transaksi):
    with open("transaksi.txt","a",encoding= "utf-8") as f:
        f.write("===== Transaksi Baru =====\n")
        f.write(f"Waktu      : {data_transaksi['waktu']}\n")
        f.write(f"Kasir      : {data_transaksi['kasir']}\n")
        f.write("Daftar Belanja:\n")
        for item in data_transaksi['daftar_belanja']:
            f.write(f"  - {item['nama']} x{item['jumlah']} - Rp{item['harga'] * item['jumlah']:.2f}\n")
        f.write(f"Total      : Rp{data_transaksi['total']:.2f}\n")
        f.write(f"Diskon     : Rp{data_transaksi['diskon']:.2f}\n")
        f.write(f"Total Bayar: Rp{data_transaksi['total bayar']:.2f}\n")
        f.write(f"Bayar      : Rp{data_transaksi['uang yang dibayar']:.2f}\n")
        f.write(f"Kembalian  : Rp{data_transaksi['kembalian']:.2f}\n")
        f.write("=========================\n\n")
def tambah_transaksi(products, daftar_belanja):
    while True:
        show_products(products)
        pid = input("Masukkan kode barang/pid: ")
        if pid in products:
            try:
                jumlah = int(input(f"Masukkan jumlah {pid} yang dibeli: "))
                if jumlah > 0:
                    harga_satuan = products[pid]['harga']
                    nama_barang = products[pid]['nama']
                    now = datetime.datetime.now()
                    times = now.strftime("%Y - %m - %d  %H : %M : %S")
                    
                    daftar_belanja.append({"nama": nama_barang, "harga": harga_satuan, "jumlah": jumlah, "waktu": times})
                    print(f"{jumlah} {nama_barang}, Berhasil Ditambahkan Dikeranjang")
                    
                    while True:
                        opsi = input("Tambah barang lagi? (y/n): ").lower()
                        if opsi == "y":
                            break
                        elif opsi == "n":
                            return  # keluar dari fungsi proses transaksi
                        else:
                            print("masukan teks yang valid")
                
                else:
                    print("⚠️jumlah input harus lebih dari 0")
            except ValueError:
                print("⚠️ Input harus berupa angka yang valid!")
        else:
            print("nama barang tidak tersedia silahkan pilih pada list yang tersedia")
            continue
        return
        
    total = sum(item['harga'] * item["jumlah"] for item in daftar_belanja)
    diskon = 0
    total2 = total
    if total > 100000:
        diskon = total * 10/100
        total2 = total - diskon
    else:
        print("Kamu Tidak Dapat Diskon")

    # Menampilkan hasil
    print("\n===== Struk Pembelian =====")
    now = datetime.datetime.now()
    timed = now.strftime("%Y - %m - %d  %H : %M : %S")
    print(f"waktu : {timed}     Admin : {user}")
    for item in daftar_belanja:
        print(f"{item['nama']} x{item['jumlah']} - Rp{item['harga'] * item['jumlah']:.2f}")

    print(f"Total: Rp{total:.2f}")
    print(f"Diskon yang didapat :Rp{diskon:.2f}")
    print(f"Jumlah yang harus dibayar :Rp{total2:.2f}")
    print("Terima kasih telah berbelanja!")

    while True :
        print("Silahkan Pilih Metode Pembayaran :")
        print("1. Tunai")
        print("2. Transfer")

        pembayaran = input("Pilih Metode Pembayaran (1/2): ")
        if pembayaran == "1":
            ban = float(input("Uang Yang DiBayarkan: "))
            if ban < total2:
                print("Uang yang dibayarkan kurang, silahkan ulangi pesanan anda.")
            else:
                kembalian = ban - total2
                print(f"Kembalian: Rp{kembalian:.2f}")
                data_transaksi ={
                    "waktu":timed,
                    "kasir":user,
                    "daftar_belanja": daftar_belanja,
                    "total": total,
                    "diskon": diskon,
                    "total bayar": total2,
                    "uang yang dibayar": ban,
                    "kembalian": kembalian

                }
                simpan_transaksi(data_transaksi)
                print("transaksi berhasil disimpan")
                return
        elif pembayaran == "2":
            print("Transfer Ke 000000000")
            print("Pembayaran Sedang diverifikasi...")
            time.sleep(1)
            print("Pembayaran Berhasil, Terima Kasih!")
            simpan_transaksi(data_transaksi)
            print("transaksi berhasil disimpan")
            return
        else:
            print("Input tidak Valid. Silahkan pilih no.1 atau no.2")

while True:
    print("\nSilahkan Pilih Menu")
    print("1. Lihat Daftar Produk")
    print("2. Tambah Transaksi")
    print("3. Lihat Riwayat Transaksi")
    print("4. Keluar!!")
    inpt = int(input("Silahkan Masukan Pilihan Anda (angka): "))
    if inpt == 1:
        show_products(products)
        input("Tekan ENTER Untuk Kembali")
    elif inpt == 2:
        tambah_transaksi(products, daftar_belanja)#Untuk memanggil fungsi transaksi
        proses_pembayaran(daftar_belanja) # Untuk Panggil fungsi pembayaran setelah transaksi selesai

    elif inpt == 3:
        lihat_riwayat(daftar_belanja)
    elif inpt == 4:
        print("Terima kasih telah menggunakan aplikasi kasir!")
        break
    else:
    	print("Pilihan tidak valid. Silahkan masukkan angka antara 1 dan 4.")