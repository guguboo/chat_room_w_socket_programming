import socket
import threading

serverPort = 50112

class Client:
    def __init__(self, username, parent, room_name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', serverPort))
        self.username = username
        self.parent = parent
        self.room = room_name
        self.queue_lock = threading.Lock()
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        #apa yang mau dikirim
        self.message_queue = []

        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

    def receive(self):
        while True:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.username.encode('ascii'))
                elif message == 'ROOM':
                    self.client.send(self.room.encode('ascii'))
                else:
                    print(message)
                    self.parent.insert_message(message)


    def write(self):
        while True:
            if self.message_queue:
                with self.queue_lock:
                    try:
                        msg = self.message_queue.pop(0)
                        message = '{}: {}'.format(self.username, msg)
                        self.client.send(message.encode('ascii'))
                    except:
                        self.parent.insert_message("Terjadi kesalahan saat mengirim pesan.")

    def send_message(self, message):
        if message:
            with self.queue_lock:
                self.message_queue.append(message)