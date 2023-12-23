import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print('Server is ready. Waiting for two clients to connect...')

clients = []
client_names = []


game_board = [[' ' for _ in range(3)] for _ in range(3)]


def check_winner():
    for row in game_board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    for col in range(3):
        if game_board[0][col] == game_board[1][col] == game_board[2][col] != ' ':
            return game_board[0][col]

    if game_board[0][0] == game_board[1][1] == game_board[2][2] != ' ':
        return game_board[0][0]

    if game_board[0][2] == game_board[1][1] == game_board[2][0] != ' ':
        return game_board[0][2]

    if all(game_board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'Draw'

    return None


def switch_turn():
    global turn_player
    turn_player = 1 - turn_player

def handle_client(client, name):
    global turn_player

    client.sendall(f'Your opponent\'s name is: {client_names[1 - clients.index(client)]}'.encode())

    while True:
        try:

            choice = int(client.recv(1024).decode()) - 1
            row, col = divmod(choice, 3)


            if game_board[row][col] == ' ':

                game_board[row][col] = 'X' if clients.index(client) == 0 else 'O'


                for c in clients:
                    c.sendall(f'Game board:\n{game_board[0][0]} | {game_board[0][1]} | {game_board[0][2]}\n'
                              f'---------\n'
                              f'{game_board[1][0]} | {game_board[1][1]} | {game_board[1][2]}\n'
                              f'---------\n'
                              f'{game_board[2][0]} | {game_board[2][1]} | {game_board[2][2]}\n'
                              f'Result: {check_winner()}'.encode())


                winner = check_winner()
                if winner or winner == 'Draw':
                    for c in clients:
                        c.sendall(f'Result: {winner}'.encode())
                    break


                switch_turn()


                for c in clients:
                    c.sendall(f'Turn: {client_names[turn_player]}'.encode())

        except (ValueError, IndexError):
            print('Error receiving data from the client.')
            break


    client.close()

while len(clients) < 2:
    client_socket, _ = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    clients.append(client_socket)
    client_names.append(client_name)
    print(f'Client {client_name} connected to the server.')


for c in clients:
    c.sendall(f'Your opponent\'s name is: {client_names[1 - clients.index(c)]}'.encode())


turn_player = 0


for c in clients:
    c.sendall(f'Turn: {client_names[turn_player]}'.encode())

threading.Thread(target=handle_client, args=(clients[0], client_names[0])).start()
threading.Thread(target=handle_client, args=(clients[1], client_names[1])).start()