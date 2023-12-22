# # تابعی برای نمایش صفحه بازی Tic-Tac-Toe
# def display_board(board):
#     print(board[0] + '|' + board[1] + '|' + board[2])
#     print('-+-+-')
#     print(board[3] + '|' + board[4] + '|' + board[5])
#     print('-+-+-')
#     print(board[6] + '|' + board[7] + '|' + board[8])

# # تابعی برای بررسی وضعیت برد
# def check_win(board):
#     # بررسی ردیف‌ها
#     for i in range(0, 7, 3):
#         if board[i] == board[i + 1] == board[i + 2] != ' ':
#             return True

#     # بررسی ستون‌ها
#     for i in range(0, 3):
#         if board[i] == board[i + 3] == board[i + 6] != ' ':
#             return True

#     # بررسی قطرها
#     if board[0] == board[4] == board[8] != ' ' or board[2] == board[4] == board[6] != ' ':
#         return True

#     return False

# # تابع اصلی بازی
# def play_game():
#     board = [' '] * 9  # صفحه خالی بازی

#     player = 'X'  # بازیکن فعلی

#     while True:
#         display_board(board)

#         position = int(input("انتخاب کنید (1-9): "))

#         if board[position - 1] == ' ':
#             board[position - 1] = player

#             if check_win(board):
#                 display_board(board)
#                 print("بازیکن", player, "برنده شد!")
#                 break

#             if ' ' not in board:
#                 display_board(board)
#                 print("بازی بازی نتیجه‌ای نداشت!")
#                 break

#             player = 'O' if player == 'X' else 'X'
#         else:
#             print("موقعیت انتخاب شده قبلاً انتخاب شده است. لطفاً موقعیت دیگری را انتخاب کنید.")

# # اجرای بازی
# play_game()


