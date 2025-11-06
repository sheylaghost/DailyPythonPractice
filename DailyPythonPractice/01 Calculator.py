# Calculadora simples em Python

# Pede dois números ao usuário
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

# Mostra o menu de operações
print("\nEscolha a operação:")
print("1 - Soma")
print("2 - Subtração")
print("3 - Multiplicação")
print("4 - Divisão")

# Lê a opção
opcao = input("Opção: ")

# Faz o cálculo conforme a opção
if opcao == "1":
    print("Resultado:", num1 + num2)
elif opcao == "2":
    print("Resultado:", num1 - num2)
elif opcao == "3":
    print("Resultado:", num1 * num2)
elif opcao == "4":
    if num2 != 0:
        print("Resultado:", num1 / num2)
    else:
        print("Erro: não é possível dividir por zero!")
else:
    print("Opção inválida!")
