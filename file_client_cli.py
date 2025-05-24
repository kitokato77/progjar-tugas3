import socket
import json
import base64
import logging
import os

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received = "" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data sending/receiving: {str(e)}")
        return False


def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {namafile} berhasil didownload")
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False

def remote_upload(local_filename="", remote_filename=""):
    if remote_filename == "":
        remote_filename = os.path.basename(local_filename)
    
    try:
        # Read the file and encode to base64
        with open(local_filename, 'rb') as fp:
            file_content = fp.read()
        
        file_content_base64 = base64.b64encode(file_content).decode()
        
        # Send the command "UPLOAD filename" first, followed by the base64 content
        # This ensures proper command parsing on the server side
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

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    
    if (hasil['status'] == 'OK'):
        print(f"{hasil['data']}")
        return True
    else:
        print(f"Gagal menghapus: {hasil['data']}")
        return False


if __name__ == '__main__':
    server_address = ('127.0.0.1', 6666)
    
    # Set up basic logging configuration
    logging.basicConfig(level=logging.WARNING)
    
    # Show menu for user interaction
    while True:
        print("\n==== FILE SERVER CLIENT ====")
        print("1. List Files")
        print("2. Download File")
        print("3. Upload File")
        print("4. Delete File")
        print("0. Exit")
        
        choice = input("Choose an option: ")
        
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
