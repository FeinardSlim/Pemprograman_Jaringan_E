import logging
import requests
import os
import time
import datetime
import socket


def get_url_list():
    urls = dict()
    urls['kompas']='https://asset.kompas.com/crops/qz_jJxyaZgGgboomdCEXsfbSpec=/0x0:998x665/740x500/data/photo/2020/03/01/5e5b52f4db896.jpg'
    urls['its']='https://www.its.ac.id/wp-content/uploads/2017/10/logo-its-1.png'
    urls['detik']='https://akcdn.detik.net.id/community/media/visual/2021/04/22/detikcom-ramadan-desktop-1.gif'
    urls['file1']='https://file-examples-com.github.io/uploads/2018/04/file_example_MOV_480_700kB.mov'
    # urls['file2']='https://file-examples-com.github.io/uploads/2018/04/file_example_MOV_1280_1_4MB.mov'
    urls['file3']='https://file-examples-com.github.io/uploads/2017/02/zip_2MB.zip'
    return urls


def download_gambar(url=None,tuliskefile=True):
    waktu_awal = datetime.datetime.now()
    if (url is None):
        return False
    ff = requests.get(url)
    tipe = dict()
    tipe['image/png']='png'
    tipe['image/jpg']='jpg'
    tipe['image/gif']='gif'
    tipe['image/jpeg']='jpg'
    tipe['application/zip']='jpg'
    tipe['video/quicktime']='mov'

    content_type = ff.headers['Content-Type']
    logging.warning(content_type)
    if (content_type in list(tipe.keys())):
        namafile = os.path.basename(url)
        ekstensi = tipe[content_type]
        if (tuliskefile):
            fp = open(f"{namafile}","wb")
            fp.write(ff.content)
            fp.close()
        waktu_process = datetime.datetime.now() - waktu_awal
        waktu_akhir =datetime.datetime.now()
        logging.warning(f"writing {namafile}.{ekstensi} dalam waktu {waktu_process} {waktu_awal} s/d {waktu_akhir} \n Sending File now")
        return send(namafile)
    else:
        return False

def send(filename):
    waktu_sekarang = datetime.datetime.now()
    host = '127.0.0.1'
    port = 8989
    address = (host,port)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(address)
    time.sleep(2)

    fp = open(f'{filename}', 'rb')
    # print('nama file',filename.encode())
    sock.send(filename.encode())
    time.sleep(1)

    # send file
    while True:
        data_buffer = fp.read(32)
        # print(data_buffer)
        if not data_buffer:
            break
        sock.sendall(data_buffer)

    sock.send('\x00end'.encode())
    sock.close()
    fp.close()
    waktu_akhir = datetime.datetime.now()
    total_process = waktu_akhir - waktu_sekarang
    logging.warning(f"sending dalam waktu {waktu_sekarang}  s/d {waktu_akhir} dengan process selama {total_process}")
    return

if __name__=='__main__':
    #check fungsi
    k = download_gambar('https://asset.kompas.com/crops/qz_jJxyaZgGgboomdCEXsfbSpec=/0x0:998x665/740x500/data/photo/2020/03/01/5e5b52f4db896.jpg')
    print(k)