import socket

HOST = '127.0.0.1'  # آدرس IP سرور
PORT = 12345  # پورت سرور

# ایجاد سوکت سرور
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print('سرور آماده است. در انتظار اتصال دو کلاینت...')

# دریافت نام کلاینت‌ها
client_sockets = []
client_names = []
for i in range(2):
    client_socket, client_address = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    client_sockets.append(client_socket)
    client_names.append(client_name)
    print(f'کلاینت {client_name} به سرور متصل شد.')

# ارسال نام کلاینت به هر دو کلاینت
for client_socket in client_sockets:
    client_socket.sendall(f'نام حریف شما: {client_names[1 - client_sockets.index(client_socket)]}'.encode())

# ماتریس بازی
game_board = [[' ' for _ in range(3)] for _ in range(3)]

# تابع بررسی بردن یا تساوی
def check_winner():
    # بررسی ردیف‌ها
    for row in game_board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # بررسی ستون‌ها
    for col in range(3):
        if game_board[0][col] == game_board[1][col] == game_board[2][col] != ' ':
            return game_board[0][col]

    # بررسی قطر اصلی
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != ' ':
        return game_board[0][0]

    # بررسی قطر فرعی
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != ' ':
        return game_board[0][2]

    # بررسی تساوی
    if all(game_board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'تساوی'

    # هیچ کس برنده نیست
    return None

# نوبت بازیکن اول
current_player = 0

# ارسال نوبت بازی به هر دو کلاینت
for client_socket in client_sockets:
    client_socket.sendall(f'نوبت بازی: {client_names[current_player]}'.encode())

while True:
    # دریافت انتخاب بازی از بازیکن فعلی
    client_socket = client_sockets[current_player]
    client_socket.sendall('انتخاب یک خانه (از 1 تا 9): '.encode())
    choice = int(client_socket.recv(1024).decode())

    row, col = divmod(choice, 3)

    # بررسی صحت انتخاب
    if game_board[row][col] == ' ':
        # بروزرسانی ماتریس بازی
        game_board[row][col] = 'X' if current_player == 0 else 'O'

        # ارسال نتیجه به سرور
        winner = check_winner()
        if winner:
            result = f'بازیکن {client_names[current_player]} برنده شد!'
            client_sockets[1 - current_player].sendall(f'بازیکن {client_names[current_player]} برنده شد!'.encode())
            client_socket.sendall(f'شما برنده شدید!'.encode())
        elif winner == 'توی':
            result = 'بازی تساوی شد!'
            for client_socket in client_sockets:
                client_socket.sendall('بازی تساوی شد!'.encode())
        else:
            result = 'نوبت حریف'
            for client_socket in client_sockets:
                client_socket.sendall('نوبت حریف'.encode())

        # ارسال نتیجه به هر دو کلاینت
        for client_socket in client_sockets:
            client_socket.sendall(f'ماتریس بازی:\n{game_board[0][0]} | {game_board[0][1]} | {game_board[0][2]}\n'
                                  f'---------\n'
                                  f'{game_board[1][0]} | {game_board[1][1]} | {game_board[1][2]}\n'
                                  f'---------\n'
                                  f'{game_board[2][0]} | {game_board[2][1]} | {game_board[2][2]}\n\n{result}'.encode())

        # بررسی پایان بازی
        if winner or winner == 'تساوی':
            break

        # تغییر نوبت بازیکن
        current_player = 1 - current_player

# بستن اتصال با کلاینت‌ها
for client_socket in client_sockets:
    client_socket.close()

# بستن سوکت سرور
server_socket.close()





# # import socket
# import threading

# # تعیین IP و پورت برای سرور
# SERVER_IP = '127.0.0.1'
# SERVER_PORT = 12345

# # ایجاد سوکت برای سرور
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((SERVER_IP, SERVER_PORT))
# server_socket.listen()

# print(f"[*] Server is listening on {SERVER_IP}:{SERVER_PORT}")

# # لیستی برای نگه‌داری اطلاعات هر کلاینت
# clients = []
# player_names = {}
# current_turn = 0
# board = ['-'] * 9

# # تابع برای مدیریت هر کلاینت
# def handle_client(client_socket):
#     global current_turn
#     try:
#         # دریافت نام اولیه از کلاینت
#         player_name = client_socket.recv(1024).decode()
#         print(f"[*] {player_name} connected.")

#         # اضافه کردن کلاینت به لیست
#         clients.append(client_socket)
#         player_names[client_socket] = player_name

#         # ارسال نام به کلاینت
#         client_socket.send("Connected to the server. Waiting for other players...".encode())

#         # چک کردن آیا تعداد کلاینت‌ها کافی است یا نه
#         if len(clients) == 2:
#             # ارسال پیام به هر دو کلاینت برای شروع بازی
#             broadcast("Both players are connected. Let's start the game!")

#             # شروع بازی
#             play_game()
#     except Exception as e:
#         print(f"[*] Client disconnected: {e}")
#         clients.remove(client_socket)
#         del player_names[client_socket]
#         broadcast_board()

# # تابع برای ارسال پیام به همه کلاینت‌ها
# def broadcast(message):
#     for client in clients:
#         client.send(message.encode())

# # تابع برای ارسال نقشه به همه کلاینت‌ها
# def broadcast_board():
#     global board
#     for client in clients:
#         client.send(str(board).encode())

# # تابع برای شروع بازی
# def play_game():
#     global current_turn, board
#     while True:
#         current_player = clients[current_turn % 2]

#         current_player.send("Your turn. Enter a move (1-9): ".encode())
#         move = int(current_player.recv(1024).decode()) - 1

#         if 0 <= move < 9 and board[move] == '-':
#             board[move] = 'X' if current_turn % 2 == 0 else 'O'
#             current_turn += 1
#             broadcast_board()

#             if check_winner():
#                 broadcast(f"{player_names[current_player]} won!")
#                 reset_game()
#             elif '-' not in board:
#                 broadcast("It's a tie!")
#                 reset_game()
#         else:
#             current_player.send("Invalid move. Try again.".encode())

# # تابع برای بررسی برنده
# def check_winner():
#     winner_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
#                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
#                            (0, 4, 8), (2, 4, 6)]

#     for combination in winner_combinations:
#         if board[combination[0]] == board[combination[1]] == board[combination[2]] != '-':
#             return True

#     return False

# # تابع برای بازنشانی بازی
# def reset_game():
#     global board, current_turn
#     board = ['-'] * 9
#     current_turn = 0
#     broadcast_board()
#     play_game()

# # تابع اصلی برای گوش دادن به اتصالات ورودی
# def main():
#     while True:
#         client_socket, addr = server_socket.accept()
#         client_thread = threading.Thread(target=handle_client, args=(client_socket,))
#         client_thread.start()

# if __name__ == "__main__":
#     main()




## import socket
# import threading

# HOST = '127.0.0.1'
# PORT = 12345

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(2)

# print('سرور آماده است. در انتظار اتصال دو کلاینت...')

# clients = []
# client_names = []

# def handle_client(client, name):
    
#     global clients
#     global client_names

#     # اطلاعات اولیه ارسال می‌شود
#     client.sendall(f'نام حریف شما: {client_names[1 - clients.index(client)]}'.encode())

#     while True:
#         try:
#             # اطمینان از تناوب نوبت
#             if client_names[clients.index(client)] == turn_player:
#                 # دریافت انتخاب بازی از بازیکن فعلی
#                 choice = int(client.recv(1024).decode()) - 1
#                 row, col = divmod(choice, 3)

#                 # بررسی صحت انتخاب
#                 if game_board[row][col] == ' ':
#                     # بروزرسانی ماتریس بازی
#                     game_board[row][col] = 'X' if clients.index(client) == 0 else 'O'

#                     # ارسال نتیجه به هر دو کلاینت
#                     for c in clients:
#                         c.sendall(f'ماتریس بازی:\n{game_board[0][0]} | {game_board[0][1]} | {game_board[0][2]}\n'
#                                   f'---------\n'
#                                   f'{game_board[1][0]} | {game_board[1][1]} | {game_board[1][2]}\n'
#                                   f'---------\n'
#                                   f'{game_board[2][0]} | {game_board[2][1]} | {game_board[2][2]}\n\n'
#                                   f'نتیجه: {check_winner()}'.encode())

#                     # بررسی پایان بازی
#                     if check_winner() or check_winner() == 'تساوی':
#                         break

#                     # تغییر نوبت بازیکن
#                     other_client = clients[1 - clients.index(client)]
#                     client = other_client
#                     global turn_player
#                     turn_player = client_names[clients.index(client)]

#             else:
#                 client.sendall(f'نوبت بازی: {turn_player}'.encode())

#         except (ValueError, IndexError):
#             print('خطا در دریافت داده از کلاینت.')
#             break

#     # بستن اتصال با کلاینت
#     client.close()

# def check_winner():
#     # تابع بررسی بردن یا تساوی
#     for row in game_board:
#         if row[0] == row[1] == row[2] != ' ':
#             return row[0]

#     for col in range(3):
#         if game_board[0][col] == game_board[1][col] == game_board[2][col] != ' ':
#             return game_board[0][col]

#     if game_board[0][0] == game_board[1][1] == game_board[2][2] != ' ':
#         return game_board[0][0]

#     if game_board[0][2] == game_board[1][1] == game_board[2][0] != ' ':
#         return game_board[0][2]

#     if all(game_board[i][j] != ' ' for i in range(3) for j in range(3)):
#         return 'تساوی'

#     return None

# while len(clients) < 2:
#     client_socket, _ = server_socket.accept()
#     client_name = client_socket.recv(1024).decode()
#     clients.append(client_socket)
#     client_names.append(client_name)
#     print(f'کلاینت {client_name} به سرور متصل شد.')

# # ارسال نام کلاینت به هر دو کلاینت
# for c in clients:
#     c.sendall(f'نام حریف شما: {client_names[1 - clients.index(c)]}'.encode())

# # ماتریس بازی
# game_board = [[' ' for _ in range(3)] for _ in range(3)]

# # نوبت بازیکن اول
# current_player = 0
# turn_player = client_names[current_player]

# # ارسال نوبت بازی به هر دو کلاینت
# for c in clients:
#     c.sendall(f'نوبت بازی: {turn_player}'.encode())

# # هنگامی که هر دو کلاینت وصل شده‌اند، مسئول ایجاد ترد جدید برای هر کلاینت می‌شود
# threading.Thread(target=handle_client, args=(clients[0], client_names[0])).start()
# threading.Thread(target=handle_client, args=(clients[1], client_names[1])).start()
 