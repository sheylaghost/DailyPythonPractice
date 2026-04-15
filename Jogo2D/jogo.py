import pygame
import random
import sys

# Inicialização
pygame.init()

# Configurações
LARGURA = 600
ALTURA = 400
TAMANHO = 10
FPS = 15

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Jogo da Cobrinha")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 20)


def gerar_comida():
    x = random.randrange(0, LARGURA, TAMANHO)
    y = random.randrange(0, ALTURA, TAMANHO)
    return (x, y)


def desenhar_texto(texto, cor, x, y):
    render = fonte.render(texto, True, cor)
    tela.blit(render, (x, y))


def jogo():
    cobra = [(100, 50)]
    direcao = (TAMANHO, 0)
    comida = gerar_comida()
    pontuacao = 0
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao != (0, TAMANHO):
                    direcao = (0, -TAMANHO)
                elif evento.key == pygame.K_DOWN and direcao != (0, -TAMANHO):
                    direcao = (0, TAMANHO)
                elif evento.key == pygame.K_LEFT and direcao != (TAMANHO, 0):
                    direcao = (-TAMANHO, 0)
                elif evento.key == pygame.K_RIGHT and direcao != (-TAMANHO, 0):
                    direcao = (TAMANHO, 0)

        # Movimento
        cabeca = cobra[0]
        nova_cabeca = (cabeca[0] + direcao[0], cabeca[1] + direcao[1])
        cobra.insert(0, nova_cabeca)

        # Comer comida
        if nova_cabeca == comida:
            comida = gerar_comida()
            pontuacao += 1
        else:
            cobra.pop()

        # Colisões
        if (
            nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA or
            nova_cabeca in cobra[1:]
        ):
            return pontuacao

        # Desenho
        tela.fill(PRETO)

        for parte in cobra:
            pygame.draw.rect(tela, VERDE, (parte[0], parte[1], TAMANHO, TAMANHO))

        pygame.draw.rect(tela, VERMELHO, (comida[0], comida[1], TAMANHO, TAMANHO))

        desenhar_texto(f"Pontuação: {pontuacao}", BRANCO, 10, 10)

        pygame.display.update()
        clock.tick(FPS)


def tela_game_over(pontuacao):
    while True:
        tela.fill(PRETO)

        desenhar_texto("GAME OVER", VERMELHO, 230, 150)
        desenhar_texto(f"Pontuação final: {pontuacao}", BRANCO, 200, 180)
        desenhar_texto("Pressione R para reiniciar", BRANCO, 180, 220)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return


# Loop principal
while True:
    pontuacao_final = jogo()
    tela_game_over(pontuacao_final)