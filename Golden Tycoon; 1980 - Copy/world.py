import pygame
from building import *
from population_handler import *
from datetime import datetime
from settings import *

class World():
    def __init__(self, display, cursor, win_h, win_w):
        self.cursor = cursor
        self.world_display = display
        pos = (500, 0)
        start = 650
        build_hub = 0
        x = build_hub
        y = 100
        second = datetime.now().second
        if second > 30:
            second - 30
            if second == 0:
                second += 1


        self.world_group = pygame.sprite.Group()
        id = 0
        #NO.1 right edge section 0
        #self.building_1 = Universal_Building((start, 0), self.world_group) #
        #self.building_2 = Universal_Building((start + 100, 0), self.world_group)

        for num in range(112):
            Universal_Building((x, y), self.world_group, extra_division_num, id=id)
            id += 1
            if x > win_w - 200:
                if y <= win_h - 200:
                    y += 100
                    x = build_hub
                else: break
            else: x += 100
        for i in self.world_group:
            i.random(second)

    def init(self):
        print("Hello World")
        #self.building_1.industrial_steel = True
        #self.building_2.arpartment_complex = True

    def update(self, cursor):
        self.cursor = cursor