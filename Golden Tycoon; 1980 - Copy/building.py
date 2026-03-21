import pygame
from random import randint
from os.path import join
from datetime import datetime
import math as mt

class Plr_Building(pygame.sprite.Sprite):
    def __init__(self, win_w, win_h, mouse_pos, groups, dt):
        super().__init__(groups)
        self.image = pygame.image.load("Building.png")
        self.rect = self.image.get_frect(center = mouse_pos)

        if self.rect.right > win_w:
            self.rect.right = win_w
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > win_h:
            self.rect.bottom = win_h

        self.dt = dt

    #def update(self):

class Universal_Building(pygame.sprite.Sprite):
    def __init__(self, pos, groups, div_num, id):
        super().__init__(groups)
        self.extra_division = div_num
        self.price = 15000
        self.income = 0
        self.product_price = 5
        self.worker_max = 0
        self.expense = 0
        self.net_income = 0
        self.tax = 0.15
        self.wage = 10
        self.computer_decrease = 10
        self.employee = 0
        self.in_menu = False
        self.market_value = 5
        self.item_cost = 5
        self.productivity = 0
        self.stock_unit = 0
        self.raw_unit = 0
        self.stock_unit_max = 0
        self.abs_max = 0
        self.worker_out = 0
        self.worker_out_mod = 2
        self.customers_line = 0
        self.building_num = id #"Failed To Enter During Coding Process This Is a Work In Progress"

        self.plr_owns= False
        self.building_shop = False
        self.building_shop2 = False
        self.building_shop3 = False
        self.operational = False
        
        self.industrial_steel = False
        self.industrial_brick =  False
        self.industrial_computers = False
        self.industrial_graphics_card = False
        self.industrial_CPU = False
        self.industrial_monitor = False
        self.opt_price = 1.25
        self.slope = -0.1
        self.day_track = 0
        self.false = False

        self.research_centre = False

        self.arpartment_complex = False
        self.house_1 = False
        self.house_2 = False
        self.hotel = False
        self.popularity = 1
        self.rent = 0

        self.type = "'Type' Use Title Case SPELL CORRECTLY"
        self.market_type = "'Type' Use Title Case SPELL CORRECTLY Abreiviations use all caps"

        self.upyear = 0 #Upyear is to increase the price over time
        self.housing_space = 0
        self.image_list = ["shop_1.png", "shop_2.png", "shop_3.png", "house_1.png", "house_2.png", "apartment.png", "brick_factory.png", "cpu-gpu_factory.png", "hotel.png", "steel_factory.png", "monitor_factory.png", "land.png"]
        self.image_index = 11
        self.image = pygame.image.load(join("buildings", self.image_list[self.image_index])).convert_alpha()
        self.rect = self.image.get_frect(topleft = pos)
        self.stock = 0
        self.worker_out_mod = 1

    def update(self, current_population, plr_min_wage):
        self.image = pygame.image.load(join("buildings", self.image_list[self.image_index])).convert_alpha()
        #Reset
        self.rent = 0
        self.worker_out = 0


        if self.popularity < 0.75:
            self.popularity = 0.75

        self.operational = False
        self.expense = 0
        self.productivity = 0.0000430 * ((self.wage)**2)
        self.market_type = "N/A"
        self.type = "Land"
        self.current_population = current_population

        if self.market_value > 100:
            self.market_value = 100

        if self.productivity < 0:
                self.productivity = 0
        if self.productivity > 1:
            self.productivity = 1

        #self.income = round(((((self.slope) * (((self.item_cost) - (self.opt_price)) ** 2) + (current_population  * (self.market_value / 100)) * self.item_cost)) * self.productivity) / self.extra_division)
        if self.market_type == "Shop":
            self.customers_line = -2.5 * (self.item_cost) + 100
        if self.market_type == "Hotel":
            self.customers_line = -0.90909090909 * (self.item_cost) + 100
        if self.market_type == "Housing":
            self.customers_line = 0
        if self.market_type == "Brick":
            self.customers_line = -6.66666666667 * (self.item_cost) + 100
        if self.market_type == "Computer":
            self.customers_line = -0.04 * (self.item_cost) + 100
        if self.market_type == "CPU":
            self.customers_line = -0.125 * (self.item_cost) + 100
        if self.market_type == "GPU":
            self.customers_line = -0.1 * (self.item_cost) + 100
        if self.market_type == "N/A":
            self.customers_line = 0
        if self.market_type == "TV":
            self.customers_line = -0.1 * (self.item_cost) + 100
        if self.market_type == "Steel":
            self.customers_line = -1.42857142857 * (self.item_cost) + 100

        self.total_customers = round((current_population * (self.market_value / 100) * self.customers_line))
        self.total_customers = round(((((self.current_population * (self.market_value / 100)) * (self.customers_line / 100))) * self.popularity) + 0)
        self.income = round((self.total_customers * self.item_cost) / self.extra_division)

        self.pop = current_population

        self.stock += self.worker_out * self.worker_max

        self.stock += self.worker_out * self.worker_max
        
        self.total_customers = round(((((self.current_population * (self.market_value / 100)) * (self.customers_line / 100))) * self.popularity) + 0)
        
        
        self.income = round((self.total_customers * self.item_cost) / self.extra_division)
        if self.building_shop:
            self.abs_worker_max = 5
            self.price = 78000 + self.upyear
            self.expense = 200 + (self.worker_max * self.wage)
            self.image_index = 0
            self.housing_space = 0
            self.opt_price = randint(1,20)
            self.type = "Shop"
            self.market_type = "Shop"
            self.stock_unit_max = 750
            self.worker_out = round((40 * self.worker_out_mod) * self.productivity)

        if self.building_shop2:
            self.abs_worker_max = 30
            self.price = 70000 + self.upyear
            self.expense = 600 + (self.worker_max * self.wage)
            self.image_index = 1
            self.housing_space = 0
            self.opt_price = randint(1,20)
            self.type = "Shop"
            self.market_type = "Shop"
            self.stock_unit_max = 5000
            self.worker_out = round((50 * self.worker_out_mod) * self.productivity)


        if self.building_shop3:
            self.abs_worker_max = 120
            self.price = 600000 + self.upyear
            self.expense = 1000 + (self.worker_max * self.wage)
            self.image_index = 2
            self.housing_space = 0
            self.opt_price = randint(1,20)
            self.type = "Shop"
            self.market_type = "Shop"
            self.stock_unit_max = 10000
            self.worker_out = round((400 * self.worker_out_mod) * self.productivity)

        if self.house_1:
            self.abs_worker_max = 0
            self.housing_space = 10
            self.price = 50000
            self.rent = 500
            self.income = 500 * self.housing_space
            self.image_index = 3
            self.expense = 0
            self.operational = True
            self.market_value = 0
            self.type = "Housing"
            self.market_type = "Housing"

        if self.house_2:
            self.abs_worker_max = 0
            self.housing_space = 5
            self.rent = 5000
            self.price = 97000
            self.income = (5000 * self.housing_space)
            self.image_index = 4
            self.expense = 0
            self.operational = True
            self.market_value = 0
            self.type = "Housing"
            self.market_type = "Housing"
        
        if self.hotel:
            self.abs_worker_max = 50
            self.image_index = 8
            self.expense = 50 + (self.worker_max * self.wage)
            self.housing_space = 0
            self.price = 200000
            self.opt_price = randint(10,100)
            self.type = "Converter"
            self.market_type = "Hotel"
            self.stock_unit_max = 10000
            self.worker_out = round((55 * self.worker_out_mod) * self.productivity)

        if self.arpartment_complex:
            self.housing_space = 620
            self.price = 500000
            self.rent = 200
            self.income = 200 * self.housing_space
            self.image_index = 5
            self.abs_worker_max = 0
            self.operational = True
            self.type = "Housing"
            self.market_type = "Housing"
            self.market_value = 0
            self.worker_out = 10 * 0

        if self.industrial_brick:
            self.image_index = 6
            self.price = 250000
            self.abs_worker_max = 50
            self.expense = 60 + (self.worker_max * self.wage)
            self.housing_space = 0
            self.opt_price = randint(1,5)
            self.type = "Converter"
            self.market_type = "Brick"
            self.stock_unit_max = 10000
            self.worker_out = round((1000 * self.worker_out_mod) * self.productivity)

        if self.industrial_computers:
            self.image_index = 7
            self.abs_worker_max = 100
            self.price = 75000
            self.expense = (3000 - self.computer_decrease) + (self.worker_max * self.wage)
            self.income = round(((current_population * (self.market_value / 100)) * self.item_cost) / self.extra_division)
            self.housing_space = 0
            self.opt_price = randint((1450),(1500))
            self.type = "Converter"
            self.market_type = "Computer"
            self.stock_unit_max = 100
            self.worker_out = round((100 * self.worker_out_mod) * self.productivity)

        if self.industrial_CPU:
            self.image_index = 7
            self.price = 50000
            self.opt_price = 100
            self.abs_worker_max = 150
            self.expense = (2000 - (self.computer_decrease * 2)) + (self.worker_max * self.wage)
            self.income = round(((current_population * (self.market_value / 100)) * self.item_cost) / self.extra_division)
            self.housing_space = 0
            self.opt_price = randint(100,150)
            self.type = "Converter"
            self.market_type = "CPU"
            self.stock_unit_max = 500000
            self.worker_out = round((50 * self.worker_out_mod) * self.productivity)

        if self.industrial_graphics_card:
            self.image_index = 7
            self.price = 60000
            self.opt_price = 600
            self.abs_worker_max = 100
            self.expense = 1000 + (self.worker_max * self.wage)
            self.income = round(((current_population * (self.market_value / 100)) * self.item_cost) / self.extra_division)
            self.housing_space = 0
            self.opt_price = randint(300,380)
            self.type = "Converter"
            self.market_type = "GPU"
            self.stock_unit_max = 10000
            self.worker_out = round((100 * self.worker_out_mod) * self.productivity)

        if self.industrial_monitor:
            self.image_index = 10
            self.price = 100000
            self.opt_price = 500
            self.abs_worker_max = 150
            self.expense = 1000 + (self.worker_max * self.wage)
            self.income = (((self.slope) * ((self.item_cost - (self.opt_price + self.computer_decrease)) ** 2) + ((current_population * (self.market_value / 100) * self.item_cost)))) / self.extra_division
            self.housing_space = 0
            self.opt_price = randint(300,500)
            self.type = "Converter"
            self.market_type = "TV"
            self.stock_unit_max = 10000
            self.worker_out = round((150 * self.worker_out_mod) * self.productivity)
            

        if self.industrial_steel:
            self.image_index = 9
            self.price = 50000
            self.abs_worker_max = 5000
            self.expense = 500 + (self.worker_max * self.wage)
            self.housing_space = 0
            self.opt_price = randint(10,50)
            self.type = "Converter"
            self.market_type = "Steel"
            self.stock_unit_max = 10000
            self.worker_out = round((100 * self.worker_out_mod) * self.productivity)
        
        if self.market_type == "Shop":
            self.customers_line = -2.5 * (self.item_cost) + 100
        if self.market_type == "Hotel":
            self.customers_line = -0.90909090909 * (self.item_cost) + 100
        if self.market_type == "Housing":
            if self.plr_owns and self.false:
                print("Not Working Code 326B")
        if self.market_type == "Brick":
            self.customers_line = -6.66666666667 * (self.item_cost) + 100
        if self.market_type == "Computer":
            self.customers_line = -0.04 * (self.item_cost) + 100
        if self.market_type == "CPU":
            self.customers_line = -0.125 * (self.item_cost) + 100
        if self.market_type == "GPU":
            self.customers_line = -0.1 * (self.item_cost) + 100
        if self.market_type == "N/A":
            self.customers_line = 0
        if self.market_type == "TV":
            self.customers_line = -0.1 * (self.item_cost) + 100
        if self.market_type == "Steel":
            self.customers_line = -1.42857142857 * (self.item_cost) + 100
        
        if self.employee == self.worker_max:
            self.operational = True
        else: self.operational = False

        self.total_customers = round(((((self.current_population * (self.market_value / 100)) * (self.customers_line / 100))) * self.popularity) + 0)
        self.stock_unit_max = 9999

        self.expense = (self.worker_max * self.wage)
        self.income = round((self.total_customers * self.item_cost) / self.extra_division)

        self.stock += self.worker_out * self.worker_max
        if self.type == "Housing":
            self.income = self.rent * self.housing_space

    def make_cash(self):
        self.total_customers = round(((((self.current_population * (self.market_value / 100)) * (self.customers_line / 100))) * self.popularity))
        self.stock += self.worker_out * self.worker_max
        if self.customers_line >= 75:
            self.popularity += 0.0025
        if self.customers_line < 75 and self.customers_line > 45:
            self.popularity += 0.0015 
        if self.customers_line < 45:
            self.popularity -= 0.00005

        if (self.total_customers - self.stock_unit) > 0:
            self.total_customers = self.total_customers - (self.total_customers - self.stock)
            self.stock = 0
            self.popularity -= 0.01
        else: 
            self.popularity += 0.1
            self.stock = self.stock - self.total_customers
        
        if self.plr_owns and self.operational:
            self.income = round((self.total_customers * self.item_cost))
            print(f"Day: {self.day_track} Building ID: {self.building_num} \nStock Unit: {self.stock_unit}")
            print(f"Customer: {self.total_customers}")
            print(f"Customer/current_pop: {self.current_population}")
            print(f"Customer/MarketV / 100: {self.market_value / 100}")
            print(f"Customer/Customerline / 100: {self.customers_line / 100}")
            print(f"Customer/Popularity: {self.popularity}")
            print(f"Income: ${self.income}")
            print(f"Net Income: ${self.net_income}")
            print(f"Worker Output: {self.worker_out}")
            print(f"Worker Max: {self.worker_max}")
            print(f"Worker Output Modifier: {self.worker_out_mod} \n __________________________________")
            self.day_track += 1
            if self.type == "Housing":
                self.income = self.rent * self.housing_space
            if ((self.income - self.expense) * self.tax) <= 0:
                self.net_income = round(((self.income - self.expense)))
            else: 
                self.net_income = round(((self.income - self.expense) - ((self.income - self.expense) * self.tax)))
        else: 
            self.net_income = 0

    def random(self, random):
        for ck in range(1):
            fu = randint(1,14)
            if fu == 1:
                print("This Remains Empty")
            elif fu == 2:
                self.building_shop = True
                self.market_value = 15
                self.stock_unit_max = 750

            elif fu == 3:
                self.building_shop2 = True
                self.market_value = 30
                self.stock_unit_max = 5000

            elif fu == 4:
                self.building_shop3 = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 5:
                self.industrial_steel = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 6:
                self.industrial_brick = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 7:
                self.industrial_computers = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 8:
                self.industrial_graphics_card = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 9:
                self.industrial_CPU = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 10:
                self.arpartment_complex = True
            elif fu == 11:
                self.house_1 = True
                self.market_value = 0
            elif fu == 12:
                self.house_2 = True
                self.market_value = 0
            elif fu == 13:
                self.hotel = True
                self.market_value = 30
                self.stock_unit_max = 10000

            elif fu == 14:
                print("This is empty land")