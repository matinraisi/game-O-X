import socket
import threading

class TicTacToeServer:
    def __init__(self):
        self.host = '127.0.0.1'  # آدرس IP سرور
        self.port = 9999  # پورت سرور
        self.server_socket = None
        self.client_sockets = []
        self.player_names = []
        self.current_player = 0
        self.board = [' '] * 9

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print('The server started. Waiting for two players to connect...')

        while len(self.client_sockets) < 2:
            client_socket, address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print('Connection established: {}'.format(address))

            player_name = client_socket.recv(1024).decode()
            self.player_names.append(player_name)
            client_socket.send('You have entered the game.'.encode())

        self.broadcast('The game is ready. Start!')
        self.play_game()

    def broadcast(self, message):
        for client_socket in self.client_sockets:
            client_socket.send(message.encode())

    def play_game(self):
        while True:
            current_client_socket = self.client_sockets[self.current_player]
            current_client_socket.send('It\'s your turn. Choose a house (1-9): '.encode())
            move = int(current_client_socket.recv(1024).decode()) - 1

            if self.is_valid_move(move):
                self.board[move] = 'X' if self.current_player == 0 else 'O'
                self.broadcast_board()

                if self.is_winner():
                    self.broadcast('Player {} wins!'.format(self.player_names[self.current_player]))
                    self.broadcast_board()
                    break

                if self.is_board_full():
                    self.broadcast('The game equalised!')
                    self.broadcast_board()
                    break

                self.current_player = 1 - self.current_player
            else:
                current_client_socket.send('The move is invalid. Try again.'.encode())

    def is_valid_move(self, move):
        return move >= 0 and move < 9 and self.board[move] == ' '

    def is_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # خطوط افقی
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # خطوط عمودی
            [0, 4, 8], [2, 4, 6]  # قطرها
        ]

        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != ' ':
                return True

        return False

    def is_board_full(self):
        return ' ' not in self.board

    def broadcast_board(self):
        board_str = '---------\n'
        for i in range(3):
            row = '|'.join(self.board[i * 3:(i + 1) * 3])
            board_str += '|{}|\n'.format(row)
            board_str += '---------\n'

        self.broadcast(board_str)

    def close(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()

if __name__ == '__main__':
    server = TicTacToeServer()
    server.start()