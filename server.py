import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting For A Connection")

current_id = '0'
pos = ['0:50,50', '1:100,100']
def threaded_client(conn):
    global current_id, pos
    conn.send(str.encode(current_id))
    current_id = '1'
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode('Lost Connection: Can Not Data'))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Lost")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, ))