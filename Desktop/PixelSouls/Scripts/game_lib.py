import pygame
import random

from game_lib2 import *
from entity import *
from items import HealtPotion

class LevelGenerator:
    def __init__(self, board, map_num=None, stage=None) -> None:
        self.board = board
        
        self.stage = board.info.stage[0] + 1
        self.stage = self.stage if self.stage <= 2 else 2
        
        print("++++", self.stage, board.info.stage[1])
        
        if map_num is None:
            self.map_num = random.randint(1, 5)
        else:
            self.map_num = map_num
            
        self.side = 1 if self.board.info.stage[1] <= 5 else 2
            
        self.field_floor, self.field_props, self.field_items = self.load_preset()
        
    def get_size_board(self):
        return len(self.field_floor[0]), len(self.field_floor)
    
    def split_on(self, lst, delimiter = ""):
        splitted = [[]]
        for item in lst:
            if item == delimiter:
                splitted.append([])
            else:
                splitted[-1].append(item)
        return splitted
    
    def load_preset(self):
        with open(f"../Preser_map\map{self.map_num}_{self.stage}_{self.side}.txt") as f:
            lst = list(map(lambda x: x.replace("\n", ""),f.readlines()))
            return self.split_on(lst)
        
    def create_wall(self, props_g):
        image = pygame.Surface((self.board.cell_size * self.board.width + 38, self.board.cell_size * self.board.height + self.board.cell_size * 2 + 38), pygame.SRCALPHA, 32)
        
        
        image_wall = load_image(rf"wall_stage_2\wall_mid.png")
        image_wall_left = load_image(rf"wall_stage_2\wall_inner_corner_mid_left.png")
        image_wall_right = load_image(rf"wall_stage_2\wall_inner_corner_mid_rigth.png")
        image_wall_top = load_image(rf"wall_stage_2\wall_inner_corner_t_top_left.png")                     
                               
        
        for i in range(self.board.width):
            if i == 0:
                b = pygame.transform.scale(image_wall_left, (self.board.cell_size, self.board.cell_size))
            elif i == self.board.width - 1:
                b = pygame.transform.scale(image_wall_right, (self.board.cell_size, self.board.cell_size))
            else:
                b = pygame.transform.scale(image_wall, (self.board.cell_size, self.board.cell_size))

            image.blit(b, (self.board.cell_size * i, 19))   
            
            if i != self.board.width - 1:
                b = pygame.transform.scale(image_wall_top, (self.board.cell_size, self.board.cell_size))
                image.blit(b, (self.board.cell_size * i, -self.board.cell_size + 19))   
            else:
                b = pygame.transform.scale(image_wall_top, (self.board.cell_size, self.board.cell_size))
                b = pygame.transform.flip(b, True, False)
                image.blit(b, (self.board.cell_size * i, -self.board.cell_size + 19))                   
            
        image_wall_left = pygame.transform.rotate(load_image(rf"wall_stage_2\wall_inner_corner_t_top_left.png")
                                 ,90)
        image_wall_right = pygame.transform.rotate(load_image(rf"wall_stage_2\wall_inner_corner_t_top_left.png")
                                 ,-90)
        
        
        image_wall_left = pygame.transform.scale(image_wall_left, (self.board.cell_size, self.board.cell_size))
        image_wall_right = pygame.transform.scale(image_wall_right, (self.board.cell_size, self.board.cell_size))
        
        for i in range(self.board.height):
            image.blit(image_wall_left, (-self.board.cell_size + 18, self.board.cell_size * (i + 1)))
            image.blit(image_wall_right, (self.board.cell_size * self.board.width - 19, self.board.cell_size * (i + 1)))
                  
                  
        image_wall = load_image(rf"wall_stage_2\wall_mid.png")
        image_wall_left = load_image(rf"wall_stage_2\wall_inner_corner_l_top_left.png")
        image_wall_right = load_image(rf"wall_stage_2\wall_inner_corner_l_top_rigth.png")
        image_wall_top = pygame.transform.flip(load_image(rf"wall_stage_2\wall_inner_corner_t_top_left.png"), False, False)                          
                       
        for i in range(self.board.width):
            b = pygame.transform.scale(image_wall, (self.board.cell_size, self.board.cell_size))
            image.blit(b, (self.board.cell_size * i, self.board.cell_size * (self.board.height + 1)))   

            if i == 0:
                b = pygame.transform.scale(image_wall_left, (self.board.cell_size, self.board.cell_size))
                image.blit(b, (self.board.cell_size * i, self.board.cell_size * self.board.height))   
            elif i == self.board.width - 1:
                b = pygame.transform.scale(image_wall_right, (self.board.cell_size, self.board.cell_size))       
                image.blit(b, (self.board.cell_size * i, self.board.cell_size * self.board.height))   
            else:
                b = pygame.transform.scale(image_wall_top, (self.board.cell_size, self.board.cell_size))
                image.blit(b, (self.board.cell_size * i, self.board.cell_size * self.board.height))   


        Decor((self.board.left, self.board.top - self.board.cell_size - 19),
            (self.board.cell_size * self.board.width + 38, self.board.cell_size * self.board.height + self.board.cell_size * 2 + 38),
            image, self.board, props_g)          


            
            
    def fill_floor(self, group):
        image = pygame.Surface((self.board.cell_size * self.board.width + 38, self.board.cell_size * self.board.height + self.board.cell_size * 2 + 38), pygame.SRCALPHA, 32)
        image = pygame.transform.scale(image, (self.board.cell_size * self.board.width, self.board.cell_size * self.board.height))

        # floor_field = []
        for y, line in enumerate(self.field_floor):
            row = []
            for x, char in enumerate(line):
                if char == "#":
                    if self.stage == 1:
                        b = pygame.transform.scale(
                            load_image(rf"floor_stage_1\floor_{random.randint(1, 10)}.png"),
                            (self.board.cell_size, self.board.cell_size)                    
                            )
                    
                    elif self.stage == 2:
                        b = pygame.transform.scale(
                            load_image(rf"floor_stage_2\floor_{random.randint(1, 8)}.png"), 
                            (self.board.cell_size, self.board.cell_size)
                            )                    
                    image.blit(b, (x * self.board.cell_size, y * self.board.cell_size))               
        
        Decor((self.board.left, self.board.top),
            (self.board.cell_size * self.board.width, self.board.cell_size * self.board.height),
            image, self.board, group)      
                    
                    # row.append(Floor(x, y, self.board, self.stage, group))
            # floor_field.append(row)  
        
        # return floor_field    
            
    
    def fill_props(self, player_g=None, enemy_g=None, esc_g=None, props_g=None):
        props_field = []
        for y, line in enumerate(self.field_props):
            row = []
            for x, char in enumerate(line):
                if char == "0":
                    row.append(Void())
                elif char == "@":
                    if self.stage == 2:
                        if self.board.info.stage[1] <= 5:
                            rand = random.randint(0, 8)
                            if rand in (0, 1, 2):
                                row.append(NormalSwampy(x, y, self.board, enemy_g))
                            elif rand in (3, 4):
                                row.append(Swampy(x, y, self.board, enemy_g))
                            elif rand in (5, 6):
                                row.append(Wogol(x, y, self.board, enemy_g))
                            elif rand == 7:
                                row.append(Ogr(x, y, self.board, enemy_g))
                            elif rand == 8:
                                row.append(Stone(x, y, self.board, enemy_g))
                        else:
                            rand = random.randint(0, 8)
                            if rand == 0:
                                row.append(NormalSwampy(x, y, self.board, enemy_g))
                            elif rand in (3, 4, 2):
                                row.append(Swampy(x, y, self.board, enemy_g))
                            elif rand in (5, 6, 1):
                                row.append(Wogol(x, y, self.board, enemy_g))
                            elif rand == 7:
                                row.append(Ogr(x, y, self.board, enemy_g))
                            elif rand == 8:
                                row.append(Stone(x, y, self.board, enemy_g))                            
                    else:
                        if self.board.info.stage[1] <= 5:
                            rand = random.randint(0, 4)
                            if rand in (0, 1):
                                row.append(GoblinShaman(x, y, self.board, enemy_g))  
                                
                            elif rand in (2, 3):
                                row.append(Goblin(x, y, self.board, enemy_g))
                            
                            elif rand == 4:
                                row.append(Slime(x, y, self.board, enemy_g))
                        else:
                            rand = random.randint(0, 5)
                            if rand in (0, 1):
                                row.append(GoblinShaman(x, y, self.board, enemy_g))  
                                
                            elif rand in (2, 3):
                                row.append(Goblin(x, y, self.board, enemy_g))
                            
                            elif rand in (4, 5):
                                row.append(Slime(x, y, self.board, enemy_g))
                            elif rand == 6:
                                row.append(MaskedGoblin(x, y, self.board, enemy_g))   
                                                                                                
                elif char == "+":
                    if self.stage == 1:
                        if random.randint(1, 2) == 1:
                            image = load_image("props/table.png")  
                        else:
                            image = load_image("props/barrel.png")  
                        row.append(Props((0, 0), (x * self.board.cell_size + self.board.left, y * self.board.cell_size + self.board.top), (self.board.cell_size, self.board.cell_size), image, self.board, props_g))
                    else:
                        if random.randint(1, 2) == 1:
                              image = load_image("props/crate.png") 
                        else:
                            image = load_image("props/barrel.png") 
                        row.append(Props((0, 0), (x * self.board.cell_size + self.board.left, y * self.board.cell_size + self.board.top), (self.board.cell_size, self.board.cell_size), image, self.board, props_g))                        
                elif char == "-":
                    self.board.escape = Escape(x, y, self.board, esc_g, stage=self.stage)
                    row.append(self.board.escape)
                elif char == "X":
                    row.append(self.board.get_player())
                    self.board.get_player().coords = (x, y)
                
            props_field.append(row)  
            self.create_wall(props_g)
        return props_field     
    
    def fill_items(self, group):
        items_field = []
        for y, line in enumerate(self.field_items):
            row = []
            for x, char in enumerate(line):        
                if char == "0":
                    row.append(None)
                elif char == "*":
                    row.append(HealtPotion(x, y, self.board, group))
                elif char == "+":
                    if random.randint(1, 4) == 1: 
                        row.append(Chest(x, y, self.board, group))
                    else:
                        row.append(None)
            items_field.append(row) 
        return items_field     
   
class Decor(pygame.sprite.Sprite):
    def __init__(self, pos, size, image, board, group):
        super().__init__(group)
        
        image = pygame.transform.scale(image, (size[0], size[1]))
        
        self.image = image
        self.rect = pygame.Rect(pos[0], pos[1], board.cell_size, board.cell_size)     
        
        
class Escape(pygame.sprite.Sprite):
    def __init__(self, x, y, board, group, stage=1):
        super().__init__(group)
        self.coords = (x, y)
        self.board = board    
        self.stage = stage
        self.create_sprite(x, y)
       


    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        if self.stage == 1:
            image = load_image(rf"floor_stage_1\escape.png")
        elif self.stage == 2:
            image = load_image(rf"floor_stage_2\escape.png")
        image = pygame.transform.scale(image, (self.board.cell_size, self.board.cell_size))
        
        self.image = image
        self.rect = pygame.Rect(x, y, self.board.cell_size, self.board.cell_size)

    def get_coords(self):
        return self.coords