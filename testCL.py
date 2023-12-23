# import socket

# HOST = '127.0.0.1'  # آدرس IP سرور
# PORT = 12345  # پورت سرور

# # اتصال به سرور
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

# # دریافت نام کاربر از ورودی
# name = input('لطفاً نام خود را وارد کنید: ')

# # ارسال نام کاربر به سرور
# client_socket.sendall(name.encode())

# # دریافت نام حریف
# opponent_name = client_socket.recv(1024).decode()
# print(f'حریف شما: {opponent_name}')

# while True:
#     # دریافت نوبت بازی
#     turn = client_socket.recv(1024).decode()
#     print(turn)

#     if turn.startswith('نام حریف شما:'):
#         break

#     # دریافت ماتریس بازی
#     game_board = client_socket.recv(1024).decode()
#     print(game_board)

#     # دریافت انتخاب کاربر و بررسی صحت آن
#     valid_choice = False
#     while not valid_choice:
#         choice = int(input('لطفاً یک خانه (از 1 تا 9) را انتخاب کنید: '))
#         if choice.isdigit() and 1 <= int(choice) <= 9:
#             valid_choice = True
#         else:
#             print('انتخاب نامعتبر! لطفاً عدد صحیحی از 1 تا 9 وارد کنید.')

#     client_socket.sendall(choice.encode())

#     # دریافت نتیجه بازی
#     result = client_socket.recv(1024).decode()
#     print(result)

# # بستن اتصال با سرور
# client_socket.close()




# ============================



# import socket
# import threading

# # تعیین IP و پورت سرور
# SERVER_IP = '127.0.0.1'
# SERVER_PORT = 12345

# # ایجاد سوکت برای کلاینت
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((SERVER_IP, SERVER_PORT))

# # دریافت نام از کاربر
# player_name = input("Enter your name: ")
# client_socket.send(player_name.encode())

# # تابع برای گوش دادن به پیام‌های سرور
# def receive_messages():
#     while True:
#         message = client_socket.recv(1024).decode()
#         print(message)

# # شروع یک نخ برای گوش دادن به پیام‌های سرور
# receive_thread = threading.Thread(target=receive_messages)
# receive_thread.start()

# # تابع برای ارسال حرکت به سرور
# def send_move():
#     while True:
#         move = input("Enter your move (1-9): ")
#         client_socket.send(move.encode())

# # شروع یک نخ برای ارسال حرکت
# send_thread = threading.Thread(target=send_move)
# send_thread.start()
