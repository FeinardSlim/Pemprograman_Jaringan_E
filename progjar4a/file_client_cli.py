import socket
import json
import base64
import logging

server_address=('127.0.0.1',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',7777))
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
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
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    pokijan_counter = 0
    downloadPerRequest = 100
    command_str=f"GET {filename}"
    while pokijan_counter < downloadPerRequest:
        print(command_str,pokijan_counter,downloadPerRequest)
        hasil = send_command(command_str)
        pokijan_counter += 1
        if (hasil['status']=='OK'):
            #proses file dalam bentuk base64 ke bentuk bytes
            namafile= hasil['data_namafile']
            namafile = namafile.split(".")
            namafile_b = namafile[0].strip() + str(pokijan_counter)
            ext = namafile[1].strip()
            namafile = namafile_b + "." + ext
            isifile = base64.b64decode(hasil['data_file'])
            fp = open(namafile,'wb+')
            fp.write(isifile)
            fp.close()
        else:
            print("Gagal")
            return False
    return True


if __name__=='__main__':
    server_address=('127.0.0.1',7777)
    # remote_list()
    # i = 0
    remote_get('pokijan.jpg')
    #remote_get('donalbebek.jpg')

