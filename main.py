import pygame
import numpy as np

pygame.init()
screen_size = (screen_width,screen_height) = (1280,720)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

class SPACESHIP:
    def __init__(self,left=screen_width/2,top=screen_height/2,width=45,height=80,color="green",speed=5):
        self.left=left
        self.top=top
        self.width=width
        self.height=height
        self.color=color
        self.speed=speed
        self.rlim=screen_width-width
        self.ulim=0
        self.llim=0
        self.dlim=screen_height-height
        # self.spaceship=pygame.Rect(left,top,width,height)

    def Draw(self):
        pygame.draw.rect(screen,self.color,(self.left,self.top,self.width,self.height))
        # pygame.draw.rect(screen,color,self.spaceship)

    def Left(self):
        self.left -= self.speed
        if self.left<self.llim:
            self.left=self.llim

    def Right(self):
        self.left += self.speed
        if self.left>self.rlim:
            self.left=self.rlim

    def Up(self):
        self.top -= self.speed
        if self.top<self.ulim:
            self.top=self.ulim

    def Down(self):
        self.top += self.speed
        if self.top>self.dlim:
            self.top=self.dlim
class ENEMY:
    def __init__(self, left, top, width=45, height=45, color="red", speed=2):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left

    def Draw(self):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.height))

    def Move(self):
        self.left += self.speed * self.direction
        if self.left <= 0 or self.left >= screen_width - self.width:
            self.direction *= -1
            self.top += 20  # Move down when changing direction


class Projectile:
    def __init__(self,x,y,r,color,speed,ulim):
        self.x=x
        self.y=y
        self.r=r
        self.color=color
        self.speed=speed
        self.ulim=ulim

    def Draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)

    def Up(self):
        self.y -= self.speed
        if self.y < self.ulim:
            self.y = self.ulim

class Projectiles:
    def __init__(self):
        self.projectiles_list = []

    def spawn_projectile(self, x, y):
        if len(self.projectiles_list) < 5:  # Limit the number of projectiles
            self.projectiles_list.append(Projectile(x + 22, y, 5, "yellow", 10, 0))

    def update(self):
        for projectile in self.projectiles_list[:]:
            projectile.Up()
            if projectile.y <= projectile.ulim:
                self.projectiles_list.remove(projectile)

    def Draw(self):
        for projectile in self.projectiles_list:
            projectile.Draw()

def check_collision(projectile, enemy):
    if (
        projectile.x + projectile.r > enemy.left and
        projectile.x - projectile.r < enemy.left + enemy.width and
        projectile.y + projectile.r > enemy.top and
        projectile.y - projectile.r < enemy.top + enemy.height
    ):
        return True
    return False

class Button:
    def __init__(self, left, top, width, height, color, text, font_size=30):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(left, top, width, height)

    def Draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


SpaceShip = SPACESHIP()
Enemies = [ENEMY(100 * i, 100) for i in range(5)]
projectiles = Projectiles()
start_button = Button(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100, "green", "Start")
end_button = Button(screen_width // 2 - 100, screen_height // 2 + 100, 200, 100, "red", "End")

def main():
    game_active = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_active = True
                if end_button.is_clicked(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN and game_active:
                if event.key == pygame.K_SPACE:
                    projectiles.spawn_projectile(SpaceShip.left, SpaceShip.top)

        screen.fill("purple")

        if len(Enemies)==0:
            game_active=False

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                SpaceShip.Right()
            if keys[pygame.K_UP]:
                SpaceShip.Up()
            if keys[pygame.K_LEFT]:
                SpaceShip.Left()
            if keys[pygame.K_DOWN]:
                SpaceShip.Down()

            # Update the game state
            SpaceShip.Draw()
            projectiles.update()
            projectiles.Draw()

            for enemy in Enemies[:]:
                enemy.Move()
                enemy.Draw()
                for projectile in projectiles.projectiles_list[:]:
                    if check_collision(projectile, enemy):
                        projectiles.projectiles_list.remove(projectile)
                        Enemies.remove(enemy)
                        break  # Exit the inner loop since the enemy is already removed

        else:
            start_button.Draw()
            end_button.Draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()