import pygame
import os
from pygame.transform import scale

class Animation:

    def __init__(self, screen, palette, y_sprite1, nb_sprites, speed=1, loop=True, width=62, height=64):
        self.screen = screen
        self.palette_name = palette
        self.palette = pygame.image.load(os.path.join("data","graphismes",self.palette_name))
        self.x_pos = 1
        self.y_pos = y_sprite1
        self.larg_sprite = width
        self.haut_sprite = height
        self.nb_sprites = nb_sprites
        self.sprite_list = []
        self.speed = speed
        self.isLoop = loop
        self.play = False
        self.play_count = 0
        self.update(self.x_pos,self.y_pos)

    def update(self, x_sprites=1, y_sprites=1):
        self.x_pos = x_sprites
        self.y_pos = y_sprites
        self.sprite_list = []
        for i_sprite in range(self.nb_sprites):
            #print(x_sprites+(self.larg_sprite+1)*i_sprite)
            sprite = self.palette.subsurface(x_sprites+(self.larg_sprite+2)*i_sprite, y_sprites, self.larg_sprite-1, self.haut_sprite-1)
            #if self.palette_name == "microman_sprites.png":
            sprite = scale(sprite, (self.larg_sprite*3,self.haut_sprite*3))
            self.sprite_list.append(sprite)

    def affiche(self, x, y, clock):
        #print(new_speed)
        if self.play_count >= self.nb_sprites * self.speed:
            if self.isLoop:
                self.play_count = 0
            else:
                self.play_count = 0
                self.play = False
        if self.play:
            sprite = self.sprite_list[self.play_count//self.speed]
            self.screen.blit(sprite, (x,y))
            self.play_count += 1


