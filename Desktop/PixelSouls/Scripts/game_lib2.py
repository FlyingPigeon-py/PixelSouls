import pygame
import random
import os
import sys


def get_round_coords(x, y):
    return [[x - 1, y], [x + 1, y], [x, y - 1],[x, y + 1]]

def get_corner_coords(x, y):
    print([[x - 1, y + 1], [x - 1, y - 1], [x + 1, y - 1], [x + 1, y + 1]])
    return [[x - 1, y + 1], [x - 1, y - 1], [x + 1, y - 1], [x + 1, y + 1]]

def floor_or_wall(x, y, board):
    if type(board.board[y][x]) == Void or type(board.board[y][x]) == Floor:
        return 0
    else:
        return 1

def get_path(board, pozIn, pozOut):
    labirint = board.board
    labirint = [[floor_or_wall(x, y, board) for x in range(len(labirint[0]))] for y in range(len(labirint))]
    pozIn = pozIn[::-1]
    pozOut = pozOut[::-1]
 
    path = [[x if x == 0 else -1 for x in y] for y in labirint]
    path[pozIn[0]][pozIn[1]] = 1; 
 
    if not found(path, pozOut):
        return None
    
    result = printPath(path, pozOut)

    return result

def load_sounds(name, colorkey=None):
    fullname = os.path.join('../Sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл с звуком '{fullname}' не найден")
        sys.exit()
        
    sound = pygame.mixer.Sound(fullname)
    return sound

def load_image(name, colorkey=None):
    fullname = os.path.join('../Data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def found(pathArr, finPoint):
    weight = 1
    for i in range(len(pathArr)*len(pathArr[0])):
        weight += 1 
        for y in range(len(pathArr)):          
            for x in range(len(pathArr[y])):                   
                if pathArr[y][x] == (weight - 1):            
                    if y > 0 and pathArr[y-1][x] == 0:
                        pathArr[y-1][x] = weight
                    if y < (len(pathArr)-1) and pathArr[y+1][x] == 0:
                        pathArr[y+1][x] = weight
                    if x > 0 and pathArr[y][x-1] == 0:
                        pathArr[y][x-1] = weight
                    if x < (len(pathArr[y])-1) and pathArr[y][x+1] == 0:
                        pathArr[y][x+1] = weight
                            
                    if (abs(y-finPoint[0]) + abs(x-finPoint[1])) == 1:
                        pathArr[finPoint[0]][finPoint[1]] = weight
                        return True           
    return False      


def printPath(pathArr, finPoint):      
    y = finPoint[0]
    x = finPoint[1]
    weight = pathArr[y][x]
    result = list(range(weight))
    while (weight):
        weight -=1
        if y > 0 and pathArr[y-1][x] == weight:
            y -= 1
            result[weight] = 'down' 
        elif y < (len(pathArr)-1) and pathArr[y+1][x] == weight:
            result[weight] = 'up' 
            y += 1
        elif x > 0 and pathArr[y][x-1] == weight:
            result[weight] = 'right' 
            x -= 1
        elif x < (len(pathArr[y])-1) and pathArr[y][x+1] == weight:
            result[weight] = 'left' 
            x += 1
            
    return result[1:]


class Void:
    def __init__(self):
        pass
    
    
class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, board, stage, group):
        super().__init__(group)
        self.step = False
        self.coords = (x, y)
        
        x = x * board.cell_size + board.left
        y = y * board.cell_size + board.top

        if stage == 1:
            image = load_image(rf"floor_stage_1\floor_{random.randint(1, 10)}.png")
        elif stage == 2:
            image = load_image(rf"floor_stage_2\floor_{random.randint(1, 8)}.png")
            
        
        
        image = pygame.transform.scale(image, (board.cell_size, board.cell_size))
        
        
        
        self.image = image
        self.rect = pygame.Rect(x, y, board.cell_size, board.cell_size)


    def isStep(self):
        return self.step

    def get_coords(self):
        return self.coords

    def correct_step(self):
        self.step = True

    def update(self):
        image = load_image(f"floor_{random.randint(4, 9)}.png")
        image = pygame.transform.scale(image, (55, 55))
        self.image = image
        
        
class Button(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, screen, game_sound, game_font, scale=(2, 2), font=None):
        super().__init__(sprite)
        
        self.font = font
        
        self.screen = screen
        self.text = ""
        self.game_sound = game_sound
        
        self.game_font = game_font
        
        self.x = x
        self.y = y
        
        self.isPress = False
        self.isSelect = False
        
        self.scale = scale
        
        self.func = lambda: print(1)
        
        screen.get_width()
        screen.get_height()
        
        
        
        self.idle = load_image("ui/menu_button.png")
        self.select = load_image("ui/menu_button_select.png")  
        self.press = load_image("ui/menu_button_press.png")  
        
        self.idle = pygame.transform.scale(self.idle, (self.idle.get_width() * self.scale[0], self.idle.get_height() * self.scale[1]))
        self.select = pygame.transform.scale(self.select, (self.select.get_width() * self.scale[0], self.select.get_height() * self.scale[1]))
        self.press = pygame.transform.scale(self.press, (self.press.get_width() * self.scale[0], self.press.get_height() * self.scale[1]))
        
        self.image = self.idle

        self.rect = pygame.Rect(x, y, self.idle.get_width() * self.scale[0], self.idle.get_height() * self.scale[1])   
        
    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.idle.get_width() * self.scale[0], self.idle.get_height() * self.scale[1])   
        
    def set_func(self, func):
        self.func = func
        
    def set_text(self, text):
        self.text = text
    
    def update(self):
        x_m, y_m = pygame.mouse.get_pos()
        
            
        if not self.isPress or not pygame.mouse.get_pressed()[0]: 
            if x_m >= self.x and x_m <= self.x + self.idle.get_width() and\
            y_m >= self.y and y_m <= self.y + self.idle.get_height():
                self.image = self.select
                if not self.isSelect:
                    self.game_sound.sound_select.play()
                    self.isSelect = True
            else:
                self.isSelect = False
                self.image = self.idle
            self.draw()
        elif x_m >= self.x and x_m <= self.x + self.idle.get_width() and\
            y_m >= self.y and y_m <= self.y + self.idle.get_height():            
                self.draw(5)

        if self.isPress:
             self.draw(5)
        else:
            self.draw()
            
    
    def clicked(self):
        x_m, y_m = pygame.mouse.get_pos()
        if x_m >= self.x and x_m <= self.x + self.idle.get_width() and\
           y_m >= self.y and y_m <= self.y + self.idle.get_height():
            self.image = self.press
            self.isPress = True
            self.game_sound.sound_press.play()
            
            
    def draw(self, y=0):
        if not self.font:
            text = self.game_font.pixel_font.render(self.text, True, (45, 45, 45) if y == 0 else (255, 255, 200))
        else:
            text = self.font.render(self.text, True, (45, 45, 45) if y == 0 else (255, 255, 200))
        
        p = text.get_rect(center=(self.x + self.idle.get_width(), self.y + self.idle.get_height()))
        p.x -= self.idle.get_width() / 2
        p.y -= self.idle.get_height() / 2 + 5 - y
        self.screen.blit(text, p)
                
                
    def run(self):
        x_m, y_m = pygame.mouse.get_pos()
        if x_m >= self.x and x_m <= self.x + self.idle.get_width() and\
           y_m >= self.y and y_m <= self.y + self.idle.get_height() and self.isPress:
            self.func()
        self.isPress = False


class GameSounds:
    def __init__(self) -> None:
        self.sound_select = load_sounds("MI_SFX 24.flac")
        self.sound_select.set_volume(0.3)
        self.sound_press = load_sounds("MI_SFX 42.flac")
        self.sound_press.set_volume(0.3)
        self.sound_dash = load_sounds("epic_swishes3s.mp3")
        self.sound_dash.set_volume(0.1)
        self.sound_hit_slime = load_sounds("mixkit-weak-fast-blow-2145.flac")
        self.sound_hit_slime.set_volume(0.1)
        self.sound_hit_player = load_sounds("MI_SFX 20.flac")
        self.sound_hit_player.set_volume(0.1)
        self.sound_potion = load_sounds("MI_SFX 11.flac")
        self.sound_potion.set_volume(0.3)
        self.sound_pause_on = load_sounds("MI_SFX 03.flac")
        self.sound_pause_on.set_volume(0.3)
        self.sound_pause_off = load_sounds("MI_SFX 21.flac")
        self.sound_pause_off.set_volume(0.3)
        self.sound_game_over = load_sounds("MI_SFX 22.flac")
        self.sound_game_over.set_volume(0.2)
        
        self.sound_ice_break = load_sounds("breaking-ice-02.wav")
        self.sound_ice_break.set_volume(0.3)
        
        self.sound_ice_freeze =load_sounds("ice-cracking-01.mp3")
        self.sound_ice_freeze.set_volume(0.3)
        
        self.sound_poison_break = load_sounds("poison_break.mp3")
        self.sound_poison_break.set_volume(0.3)
        
        self.sound_poison_start =load_sounds("poison_start.mp3")
        self.sound_poison_start.set_volume(0.3)
        
class FontManager:
    def __init__(self) -> None:
        self.pixel_font = pygame.font.Font(r"../Font\Sonic 1 Title Screen Filled.ttf", 24)
        self.pixel_font_30 = pygame.font.Font(r"../Font\Sonic 1 Title Screen Filled.ttf", 30)
        
class Image(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_path, group) -> None:
        super().__init__(group)
        self.size = size
        self.pos = pos
        self.image_path = image_path
        
        image = self.press = load_image(image_path)
        self.image =  pygame.transform.scale(image, (size[0], size[1]))
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())   
        
class Text:
    def __init__(self, x=0, y=0, text="", color=(0, 0, 0,), size=24, font=None) -> None:
         self.x = x
         self.y = y
         self.color = color
         self.size = size
         self.font = font
         
         self.fraze = text
         font = font
         text = text 
         
         if not self.font:
            self.font = pygame.font.Font(r"../Font\Sonic 1 Title Screen Filled.ttf", size)
         self.text = self.font.render(text, True, color)
         
    def set_text(self, text):
        if len(self.fraze) == 2 and len(text) == 3:
            self.x -= 20
        elif len(self.fraze) == 3 and len(text) == 2:
            self.x += 20
        self.fraze = text   
        self.text = self.font.render(text, True, self.color)
         
    def get_surf(self):
        return self.text
         
    def get_size(self):
        return self.text.get_size() 
         
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y

    def draw(self, screen):
        screen.blit(self.text, (self.x, self.y)) 
        
class Widget:
    def __init__(self, x, y, size) -> None:
        self.widgets_sprites = pygame.sprite.Group()
        self.widgets_buttons = pygame.sprite.Group()
        self.text = []
        self.background_image = None
        self.x = x
        self.y = y
        self.size = size
        
        self.direction = True
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
        for i in self.widgets_buttons:
            i.x += x
            i.y += y
            i.update_rect()
        
        for i in self.widgets_sprites:
            i.rect.x += x
            i.rect.y += y
        
        for i in self.text:
            i.x += x
            i.y += y
        
    def add_text(self, text):
        self.text.append(text)
        
    def get_center_w(self, n):
        return ((self.size[0]) - n) / 2 + self.x
        
    def get_center_h(self, n):
        return ((self.size[1]) - n) / 2 + self.y
        
    def close(self):
        for i in self.widgets_sprites.sprites():
            i.kill()
        
        for i in self.widgets_buttons.sprites():
            i.kill()
            
    def draw(self, screen):
        self.widgets_sprites.draw(screen)
        self.widgets_buttons.draw(screen)
        self.widgets_buttons.update()
        self.widgets_sprites.update()
        
        for i in self.text:
            i.draw(screen)
    
    def widget_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self.widgets_buttons.sprites():
                i.clicked()
                
        if event.type == pygame.MOUSEBUTTONUP:
            for i in self.widgets_buttons.sprites():
                i.run()
                
    def get_widgets_buttons(self):
        return self.widgets_buttons
    
    def get_widgets_sprites(self):
        return self.widgets_sprites
    
    def __del__(self):
        for i in self.widgets_sprites.sprites():
            i.kill()
        for i in self.widgets_buttons.sprites():
            i.kill()            
        
    
class InfoLable(pygame.sprite.Sprite):
    def __init__(self, x, y, size, board, *groups) -> None:
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.tick = 0
        self.max_tick = 5
        self.board = board
        self.size = size
        self.text = Text(text="", color=(255, 0, 0)).get_surf()
        surf = pygame.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        self.image = surf
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.create()
        self.isChange = True
        
    def set_text(self, text):
        self.text = text
        
    def create(self):
        pass
    
    
class WeaponLabel(InfoLable):
    def create(self):
        self.backgroud = load_image("ui/menu_background.png")
        self.backgroud_dark = load_image("ui/menu_background_dark.png")
        
        self.backgroud = pygame.transform.scale(self.backgroud, (self.size[0] - 10, self.size[1] - 10))
        self.backgroud_dark = pygame.transform.scale(self.backgroud_dark, (self.size[0], self.size[1]))

        # self.backgroud_dark.blit(self.backgroud, (10, 10))
        
        self.image.blit(self.backgroud_dark, (0, 0))
        self.image.blit(self.backgroud, (0, 0))
    
    def set_text(self):
        font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 20)
        self.name = Text(text=f"{self.board.player.weapon.name}", color=(255, 255, 150), font=font).get_surf()
        font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 25)
        self.damage = Text(text=f"Damage: {self.board.player.weapon.damage}", color=(255, 255, 255), font=font).get_surf()
    
    def update(self):
        if self.isChange:
            self.set_text()
            self.image.blit(self.backgroud_dark, (0, 0))
            self.image.blit(self.backgroud, (0, 0))
            text_size = self.name.get_size()
            self.image.blit(self.name, ((self.size[0] - text_size[0]) / 2, 15))
            text_size = self.damage.get_size()
            self.image.blit(self.damage, ((self.size[0] - text_size[0]) / 2, 170))
            w = pygame.transform.scale(self.board.player.weapon.image, ((self.size[0] - 10) / 2 * 0.7, (self.size[1] - 10) * 0.8))
            w = pygame.transform.rotate(w, -90)
            self.image.blit(w, (25, 65))
            self.isChange = False
        
        
class HealtLable(InfoLable):
    def set_text(self, text):
        font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 20)
        self.text = Text(text=f"{text} / {self.board.get_player().max_hp}", color=(255, 55, 55), font=font).get_surf()
        
    def create(self):
        self.backgroud = load_image("ui/menu_background.png")
        self.backgroud_dark = load_image("ui/menu_background_dark.png")
        
        self.backgroud = pygame.transform.scale(self.backgroud, (self.size[0] - 10, self.size[1] - 10))
        self.backgroud_dark = pygame.transform.scale(self.backgroud_dark, (self.size[0], self.size[1]))
        
        self.image.blit(self.backgroud_dark, (0, 0))
        self.image.blit(self.backgroud, (0, 0))
        
        self.healt = load_image(r"ui\ui_heart_full.png")
        self.healt = pygame.transform.scale(self.healt, (40, 40))
        
    def update(self):
        if self.isChange:
            self.set_text(str(self.board.get_player().hp if self.board.get_player().hp > 0 else 0))
            text_size = self.text.get_size()
            self.image.blit(self.backgroud_dark, (10, 10))
            self.image.blit(self.backgroud, (0, 0)) 
            
            self.image.blit(self.text, (60 + 25 - 10, (self.size[1] - 10 - text_size[1]) / 2))
            self.image.blit(self.healt, (10 + 25, (self.size[1] - 40) / 2 - 5))
            self.isChange = False
        

class EnamyInfoLabel(pygame.sprite.Sprite):
    def __init__(self, enemy, board, *groups) -> None:
        super().__init__(*groups)
        if board.enenmy_info_label:
            self.kill()
        else:
            board.enenmy_info_label = True
            
        self.size = 90, 45
        self.coords = enemy.coords
        self.enemy = enemy
        self.board = board
        self.text = None
        
        
        self.rect = pygame.Rect(self.coords[0] * board.cell_size + self.board.left - (self.size[0] - board.cell_size) / 2,
                                self.coords[1] * board.cell_size + self.board.top - self.size[1],
                                self.size[0], self.size[1]
                                )
        self.crate_image()
        
    def set_text(self, text):
        font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 20)
        self.text = Text(text=f"{text}", color=(255, 55, 55), font=font).get_surf()
        
    def crate_image(self):
        self.surf = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA, 32)
        backgroud = load_image("ui/menu_background.png")
        backgroud = pygame.transform.scale(backgroud, (self.size[0], self.size[1]))
        healt = load_image(r"ui\ui_heart_full.png")
        healt = pygame.transform.scale(healt, (40, 40))
        self.surf.blit(backgroud, (0, 0))
        self.surf.set_alpha(200)
        self.image = self.surf.copy()
        self.surf.blit(healt, (10, (self.size[1] - 40) / 2))
        
    def update(self) -> None:
        self.set_text(str(max(self.enemy.hp, 0)))
        text_size = self.text.get_size()
        self.image = self.surf.copy()
        self.image.blit(self.text, (60, (self.size[1] - text_size[1]) / 2))    
        
        if self.coords != get_cell_clicked(self.board, pygame.mouse.get_pos()) or type(self.board.board[self.coords[1]][self.coords[0]]) != type(self.enemy):
            self.kill()
            self.board.enenmy_info_label = False
            

class StageLable(InfoLable):
    def set_text(self, text):
        font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 20)
        self.text = Text(text=f"{text}", color=(200, 200, 200), font=font).get_surf()
        
    def create(self):
        self.backgroud = load_image("ui/menu_background.png")
        self.backgroud_dark = load_image("ui/menu_background_dark.png")
        
        self.backgroud = pygame.transform.scale(self.backgroud, (self.size[0] - 10, self.size[1] - 10))
        self.backgroud_dark = pygame.transform.scale(self.backgroud_dark, (self.size[0], self.size[1]))
        
        self.image.blit(self.backgroud_dark, (0, 0))
        self.image.blit(self.backgroud, (0, 0))
        
    def update(self):
        if self.isChange:
            self.set_text(str(" - ".join(map(str, self.board.info.stage))))
            text_size = self.text.get_size()
            self.image.blit(self.backgroud_dark, (10, 10))
            self.image.blit(self.backgroud, (0, 0)) 
            self.image.blit(self.text, (94, 4))
            
            self.isChange = False


def get_cell_clicked(board, pos):
    width, height = board.width * board.cell_size, board.height * board.cell_size
    if board.left < pos[0] < board.left + width:
        if board.top < pos[1] < board.top + height:
            cell_coords = (pos[0] - board.left) // board.cell_size, (pos[1] - board.top) // board.cell_size
            return cell_coords
    return None