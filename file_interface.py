import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        # Ensure the files directory exists
        if not os.path.exists('files'):
            os.makedirs('files')
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
                
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            fp.close()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def upload(self, params=[]):
        try:
            if len(params) < 2:
                return dict(status='ERROR', data='Parameter tidak lengkap')
                
            filename = params[0]
            file_content_base64 = params[1]
            
            if (filename == '' or file_content_base64 == ''):
                return dict(status='ERROR', data='Nama file atau konten tidak boleh kosong')
                
            # Decode base64 content to binary
            file_content = base64.b64decode(file_content_base64)
            
            # Write to file
            with open(filename, 'wb') as fp:
                fp.write(file_content)
                
            return dict(status='OK', data_namafile=filename)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def delete(self, params=[]):
        try:
            if len(params) < 1:
                return dict(status='ERROR', data='Parameter tidak lengkap')
                
            filename = params[0]
            if (filename == ''):
                return dict(status='ERROR', data='Nama file tidak boleh kosong')
                
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File {filename} tidak ditemukan')
                
            # Delete the file
            os.remove(filename)
            return dict(status='OK', data=f'File {filename} berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    f = FileInterface()
    print(f.list())
    # Test get operation
    print(f.get(['example.txt']))
    # Test upload operation
    print(f.upload(['test.txt', base64.b64encode(b'This is a test file').decode()]))
    print(f.list())
    # Test delete operation
    print(f.delete(['test.txt']))
    print(f.list())
