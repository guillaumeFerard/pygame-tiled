# Pygame template - skeleton for a new pygame project
import random
import os
import pygame



WIDTH = 1080
HEIGHT = 720
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")


class Player(pygame.sprite.Sprite):
    "sprite for the player"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "ship2.png")).convert() # import image and use as image sprtite convert is used to convert image into format pygame to be used faster
        self.image.set_colorkey(BLACK) # replace the player rectangle background's color into transparent, the argument is black here cause black was the background color setted
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 #every sprite has rectangle image sprite is in a rectangle recquired for hitbox for example
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 0


    def update(self):
        """hi"""
        self.speedx = 0
        self.speedy = 0
        keystatus = pygame.key.get_pressed()
        if keystatus[pygame.K_LEFT]:
            self.speedx = - 10
        if keystatus[pygame.K_RIGHT]:
            self.speedx = 10
        if keystatus[pygame.K_DOWN]:
            self.speedy = 10
        if keystatus[pygame.K_UP]:
            self.speedy = -10
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  #bullet pop in front of the player
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "drone.png"))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) # random places where enemy will pop
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.dead = False
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:         #when mob is at this point it restart moving at the top of the screen where it poped first
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        if self.dead == True:
            self.image = pygame.image.load(os.path.join(img_folder, "drone.png"))


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y): # x and y are used to figured out where the player is and then keep bullets starting from the front of the player while he is moving
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "ebullet2.png"))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves of the top of the screen
        if self.rect.bottom < 0:
            self.kill()




#        self.rect.x += 5 # sprite move + pixels
#        self.rect.y += self.y_speed
#        if self.rect. bottom > HEIGHT - 200:
#            self.y_speed = - 5
#        if self.rect.top < 200:
#            self.y_speed = 5
#        if self.rect.x > WIDTH: # if sprite leave the screen on x it restart to the left
#            self.rect.x = 0




# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
points = 0
all_sprites = pygame.sprite.Group() # empty group created to put all the sprites group in it when running the game
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()

    #check if a bullet hit mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:  #for each mob killed another respawn
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        points += 5
        print(points)
    # check if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, False, ) # return a list
    if hits:
        running = False # if player get hit game stop
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #*after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()