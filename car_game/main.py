import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rally Fury Style Racing Game")

# Load images
player_img = pygame.image.load("assets/playercar.png")
blackcar_img = pygame.image.load("assets/blackcar.png")
bluecar_img = pygame.image.load("assets/bluecar.png")
road_img = pygame.image.load("assets/road.png")
finish_img = pygame.image.load("assets/background2.png")

# Resize images
player_img = pygame.transform.scale(player_img, (50, 100))
enemy_imgs = [
    pygame.transform.scale(blackcar_img, (50, 100)),
    pygame.transform.scale(bluecar_img, (50, 100))
]
road_img = pygame.transform.scale(road_img, (WIDTH, 200))
finish_img = pygame.transform.scale(finish_img, (WIDTH, 100))

# Fonts
font = pygame.font.SysFont("arial", 30)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Car class
class Car:
    def __init__(self, x, y, img, is_player=False):
        self.x = x
        self.y = y
        self.img = img
        self.is_player = is_player
        self.speed = 5 if is_player else random.randint(2, 4)
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, keys=None):
        if self.is_player and keys:
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < WIDTH - 50:
                self.x += self.speed
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < HEIGHT - 100:
                self.y += self.speed
        else:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

# Drawing window function
def draw_window(player, enemies, roads, finish_line, score):
    WIN.fill((0, 0, 0))

    for road in roads:
        WIN.blit(road[0], (0, road[1]))

    if finish_line[1] > -100:
        WIN.blit(finish_line[0], (0, finish_line[1]))

    for enemy in enemies:
        enemy.draw(WIN)

    player.draw(WIN)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))
    pygame.display.update()

# Main game loop
def main():
    run = True
    player = Car(WIDTH // 2, HEIGHT - 120, player_img, is_player=True)

    enemies = []
    for i in range(5):
        x = random.randint(100, WIDTH - 150)
        y = HEIGHT + i * -150
        img = random.choice(enemy_imgs)
        enemies.append(Car(x, y, img))

    roads = []
    road_y = 0
    for i in range(10):
        roads.append([road_img, road_y])
        road_y -= 200

    finish_line = [finish_img, road_y - 200]
    score = 0
    game_over = False

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            player.move(keys)

            # Move enemies
            for enemy in enemies:
                enemy.move()
                if player.rect.colliderect(enemy.rect):
                    game_over = True

            # Scroll roads and finish line
            for road in roads:
                road[1] += 3
            finish_line[1] += 3

            # Update enemy positions
            for enemy in enemies:
                if enemy.y > HEIGHT:
                    enemy.y = -100
                    enemy.x = random.randint(100, WIDTH - 150)
                    enemy.img = random.choice(enemy_imgs)
                    score += 10

            # Check finish line
            if player.rect.colliderect(pygame.Rect(0, finish_line[1], WIDTH, 100)):
                game_over = True
                score += 100

            draw_window(player, enemies, roads, finish_line, score)

        else:
            WIN.fill((0, 0, 0))
            over_text = font.render("🏁 Race Over!", True, (255, 0, 0))
            score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

            WIN.blit(over_text, (WIDTH//2 - 100, HEIGHT//2 - 60))
            WIN.blit(score_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
            WIN.blit(restart_text, (WIDTH//2 - 180, HEIGHT//2 + 30))
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()