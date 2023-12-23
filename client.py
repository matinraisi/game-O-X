import socket
HOST = '127.0.0.1'
PORT = 12345


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


name = input('Please enter your name: ')

client_socket.sendall(name.encode())


opponent_name = client_socket.recv(1024).decode()
print(f'Your opponent: {opponent_name}')

while True:

    turn = client_socket.recv(1024).decode()
    print(turn)

    if turn.startswith('Your opponent'):
        break


    game_board = client_socket.recv(1024).decode()
    print(game_board)


    valid_choice = False
    while not valid_choice:
        choice = input('Please select a cell (1 to 9): ')
        if choice.isdigit() and 1 <= int(choice) <= 9:
            valid_choice = True
        else:
            print('Invalid choice! Please enter an integer between 1 and 9.')

    client_socket.sendall(str(int(choice)).encode())


    result = client_socket.recv(1024).decode()
    print(result)


client_socket.close()