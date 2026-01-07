import tkinter as tk
from tkinter import messagebox

# Tabuleiro inicial
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        tk.Button(root, text="Verificar", command=self.check_solution).grid(row=10, column=0, columnspan=9, pady=10)

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(
                    self.root,
                    width=2,
                    font=("Arial", 18),
                    justify="center"
                )
                entry.grid(row=i, column=j, padx=2, pady=2)

                if board[i][j] != 0:
                    entry.insert(0, str(board[i][j]))
                    entry.config(state="disabled", disabledforeground="black")

                self.cells[i][j] = entry

    def check_solution(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()
                if value == "":
                    messagebox.showerror("Erro", "Preencha todas as células.")
                    return
                row.append(int(value))
            grid.append(row)

        if self.is_valid(grid):
            messagebox.showinfo("Sudoku", "Parabéns! Sudoku correto!")
        else:
            messagebox.showerror("Sudoku", "Há erros no Sudoku.")

    def is_valid(self, grid):
        for i in range(9):
            if len(set(grid[i])) != 9:
                return False
            if len(set(row[i] for row in grid)) != 9:
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(grid[box_row + i][box_col + j])
                if len(set(box)) != 9:
                    return False
        return True

root = tk.Tk()
SudokuGUI(root)
root.mainloop()
