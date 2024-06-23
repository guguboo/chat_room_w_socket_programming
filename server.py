import threading
import socket
import mysql.connector
from collections import defaultdict
from object_client import ClientObj

host = 'localhost'
port = 50112

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

room_members = {}

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='jarkom',
            user='root',
            password=''
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

conn = connect_to_database()
cursor = conn.cursor()
cursor.execute("SELECT Room_Name FROM chat_room")
room_names = cursor.fetchall()
for name in room_names:
    room_members[name[0]] = []
conn.close()

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

        # print(room)
        new_client = ClientObj(nickname, client, room)
        if room not in room_members:
            print("baru bikin room")
            room_members[room] = [new_client]
        else:
            print("sudah ada room, nambah user")
            print(room_members[room])
            room_members[room].append(new_client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), room)

        thread = threading.Thread(target=handle, args=(new_client,))
        thread.start()


print("Server is running")
print(room_members)
receive()