import socket

class TicTacToeServer:
    def __init__(self):
        self.host = '127.0.0.1'  
        self.port = 5555  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clients = []
        self.maps = {}
        self.current_player = 0

    def start(self):
        self.server.listen()
        print("سرور در حال اجراست...")
        while True:
            client_socket, client_address = self.server.accept()
            print(f"اتصال برقرار شد با {client_address}")
            self.clients.append(client_socket)
            client_socket.send("با موفقیت به سرور متصل شدید.".encode())
            client_name = client_socket.recv(1024).decode()
            print(f"بازیکن جدید: {client_name}")
            self.maps[client_name] = "---------"
            if len(self.clients) == 2:
                self.play_game()

    def play_game(self):
        while True:
            for i, client_socket in enumerate(self.clients):
                try:
                    client_socket.send(self.maps[self.get_client_name(i)].encode())
                    position = client_socket.recv(1024).decode()
                    self.update_map(i, position)
                    if self.check_winner():
                        self.send_to_all(f"برنده: {self.get_client_name(i)}")
                        self.reset()
                        return
                    elif self.check_draw():
                        self.send_to_all("تساوی!")
                        self.reset()
                        return
                except ConnectionResetError:
                    print(f"اتصال با {self.get_client_name(i)} قطع شد.")
                    self.reset()
                    return

    def update_map(self, player_index, position):
        map_str = self.maps[self.get_client_name(player_index)]
        updated_map = map_str[:int(position)] + self.get_player_symbol(player_index) + map_str[int(position)+1:]
        self.maps[self.get_client_name(player_index)] = updated_map
        self.send_to_all(updated_map)

    def check_winner(self):
        map_str = self.maps[self.get_client_name(self.current_player)]
        winning_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in winning_conditions:
            if map_str[condition[0]] == map_str[condition[1]] == map_str[condition[2]] != '-':
                return True
        return False

    def check_draw(self):
        map_str = self.maps[self.get_client_name(self.current_player)]
        if '-' not in map_str:
            return True
        return False

    def send_to_all(self, message):
        for client_socket in self.clients:
            client_socket.send(message.encode())

    def reset(self):
        self.maps = {}
        self.current_player = 0
        self.clients.clear()

    def get_client_name(self, index):
        return list(self.maps.keys())[index]

    def get_player_symbol(self, index):
        symbols = ['X', 'O']
        return symbols[index]

if __name__ == '__main__':
    server = TicTacToeServer()
    server.start()