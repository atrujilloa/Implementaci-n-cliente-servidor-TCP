import socket
import os
import math
import hashlib
import time

port = 65432
s = socket.socket()
host = "0.0.0.0"
s.bind((host, port))

s.listen(25)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

countC = 0
while True:
    conn, addr = s.accept()
    countC = countC + 1
    if(countC>0):
        menu = "1. Archivo 100 Mb\n2. Archivo 250 Mb\n"
        conn.send(menu.encode())
        data = conn.recv(1024)
        eleccion = data.decode()
        try:
            if(eleccion=="1"):
                start = time.time()
                hashMD = md5("archivo1.mp4")
                conn.send(hashMD.encode())
                size = os.path.getsize('archivo1.mp4')
                sizes = size/1024
                with open("archivo1.mp4", "rb") as f:
                    while True:
                        byte = f.read(1024)
                        if not byte:
                            break
                        conn.send(byte)
                f.close()
                end = time.time()
                with open("log.txt", "a") as f:
                    f.write("Cliente: "+addr[0]+"\n")
                    f.write(str(end - start)+" segundos en la transferencia del archivo #1.\n")
            else:
                start = time.time()
                hashMD = md5("archivo2.mp4")
                conn.send(hashMD.encode())
                with open("archivo2.mp4", "rb") as f:
                    while True:
                        byte = f.read(1024)
                        if not byte:
                            break
                        conn.send(byte)
                f.close()
                end = time.time()
                with open("log.txt", "a") as f:
                    f.write("Cliente: "+addr[0]+"\n")
                    f.write(str(end - start)+" segundos en la transferencia del archivo #2.\n")
            conn.close()
            conn, addr = s.accept()
            data = conn.recv(1024)
            print(data)
        except Exception as e:
            print(e)
            conn.send(b"Eleccion invalida")
    else:
        print("No se encuentra listo")
conn.close()
