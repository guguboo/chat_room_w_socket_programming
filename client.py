import socket
import threading
import object_client
from app import ChatWindow

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 55555))

app = ChatWindow()
app.run()

nama = input("nama anda: ")
nickname = input("username anda: ")


def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))



# receive_thread = threading.Thread(target=receive)
# receive_thread.start()
#
# write_thread = threading.Thread(target=write)
# write_thread.start()