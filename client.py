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

        player_name = input('enter your name: ')
        self.client_socket.send(player_name.encode())

        print(self.client_socket.recv(1024).decode())

        self.receive_messages()

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            print(message)

            if 'is the winner!' in message or 'The game equalised!' in message:
                self.client_socket.close()
                break

            if 'it s your turn Choosing a house (1-9): ' in message:
                valid_moves = [str(i + 1) for i in range(9) if self.is_valid_move(i + 1)]
                print('Valid moves:', ', '.join(valid_moves))
                move = input()
                self.client_socket.send(move.encode())

    def is_valid_move(self, move):
        # اینجا قوانین اعتبارسنجی حرکت را پیاده‌سازی کنید
        # مثال: بررسی این که حرکت در بازه 1 تا 9 باشد و خانه‌ای که قبلاً انتخاب نشده است
        return True

if __name__ == '__main__':
    client = TicTacToeClient()
    client.start()