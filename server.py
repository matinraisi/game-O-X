import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print('سرور آماده است. در انتظار اتصال دو کلاینت...')

clients = []
client_names = []

# ماتریس بازی
game_board = [[' ' for _ in range(3)] for _ in range(3)]

# تابع کمکی برای چک کردن برنده
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
        return 'تساوی'

    return None

# تابع کمکی برای تغییر نوبت
def switch_turn():
    global turn_player
    turn_player = 1 - turn_player

def handle_client(client, name):
    global turn_player

    # اطلاعات اولیه ارسال می‌شود
    client.sendall(f'نام حریف شما: {client_names[1 - clients.index(client)]}'.encode())

    while True:
        try:
            # دریافت انتخاب بازی از بازیکن فعلی
            choice = int(client.recv(1024).decode()) - 1
            row, col = divmod(choice, 3)

            # بررسی صحت انتخاب
            if game_board[row][col] == ' ':
                # بروزرسانی ماتریس بازی
                game_board[row][col] = 'X' if clients.index(client) == 0 else 'O'

                # ارسال نتیجه به هر دو کلاینت
            for c in clients:
                c.sendall(f'ماتریس بازی:\n{game_board[0][0]} | {game_board[0][1]} | {game_board[0][2]}\n'
                        f'---------\n'
                        f'{game_board[1][0]} | {game_board[1][1]} | {game_board[1][2]}\n'
                        f'---------\n'
                        f'{game_board[2][0]} | {game_board[2][1]} | {game_board[2][2]}\n'
                        f'نتیجه: {check_winner()}'.encode())

                # بررسی پایان بازی
                # بررسی پایان بازی
                winner = check_winner()
                if winner or winner == 'تساوی':
                    for c in clients:
                        c.sendall(f'نتیجه: {winner}'.encode())
                    break

                # تغییر نوبت بازیکن
                switch_turn()

                # ارسال نوبت جدید به هر دو کلاینت
                for c in clients:
                    c.sendall(f'نوبت بازی: {client_names[turn_player]}'.encode())

        except (ValueError, IndexError):
            print('خطا در دریافت داده از کلاینت.')
            break

    # بستن اتصال با کلاینت
    client.close()

while len(clients) < 2:
    client_socket, _ = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    clients.append(client_socket)
    client_names.append(client_name)
    print(f'کلاینت {client_name} به سرور متصل شد.')

# ارسال نام کلاینت به هر دو کلاینت
for c in clients:
    c.sendall(f'نام حریف شما: {client_names[1 - clients.index(c)]}'.encode())

# نوبت بازیکن اول
turn_player = 0

# ارسال نوبت بازی به هر دو کلاینت
for c in clients:
    c.sendall(f'نوبت بازی: {client_names[turn_player]}'.encode())

# هنگامی که هر دو کلاینت وصل شده‌اند، مسئول ایجاد ترد جدید برای هر کلاینت می‌شود
threading.Thread(target=handle_client, args=(clients[0], client_names[0])).start()
threading.Thread(target=handle_client, args=(clients[1], client_names[1])).start()


