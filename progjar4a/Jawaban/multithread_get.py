from file_client_cli import remote_get
import threading

def download(filename):
    texec = dict()
    for i in range(100):
        print(f'Downloading File of {i}')
        texec[i] = threading.Thread(target=remote_get, args=(filename,))
        texec[i].start()
    for i in texec:
        texec[i].join()

if __name__ == '__main__':
    filename = 'pokijan.jpg'
    download(filename)