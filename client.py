import socket
import threading

class TicTacToeClient:
    def __init__(self):
        self.host = '127.0.0.1'  # آدرس IP سرور
        self.port = 9999  # پورت سرور
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        player_name = input('Enter your name: ')
        self.client_socket.send(player_name.encode())

        print(self.client_socket.recv(1024).decode())

        self.receive_messages()

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            print(message)

            if 'wins!' in message or 'equalised' in message:
                self.client_socket.close()
                break

            move = input('Your move (1-9): ')
            self.client_socket.send(move.encode())

if __name__ == '__main__':
    client = TicTacToeClient()
    client.start()