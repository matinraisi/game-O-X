import socket
import threading

# تعیین IP و پورت برای سرور
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# ایجاد سوکت برای سرور
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print(f"[*] Server is listening on {SERVER_IP}:{SERVER_PORT}")

# لیستی برای نگه‌داری اطلاعات هر کلاینت
clients = []
player_names = {}
current_turn = 0
board = ['-'] * 9

# تابع برای مدیریت هر کلاینت
def handle_client(client_socket):
    global current_turn
    try:
        # دریافت نام اولیه از کلاینت
        player_name = client_socket.recv(1024).decode()
        print(f"[*] {player_name} connected.")

        # اضافه کردن کلاینت به لیست
        clients.append(client_socket)
        player_names[client_socket] = player_name

        # ارسال نام به کلاینت
        client_socket.send("Connected to the server. Waiting for other players...".encode())

        # چک کردن آیا تعداد کلاینت‌ها کافی است یا نه
        if len(clients) == 2:
            # ارسال پیام به هر دو کلاینت برای شروع بازی
            broadcast("Both players are connected. Let's start the game!")

            # شروع بازی
            play_game()
    except Exception as e:
        print(f"[*] Client disconnected: {e}")
        clients.remove(client_socket)
        del player_names[client_socket]
        broadcast_board()

# تابع برای ارسال پیام به همه کلاینت‌ها
def broadcast(message):
    for client in clients:
        client.send(message.encode())

# تابع برای ارسال نقشه به همه کلاینت‌ها
def broadcast_board():
    global board
    for client in clients:
        client.send(str(board).encode())

# تابع برای شروع بازی
def play_game():
    global current_turn, board
    while True:
        current_player = clients[current_turn % 2]

        current_player.send("Your turn. Enter a move (1-9): ".encode())
        move = int(current_player.recv(1024).decode()) - 1

        if 0 <= move < 9 and board[move] == '-':
            board[move] = 'X' if current_turn % 2 == 0 else 'O'
            current_turn += 1
            broadcast_board()

            if check_winner():
                broadcast(f"{player_names[current_player]} won!")
                reset_game()
            elif '-' not in board:
                broadcast("It's a tie!")
                reset_game()
        else:
            current_player.send("Invalid move. Try again.".encode())

# تابع برای بررسی برنده
def check_winner():
    winner_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                           (0, 3, 6), (1, 4, 7), (2, 5, 8),
                           (0, 4, 8), (2, 4, 6)]

    for combination in winner_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != '-':
            return True

    return False

# تابع برای بازنشانی بازی
def reset_game():
    global board, current_turn
    board = ['-'] * 9
    current_turn = 0
    broadcast_board()
    play_game()

# تابع اصلی برای گوش دادن به اتصالات ورودی
def main():
    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
