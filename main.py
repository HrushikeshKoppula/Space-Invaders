import pygame
import numpy as np

pygame.init()
screen_size = (screen_width,screen_height) = (800,600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img,(800,600))
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img,(800,600))
spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img,(45,80))
enemies_img = pygame.image.load("enemies.png")
enemies_img = pygame.transform.scale(enemies_img,(40,40))

class SPACESHIP:
    def __init__(self,left=screen_width/2,top=screen_height/2,width=45,height=80,color="green",speed=5):
        self.image = spaceship_img
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.rlim = screen_width-width
        self.ulim = 0
        self.llim = 0
        self.dlim = screen_height-height
        # self.spaceship = pygame.Rect(left,top,width,height)

    def Draw(self):
        screen.blit(self.image,(self.left,self.top))
        # pygame.draw.rect(screen,self.color,(self.left,self.top,self.width,self.height))
        # pygame.draw.rect(screen,color,self.spaceship)

    def Left(self):
        self.left-=self.speed
        if self.left<self.llim:
            self.left=self.llim

    def Right(self):
        self.left+=self.speed
        if self.left>self.rlim:
            self.left=self.rlim

    def Up(self):
        self.top-=self.speed
        if self.top<self.ulim:
            self.top=self.ulim

    def Down(self):
        self.top+=self.speed
        if self.top>self.dlim:
            self.top=self.dlim

class ENEMY:
    def __init__(self,left,top,width=45,height=45,color="red",speed=2):
        self.image = enemies_img
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def Draw(self):
        screen.blit(self.image,(self.left,self.top))
        # pygame.draw.rect(screen,self.color,(self.left,self.top,self.width,self.height))

    def Move(self,direction):
        self.left+=self.speed*direction
        
    def edge_check(self):
        if self.left<=0 or self.left>=screen_width-self.width:
            return True
            # self.direction*=-1
            # self.top+=20

class Projectile:
    def __init__(self,x,y,r,color,speed,ulim):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.speed = speed
        self.ulim = ulim

    def Draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)

    def Up(self):
        self.y-=self.speed
        if self.y<self.ulim:
            self.y=self.ulim

class Projectiles:
    def __init__(self):
        self.projectiles_list = []

    def spawn_projectile(self,x,y):
        if len(self.projectiles_list)<5:
            self.projectiles_list.append(Projectile(x+22,y,5,"yellow",10,0))

    def update(self):
        for projectile in self.projectiles_list[:]:
            projectile.Up()
            if projectile.y<=projectile.ulim:
                self.projectiles_list.remove(projectile)

    def Draw(self):
        for projectile in self.projectiles_list:
            projectile.Draw()

def check_collision(projectile,enemy):
    if (projectile.x+projectile.r>enemy.left)and(projectile.x-projectile.r<enemy.left+enemy.width)and(projectile.y+projectile.r>enemy.top)and(projectile.y-projectile.r<enemy.top+enemy.height):
        return True
    return False

class ENEMIES:
    def __init__(self,row,col):
        self.Enemies = []
        for row in range(3):
            for col in range(7):
                left = col*100+100
                top = row*60+50
                self.Enemies.append(ENEMY(left,top))
        self.swarm_direction = 1
    
    def Move_and_check_collision(self,projectiles):
        self.edge_checker_for_all()
        for enemy in self.Enemies:
            enemy.Move(self.swarm_direction)
            enemy.Draw()
            for projectile in projectiles.projectiles_list:
                if check_collision(projectile,enemy):
                    projectiles.projectiles_list.remove(projectile)
                    self.Enemies.remove(enemy)
                    break

    def edge_checker_for_all(self):
        for enemie in self.Enemies:
            if enemie.edge_check():
                self.swarm_direction*=-1
                break


class Button:
    def __init__(self,left,top,width,height,color,text,font_size=30):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(left,top,width,height)

    def Draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
        text_surface = self.font.render(self.text,True,"white")
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface,text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


SpaceShip = SPACESHIP()
projectiles = Projectiles()
start_button = Button(screen_width//2-100,screen_height//2+150,200,100,"green","Start")
end_button = Button(screen_width//2+100,screen_height//2+150,200,100,"red","End")
Enemies = ENEMIES(3,7)

def main():
    game_active = False
    game_end = False
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
                    projectiles.spawn_projectile(SpaceShip.left,SpaceShip.top)

        # screen.fill("purple")

        if len(Enemies.Enemies)==0:
            game_active = False
            game_end = True

        if game_active:
            screen.blit(background_img,(0,0))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                SpaceShip.Right()
            if keys[pygame.K_UP]:
                SpaceShip.Up()
            if keys[pygame.K_LEFT]:
                SpaceShip.Left()
            if keys[pygame.K_DOWN]:
                SpaceShip.Down()

            SpaceShip.Draw()
            projectiles.update()
            projectiles.Draw()

            Enemies.Move_and_check_collision(projectiles)

        elif not game_end:
            screen.blit(start_img,(0,0))
            start_button.Draw()

        else:
            screen.blit(start_img,(0,0))
            end_button.Draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
