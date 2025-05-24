from socket import *
import socket
import threading
import logging
import time
import sys


from file_protocol import FileProtocol  # Mengimpor FileProtocol (modul harus tersedia)
fp = FileProtocol()  # Membuat instance dari FileProtocol untuk memproses perintah file


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection   # Menyimpan socket koneksi klien
        self.address = address         # Menyimpan alamat klien
        threading.Thread.__init__(self)  # Inisialisasi kelas Thread

    def run(self):
        buffer_size = 2048  # Ukuran buffer saat membaca data dari klien (disesuaikan agar cukup untuk upload file)
        data_received = ""  # Menampung data yang diterima secara bertahap
        
        while True:
            data = self.connection.recv(buffer_size)  # Menerima data dari klien
            if data:
                d = data.decode()             # Decode dari bytes ke string
                data_received += d            # Tambahkan ke buffer sementara
                
                # Proses data hanya jika ada input
                if len(data_received) > 0:
                    hasil = fp.proses_string(data_received)  # Proses menggunakan FileProtocol
                    hasil = hasil + "\r\n\r\n"               # Akhiri dengan pemisah agar klien tahu akhir pesan
                    self.connection.sendall(hasil.encode())  # Kirim balik hasilnya
                    data_received = ""                       # Reset buffer
            else:
                break  # Jika tidak ada data diterima, keluar dari loop
        self.connection.close()  # Tutup koneksi setelah klien selesai

class Server(threading.Thread):
    def __init__(self, ipaddress='0.0.0.0', port=8889):
        self.ipinfo = (ipaddress, port)       # Simpan info IP dan port
        self.the_clients = []                 # List untuk menyimpan thread klien yang sedang berjalan
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat socket TCP
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse alamat/port agar bisa restart server
        threading.Thread.__init__(self)  # Inisialisasi thread

    def run(self):
        logging.warning(f"server berjalan di ip address {self.ipinfo}")  # Cetak info IP dan port
        self.my_socket.bind(self.ipinfo)  # Binding socket ke IP dan port
        self.my_socket.listen(1)          # Server mulai mendengarkan (1 klien minimum dalam backlog)
        
        while True:
            self.connection, self.client_address = self.my_socket.accept()  # Menerima koneksi dari klien
            logging.warning(f"connection from {self.client_address}")       # Cetak alamat klien yang terkoneksi

            clt = ProcessTheClient(self.connection, self.client_address)  # Buat thread baru untuk klien
            clt.start()                         # Jalankan thread klien
            self.the_clients.append(clt)        # Tambahkan ke daftar thread aktif

def main():
    # Konfigurasi logging agar pesan level WARNING dicetak
    logging.basicConfig(level=logging.WARNING)
    
    # Inisialisasi server dengan IP 0.0.0.0 (semua interface) dan port 6666
    svr = Server(ipaddress='0.0.0.0', port=6666)
    svr.start()  # Jalankan thread server

# Menjalankan fungsi main jika file ini dijalankan langsung
if __name__ == "__main__":
    main()
