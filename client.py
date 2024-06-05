import socket
import threading

serverPort = 50112


class Client:
    def __init__(self, username, parent):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', serverPort))
        self.username = username
        self.queue_lock = threading.Lock()
        self.parent = parent
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        #apa yang mau dikirim
        self.message_queue = []

        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

    def receive(self):
        while True:
            # try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.username.encode('ascii'))
                else:
                    print(message)
                    self.parent.insert_message(message)
            # except:
            #     # Close Connection When Error
            #     print("An error occured!")
            #     self.client.close()
            #     break

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