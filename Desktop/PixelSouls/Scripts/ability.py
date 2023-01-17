import pygame
from game_lib2 import load_image


class Impact(pygame.sprite.Sprite):
    def __init__(self, entity, steps, group):
        super().__init__(group)
        self.group = group
        self.entity = entity
        self.steps = steps
        self.hold = []
        self.start = []
        self.end = []
        
        self.stage = 1
        self.tick_max = 2
        self.tick = 0
        
        self.cur_frame = 0
        
        self.create()
        self.add_image()

    def add_image(self):
        pass
        
    def create(self):
        pass
    
    
class Poison(Impact):
    def create(self):
        self.entity.board.game_sound.sound_poison_start.play()
        self.damage = 1
        
    def action(self):
        if self.steps > 0:
            self.entity.damage_take(self.damage, self.group)
            self.steps -= 1   
            
    def add_image(self):
        size = self.entity.board.cell_size
        self.frames = [pygame.transform.scale(load_image(rf"effects\elemental_effects\Poison Effect\{i}.png"), (size + 40, size + 20)) for i in range(1, 61)]            
        
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.entity.rect.x - 15, self.entity.rect.y - 10, size, size)
        
        
    def update(self):
        self.rect.x = self.entity.rect.x - 30
        self.rect.y = self.entity.rect.y - 35
        
        if self.tick >= self.tick_max:
            self.image = self.frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.tick = 0
        else:
            self.tick += 1 
        self.image.set_alpha(200)
        
        
class Fire(Impact):
    def create(self):
        self.entity.board.game_sound.sound_poison_start.play()
        self.damage = 2
        
    def action(self):
        if self.steps > 0:
            self.entity.damage_take(self.damage, self.group)
            self.steps -= 1   
            
    def add_image(self):
        size = self.entity.board.cell_size
        self.frames = [pygame.transform.scale(load_image(rf"effects\elemental_effects\Fire Effect\{i}.png"), (size + 40, size + 20)) for i in range(1, 61)]            
        
        self.image = self.frames[0]
        self.rect = pygame.Rect(self.entity.rect.x - 15, self.entity.rect.y - 10, size, size)
        
        
    def update(self):
        self.rect.x = self.entity.rect.x - 30
        self.rect.y = self.entity.rect.y - 35
        
        if self.tick >= self.tick_max:
            self.image = self.frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.tick = 0
        else:
            self.tick += 1 
        self.image.set_alpha(200)        
            
            
class Freeze(Impact):
    def create(self):
        self.entity.board.game_sound.sound_ice_freeze.play()
        self.damage = 0
        
    def action(self):
        if self.stage != 3:
            if self.steps > 1:
                self.entity.freeze = True
            else:
                self.entity.board.game_sound.sound_ice_break.play()
                self.entity.freeze = False
                self.stage = 3
            self.steps -= 1
        
    def add_image(self):
        size = self.entity.board.cell_size
        
        self.start = [pygame.transform.scale(load_image(rf"effects\elemental_effects\Separated Frames\Ice VFX 2 Start{i}.png"), (size + 20, size)) for i in range(1, 12)]
        self.hold = [pygame.transform.scale(load_image(rf"effects\elemental_effects\Separated Frames\Ice VFX 2 Active{i}.png"), (size + 20, size)) for i in range(4, 9)]
        self.end = [pygame.transform.scale(load_image(rf"effects\elemental_effects\Separated Frames\Ice VFX 2 Ending{i}.png"), (size + 20, size)) for i in range(1, 19)]

        self.image = self.start[0]
        self.rect = pygame.Rect(self.entity.rect.x - 15, self.entity.rect.y - 10, size, size)
        
    def update(self):
        self.rect.x = self.entity.rect.x - 15
        self.rect.y = self.entity.rect.y - 10
        
        
        if self.stage == 1:
            if self.tick >= self.tick_max:
                self.image = self.start[self.cur_frame]
                self.cur_frame += 1
                self.tick = 0
            else:
                self.tick += 1            
            
            if self.cur_frame == len(self.start):
                self.cur_frame = 0
                self.stage = 2
                
        elif self.stage == 2:
            if self.tick >= 20:
                self.image = self.hold[self.cur_frame]
                self.cur_frame = (self.cur_frame + 1) % len(self.hold)
                self.tick = 0
            else:
                self.tick += 1
        
        elif self.stage == 3:
            if self.tick >= self.tick_max:
                self.image = self.end[self.cur_frame]
                self.cur_frame += 1
                self.tick = 0
            else:
                self.tick += 1            
            
            if self.cur_frame == len(self.start):
                self.kill()   