import socket
import threading

# تعیین IP و پورت سرور
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# ایجاد سوکت برای کلاینت
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# دریافت نام از کاربر
player_name = input("Enter your name: ")
client_socket.send(player_name.encode())

# تابع برای گوش دادن به پیام‌های سرور
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

# شروع یک نخ برای گوش دادن به پیام‌های سرور
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# تابع برای ارسال حرکت به سرور
def send_move():
    while True:
        move = input("Enter your move (1-9): ")
        client_socket.send(move.encode())

# شروع یک نخ برای ارسال حرکت
send_thread = threading.Thread(target=send_move)
send_thread.start()
