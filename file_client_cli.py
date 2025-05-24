import socket 
import json  
import base64 
import logging 
import os

# Alamat dan port default server
server_address = ('0.0.0.0', 7777)

# Fungsi untuk mengirim perintah ke server
def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat socket TCP
    sock.connect(server_address)  # Terhubung ke server
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())  # Kirim perintah sebagai bytes

        # Menerima data dari server, dalam bentuk bertahap (chunk)
        data_received = ""  # buffer untuk menampung data
        while True:
            data = sock.recv(16)  # Terima data dalam potongan 16 byte
            if data:
                data_received += data.decode()  # Gabungkan ke buffer
                if "\r\n\r\n" in data_received:  # Protokol untuk akhir data
                    break
            else:
                break  # Tidak ada data lagi

        # Ubah string JSON menjadi dictionary Python
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data sending/receiving: {str(e)}")
        return False

# Fungsi untuk menampilkan daftar file di server
def remote_list():
    command_str = f"LIST"  # Kirim perintah LIST
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:  # Tampilkan semua nama file
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

# Fungsi untuk mengunduh file dari server
def remote_get(filename=""):
    command_str = f"GET {filename}"  # Kirim perintah GET <nama file>
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        # Decode isi file dari base64 ke bytes
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])

        # Simpan file hasil download ke disk
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {namafile} berhasil didownload")
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False

# Fungsi untuk mengunggah file ke server
def remote_upload(local_filename="", remote_filename=""):
    if remote_filename == "":
        # Jika nama remote tidak diisi, gunakan nama file lokal
        remote_filename = os.path.basename(local_filename)

    try:
        # Baca isi file lokal dan encode ke base64
        with open(local_filename, 'rb') as fp:
            file_content = fp.read()
        file_content_base64 = base64.b64encode(file_content).decode()

        # Format perintah: UPLOAD <nama file> <isi file base64>
        command_str = f"UPLOAD {remote_filename} {file_content_base64}"
        hasil = send_command(command_str)

        if (hasil['status'] == 'OK'):
            print(f"File {remote_filename} berhasil diupload")
            return True
        else:
            print(f"Gagal upload: {hasil['data']}")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Fungsi untuk menghapus file dari server
def remote_delete(filename=""):
    command_str = f"DELETE {filename}"  # Kirim perintah DELETE <nama file>
    hasil = send_command(command_str)
    
    if (hasil['status'] == 'OK'):
        print(f"{hasil['data']}")
        return True
    else:
        print(f"Gagal menghapus: {hasil['data']}")
        return False

# Bagian utama program
if __name__ == '__main__':
    server_address = ('127.0.0.1', 6666)  # Ganti alamat server saat dijalankan

    # Konfigurasi logging
    logging.basicConfig(level=logging.WARNING)

    # Menu interaktif untuk pengguna
    while True:
        print("\n==== FILE SERVER CLIENT ====")
        print("1. List Files")        # Menampilkan semua file yang tersedia di server
        print("2. Download File")     # Mengunduh file dari server
        print("3. Upload File")       # Mengunggah file ke server
        print("4. Delete File")       # Menghapus file dari server
        print("0. Exit")              # Keluar dari program
        
        choice = input("Choose an option: ")  # Ambil input pilihan

        if choice == "1":
            remote_list()
        elif choice == "2":
            filename = input("Enter filename to download: ")
            remote_get(filename)
        elif choice == "3":
            local_filename = input("Enter local filename to upload: ")
            remote_filename = input("Enter remote filename (leave blank to use local filename): ")
            remote_upload(local_filename, remote_filename)
        elif choice == "4":
            filename = input("Enter filename to delete: ")
            remote_delete(filename)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")
