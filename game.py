import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

tile_size = 50
game_over = 0

bg = pygame.image.load('img/bg.png')
bg_img = pygame.transform.scale(bg, (800,800))


class world():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('img/dirt.png')
        dirt2_img = pygame.image.load('img/dirt2.png')
        barrier_img = pygame.image.load('img/invisible_block.png')

        row_count = 0
        for row in data: 
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale (dirt_img, (tile_size,tile_size))
                    img_rectangle = img.get_rect() #change the img to rectangle
                    img_rectangle.x = col_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img,img_rectangle)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale (dirt2_img, (tile_size,tile_size))
                    img_rectangle = img.get_rect() #change the img to rectangle
                    img_rectangle.x = col_count * tile_size
                    img_rectangle.y = row_count * tile_size 
                    tile = (img,img_rectangle)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy1 = enemy(col_count * tile_size, row_count * tile_size + 19)
                    enemy_group.add(enemy1)
                if tile == 4:
                    spikes1 = spikes(col_count * tile_size, row_count * tile_size+10)
                    spikes_group.add(spikes1)
                if tile == 9:
                    img = pygame.transform.scale (barrier_img, (tile_size,tile_size))
                    img_rectangle = img.get_rect() #change the img to rectangle
                    img_rectangle.x = col_count * tile_size
                    img_rectangle.y = row_count * tile_size
                    tile = (img,img_rectangle)
                    self.tile_list.append(tile)
                col_count +=1
            row_count+=1
    
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class player():
    def __init__(self, x, y):
        img = pygame.image.load('img/character.png')
        self.image = pygame.transform.scale(img, (28,64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
    
    def update(self, game_over):
        dx = 0
        dy = 0

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 5
            if key[pygame.K_d]:
                dx += 5
            
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            
            for tile in world1.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
                    if self.vel_y < 0 :  
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
            
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
            
            if pygame.sprite.spritecollide(self, spikes_group, False):
                game_over = -1
                    
            self.rect.x += dx
            self.rect.y += dy
        

        screen.blit(self.image, self.rect)

        return game_over

class enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/purple_slime.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 100:
            self.move_direction *= -1
            self.move_counter *= -1


class spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/spikes.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size-10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

world_lst = [
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 9],
    [9, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 0, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 9],
    [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
]

player1 = player(100, screen_height-114)
enemy_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
world1 = world(world_lst)


run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0,0))

    world1.draw()

    if game_over == 0 :
        enemy_group.update()
    enemy_group.draw(screen)
    spikes_group.draw(screen)

    game_over = player1.update(game_over)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()