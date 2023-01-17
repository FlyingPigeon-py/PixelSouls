from math import inf
import pygame
import os
import sys
import random

from entity import *
from game_lib2 import *
from game_lib import *
from dbmanager import *


def make_a_move(board):
    if board.move_list:
        for i in board.move_list:
            x_p, y_p = i.get_move_d()
            
            velocity = 5
            
            x = 0
            y = 0

            if x_p == 0:
                pass
            elif x_p < 0:
                x = min(int(velocity), abs(x_p))
                i.move_d = (x_p + x, y)
                x = -x
            elif x_p > 0:
                x = min(int(velocity), x_p)
                i.move_d = (x_p - x, y)
            if y_p < 0:
                y = min(int(velocity), abs(y_p))
                i.move_d = (x, y_p + y)
                y = -y
            elif y_p > 0:
                y = min(int(velocity), y_p)
                i.move_d = (x, y_p - y)
            i.move_rect(x, y)

            if i.move_d == (0, 0):
                board.move_list.remove(i)           
                if board.get_player().get_coords() == board.get_escape().get_coords():
                    next_board() 

def make_attack(board, game_sound, text, effects):
    if not board.move_list or board.get_player().isAttack:
        for i in board.attack_list:
            if board.attack_list:
                x_p, y_p = i.move_a
                
                velocity = 5
                
                x = 0
                y = 0

                if x_p == 0:
                    pass
                elif x_p < 0:
                    x = min(int(velocity), abs(x_p))
                    i.move_a= (x_p + x, y)
                    x = -x
                elif x_p > 0:
                    x = min(int(velocity), x_p)
                    i.move_a = (x_p - x, y)
                if y_p < 0:
                    y = min(int(velocity), abs(y_p))
                    i.move_a = (x, y_p + y)
                    y = -y
                elif y_p > 0:
                    y = min(int(velocity), y_p)
                    i.move_a = (x, y_p - y)
                i.move_rect(x, y)

                if i.move_a == (0, 0):
                    
                    for obj in i.obj_att:
                        try:
                            obj.take_hit(game_sound, text, effects)    
                        except Exception:
                            pass
                    i.isAttak = False
                    board.attack_list.remove(i)
                    i.move_d = i.move_a_r
                    board.add_in_move_list(i)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.move_list = []
        self.attack_list = []
        self.game_sound = game_sound
        self.effects = effects
        self.player = None
        self.info = info
        self.enenmy_info_label = False
        self.healt_bar = HealtLable(20, 20, (250, 45), self, ui)
        self.weapon_bar = WeaponLabel(20, 100, (250, 250), self, ui)
        self.stage_bar = StageLable(20, 100 + 100 - 65 + 250, (250, 45), self, ui)
        
    def set_player(self, player):
        self.player = player

    def add_in_attack_list(self, obj):
        self.attack_list.append(obj)

    def add_in_move_list(self, obj):
        self.move_list.append(obj)

    def get_player(self):
        return self.player

    def get_escape(self):
        return self.escape

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generation_board()
        
    def generation_board(self):        
        LvG = LevelGenerator(self)
        LvG.load_preset()
        w, h = LvG.get_size_board()
        
        self.width = w
        self.height = h
        self.top = (size[1] - (self.height * self.cell_size)) // 2
        self.left = (size[0] - (self.width * self.cell_size)) // 2  
        if not self.player:
            self.player = Player(0, 0, self, game_sound, all_sprites)
        
        self.floor = LvG.fill_floor(floor) 
        self.board = LvG.fill_props(all_sprites, enemys, esc, props)
        
        self.items = LvG.fill_items(items)
        
        self.player.reset_pos()
    
    def render(self, screen):
        # for y in range(self.height):
        #     for x in range(self.width):
        #         pygame.draw.rect(screen, (30, 30, 30), (
        #         x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
        #         self.cell_size), 1)
        pass

    def get_cell_clicked(self, pos):
        width, height = self.width * self.cell_size, self.height * self.cell_size
        if self.left < pos[0] < self.left + width:
            if self.top < pos[1] < self.top + height:
                cell_coords = (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
                self.on_clicke(cell_coords[::-1])
                return cell_coords
        return None   
    
    def get_cell(self, pos):
        pass
        width, height = self.width * self.cell_size, self.height * self.cell_size
        if self.left < pos[0] < self.left + width:
            if self.top < pos[1] < self.top + height:
                cell_coords = (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
                self.check_next_step(cell_coords[::-1])
                return cell_coords
        return None

    def check_next_step(self, cell_coords):
        if not info.play_stop and type(info.play_end) == bool:
            y, x = cell_coords
            x_p, y_p = self.player.get_coords()
            if type(self.board[y][x]) == Escape:
                cursor_img = pygame.transform.scale(load_image("cursor/crosshair_2_1.png"), (20, 20))
            elif type(self.board[y][x]) == Void:
                if [x, y] in get_round_coords(x_p, y_p):
                    cursor_img = pygame.transform.scale(load_image("cursor/crosshair_2.png"), (20, 20))
                else:
                    cursor_img = pygame.transform.scale(load_image("cursor/crosshair_3.png"), (20, 20))
            elif issubclass(type(self.board[y][x]), Enemy):
                cursor_img = pygame.transform.scale(load_image("cursor/crosshair_1.png"), (20, 20))
                EnamyInfoLabel(self.board[y][x], self, ui)
            else:
                cursor_img = pygame.transform.scale(load_image("cursor/crosshair_2_1.png"), (20, 20))
        elif info.play_stop or not type(info.play_end) == bool:
            cursor_img = pygame.transform.scale(load_image("cursor/crosshair_3.png"), (20, 20))
        cur.image = cursor_img   

    def on_clicke(self, cell_coords):
        x_p, y_p = self.player.get_coords()
        y, x = cell_coords
        
        if [x, y] in get_round_coords(x_p, y_p):
            if type(self.board[y][x]) == Void or type(self.board[y][x]) == Escape:
                if x_p - 1 == x and y_p == y:
                    self.player.move("left", self)
                elif x_p + 1 == x and y_p == y:
                    self.player.move("right", self)
                elif x_p == x and y_p == y + 1:
                    self.player.move("up", self)
                elif x_p == x and y_p == y - 1:
                    self.player.move("down", self)
                if type(self.board[y][x]) == Void:
                    update()

            elif issubclass(type(self.board[y][x]), Enemy):

                enemy = self.board[y][x]
                
                if x_p - 1 == x and y_p == y:
                    direction = "left"
                elif x_p + 1 == x and y_p == y:
                    direction = "right"
                elif x_p == x and y_p == y + 1:
                    direction = "up"
                elif x_p == x and y_p == y - 1:
                    direction = "down"

                if enemy.get_hp() - self.player.get_damage() <= 0:
                    # enemy.damage_take(self.player.get_damage(), effects)
                    # enemy.take_hit(game_sound, effects, text)
                    self.player.attack(enemy, direction, effects, go_move=False)
                    self.player.move(direction, self)
                    game_sound.sound_hit_slime.play()
                    self.player.isAttack = False
                    self.board[y][x] = Void()      
                                  
                elif enemy.get_hp() - self.player.get_damage() > 0:
                    self.player.attack(enemy, direction, effects)
                    
                update()         
                


      

def update():
    global count, isMenu, isPlay, board
    count += 1
          
    board.player.apply_effects()   
    
    for i in enemys.sprites():
        i.apply_effects()      
          
    for i in enemys.sprites():
        if not i.freeze:
            i.next_action()
        

def game_draw():
    board.get_cell(pygame.mouse.get_pos())
    
    # screen.fill((0, 0, 0))
    screen.fill((26, 13, 13))
    
    floor.draw(screen)
    board.render(screen)
    items.draw(screen)
    enemys.draw(screen)
    esc.draw(screen)
    all_sprites.draw(screen)
    effects.draw(screen)    
    props.draw(screen)  
    text.draw(screen)
    ui.draw(screen)
    
    
    if not info.play_stop and type(info.play_end) == bool:
        items.update() 
        enemys.update()
        all_sprites.update() 
        effects.update()
        text.update()
        ui.update()
    s = 0
    # s += len(ui.sprites())
    # s += len(floor.sprites())
    # s += len(enemys.sprites())
    # s += len(esc.sprites())
    # s += len(all_sprites.sprites())
    # s += len(props.sprites())
    s += len(effects.sprites())
    # s += len(text.sprites())
    # print(s)
    
def start_board():
    clean()
    global board
    board = Board(1, 1)
    player.reset(board)
    board.set_player(player)
    board.set_view(100, 100, 75)    
    
def next_board():
    global board, player
    player = board.get_player()
    if info.stage[1] == 9:
        info.stage[1] = 0
        info.stage[0] += 1
    else:
        info.stage[1] += 1
        
    if info.stage == [2, 0]:
        info.isPlay = True
        info.play_end = True
        board.player.isAlive = False
        info.end_text = "You are Win"
    else:
        info.IsTransition = True

    
def clean():
    elements = [enemys, floor, effects, props, text, esc, props, items, ui]
    for i in elements:
        for j in i.sprites():
            j.kill()
                    
 
                       
def generate_board():
    global all_sprites, floor, enemys, effects, board,count, isPlay, isMenu, text, props
    global ui, esc, items
    all_sprites = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    enemys = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    text = pygame.sprite.Group()
    props = pygame.sprite.Group()
    esc = pygame.sprite.Group()
    items = pygame.sprite.Group()
    ui = pygame.sprite.Group()
    
    count = 0     
    board = Board(1, 1)
    board.set_view(100, 100, 75)
    
    info.kills = 0
    info.score = 0
    
    info.isPlay = True
    info.isMenu = False
    info.setting_w.direction = False
    info.isSetting = False
    
    info.menu_w.move(300, 0)
    info.menu_w.direction = True
        
    
    
def pause():
    global pause_w, dark
    dark = 0
    info.play_stop = not info.play_stop
    if info.play_stop:
        game_sound.sound_pause_off.play()
        pause_w = Widget((1200 - 300) / 2, (700 - 450) / 2, (300, 450))
        buttons = pause_w.get_widgets_buttons()
        other = pause_w.get_widgets_sprites()
        
        Image((350, 500), (pause_w.get_center_w(350), pause_w.get_center_h(500)), "ui/menu_background_dark.png", other)    
        Image((300, 450), (pause_w.x, pause_w.y), "ui/menu_background.png", other)
        
        button = Button(buttons, pause_w.get_center_w(192), pause_w.get_center_h(450) + 100, screen, game_sound, game_font)
        button.set_func(lambda: pause())
        button.set_text("Resume")
        
        button = Button(buttons, pause_w.get_center_w(192), pause_w.get_center_h(450) + 200, screen, game_sound, game_font)
        button.set_func(open_close_settings)
        button.set_text("Options")
        
        button = Button(buttons, pause_w.get_center_w(192), pause_w.get_center_h(450) + 300, screen, game_sound, game_font)
        button.set_func(close_game)
        button.set_text("Menu") 
            
        text = Text(0, 0, "PAUSE", (46, 73, 88), 40)
        size = text.get_size()
        
        text.set_x(pause_w.get_center_w(size[0]))
        text.set_y(pause_w.y +15)
        pause_w.add_text(text)
    else:
        game_sound.sound_pause_on.play()
        info.isSetting = False
        del pause_w 
        
def close_game():
    info.play_end = True
    info.play_stop = False
    board.player.isAlive = False
    info.end_text = "Surrendered"
                     
def go_to_menu():
    game_sound.sound_dash.play()
    info.play_end = False
    info.isPlay = False
    info.isMenu = True
    info.play_stop = False    
    info.stage[1] = 0
    info.stage[0] = 0    
    
def game_event():
    global running
    if event.type == pygame.MOUSEBUTTONDOWN and len(board.move_list) == 0 and len(board.attack_list) == 0:
        if not info.play_stop:
            board.get_cell_clicked(pygame.mouse.get_pos())
            
    if event.type == pygame.KEYDOWN:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause()
        if pygame.key.get_pressed()[pygame.K_f]:
            x, y = board.player.get_coords()

            if type(board.items[y][x]) == Chest:
                if board.items[y][x].cur_frame == 4:
                    board.items[y][x].change_item()
           

        
class Backgroud(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__(sprite)   
        
        self.cur_frame = 0
        self.tick_max = 18
        self.tick = 0
        
        x = 0
        y = 0
    
        self.frames = [pygame.transform.scale(load_image(f"background/e74b597961bae8f46a69dbad3633174a.gif_p{i}.png"), (768 * 2, 368 * 2)) for i in range(1, 8)]
        self.image = self.frames[0]
        self.rect = pygame.Rect(x, y, size[0], size[1])

    def update(self):
        if self.tick >= self.tick_max:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.tick = 0
        else:
            self.tick += 1  

class Info:
    def __init__(self) -> None:
        self.play_stop = False
        self.isPlay = False
        self.isMenu = True
        self.running = True
        self.play_end = False
        self.menu_w = None
        self.isSetting = False
        self.setting_w = None
        
        self.isMusic = True
        
        self.isDark = True
        self.IsTransition = False
        self.dark = 0
        
        

        self.end_text = None
        
        self.stage = [0, 0]
        
        self.dbmanager = Manager(r"../Database\db")
        self.vol = self.dbmanager.get_vol()[0][0]
        
        
        self.score = 0
        self.kills = 0
        
def set_vol(o):
    if o == "+":
        info.vol += 10
    elif o == "-":
        info.vol -= 10
        
    if info.vol > 100:
        info.vol = 100
    elif info.vol < 0:
        info.vol = 0
        
    info.dbmanager.set_vol(info.vol)
    
    pygame.mixer.music.set_volume(info.vol / 100)
    
    info.setting_w.text[0].set_text(str(int(info.vol)))
    
        
def create_settings(pos=(100 - 800, (700 - 450) / 2)):
    setting_w = Widget(pos[0], pos[1], (600 - 20, 400))  #850
    if pos == (100 - 800, (700 - 450) / 2):
        setting_w.direction = True
        
    info.setting_w = setting_w
    buttons = setting_w.get_widgets_buttons()
    other = setting_w.get_widgets_sprites()
    
    Image((setting_w.size[0] + 30, setting_w.size[1] + 30), (setting_w.get_center_w(setting_w.size[0] + 30), setting_w.get_center_h(setting_w.size[1] + 30)), "ui/menu_background_dark.png", other)    
    Image((setting_w.size[0], setting_w.size[1]), (setting_w.x, setting_w.y), "ui/menu_background.png", other)
    font = pygame.font.Font(r"../Font\pico-8.ttf", 30)
    
    button = Button(buttons, setting_w.x + 20, setting_w.y + 125 + 20, screen, game_sound, game_font, font=font, scale=(1, 2))
    button.set_func(lambda: set_vol("+"))
    button.set_text(" +")
    
    button = Button(buttons, setting_w.x + 20 + 200, setting_w.y + 125 + 20, screen, game_sound, game_font, font=font, scale=(1, 2))
    button.set_func(lambda: set_vol("-"))
    button.set_text(" -")
    
    button = Button(buttons, setting_w.x + 20 + 200 + 150, setting_w.y + 125 + 20, screen, game_sound, game_font, scale=(2, 2))
    button.set_func(lambda: [pygame.mixer.music.load(rf"../Sounds\Medieval Vol. 2 {random.randint(1, 8)}.mp3"), pygame.mixer.music.play()])
    button.set_text("mix")
    
    button = Button(buttons, setting_w.x + 20, setting_w.y + 300, screen, game_sound, game_font, scale=(2, 2))
    button.set_func(stop_play_music)
    button.set_text("Stop")
        
    button = Button(buttons, setting_w.x + 20 + 200 + 150, setting_w.y + 300, screen, game_sound, game_font)
    button.set_func(open_close_settings)
    button.set_text("Close") 
    
    font = pygame.font.Font(r"../Font\pico-8.ttf", 30)
    vol = Text(0, 0, str(int(info.vol)), (76, 103, 118), 30, font=font)
    
    if len(str(int(info.vol))) > 2:
        vol.set_x(setting_w.x + 20 + 125 - 20)
    else:
        vol.set_x(setting_w.x + 20 + 125)
        
    vol.set_y(setting_w.y + 135 + 20)       
    setting_w.add_text(vol)
    
    text = Text(0, 0, "Options", (76, 103, 118), 40)
    size = text.get_size()
    text.set_x(setting_w.x + 20)
    text.set_y(setting_w.y +15)
    setting_w.add_text(text)
    
    text = Text(0, 0, "Music", (76, 103, 118), 25)
    text.set_x(setting_w.x + 20)
    text.set_y(setting_w.y + 135 - 30) 
    setting_w.add_text(text)
    
    text = Text(0, 0, "Choise", (76, 103, 118), 25)
    text.set_x(setting_w.x + 20 + 350)
    text.set_y(setting_w.y + 135 - 30) 
    setting_w.add_text(text)
    
def stop_play_music():
    info.isMusic = not info.isMusic 
    if info.isMusic:
        info.setting_w.widgets_buttons.sprites()[3].set_text("Stop")
        pygame.mixer.music.unpause()
    else:
        info.setting_w.widgets_buttons.sprites()[3].set_text("Play")
        pygame.mixer.music.pause()
        
def create_menu():
    menu_w = Widget(1200, (700 - 450) / 2, (250, 400))  #850
    
    info.menu_w = menu_w
    buttons = menu_w.get_widgets_buttons()
    other = menu_w.get_widgets_sprites()
    menu_w.backgroud = Backgroud(other)

    Image((menu_w.size[0] + 30, menu_w.size[1] + 30), (menu_w.get_center_w(menu_w.size[0] + 30), menu_w.get_center_h(menu_w.size[1] + 30)), "ui/menu_background_dark.png", other)    
    Image((menu_w.size[0], menu_w.size[1]), (menu_w.x, menu_w.y), "ui/menu_background.png", other)
    Image((800, 800), (300, -150), "background\logo1.png", other)
          
    button = Button(buttons, menu_w.get_center_w(192), menu_w.get_center_h(450) + 125, screen, game_sound, game_font)
    button.set_func(generate_board)
    button.set_text("PLay")
    
    button = Button(buttons, menu_w.get_center_w(192), menu_w.get_center_h(450) + 225, screen, game_sound, game_font)
    button.set_func(open_close_settings)
    button.set_text("Options")
    
    button = Button(buttons, menu_w.get_center_w(192), menu_w.get_center_h(450) + 325, screen, game_sound, game_font)
    button.set_func(lambda: sys.exit())
    button.set_text("Quit") 
        
    text = Text(0, 0, "MENU", (76, 103, 118), 40)
    size = text.get_size()
    
    text.set_x(menu_w.get_center_w(size[0]))
    text.set_y(menu_w.y +15)
    menu_w.add_text(text)
    
def open_close_settings():
    game_sound.sound_dash.play()
    info.isSetting = not info.isSetting
    if info.isSetting:
        if info.play_stop:
            create_settings(((1200 - 600 - 20) / 2, (700 - 450) / 2))
        else:
            create_settings()
        
def play_end_create():
    info.play_end = Widget(0, 0, (1200, 700))
    buttons = info.play_end.get_widgets_buttons()
    other = info.play_end.get_widgets_sprites()
    
    Image((500, 700), (info.play_end.get_center_w(500), info.play_end.get_center_h(700)), "ui/menu_background_dark.png", other)    
    
    Image((450, 650), (info.play_end.get_center_w(450), info.play_end.get_center_h(650)), "ui/menu_background.png", other)
    
    button = Button(buttons, info.play_end.get_center_w(400), info.play_end.get_center_h(450) + 440, screen, game_sound, game_font, scale=(4.1666, 2))
    button.set_func(go_to_menu)
    button.set_text("Menu")
    
    
    font = pygame.font.Font(r"../Font\retro-land-mayhem.ttf", 25)
    Image((400, 140), (info.play_end.get_center_w(400), 140), "ui/menu_background_dark.png", other)
    Image((400, 55), (info.play_end.get_center_w(400), 280 + 20), "ui/menu_background_dark.png", other)    
    Image((400, 55), (info.play_end.get_center_w(400), 420 + 55), "ui/menu_background_dark.png", other)    
    
    text = Text(0, 0, info.end_text, (160, 73, 88), 30)
    size = text.get_size()
    text.set_x(info.play_end.get_center_w(size[0]))
    text.set_y(info.play_end.y + 50)
    info.play_end.add_text(text)
        
    h = 150
    
    field = ["Score:", "Kills:", "Stage:"]
    
    best = info.dbmanager.get_convert()[0][0]
    
    if info.score > best:
        info.dbmanager.set_convert(info.score)
        best = info.score
    
    ident = 411.5
    for i, res in enumerate([info.score, info.kills, " - ".join(map(str, info.stage))]): 
        
        text = Text(0, 0, field[i], (200, 200, 200), 18, font=font)
        size = text.get_size()
        text.set_x(ident)
        text.set_y(info.play_end.y + h)
        info.play_end.add_text(text)
    
        text = Text(0, 0, f"{res}", (255, 200, 200), 18, font=font)
        size = text.get_size()
        text.set_x(1200 - ident - size[0])
        text.set_y(info.play_end.y + h)
        info.play_end.add_text(text)
        
        h += 40               
        
    h += 40
    
    field = ["New items:", "Best score"]
    for i, res in enumerate([2, best]): 
        
        text = Text(0, 0, field[i], (200, 200, 200), 18, font=font)
        size = text.get_size()
        text.set_x(ident)
        text.set_y(info.play_end.y + h)
        info.play_end.add_text(text)
    
        text = Text(0, 0, f"{res}", (255, 255, 200), 18, font=font)
        size = text.get_size()
        text.set_x(1200 - ident - size[0])
        text.set_y(info.play_end.y + h)
        info.play_end.add_text(text)    
        h += 175          
    
def dark_screen(color, alph):
    surf = pygame.Surface((1200, 700), pygame.SRCALPHA, 32)
    surf.fill(color)
    surf.set_alpha(alph)
    screen.blit(surf, (0, 0))
        
if __name__ == '__main__':
    pygame.mixer.init()
    STOPPED_PLAYING = pygame.USEREVENT + 1    
    pygame.mixer.music.set_endevent(STOPPED_PLAYING)
    print(a := random.randint(1, 8))
    pygame.mixer.music.load(rf"../Sounds\Medieval Vol. 2 {a}.mp3")
    pygame.mixer.music.play()
    pygame.init()
    pygame.display.set_caption('PixelSouls')

    clock = pygame.time.Clock()
    fps = 120
    size = 1200, 700
    screen = pygame.display.set_mode(size)
    
    info = Info()
    # running = True
    # play_stop = False
    game_font = FontManager()
    game_sound = GameSounds()
    
    game_sound.sound_dash.play()
    create_menu()
    create_settings()  
    # isPlay = False
    # isMenu = True
    
    velocity = 0
    
    cursor = pygame.sprite.Group()
    sc = pygame.display.set_mode((size[0], size[1]))
    pygame.mouse.set_visible(False)

    cursor_img = load_image("cursor/crosshair_3.png")
    cursor_img = pygame.transform.scale(cursor_img, (20, 20))

    cur = pygame.sprite.Sprite(cursor)
    cur.image = cursor_img
    cur.rect = cur.image.get_rect()
    
    pygame.mixer.music.set_volume(info.vol / 100)
    
    while info.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info.running = False  
            if STOPPED_PLAYING == event.type:
                pygame.mixer.music.load(rf"../Sounds\Medieval Vol. 2 {random.randint(1, 8)}.mp3")
                pygame.mixer.music.play()       
                          
            if info.isPlay and board.get_player().isAlive:
                game_event()
                
            elif info.isMenu:
                info.menu_w.widget_event(event)
                
            elif type(info.play_end) != bool:
                info.play_end.widget_event(event)
                
                
            if info.isSetting:
                info.setting_w.widget_event(event)
                
            if info.play_stop and not info.isSetting:
                pause_w.widget_event(event)
        
        screen.fill((0, 0, 0))
        
        if info.isPlay:
            make_a_move(board) 
            make_attack(board, game_sound, text, effects)        
            game_draw()          
        
        if info.play_end:
            if type(info.play_end) == bool:
                play_end_create()
                info.play_end.move(0, 700)
                game_sound.sound_dash.play()
                dark = 0
                velocity = 0
            else:
                dark_screen((0, 0, 0), dark)
                
                
                if info.play_end.direction:
                    if (info.play_end.y - velocity) < 0:
                        info.play_end.move(0, -info.play_end.y)
                    else:
                        info.play_end.move(0, -velocity)
                    velocity += 5
                    
                if info.play_end.y <= 0:
                    info.play_end.direction = False
                    velocity = 0

                if dark < 150:
                    dark += 5
                    
                info.play_end.draw(screen)
        
        if info.isMenu:
            if not info.isSetting:
                if info.menu_w.x <= 900:
                    info.menu_w.direction = False
                    velocity = 0            
                    
                if info.menu_w.direction:
                    if (info.menu_w.x - velocity) < 900:
                        info.menu_w.move(900 - info.menu_w.x, 0)
                    else:
                        info.menu_w.move(-velocity, 0)
                    
                    velocity += 5        
            info.menu_w.draw(screen)
            
        if info.play_stop:
            dark_screen((0, 0, 0), dark)
            if not info.isSetting:
                pause_w.draw(screen)
            
            if dark < 150:
                dark += 5  
                
        if info.isSetting:  
            if info.setting_w.direction and info.isMenu:
                if (info.setting_w.x + velocity) >= 100:
                    info.setting_w.move(100 - info.setting_w.x, 0)
                else:
                    info.setting_w.move(velocity, 0)
                velocity += 25  
                    
            if info.setting_w.x >= 100 and info.isMenu:
                info.setting_w.direction = False
                velocity = 0                      
                
            info.setting_w.draw(screen)   
            
        if not info.play_stop and not info.isSetting and info.IsTransition:
            dark_screen((0, 0, 0), info.dark)  
                    
            if info.isDark:
                info.dark += 15
            else:
                info.dark -= 15
            
            if info.dark >= 255:
                info.isDark= False
                start_board()
            if info.dark <= 0:
                info.dark = 0
                info.isDark= True
                info.IsTransition = False
        
        if pygame.mouse.get_focused():
            mos_pos = pygame.mouse.get_pos()
            cur.rect.x, cur.rect.y = mos_pos
            cursor.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
        
    pygame.quit()
