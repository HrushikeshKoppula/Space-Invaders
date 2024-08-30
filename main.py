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
        self.projectiles_list=np.array()

    def spawn_projectile(self):
        if len(self.projectiles_list)<5:
            self.projectiles_list.append(SpaceShip.left,SpaceShip.top)

SpaceShip = SPACESHIP()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            SpaceShip.Right()
        if keys[pygame.K_UP]:
            SpaceShip.Up()
        if keys[pygame.K_LEFT]:
            SpaceShip.Left()
        if keys[pygame.K_DOWN]:
            SpaceShip.Down()

        screen.fill("purple")
        SpaceShip.Draw()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
