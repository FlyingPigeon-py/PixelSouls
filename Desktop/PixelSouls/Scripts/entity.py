import pygame

from game_lib2 import *
from items import *
from ability import *
     
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, board, game_sound, group):
        super().__init__(group)
        
        self.weapon = Sword(self)

        self.move_d = (0, 0)
        
        self.move_a = (0, 0)
        self.move_a_r = (0, 0)
        
        self.obj_att = None
        
        self.cur_frame = 0
        self.tick_max = 10
        self.tick = 0

        self.board = board
        self.game_sound = game_sound

        self.right = True
        
        self.isAttack = False
        self.max_hp = 20
        self.hp = 20
        self.damage = 0
        self.isAlive = True
        self.time_after_death = 120
        self.coords = (x, y)
        
        self.effects = []
        
        x = x * board.cell_size + board.left
        y = y * board.cell_size + board.top
        
        
        self.frames = [pygame.transform.scale(load_image(f"entity/knight_idle_anim_f{i}.png"), (board.cell_size, board.cell_size)) for i in range(6)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        image = self.frames[0]
        
        self.frames_m = [pygame.transform.scale(load_image(f"entity/knight_run_anim_f{i}.png"), (board.cell_size, board.cell_size)) for i in range(6)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]
        
        self.death_f = [pygame.transform.scale(load_image(f"entity/knight_death_anim_f{i}.png"), (board.cell_size, board.cell_size)) for i in range(6)]
        
        self.image1 = pygame.transform.scale(image, (board.cell_size, board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x -5, y -5, board.cell_size, board.cell_size)
        # self.image = pygame.Surface((board.cell_size, board.cell_size),
        #                             pygame.SRCALPHA, 32)
        # pygame.draw.circle(self.image, pygame.Color("Blue"),
        #                    (board.cell_size / 2, board.cell_size / 2), radius)

    def del_effects(self):
        for i in self.effects:
            if type(i) == Freeze:
                self.board.game_sound.sound_ice_break.play()
                i.stage = 3
            else:
                if type(i) == Poison:
                    self.board.game_sound.sound_poison_break.play()
                i.kill()

    def add_effect(self, effect):
        replace = False
        for i in self.effects:
            if type(i) == type(effect):
                effect.kill()
                replace = True

        if not replace:
            self.effects.append(effect)

    def apply_effects(self):
        death_list = []
        
        for effect in self.effects:
            if effect.steps <= 0:
                death_list.append(effect)
                if type(effect) == Poison:
                    self.board.game_sound.sound_poison_break.play()
                
        for i in death_list:
            del self.effects[self.effects.index(i)]
            i.kill()
                
        for effect in self.effects:
            effect.action()
            if type(effect) != Freeze:
                FlyNumber(effect.damage, self, self.board, self.board.effects)
            
            if effect.stage == 3:
                self.freeze = False 
    
    def reset(self, board):
        self.board = board
        self.move_d = (0, 0)
        
        self.move_a = (0, 0)
        self.move_a_r = (0, 0)
        
        self.obj_att = None
        self.right = True
        
        self.isAttack = False       
        
    
    def update(self):
        
        if self.isAlive:
            if self.tick >= self.tick_max:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.right and self.move_d == (0, 0):
                    self.image = self.frames[self.cur_frame]
                elif not self.right and self.move_d == (0, 0):
                    self.image = self.frames_r[self.cur_frame] 
                    
                elif self.right and self.move_d != (0, 0):
                    self.image = self.frames_m[self.cur_frame]
                elif not self.right and self.move_d != (0, 0):
                    self.image = self.frames_r_m[self.cur_frame]
                    
                self.tick = 0
            else:
                self.tick += 1
        else:
            
            
            if self.cur_frame != 6:
                if self.tick >= self.tick_max:
                    self.image = self.death_f[self.cur_frame]
                    self.cur_frame += 1
                    self.tick = 0
                else:
                    self.tick += 1
                    
            if self.time_after_death > 0:
               self.time_after_death -= 1
            else:
                self.board.info.isPlay = True
                self.board.info.play_end = True
            
    def reset_pos(self):
        x = self.coords[0] * self.board.cell_size + self.board.left
        y = self.coords[1] * self.board.cell_size + self.board.top
        self.rect.x = x
        self.rect.y = y
        
    def get_move_d(self):
        return self.move_d
    
    def take_hit(self, game_sound, text, effects):
        game_sound.sound_hit_player.play()
        self.image = pygame.transform.scale(load_image(f"entity/knight_take_damage.png"), (self.board.cell_size, self.board.cell_size))
        Hit(self, self.board, effects)
    
    def attack(self, obj, direction, group, go_move=True):
        self.isAttack = True
        obj_coords = obj.get_coords()
        self.board.add_in_attack_list(self)
        self.obj_att = self.weapon.give_damage(direction)
        
        
        if go_move:
            if direction == "left":
                self.move_a = (-40, 0)
            elif direction == "right":
                self.move_a = (40, 0)            
            elif direction == "up":
                self.move_a = (0, -40)      
            elif direction == "down":
                self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])

    def death(self):
        self.isAlive = False
        self.game_sound.sound_game_over.play()
        self.cur_frame = 0
        AfterDead(self, self.board, self.board.effects)

    def damage_take(self, damage, group=None):
        self.hp -= damage
        self.board.healt_bar.isChange = True
        if self.hp <= 0:
            self.death()

    def get_damage(self):
        return self.damage + self.weapon.damage

    def take_healt(self, count):
        self.hp += count
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.board.healt_bar.isChange = True
    
    def get_hp(self):
        return self.hp

    def get_coords(self):
        return self.coords

    def move_rect(self, x, y):
        self.rect = self.rect.move(x, y)

    def move(self, vec, board):
        self.game_sound.sound_dash.play()
        self.board.board[self.coords[1]][self.coords[0]] = Void()
        
        if vec == "left":
            self.coords = (self.coords[0] - 1, self.coords[1])
            x, y = -board.cell_size, 0
            if self.right:
                self.image1 = pygame.transform.flip(self.image1, True, False)
                self.image = self.image1
                self.right = False
        elif vec == "right":
            self.coords = (self.coords[0] + 1, self.coords[1])
            x, y = board.cell_size, 0
            if not self.right:
                self.image1 = pygame.transform.flip(self.image1, True, False)
                self.image = self.image1
                self.right = True
        elif vec == "up":
            self.coords = (self.coords[0], self.coords[1] - 1)
            x, y = 0, -board.cell_size
        elif vec == "down":
            self.coords = (self.coords[0], self.coords[1] + 1)
            x, y = 0, board.cell_size
        self.move_d = (x, y)
        board.add_in_move_list(self)
        

class FlyNumber(pygame.sprite.Sprite):
    def __init__(self, damage, obj, board, group, color=(255, 50, 50, 0)):
        super().__init__(group)   
        
        self.damage = damage
        
        self.obj = obj
        self.board = board
        self.cur_frame = 0
        self.tick_max = 6
        self.tick = 0
        
        self.color = color
        
        self.image = pygame.Surface((self.board.cell_size, self.board.cell_size),
                                    pygame.SRCALPHA, 32)

        self.draw()
        self.rect = pygame.Rect(self.obj.get_coords()[0] + self.board.cell_size, self.obj.get_coords()[0] + self.board.cell_size, self.board.cell_size, self.board.cell_size)
        self.rect.x = self.obj.get_coords()[0] * self.board.cell_size + board.left
        self.rect.y = self.obj.get_coords()[1] * self.board.cell_size + board.top - self.board.cell_size / 2
 
 
        self.alpha = 255
        
        self.step = (self.board.cell_size / 2) * 0.6
        
        self.step_alpha = 255 / (self.tick_max / 2)
        
    def draw(self):
        f = pygame.font.Font(r"../Font\pico-8.ttf", 15)
        text = f.render(f"-{self.damage}", True, self.color)
        p = text.get_rect(center=(self.obj.get_coords()[0] + self.board.cell_size, self.obj.get_coords()[1] + self.board.cell_size))
        p.x -= self.board.cell_size / 2
        p.y -= self.board.cell_size / 2
        self.dir = random.randint(0, 1)
        self.dit_step = random.randint(-1, 1)
        self.image.blit(text, p)
        
        
    def update(self):
        if self.tick >= 100:
            self.kill()
        else:
            self.alpha -= self.step_alpha
            if self.tick >= 50:
                self.image.set_alpha(self.alpha)
            
            if self.tick < 25:
                self.rect.x += self.dit_step            
                self.rect.y -= self.step
                
            self.step /= 4
            self.tick += 1
            
            
class Hit(pygame.sprite.Sprite):
    def __init__(self, obj, board, group):
        super().__init__(group)   
        
        self.obj = obj
        
        self.cur_frame = 0
        self.tick_max = 3
        self.tick = 0
        
        self.frames = [pygame.transform.scale(load_image(f"effects/other/hit_effect_anim_f{i}.png"), (board.cell_size - 30, board.cell_size - 30)) for i in range(3)]
        self.image = self.frames[0]
        self.rect = pygame.Rect(-100, -100, board.cell_size - 30, board.cell_size - 30)

    def update(self):
        self.rect.x = self.obj.rect.x + 15
        self.rect.y = self.obj.rect.y + 15
        
        if self.cur_frame == 3:
            self.kill()
        
        if self.tick >= self.tick_max:
            self.image = self.frames[self.cur_frame]
            self.cur_frame += 1
            self.tick = 0
        else:
            self.tick += 1
            
            
class AfterDead(pygame.sprite.Sprite):
    def __init__(self, obj, board, group):
        super().__init__(group)   
        
        self.obj = obj
        
        self.cur_frame = 0
        self.tick_max = 6
        self.tick = 0
        
        self.frames = [pygame.transform.scale(load_image(f"effects/other/enemy_afterdead_explosion_anim_f{i}.png"), (board.cell_size + 15, board.cell_size + 15)) for i in range(3)]
        self.image = self.frames[0]
        self.rect = pygame.Rect(-100, -100, board.cell_size + 15, board.cell_size + 15)

    def update(self):
        self.rect.x = self.obj.rect.x - 15
        self.rect.y = self.obj.rect.y - 15
        
        if self.cur_frame == 3:
            self.kill()
        
        if self.tick >= self.tick_max:
            self.image = self.frames[self.cur_frame]
            self.cur_frame += 1
            self.tick = 0
        else:
            self.tick += 1
            
            
class Props(pygame.sprite.Sprite):
    def __init__(self, coords, pos_i, size, image, board, group):
        super().__init__(group)
        image = pygame.transform.scale(image, (size[0], size[1]))
    
        self.coords = coords
        self.image = image
        self.rect = pygame.Rect(pos_i[0], pos_i[1], board.cell_size, board.cell_size)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, board, group):
        super().__init__(group)
        
        self.board = board        
        self.coords = (x, y)        
        

        self.damage = None
        self.hp = None
        self.hp_max = None
        
        self.freeze = False
                
        self.cur_frame = 0
        self.tick_max = 10
        self.tick = 0
        
        self.create_sprite(x, y)
        self.set_stats()

        self.move_d = (0, 0)
        
        self.move_attack = (0, 0)
        self.move_attack_r = (0, 0)
        self.obj_att = []
        
        self.effects = []
        
        self.right = True 
        
    def get_healt(self, points):
        self.hp += points
        print(self.hp_max)
        if self.hp >= self.hp_max:
            self.hp = self.hp_max
        FlyNumber(points, self, self.board, self.board.effects, color=(50, 255, 50, 0))

        
    def add_effect(self, effect):
        replace = False
        for i in self.effects:
            if type(i) == type(effect):
                effect.kill()
                replace = True

        if not replace:
            self.effects.append(effect)

    def apply_effects(self):
        death_list = []
        
        for effect in self.effects:
            if effect.steps <= 0:
                death_list.append(effect)
                if type(effect) == Poison:
                    self.board.game_sound.sound_poison_break.play()
                
        for i in death_list:
            del self.effects[self.effects.index(i)]
            i.kill()
                
        for effect in self.effects:
            effect.action()
            if type(effect) != Freeze:
                FlyNumber(effect.damage, self, self.board, self.board.effects)
            
            if effect.stage == 3:
                self.freeze = False 
                
    def update(self):
        if not self.freeze:
            if self.tick >= self.tick_max:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.right and self.move_d == (0, 0):
                    self.image = self.frames[self.cur_frame]
                elif not self.right and self.move_d == (0, 0):
                    self.image = self.frames_r[self.cur_frame]
                elif self.right and self.move_d != (0, 0):
                    self.image = self.frames_m[self.cur_frame]
                elif not self.right and self.move_d != (0, 0):
                    self.image = self.frames_r_m[self.cur_frame]

                self.tick = 0
            else:
                self.tick += 1

    def get_move_d(self):
        return self.move_d

    def take_hit(self, game_sound, group, group_t):
        if not self.freeze:
            self.image = pygame.transform.scale(load_image(f"entity/slime_take_damage.png"), (self.board.cell_size, self.board.cell_size))
        FlyNumber(self.dam, self, self.board, group_t)
        Hit(self, self.board, group)

        game_sound.sound_hit_slime.play()

    def del_effects(self):
        for i in self.effects:
            if type(i) == Freeze:
                self.board.game_sound.sound_ice_break.play()
                i.stage = 3
            else:
                if type(i) == Poison:
                    self.board.game_sound.sound_poison_break.play()
                i.kill()

    def damage_take(self, damage, group):
        self.dam = damage
        self.hp -= damage
        if not self.isAlive():
            AfterDead(self, self.board, group)
            self.board.board[self.coords[1]][self.coords[0]] = Void()
            self.del_effects()
            self.kill()
            self.board.info.score += self.points
            self.board.info.kills += 1

    def isAlive(self):
        return True if self.hp > 0 else False

    def get_hp(self):
        return self.hp

    def get_damage(self):
        return self.damage

    def set_stats(self):
        self.hp = None
        self.damage = None

    def create_sprite(self, x, y):
        pass
    
    def get_coords(self):
        return self.coords

    def move_rect(self, x, y):
        self.rect = self.rect.move(x, y)

    def move(self, vec, board):
        board.board[self.coords[1]][self.coords[0]] = Void()
        if vec == "left":
            self.coords = (self.coords[0] - 1, self.coords[1])
            x, y = -board.cell_size, 0
            if self.right:
                self.image1 = pygame.transform.flip(self.image1, True, False)
                self.image = self.image1
                self.right = False
        elif vec == "right":
            self.coords = (self.coords[0] + 1, self.coords[1])
            x, y = board.cell_size, 0
            if not self.right:
                self.image1 = pygame.transform.flip(self.image1, True, False)
                self.image = self.image1
                self.right = True
        elif vec == "up":
            self.coords = (self.coords[0], self.coords[1] - 1)
            x, y = 0, -board.cell_size
        elif vec == "down":
            self.coords = (self.coords[0], self.coords[1] + 1)
            x, y = 0, board.cell_size

        board.board[self.coords[1]][self.coords[0]] = self

        self.move_d = (x, y)

        board.add_in_move_list(self)


class Slime(Enemy):
    def set_stats(self):
        self.hp = 4
        self.hp_max = 4
        self.damage = 1
        self.points = 150
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            self.board.get_player().damage_take(self.damage)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/slime_idle_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(6)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        
        self.frames_m = [pygame.transform.scale(load_image(f"entity/slime_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(6)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
        
        
class Swampy(Enemy):
    def set_stats(self):
        self.hp_max = 2
        self.hp = 2
        self.damage = 2
        self.tick_max = 20
        self.points = 100
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            self.board.get_player().add_effect(Poison(self.board.get_player(), 2, self.board.effects))
            # self.board.get_player().damage_take(self.damage)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/swampy_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        
        self.frames_m = [pygame.transform.scale(load_image(f"entity/swampy_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
        
        
class NormalSwampy(Enemy):
    def set_stats(self):
        self.hp = 2
        self.hp_max = 2
        self.damage = 2
        self.tick_max = 20
        self.points = 50
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            # self.board.get_player().damage_take(self.damage)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/muddy_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        
        self.frames_m = [pygame.transform.scale(load_image(f"entity/muddy_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
        
class Goblin(Enemy):
    def set_stats(self):
        self.hp = 2
        self.hp_max = 3
        self.damage = 0
        self.tick_max = 20
        self.points = 50
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)
        self.damage = 0
        
        for pos in get_round_coords(x, y) + get_corner_coords(x, y):
            try:
                if type(self.board.board[pos[1]][pos[0]]) in (Goblin, GoblinShaman, MaskedGoblin):
                    self.damage += 1
            except:
                pass

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/orc_warrior_idle_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        self.frames_m = [pygame.transform.scale(load_image(f"entity/orc_warrior_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
        
        
class GoblinShaman(Enemy):
    def set_stats(self):
        self.hp = 2
        self.hp_max = 2
        self.damage = 0
        self.tick_max = 20
        self.points = 50
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])

    def check(self, step):
        try:
            if type(self.board.board[step[0]][step[1]]) == Void and\
               step[0] >= 0 and step[1] >= 0 and step[0] <= self.board.width and step[1] <= self.board.height:
                return True
            else:
                return False
        except IndexError:
            pass
      
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)
        self.damage = 0
        
        walk = True
        
        for pos in get_round_coords(x, y) + get_corner_coords(x, y):
            try:
                if issubclass(type(self.board.board[pos[1]][pos[0]]), Enemy):
                    if pos[1] >= 0 and pos[0] >= 0:
                        self.board.board[pos[1]][pos[0]].get_healt(1)
                        walk = False
            except Exception as e:
                pass
        if walk:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction and len(direction) > 1:
                self.move(direction[0], self.board)


    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/orc_shaman_idle_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        self.frames_m = [pygame.transform.scale(load_image(f"entity/orc_shaman_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)

        
class Stone(Enemy):
    def set_stats(self):
        self.hp = 10
        self.hp_max = 10
        self.damage = 2
        self.tick_max = 20
        self.points = 50
        self.step = 1
        self.max_step = 2
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            self.step = 0
        else:
            if self.step == 2:
                direction = get_path(self.board, self.coords, self.board.player.get_coords())
                if direction:
                    self.move(direction[0], self.board)
            
            if self.step > 2:
                self.step = 1
                
        self.step += 1

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        self.frames = [pygame.transform.scale(load_image(f"entity/big_zombie_idle_anim_f{i}.png"), (self.board.cell_size + 10, self.board.cell_size + 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        self.frames_m = [pygame.transform.scale(load_image(f"entity/big_zombie_run_anim_f{i}.png"), (self.board.cell_size + 10, self.board.cell_size + 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x - 15, y - 15, self.board.cell_size, self.board.cell_size)


class Ogr(Enemy):
    def set_stats(self):
        self.hp = 5
        self.hp_max = 5
        self.damage = 3
        self.tick_max = 20
        self.points = 50
        self.step = 1
        self.max_step = 2
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            self.step = 0
        else:
            if self.step == 2:
                direction = get_path(self.board, self.coords, self.board.player.get_coords())
                if direction:
                    self.move(direction[0], self.board)
            
            if self.step > 2:
                self.step = 1
                
        self.step += 1

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        self.frames = [pygame.transform.scale(load_image(f"entity/ogre_idle_anim_f{i}.png"), (self.board.cell_size + 10, self.board.cell_size + 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        self.frames_m = [pygame.transform.scale(load_image(f"entity/ogre_run_anim_f{i}.png"), (self.board.cell_size + 10, self.board.cell_size + 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x - 15, y - 15, self.board.cell_size, self.board.cell_size)
        
        
class Wogol(Enemy):
    def set_stats(self):
        self.hp_max = 2
        self.hp = 3
        self.damage = 1
        self.tick_max = 20
        self.points = 100
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
            self.board.get_player().add_effect(Fire(self.board.get_player(), 2, self.board.effects))
            # self.board.get_player().damage_take(self.damage)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/wogol_idle_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        
        self.frames_m = [pygame.transform.scale(load_image(f"entity/wogol_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
        

class MaskedGoblin(Enemy):
    def set_stats(self):
        self.hp = 2
        self.hp_max = 3
        self.damage = 3
        self.tick_max = 20
        self.points = 50
        
    def attack(self, obj, direction):
        self.isAttack = True
        self.obj_att = [obj]
        
        obj.damage_take(self.get_damage())
        self.board.add_in_attack_list(self)
        
        if direction == "left":
            self.move_a = (-40, 0)
        elif direction == "right":
            self.move_a = (40, 0)            
        elif direction == "up":
            self.move_a = (0, -40)      
        elif direction == "down":
            self.move_a = (0, 40)
            
        if direction == "left" and self.right:
            self.right = False
        elif direction == "right" and not self.right:
            self.right = True
            
        self.move_a_r = (-self.move_a[0], -self.move_a[1])
        
    def next_action(self):
        x, y = self.coords
        steps = get_round_coords(x, y)

        if list(self.board.get_player().get_coords()) in steps:
            x, y = self.board.get_player().get_coords()
            x_p, y_p = self.get_coords()            
            if x_p - 1 == x and y_p == y:
                direction = "left"
            elif x_p + 1 == x and y_p == y:
                direction = "right"
            elif x_p == x and y_p == y + 1:
                direction = "up"
            elif x_p == x and y_p == y - 1:
                direction = "down"     
            self.attack(self.board.get_player(), direction)
        else:
            direction = get_path(self.board, self.coords, self.board.player.get_coords())
            if direction:
                self.move(direction[0], self.board)

    def create_sprite(self, x, y):
        x = x * self.board.cell_size + self.board.left
        y = y * self.board.cell_size + self.board.top
        
        self.frames = [pygame.transform.scale(load_image(f"entity/masked_orc_idle_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r = [pygame.transform.flip(i, True, False) for i in self.frames]
        self.image = self.frames[0]
        self.frames_m = [pygame.transform.scale(load_image(f"entity/masked_run_anim_f{i}.png"), (self.board.cell_size - 10, self.board.cell_size - 10)) for i in range(4)]
        self.frames_r_m = [pygame.transform.flip(i, True, False) for i in self.frames_m]   
        
        self.image1 = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.image = self.image1
        self.rect = pygame.Rect(x + 5, y + 5, self.board.cell_size, self.board.cell_size)
