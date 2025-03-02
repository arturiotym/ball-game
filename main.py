import pygame, sys,random, json

created = 0
score = 0
highestid=0

class Retangulo:
    """
    Classe que representa um retângulo.
    """
    def __init__(self, id, x, y, largura, mult):
        """
        Inicializa um retângulo.

        Args:
            id (int): Identificador único do retângulo.
            x (int): Posição X do canto superior esquerdo.
            y (int): Posição Y do canto superior esquerdo.
            largura (int): Largura do retângulo.
            altura (int): Altura do retângulo.
        """
        self.id = id
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = 20
        self.cor = BRANCO
        self.mult = mult

    def criar_retangulos():
        """
        Lê um arquivo JSON contendo informações sobre retângulos e retorna uma lista de objetos Retangulo.

        Returns:
            list: Lista de objetos da classe Retangulo.
        """
        caminho_arquivo = "formas.json"
        try:
            # Abre o arquivo JSON e carrega os dados
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

            # Verifica se o arquivo contém a chave 'retangulos'
            if 'retangulos' not in dados:
                raise ValueError("O arquivo JSON deve conter uma chave 'retangulos'.")

            # Cria a lista de retângulos
            for retangulo in dados['retangulos']:
                # Verifica se todas as chaves necessárias estão presentes
                if all(chave in retangulo for chave in ['id', 'x', 'y', 'largura']):
                    # Cria um objeto Retangulo e adiciona à lista
                    novo_retangulo = Retangulo(
                        id=retangulo['id'],
                        x=retangulo['x'],
                        y=retangulo['y'],
                        largura=retangulo['largura'],
                        mult=retangulo['mult']
                    )
                    retangulos.append(novo_retangulo)
            return retangulos

        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"Erro: O arquivo '{caminho_arquivo}' não é um JSON válido.")
            return []
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return []
    
    def colidiu_com(retangulo, circulo):
        """
        Verifica se um círculo colidiu com um retângulo.

        Args:
            circulo (dict ou objeto): Círculo com as chaves/propriedades 'x', 'y', 'circulo.raio'.
            retangulo (dict ou objeto): Retângulo com as chaves/propriedades 'x', 'y', 'retangulo.largura', 'retangulo.altura'.

        Returns:
            bool: True se houve colisão, False caso contrário.
        """
        # Encontra o ponto mais próximo do círculo ao retângulo
        ponto_proximo_x = max(retangulo.x, min(circulo.x, retangulo.x + retangulo.largura))
        ponto_proximo_y = max(retangulo.y, min(circulo.y, retangulo.y + retangulo.altura))

        # Calcula a distância entre o círculo e o ponto mais próximo
        distancia_x = circulo.x - ponto_proximo_x
        distancia_y = circulo.y - ponto_proximo_y
        distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5

        # Verifica se a distância é menor que o circulo.raio do círculo
        return distancia <= circulo.radius
         
    def desenhar(self, TELA):
        """
        Desenha o retângulo na tela.

        Args:
            TELA (pygame.Surface): A superfície da janela do jogo.
        """
        pygame.draw.rect(TELA, (255, 255, 255), (self.x, self.y, self.largura, self.altura))

class Ball:
    gravity_scale = 0.7
    def __init__(self, x, y, radius, color, contacts=[-1], drawn=False, id=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_y = 0
        self.speed_x = random.uniform(-1.5, 1.5)
        self.base_gravity = 0.5
        self.bounce_factor = 0.7
        self.mass = self.radius * self.radius
        self.velocity_damping = 0.997
        self.min_speed = 0.1
        self.contacts = contacts
        self.drawn = drawn
        self.id=id

    def generate(x,y,created):
        lastID=0
        for _ in range(LIMITE_DE_CRIACAO):
            raio = RAIO # Raio 
            cor = (BRANCO)  # Cor 
            ball = Ball(x, y, raio, cor, list(),id=lastID+1)  # Cria um objeto Circulo
            balls.append(ball)  # Adiciona à lista
            created += 1

    def collide_with(self, other):
        if not other or not isinstance(other, Ball):
            return
            
        try:
            dx = self.x - other.x
            dy = self.y - other.y
            distance_sq = dx * dx + dy * dy
            min_distance = self.radius + other.radius
            if distance_sq < min_distance * min_distance:
                distance = max(0.0001, (distance_sq) ** 0.5)  
                if distance < 0.01:
                    self.x += random.uniform(-0.1, 0.1)
                    self.y += random.uniform(-0.1, 0.1)
                    return
                
                nx = dx / distance
                ny = dy / distance
                rel_vx = self.speed_x - other.speed_x
                rel_vy = self.speed_y - other.speed_y
                rel_v_normal = rel_vx * nx + rel_vy * ny
                if rel_v_normal > 0:
                    return
                
                restitution = 0.8
                j = -(1 + restitution) * rel_v_normal
                j /= max(0.0001, 1/self.mass + 1/other.mass)  
                
                if abs(j) < 0.01:
                    return
                
                self.speed_x = max(min(self.speed_x + (j * nx) / self.mass, 1000), -1000)  
                self.speed_y = max(min(self.speed_y + (j * ny) / self.mass, 1000), -1000)
                other.speed_x = max(min(other.speed_x - (j * nx) / other.mass, 1000), -1000)
                other.speed_y = max(min(other.speed_y - (j * ny) / other.mass, 1000), -1000)
                percent = 0.8
                slop = 0.01
                penetration = min_distance - distance
                if penetration > slop:
                    correction = (penetration - slop) / distance * percent
                    correction_x = nx * correction
                    correction_y = ny * correction
                    mass_sum = self.mass + other.mass
                    mass_ratio1 = self.mass / mass_sum if mass_sum > 0 else 0.5
                    mass_ratio2 = other.mass / mass_sum if mass_sum > 0 else 0.5
                    self.x += correction_x * mass_ratio2
                    self.y += correction_y * mass_ratio2
                    other.x -= correction_x * mass_ratio1
                    other.y -= correction_y * mass_ratio1
        except Exception as e:
            print(f"Collision error: {str(e)}")
    
    def multiply(self, x,id, lastID):
        self.y += 10
        for _ in range(x-1):
            lastID += 1
            balls.append(Ball(self.x, self.y+1, self.radius, VERMELHO,[id],True,lastID))
            

    def ground_collision(self):
        """Verifica e responde à colisão com o chão."""
        if self.y + self.radius >= ALTURA:
            """ self.y = ALTURA - self.radius  # Corrige a posição
            self.velocidade_y *= -0.8  # Inverte a velocidade com um pouco de amortecimento
            self.velocidade_x *= 0.9  # Reduz a velocidade horizontal ao quicar """
            return True
        return False

    def update(self, time_scale=1.0):
        if self.drawn:
            try:
                time_scale = max(0.1, min(time_scale, 2.0))  
                self.speed_y += self.base_gravity * Ball.gravity_scale * time_scale
                self.speed_x *= self.velocity_damping
                self.speed_y *= self.velocity_damping
                self.speed_x = max(min(self.speed_x, 1000), -1000)
                self.speed_y = max(min(self.speed_y, 1000), -1000)
                if abs(self.speed_x) < self.min_speed:
                    self.speed_x = 0
                if abs(self.speed_y) < self.min_speed and abs(self.y + self.radius - ALTURA) < 1:
                    self.speed_y = 0
                
                self.x += self.speed_x * time_scale
                self.y += self.speed_y * time_scale
                
                # collision with object physics
                """ if self.y + self.radius > ALTURA: 
                    self.y = ALTURA - self.radius
                    self.speed_y = -self.speed_y * self.bounce_factor 
                    self.speed_x *= 0.95 """
                
                if self.x - self.radius < 0:  
                    self.x = self.radius  
                    self.speed_x = -self.speed_x * self.bounce_factor
                elif self.x + self.radius > LARGURA:  
                    self.x = LARGURA - self.radius  
                    self.speed_x = -self.speed_x * self.bounce_factor
            except Exception as e:
                print(f"Update error: {str(e)}")

    def draw(self, screen):
        if self.drawn:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Circulo:
    

    def __init__(self, x, y, raio, cor, velocidade_x, velocidade_y, contatos=[-1],drawn=False):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.drawn = drawn
        self.contatos = contatos

    def mover(self):
        if self.drawn:
            self.x += self.velocidade_x
            self.y += self.velocidade_y

    def aplicar_gravidade(self):
        """Aplica a gravidade à bolinha."""
        if self.velocidade_y <= 5:
            self.velocidade_y += GRAVIDADE/FPS

    def verificar_colisao_chao(self):
        """Verifica e responde à colisão com o chão."""
        if self.y + self.raio >= ALTURA:
            self.y = ALTURA - self.raio  # Corrige a posição
            self.velocidade_y *= -0.8  # Inverte a velocidade com um pouco de amortecimento
            self.velocidade_x *= 0.9  # Reduz a velocidade horizontal ao quicar
            return True
        return False
    
    def verificar_colisao_paredes(self):
        """Verifica e responde à colisão com as paredes."""
        if self.x - self.raio <= 0 or self.x + self.raio >= LARGURA:
            self.velocidade_x *= -1  # Inverte a velocidade horizontal
            self.x = max(self.raio, min(self.x, LARGURA - self.raio))  # Corrige a posição

    def desenhar(self, tela):
        if self.drawn:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

    def colidiu_com(self, outro_circulo):
        if self.drawn:
            distancia = ((self.x - outro_circulo.x) ** 2 + (self.y - outro_circulo.y) ** 2) ** 0.5
            return distancia < self.raio + outro_circulo.raio
    
    def criar(x,y,created):
        for _ in range(LIMITE_DE_CRIACAO):
            raio = RAIO # Raio 
            cor = (BRANCO)  # Cor aleatória
            velocidade_x = 0 # Velocidade horizontal aleatória
            velocidade_y = GRAVIDADE  # Velocidade vertical 
            ball = Circulo(x, y, raio, cor, velocidade_x, velocidade_y,list())  # Cria um objeto Circulo
            balls.append(ball)  # Adiciona à lista
            created += 1

    def multiplicar(self, x, id):
        self.y += 10
        for _ in range(x-1):
            balls.append(Circulo(self.x, self.y-10, self.raio, VERMELHO, self.velocidade_x, self.velocidade_y,[id],True))

class CloseButton:
    def __init__(self):
        self.size = 20  
        self.padding = 10  
        self.rect = pygame.Rect(LARGURA - self.size - self.padding, self.padding, self.size, self.size)
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    
    def draw(self, screen):
        if self.is_hovered:
            color = (255, 255, 255)  
            LARGURA = 2  
        else:
            color = (150, 150, 150)  
            LARGURA = 1  
        
        x, y = self.rect.topleft
        size = self.size
        margin = size * 0.3  
        start_pos1 = (x + margin, y + margin)
        end_pos1 = (x + size - margin, y + size - margin)
        start_pos2 = (x + size - margin, y + margin)
        end_pos2 = (x + margin, y + size - margin)
        pygame.draw.line(screen, color, start_pos1, end_pos1, LARGURA)
        pygame.draw.line(screen, color, start_pos2, end_pos2, LARGURA)

def colisaoDaMultiplicação():
    for i in range(len(retangulos)):
        for j in range(len(balls)):
            if retangulos[i].colidiu_com(balls[j]) and retangulos[i].id not in balls[j].contacts:
                balls[j].multiply(retangulos[i].mult, retangulos[i].id,balls[len(balls)-1].id)
                balls[j].contacts.append(retangulos[i].id)

# Inicializa o Pygame
pygame.init()

lastTick = 0

# Configurações da tela
FPS = 60
LARGURA = 540
ALTURA = 960
TELA = pygame.display.set_mode((LARGURA, ALTURA))
FONTE = pygame.font.Font(None, 48)
pygame.display.set_caption("Meu Primeiro Jogo com Pygame")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO =(0,0,0)

RAIO = 8  # Raio dos círculos
LIMITE_DE_CRIACAO = 15  # Limite de círculos à serem criados
balls = []
retangulos = []

Retangulo.criar_retangulos() # Cria os retângulos


# Loop principal do jogo
rodando = True
while rodando:
    # Verifica eventos (como fechar a janela)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:  # Captura clique do mouse
            if evento.button == 1 and created < LIMITE_DE_CRIACAO:  # Botão esquerdo do mouse
                # Obtém a posição do clique
                x, y = evento.pos
                # Define propriedades aleatórias para o novo círculo
                Ball.generate(x,y,created)
                created =+ len(balls)
        CloseButton().handle_event(evento)

    # Captura teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_ESCAPE]:
        rodando = False
        # Preenche a tela com branco
    TELA.fill((0,0,0))
    
    for retangulo in retangulos:
        retangulo.desenhar(TELA)

    for ball in balls:

        ball.update()  # Atualiza a posição do círculo

        """ball.aplicar_gravidade()  # Aplica a gravidade
        ball.verificar_colisao_chao()  # Verifica a colisão com o chão
        ball.verificar_colisao_paredes()  # Verifica a colisão com as paredes 
        """
        ball.collide_with(ball)  # Verifica a colisão com outros círculos

        if not ball.drawn and lastTick + 200 < pygame.time.get_ticks():
            ball.drawn = True
            lastTick = pygame.time.get_ticks()
        elif ball.drawn:
            
            if ball.ground_collision():  # Verifica a colisão com o chão e remove o círculo da lista
                balls.remove(ball) # Remove o círculo do jogo
                score += 1
                if len(balls) == 0:
                    rodando = False

            #ball.verificar_colisao_paredes()  # Verifica a colisão com as paredes

        ball.draw(TELA)  # Desenha o círculo
    
    
    
   
    colisaoDaMultiplicação()  # ativa colisões de multiplicação

    #atualizar score na tela

    texto_score = FONTE.render(f'{score}', False, VERMELHO)  # Render the score text
    TELA.blit(texto_score, (10, 10))  # Draw the score at position (10, 10)

    CloseButton().draw(TELA)

    # Atualiza a tela
    pygame.display.flip()

    # Controla a taxa de atualização (FPS)
    pygame.time.Clock().tick(FPS)
print(score)
# Encerra o Pygame
pygame.quit()
sys.exit()

