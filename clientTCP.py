import socket                   # Import socket module
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

s = socket.socket()             # Create a socket object
host = '104.248.118.20'         # Get local machine name
port = 65432                    # Reserve a port for your service.

s.connect((host, port))

data = s.recv(1024)
print(data.decode())
eleccion = input("Inserte su opción: ")
s.send(eleccion.encode())
sizeF = s.recv(1024)
with open('received_file.mp4', 'wb') as f:
    while True:
        data = s.recv(1024)
        if not data:
            break
            # write data to a file
        f.write(data)
f.close()

hashMD = md5("received_file.mp4")

sizeFF = sizeF.decode()
if(sizeFF==hashMD):
    print("Integridad verificada")
    print("Servidor ", sizeFF)
    print("Client ", hashMD)
    
else:
    print("Servidor ", sizeFF)
    print("Client ", hashMD)

print('connection closed')
s.close()
s = socket.socket()             # Create a socket object
s.connect((host, port))
verif = "Archivo recibido"
s.send(verif.encode())
s.close()
