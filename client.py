import socket

class TicTacToeClient:
    def __init__(self):
        self.host = '127.0.0.1'  
        self.port = 5555 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""

    def connect(self):
        self.client.connect((self.host, self.port))
        self.name = input("لطفاً نام خود را وارد کنید: ")
        self.client.send(self.name.encode())
        message = self.client.recv(1024).decode()
        print(message)

    def play(self):
        while True:
            try:
                map_data = self.client.recv(1024).decode()
                if map_data.startswith("برنده") or map_data == "تساوی!":
                    print(map_data)
                    break
                else:
                    print(map_data)
                    position = input("لطفاً موقعیت مورد نظر را انتخاب کنید (0-8): ")
                    self.client.send(position.encode())
            except ConnectionResetError:
                print("اتصال قطع شد.")
                break

if __name__ == '__main__':
    client = TicTacToeClient()
    client.connect()
    client.play()