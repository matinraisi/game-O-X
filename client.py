import socket

HOST = '127.0.0.1'
PORT = 12345

# اتصال به سرور
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# دریافت نام کاربر از ورودی
name = input('لطفاً نام خود را وارد کنید: ')

# ارسال نام کاربر به سرور
client_socket.sendall(name.encode())

# دریافت نام حریف
opponent_name = client_socket.recv(1024).decode()
print(f'حریف شما: {opponent_name}')

while True:
    # دریافت نوبت بازی
    turn = client_socket.recv(1024).decode()
    print(turn)

    if turn.startswith('نام حریف شما:'):
        break

    # دریافت ماتریس بازی
    game_board = client_socket.recv(1024).decode()
    print(game_board)

    # دریافت انتخاب کاربر و بررسی صحت آن
    valid_choice = False
    while not valid_choice:
        choice = input('لطفاً یک خانه (از 1 تا 9) را انتخاب کنید: ')
        if choice.isdigit() and 1 <= int(choice) <= 9:
            valid_choice = True
        else:
            print('انتخاب نامعتبر! لطفاً عدد صحیحی از 1 تا 9 وارد کنید.')

    client_socket.sendall(str(int(choice)).encode())

    # دریافت نتیجه بازی
    result = client_socket.recv(1024).decode()
    print(result)

# بستن اتصال با سرور
client_socket.close()


# import socket

# HOST = '127.0.0.1'
# PORT = 12345

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
#         choice = input('لطفاً یک خانه (از 1 تا 9) را انتخاب کنید: ')
#         if choice.isdigit() and 1 <= int(choice) <= 9:
#             valid_choice = True
#         else:
#             print('انتخاب نامعتبر! لطفاً عدد صحیحی از 1 تا 9 وارد کنید.')

#     client_socket.sendall(str(int(choice)).encode())

#     # دریافت نتیجه بازی
#     result = client_socket.recv(1024).decode()
#     print(result)

# # بستن اتصال با سرور
# client_socket.close()
