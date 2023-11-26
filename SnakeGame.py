import pygame
import random

pygame.init()
pygame.display.set_caption("SnakeGame")

largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
ticks = pygame.time.Clock()

#* cores RGB e Músicas

som_comer = pygame.mixer.Sound('./music/comer.wav') # som precisa sem .wav
som_perder = pygame.mixer.Sound('./music/perder.wav')
pygame.mixer.music.set_volume(0.02)
musica_de_fundo = pygame.mixer.music.load('./music/musica_de_fundo.mp3') #apenas musica de fundo é .mp3

cor_fundo = (255,255, 255)
cor_cobra = (0, 255, 0)
cor_comida = (255, 0, 0)
cor_texto = (0, 0, 0)

pygame.mixer.music.play(-1)


#* parametros da cobrinha

pixel = 20 # Tamanho de cada pixel no jogo, a cobra e a comida.
velocidade_jogo = 10

def gerar_comida():
    posicao_comida_x = round(random.randrange(0, largura - pixel) / float(pixel)) * float(pixel) # Caber direito na tabela
    posicao_comida_y = round(random.randrange(0, altura - pixel) / float(pixel)) * float(pixel)
    return posicao_comida_x, posicao_comida_y

def desenhar_comida(pixel, posicao_comida_x, posicao_comida_y):
    pygame.draw.rect(tela, cor_comida, [posicao_comida_x, posicao_comida_y, pixel, pixel])

def desenhar_cobra(pixel, tamanho_cobra):
    for item in tamanho_cobra: 
        pygame.draw.rect(tela, cor_cobra, [item[0], item[1], pixel, pixel])

def desenhar_pontuacao(pontos):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontos}", True, cor_texto)
    tela.blit(texto, [1, 1])

def mover_personagem(tecla):
    if tecla == pygame.K_DOWN:
        posicao_x = 0
        posicao_y = pixel

    elif tecla == pygame.K_UP:
        posicao_x = 0
        posicao_y = -pixel

    elif tecla == pygame.K_RIGHT:
        posicao_x = pixel
        posicao_y = 0

    elif tecla == pygame.K_LEFT:
        posicao_x = -pixel
        posicao_y = 0

    return posicao_x, posicao_y

x = largura / 2
y = altura / 2
posicao_x = 0
posicao_y = 0
pontuacao = 1
tamanho_cobra = []
posicao_comida_x, posicao_comida_y = gerar_comida()

while True:
    tela.fill(cor_fundo)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            exit()

        elif evento.type == pygame.KEYDOWN:
            posicao_x, posicao_y = mover_personagem(evento.key)

    desenhar_comida(pixel, posicao_comida_x, posicao_comida_y)

    if x < 0 or x >= largura or y < 0 or y >= altura:
        som_perder.play()
        exit()

    x += posicao_x
    y += posicao_y

    tamanho_cobra.append([x, y])
    if len(tamanho_cobra) > pontuacao:
        del tamanho_cobra[0]

    for item in tamanho_cobra[:-1]:
        if item == [x, y]:
            som_perder.play()
            exit()

    desenhar_cobra(pixel, tamanho_cobra)
    
    desenhar_pontuacao(pontuacao - 1)

    pygame.display.update()

    if x == posicao_comida_x and y == posicao_comida_y:
        pontuacao += 1
        posicao_comida_x, posicao_comida_y = gerar_comida()
        som_comer.play()

    ticks.tick(velocidade_jogo)