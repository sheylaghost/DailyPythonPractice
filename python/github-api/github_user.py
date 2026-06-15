import requests

usuario = input("Digite um usuário do GitHub: ")

dados = requests.get(
    f"https://api.github.com/users/{usuario}"
).json()

print("Nome:", dados.get("name"))
print("Seguidores:", dados.get("followers"))
print("Repositórios:", dados.get("public_repos"))
print("Perfil:", dados.get("html_url"))
