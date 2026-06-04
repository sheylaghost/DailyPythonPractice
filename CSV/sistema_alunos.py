import csv

nome = input("Nome do aluno: ")
nota = float(input("Nota: "))

with open("alunos.csv", "a", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow([nome, nota])

print("Aluno cadastrado com sucesso!")