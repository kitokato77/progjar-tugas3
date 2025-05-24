import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
        
    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        
        # Extract the command first
        command_parts = string_datamasuk.split(' ', 1)
        if len(command_parts) == 0:
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))
            
        c_request = command_parts[0].strip().lower()
        logging.warning(f"memproses request: {c_request}")
        
        # Handle different commands with special parsing if needed
        if c_request == 'list':
            # LIST has no parameters
            cl = self.file.list([])
            return json.dumps(cl)
            
        elif c_request == 'get':
            # GET has one parameter: filename
            if len(command_parts) < 2:
                return json.dumps(dict(status='ERROR', data='parameter tidak lengkap'))
            filename = command_parts[1].strip()
            cl = self.file.get([filename])
            return json.dumps(cl)
            
        elif c_request == 'upload':
            # UPLOAD has two parameters: filename and base64 content
            # We need to carefully split these because base64 might contain spaces
            if len(command_parts) < 2:
                return json.dumps(dict(status='ERROR', data='parameter tidak lengkap'))
            
            # Split only the first space after the command to get filename
            params_parts = command_parts[1].split(' ', 1)
            if len(params_parts) < 2:
                return json.dumps(dict(status='ERROR', data='parameter tidak lengkap'))
                
            filename = params_parts[0].strip()
            file_content_base64 = params_parts[1].strip()
            
            cl = self.file.upload([filename, file_content_base64])
            return json.dumps(cl)
            
        elif c_request == 'delete':
            # DELETE has one parameter: filename
            if len(command_parts) < 2:
                return json.dumps(dict(status='ERROR', data='parameter tidak lengkap'))
            filename = command_parts[1].strip()
            cl = self.file.delete([filename])
            return json.dumps(cl)
            
        else:
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))


if __name__ == '__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET example.txt"))
    # Test upload
    test_content = base64.b64encode(b"This is test content").decode()
    print(fp.proses_string(f"UPLOAD test.txt {test_content}"))
    # Test delete
    print(fp.proses_string("DELETE test.txt"))
