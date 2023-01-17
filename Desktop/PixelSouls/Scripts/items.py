import random
import pygame

from ability import *
from game_lib2 import load_image


class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y, board, group):
        super().__init__(group)
        self.board = board
        self.x = x 
        self.y = y
        
        self.set_image()
    
    def set_image(self):
        pass
    
    
class HealtPotion(Potion):
    def set_image(self):
        self.cur_frame = 0
        self.tick_max = 30
        self.tick = 0
        self.frames = [pygame.transform.scale(load_image(rf"items\Potios\flasks_1_{i}.png"), (self.board.cell_size, self.board.cell_size)) for i in range(1, 4)]
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.x * self.board.cell_size + self.board.left, self.y * self.board.cell_size + self.board.top, self.board.cell_size, self.board.cell_size)
     
    def update(self):
        if self.board.get_player().get_coords() == (self.x, self.y):
            self.board.game_sound.sound_potion.play()
            
            self.board.get_player().take_healt(10)
            
            if self.board.get_player().right:
                self.board.get_player().image = pygame.transform.scale(load_image("entity/knight_take_healt.png"), (self.board.cell_size, self.board.cell_size))
            else:
                self.board.get_player().image = pygame.transform.flip(pygame.transform.scale(load_image("entity/knight_take_healt.png"), (self.board.cell_size, self.board.cell_size)), True, False)
            self.kill()
        if self.tick >= self.tick_max:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.tick = 0
        else:
            self.tick += 1
            

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, board, group):
        super().__init__(group)
        self.board = board
        self.x = x 
        self.y = y
        self.open = False
        if self.board.info.stage[0] == 0 and self.board.info.stage[1] <= 5:
            self.items = random.choice([Katana, Axe, BigSword, SpikeSword])(board.player)
        elif self.board.info.stage[0] == 0 and self.board.info.stage[1] > 5:
            self.items = random.choice([Axe, IceSword, IceSwordLong, PoisonSword, FireSword])(board.player)
        elif self.board.info.stage[0] == 1:
            self.items = random.choice([IceSword, IceSwordLong, PoisonSword, FireSword, UltimateSword, UltimateSwordLong])(board.player)
        self.set_image()
        self.onPlayer = False
        self.change = True
    
    def set_image(self):
        self.cur_frame = 0
        self.tick_max = 10
        self.tick = 0
        self.frames = [pygame.transform.scale(load_image(rf"props\chest_empty_open_anim_f{i}.png"), (self.board.cell_size, self.board.cell_size)) for i in range(3)]
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.x * self.board.cell_size + self.board.left, self.y * self.board.cell_size + self.board.top, self.board.cell_size, self.board.cell_size)

    def update(self):
        if self.board.get_player().get_coords() == (self.x, self.y):
            if not self.open:
                self.board.game_sound.sound_potion.play()
                self.open = True

        if self.cur_frame < 3 and self.open:
            if self.tick >= self.tick_max:
                self.image = self.frames[self.cur_frame]
                self.cur_frame += 1
                self.tick = 0
            else:
                self.tick += 1
        elif self.cur_frame == 3 and not self.onPlayer:
            self.rect.y -= self.board.cell_size
            self.set_item(self.items)
            self.cur_frame = 4
            self.onPlayer = True
            
    def change_item(self):
        a = self.board.player.weapon
        self.board.player.weapon = self.items
        self.items = a
        self.change = False
        self.set_item(self.items)
        self.board.weapon_bar.isChange = True 
            
    def set_item(self, item):
            self.items = item
            surf = pygame.Surface((self.board.cell_size, self.board.cell_size * 2), pygame.SRCALPHA, 32)
            surf.blit(self.frames[-1], (0, self.board.cell_size))
            surf.blit(pygame.transform.scale(item.image, (self.board.cell_size * 0.5, self.board.cell_size)), (self.board.cell_size / 4,  self.board.cell_size / 2))
            self.image = surf     

class Weapon:
    def __init__(self, owner) -> None:
        self.owner = owner
        self.name = None
        self.damage = None
        self.pattern = {}
        self.effect = []
        self.set_stats()
                
    def give_hit(self, d):
        coords = self.owner.coords
        board = self.owner.board
        for i in self.pattern[d]:
            x, y = coords[0] + i[0],  coords[1] + i[1]
            try:
                board.board[y][x].take_hit(board.game_sound, board.effects, board.effects)
            except:
                pass
            
    def give_damage(self, d):
        coords = self.owner.coords
        board = self.owner.board
        
        att_obj = []
        for i in self.pattern[d]:
            x, y = coords[0] + i[0],  coords[1] + i[1]
            try:
                board.board[y][x].damage_take(self.damage, board.effects)
                for i in self.effect:
                    if random.randint(1, i[2]) == 1:
                        print("Freeeze")
                        board.board[y][x].add_effect(i[0](board.board[y][x], i[1], board.effects)) 
                att_obj.append(board.board[y][x])
            except:
                pass
            
        return att_obj
    
    def set_image(self, path):
        self.image = load_image(path)
            
        

class BigSword(Weapon):
    def set_stats(self):
        self.name = "Ибонитовая палочка 2.0 reborn"
        self.damage = 2
        self.pattern = {
            "left": ((-1, 0), (-2, 0)),
            "right": ((+1, 0), (+2, 0)),
    
            "up": ((0, -1), (0, -2)),
            "down": ((0, +1), (0, +2))
        }
        
        
class Sword(Weapon):
    def set_stats(self):
        self.name = "Sword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image("weapon\weapon_knife.png")
    
        
class IceSword(Weapon):
    def set_stats(self):
        self.effect = [(Freeze, 5, 1)]
        self.name = "IceSword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image("weapon\weapon_knight_sword.png")
        
class IceSwordLong(Weapon):
    def set_stats(self):
        self.effect = [(Freeze, 5, 1)]
        self.name = "IceRapier"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0), (-2, 0)),
            "right": ((+1, 0), (+2, 0)),
    
            "up": ((0, -1), (0, -2)),
            "down": ((0, +1), (0, +2))
        }
        self.set_image("weapon\weapon_duel_sword.png")
        

class PoisonSword(Weapon):
    def set_stats(self):
        self.effect = [(Poison, 2, 1)]
        self.name = "PoisonSword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image("weapon\weapon_golden_sword.png")
        
class FireSword(Weapon):
    def set_stats(self):
        self.effect = [(Fire, 1, 1)]
        self.name = "FireSword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image("weapon\weapon_red_gem_sword.png")
        

class UltimateSword(Weapon):
    def set_stats(self):
        self.effect = [(Freeze, 2, 1), (Poison, 1, 1), (Fire, 1, 1)]
        self.name = "MegaSword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image("weapon\weapon_rusty_sword.png")
        
class UltimateSwordLong(Weapon):
    def set_stats(self):
        self.effect = [(Freeze, 2, 1), (Poison, 2, 1), (Fire, 2, 1)]
        self.name = "UltimateSword"
        self.damage = 2
        self.pattern = {
            "left": ((-1, 0), (-2, 0)),
            "right": ((+1, 0), (+2, 0)),
    
            "up": ((0, -1), (0, -2)),
            "down": ((0, +1), (0, +2))
        }
        self.set_image("weapon\weapon_lavish_sword.png")
        
        
class Katana(Weapon):
    def set_stats(self):
        self.name = "Katana"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0), (-1, +1), (-1, -1)),
            "right": ((+1, 0), (+1, +1), (+1, -1)),
    
            "up": ((0, -1), (+1, -1), (-1, -1)),
            "down": ((0, +1), (+1, +1), (-1, +1))
        }
        self.set_image("weapon\weapon_katana.png")
        
class Axe(Weapon):
    def set_stats(self):
        self.name = "Katana"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0), (0, +1), (0, -1)),
            "right": ((+1, 0), (0, +1), (0, -1)),
    
            "up": ((0, -1), (+1, 0), (-1, 0)),
            "down": ((0, +1), (+1, 0), (-1, 0))
        }
        self.set_image(r"weapon\weapon_axe.png")
        
class BigSword(Weapon):
    def set_stats(self):
        self.name = "BigSword"
        self.damage = 1
        self.pattern = {
            "left": ((-1, 0), (-2, 0)),
            "right": ((+1, 0), (+2, 0)),
    
            "up": ((0, -1), (0, -2)),
            "down": ((0, +1), (0, +2))
        }
        self.set_image(r"weapon\weapon_regular_sword.png")
        
class SpikeSword(Weapon):
    def set_stats(self):
        self.name = "BigSword"
        self.damage = 2
        self.pattern = {
            "left": ((-1, 0),),
            "right": ((+1, 0),),
    
            "up": ((0, -1),),
            "down": ((0, +1),)
        }
        self.set_image(r"weapon\weapon_saw_sword.png")
    