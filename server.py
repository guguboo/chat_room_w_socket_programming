import threading
import socket
from collections import defaultdict
from object_client import ClientObj

host = 'localhost'
port = 50112

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

room_members = {}


def broadcast(msg, room):
    print(room_members)
    for member in room_members[room]:
        member.client.send(msg)


def handle(new_client):
    client = new_client.client
    while True:
        try:
            message = client.recv(1024)
            print(message)
            broadcast(message, new_client.room)
        except:
            curr_room = room_members[new_client.room]
            for member in curr_room:
                if(new_client.username == member.username):
                    client.close()
                    curr_room.remove(member)
                    broadcast(f"{new_client.username} meninggalkan chat".encode('ascii'), new_client.room)

def receive():
    while True:
        client, address = server.accept()
        print(f"{client} bergabung dengan {address}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client.send('ROOM'.encode('ascii'))
        room = client.recv(1024).decode('ascii')

        if "creatingchatroom_" in room:
            room = room.split("_")[1]
            print(room)
            if room in room_members:
                client.send('CREATING_ROOM_ERR'.encode('ascii'))
            else:
                new_client = ClientObj(nickname, client, room)
                room_members[room] = [new_client]
                print("testing")
                client.send('SUCCESS'.encode('ascii'))
        else:
            print("room yang dijoin", room)
            if room in room_members:
                in_room = False
                for member in room_members[room]:
                    if member.username == nickname:
                        in_room = True
                        break
                print(in_room)
                if in_room:
                    for member in room_members[room]:
                        if member.username == nickname:
                            room_members[room].remove(member)
                new_client = ClientObj(nickname, client, room)
                room_members[room].append(new_client)
                broadcast("{} joined!".format(nickname).encode('ascii'), room)
        print("Nickname is {}".format(nickname))

        thread = threading.Thread(target=handle, args=(new_client,))
        thread.start()


print("Server is running")
receive()