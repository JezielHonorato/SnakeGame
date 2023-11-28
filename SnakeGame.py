import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("SnakeGame")

largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
fundo = pygame.image.load('./image/background.jpg')

ticks = pygame.time.Clock()

#* Músicas

som_comer = pygame.mixer.Sound('./music/comer.wav') # som precisa sem .wav
som_perder = pygame.mixer.Sound('./music/perder.wav')
pygame.mixer.music.set_volume(0.02)
musica_de_fundo = pygame.mixer.music.load('./music/musica_de_fundo.mp3') #apenas musica de fundo é .mp3
pygame.mixer.music.play(-1)

#* Cores

cor_fundo = (255,255, 255)
cor_cobra = (0, 255, 0)
cor_comida = (255, 0, 0)
cor_texto = (0, 0, 0)


#* parametros iniciais

pixel = 20 # Tamanho de cada pixel no jogo, a cobra e a comida.
velocidade_jogo = 10


#* Funções

def desenhar_texto(mensagem, x, y):
    fonte = pygame.font.SysFont("Arial", 20)
    texto = fonte.render(f"Pontos: {mensagem}", True, cor_texto)
    text_quadro = texto.get_rect(center = (largura/x, altura/y))
    tela.blit(texto, text_quadro)


def main_menu(): # Função do menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    snake_game() # ao clicar inicia o jogo

        # Limpar a tela
        tela.fill(cor_fundo)
        tela.blit(fundo, (0, 0))

        desenhar_texto("Menu Principal", 2, 4)
        desenhar_texto("Pressione Enter para iniciar o jogo da cobrinha", 2, 2)

        # Atualizar a tela
        pygame.display.flip()

# Função do jogo da cobrinha
def snake_game():

    def gerar_comida():
        posicao_comida_x = round(random.randrange(0, largura - pixel) / float(pixel)) * float(pixel) # Caber direito na tabela
        posicao_comida_y = round(random.randrange(0, altura - pixel) / float(pixel)) * float(pixel)
        return posicao_comida_x, posicao_comida_y

    def desenhar_comida(pixel, posicao_comida_x, posicao_comida_y):
        pygame.draw.rect(tela, cor_comida, [posicao_comida_x, posicao_comida_y, pixel, pixel])

    def desenhar_cobra(pixel, tamanho_cobra):
        for item in tamanho_cobra: 
            pygame.draw.rect(tela, cor_cobra, [item[0], item[1], pixel, pixel])

    def mover_personagem(tecla):
        if tecla == pygame.K_DOWN or tecla == pygame.K_s:
            posicao_x = 0
            posicao_y = pixel

        elif tecla == pygame.K_UP or tecla == pygame.K_w:
            posicao_x = 0
            posicao_y = -pixel

        elif tecla == pygame.K_RIGHT or tecla == pygame.K_d:
            posicao_x = pixel
            posicao_y = 0

        elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
            posicao_x = -pixel
            posicao_y = 0

        return posicao_x, posicao_y

    x = largura / 2
    y = altura / 2
    posicao_x = 0 # posição da cabeça cobra
    posicao_y = 0
    pontuacao = 1
    tamanho_cobra = []
    posicao_comida_x, posicao_comida_y = gerar_comida()
    jogando = True

    while jogando:
        tela.fill(cor_fundo)
        tela.blit(fundo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False

            elif evento.type == pygame.KEYDOWN:
                posicao_x, posicao_y = mover_personagem(evento.key)

        desenhar_comida(pixel, posicao_comida_x, posicao_comida_y)

        if x < 0 or x >= largura or y < 0 or y >= altura:
            som_perder.play()
            jogando = False

        x += posicao_x
        y += posicao_y

        tamanho_cobra.append([x, y])
        if len(tamanho_cobra) > pontuacao:
            del tamanho_cobra[0]

        for item in tamanho_cobra[:-1]:
            if item == [x, y]:
                som_perder.play()
                jogando = False


        desenhar_cobra(pixel, tamanho_cobra)
        
        desenhar_texto(pontuacao - 1, 2, 10)

        pygame.display.update()

        if x == posicao_comida_x and y == posicao_comida_y:
            pontuacao += 1
            posicao_comida_x, posicao_comida_y = gerar_comida()
            som_comer.play()

        ticks.tick(velocidade_jogo)

# Iniciar o menu
main_menu()
