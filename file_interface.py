import os      # Modul os digunakan untuk operasi terkait sistem file, seperti memeriksa atau membuat direktori
import json    # Modul json untuk encoding dan decoding data JSON (meskipun pada kode ini tidak langsung digunakan)
import base64  # Modul base64 untuk encoding file dalam format base64 dan decoding kembali ke binary
from glob import glob  # Fungsi glob untuk mencari file dengan pola tertentu (misalnya: *.*)

class FileInterface:
    def __init__(self):
        # Pastikan direktori 'files' ada, jika tidak maka dibuat
        if not os.path.exists('files'):
            os.makedirs('files')
        # Ubah direktori kerja ke folder 'files'
        os.chdir('files/')

    def list(self, params=[]):
        """
        Fungsi untuk mengambil daftar file dalam direktori saat ini.
        Menggunakan glob dengan pola '*.*' untuk mencari file yang memiliki titik (mengindikasikan adanya ekstensi)
        """
        try:
            filelist = glob('*.*')  # Mencari file dengan pola yang diberikan
            return dict(status='OK', data=filelist)  # Kembalikan dictionary dengan status OK dan daftar file
        except Exception as e:
            # Jika terjadi error, kembalikan status ERROR dan pesan errornya
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        """
        Fungsi untuk membaca dan mengembalikan isi file yang diminta.
        File yang dibaca dikonversi ke dalam format base64 sebelum dikembalikan.
        
        Parameter:
          params[0] : nama file yang ingin diambil
        """
        try:
            filename = params[0]
            if (filename == ''):
                # Jika nama file kosong, kembalikan error
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
                
            if not os.path.exists(filename):
                # Jika file tidak ditemukan, kembalikan error
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            # Buka file dalam mode binary untuk membaca isi file
            fp = open(f"{filename}", 'rb')
            # Baca file dan encode ke dalam base64
            isifile = base64.b64encode(fp.read()).decode()
            fp.close()
            # Kembalikan hasil dalam dictionary beserta nama file dan isinya yang sudah diencode
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def upload(self, params=[]):
        """
        Fungsi untuk menerima file yang diunggah.
        File akan diterima dalam bentuk string base64 yang kemudian didecode dan disimpan ke dalam file baru.
        
        Parameter:
          params[0] : nama file yang akan disimpan
          params[1] : konten file dalam bentuk base64
        """
        try:
            # Pastikan terdapat minimal 2 parameter (nama file dan konten file)
            if len(params) < 2:
                return dict(status='ERROR', data='Parameter tidak lengkap')
                
            filename = params[0]
            file_content_base64 = params[1]
            
            # Jika nama file atau konten kosong, kembalikan error
            if (filename == '' or file_content_base64 == ''):
                return dict(status='ERROR', data='Nama file atau konten tidak boleh kosong')
                
            # Decode konten file dari base64 menjadi bytes
            file_content = base64.b64decode(file_content_base64)
            
            # Tulis bytes ke file dengan mode write binary
            with open(filename, 'wb') as fp:
                fp.write(file_content)
                
            # Kembalikan status OK beserta nama file yang disimpan
            return dict(status='OK', data_namafile=filename)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def delete(self, params=[]):
        """
        Fungsi untuk menghapus file yang diminta.
        
        Parameter:
          params[0] : nama file yang akan dihapus
        """
        try:
            # Pastikan parameter tidak kosong
            if len(params) < 1:
                return dict(status='ERROR', data='Parameter tidak lengkap')
                
            filename = params[0]
            if (filename == ''):
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
                
            # Periksa apakah file benar-benar ada
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            # Hapus file tersebut
            os.remove(filename)
            return dict(status='OK', data=f'File {filename} berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    # Inisialisasi objek FileInterface
    f = FileInterface()
    
    # Panggil method list untuk menampilkan daftar file yang ada
    print(f.list())
    
    # Uji operasi get (membaca file), misalnya file 'example.txt'
    print(f.get(['example.txt']))
    
    # Uji operasi upload:
    # Mengunggah file dengan nama 'test.txt' dan isi "This is a test file"
    print(f.upload(['test.txt', base64.b64encode(b'This is a test file').decode()]))
    
    # Tampilkan kembali daftar file untuk melihat file baru yang diupload
    print(f.list())
    
    # Uji operasi delete: menghapus file 'test.txt'
    print(f.delete(['test.txt']))
    
    # Tampilkan daftar file kembali setelah proses penghapusan
    print(f.list())
