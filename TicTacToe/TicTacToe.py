from tkinter import *
import random


BG_COLOR = "#465FEE"
BTN_COLOR = "#c2c3fd"
WIN_COLOR = "#7e80f3"
TIE_COLOR = "#8aaaee"
TEXT_COLOR = "#050D1D"

def next_turn(row, column):
    global player

    if buttons[row][column]["text"] != "" or check_winner():
        return

    buttons[row][column]["text"] = player

    result = check_winner()

    if result is False:
        player = players[1] if player == players[0] else players[0]
        label.config(text=f"{player} turn")

    elif result is True:
        label.config(text=f"{player} wins")

    elif result == "Tie":
        label.config(text="Tie!")

def check_winner():

    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            for j in range(3):
                buttons[i][j].config(bg=WIN_COLOR)
            return True

        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            for j in range(3):
                buttons[j][i].config(bg=WIN_COLOR)
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        for i in range(3):
            buttons[i][i].config(bg=WIN_COLOR)
        return True

    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        buttons[0][2].config(bg=WIN_COLOR)
        buttons[1][1].config(bg=WIN_COLOR)
        buttons[2][0].config(bg=WIN_COLOR)
        return True

    if not empty_spaces():
        for row in range(3):
            for col in range(3):
                buttons[row][col].config(bg=TIE_COLOR)
        return "Tie"

    return False

def empty_spaces():
    for row in range(3):
        for col in range(3):
            if buttons[row][col]["text"] == "":
                return True
    return False

def new_game():
    global player
    player = random.choice(players)
    label.config(text=f"{player} turn")

    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", bg=BTN_COLOR)


window = Tk()
window.title("Tic-Tac-Toe")
window.config(bg=BG_COLOR)

players = ["X", "O"]
player = random.choice(players)

label = Label(
    window,
    text=f"{player} turn",
    font=("Consolas", 32),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
label.pack(pady=10)

reset_button = Button(
    window,
    text="Restart",
    font=("Consolas", 18),
    bg="#BDC1CA",
    fg="white",
    command=new_game
)
reset_button.pack(pady=5)

frame = Frame(window, bg=BG_COLOR)
frame.pack()

buttons = [[None]*3 for _ in range(3)]

for row in range(3):
    for col in range(3):
        buttons[row][col] = Button(
            frame,
            text="",
            font=("Consolas", 40),
            width=5,
            height=2,
            bg=BTN_COLOR,
            fg=TEXT_COLOR,
            command=lambda r=row, c=col: next_turn(r, c)
        )
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

window.mainloop()

