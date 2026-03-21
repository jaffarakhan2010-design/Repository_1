import pygame
from building import Universal_Building
from controller_cursor import cursor
from buttons import *
from population_handler import population
from world import World
from text import *
from save_details import *
from settings import *
import math as mt

class Game():
    def __init__(self, border_width):
        pygame.init()
        pygame.mixer.init()
        self.win_w, self.win_h = 1920, 1080
        self.display = pygame.display.set_mode((self.win_w, self.win_h), pygame.FULLSCREEN) #

        self.running = True
        self.menu = True
        self.economics = False
        self.game = False
        self.pause = True 
        self.building_menu = False
        self.stock_menu = False
        self.bank_menu = False
        self.building_menu_1 = True
        self.building_menu_2 = False

        self.all_sprites = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()

        self.day = 1
        self.month = 1
        self.year = 1980

        self.buffer = 0
        self.december = 31 + self.buffer
        self.november = 30 + self.buffer
        self.october = 31 + self.buffer
        self.september = 30 + self.buffer
        self.august = 31 + self.buffer
        self.july = 31 + self.buffer
        self.june = 30 + self.buffer
        self.may = 31 + self.buffer
        self.april = 30 + self.buffer
        self.march = 31 + self.buffer
        self.febuary = 28 + self.buffer
        self.january = 31 + self.buffer
        self.months = [self.january, self.febuary, self.march, self.april, self.may, self.june, self.july, self.august, self.september, self.october, self.november, self.december]
        self.month_index = 0
        self.month_text = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month_display = self.month_text[self.month_index]

        self.current_month = self.months[self.month_index]

        self.change = 10000
        self.max_time = 15
        
        self.money = 1000000
        self.credit = 0
        self.debt = 0

        self.font = pygame.font.Font("Retro Gaming.ttf", 100)
        self.fontlower = pygame.font.Font("Retro Gaming.ttf", 50)
        self.retfontlower = pygame.font.Font("vgafix.fon", 36)

        self.blue = (0,0,170)

        self.clock = pygame.time.Clock()

        self.mouse_pos = pygame.mouse.get_pos()
        self.port_mouse = cursor(self.win_w, self.win_h, (self.all_sprites, self.cursor))

        self.ping = pygame.mixer.Sound("ping1.ogg")
        self.noise = pygame.mixer.Sound("noise.ogg")
        self.noise.set_volume(0.75)
        self.ping.set_volume(0.75)
        self.music_list = ["music audio/8bit-main.ogg", "music audio/compressed-compressed-compressed-compressed-compressed-lowerhz-compressed-compressed-dai-sy.ogg", "music audio/COmprented-compressed.ogg", "music audio/compressed-compressed-compressed-2025bit.ogg", "music audio/theme2.ogg"]
        self.music_max_index = len(self.music_list) - 1
        self.music_index = self.music_max_index
        self.current_music = pygame.mixer.Sound(self.music_list[self.music_index])

        self.min_wage = 10
        self.product_price = 0
        self.potential_positions = 0
        self.maximum_positions = 0
        self.cooldown = False
        self.menu_cooldown = True

        self.play_button = Play_Button(self.fontlower, self.win_w, self.win_h)
        self.exit_button = Exit_Button(self.fontlower,self.win_w, self.win_h)

        self.pg_2 = Building_page_2(self.fontlower, self.win_w, self.win_h, self.min_wage, self.product_price)

        self.population = population()

        self.world = World(self.display, self.port_mouse, self.win_h, self.win_w)
        self.world.init()

        self.total_housing = 0
        self.workable = 0

        self.text_money = Text_Money(self.fontlower, self.money, self.win_w, self.win_h)
        self.text_building_menu = Building_Menu_Text(self.fontlower, self.win_w, self.win_h)

        self.arrow_button = pygame.image.load("arrow.png")
        self.arrow_button_rect = self.arrow_button.get_frect(midbottom = (self.win_w / 2, self.win_h))

        self.toggle_cursor = self.fontlower.render("Toggle Cursor", False, "White")
        self.toggle_cursor_rect = self.toggle_cursor.get_frect(bottomleft = (0, self.win_h))

        self.bank_text = self.fontlower.render("Bank", False, 'White')
        self.bank_text_rect = self.bank_text.get_frect(topright = (self.win_w, 0))

        self.next_page = False

        self.unemployed_population = 0

        self.new_rect = 0

        self.cursor_allowed = True
        
        self.conversion_cost = 0

        self.start_time = 0
        self.current_time = 0
        self.duration = 250

        self.dist = 150

        self.fps = 0
        self.fps_text = self.fontlower.render(str(self.fps), False, "White")
        self.fps_rect = self.fps_text.get_frect(topleft = (0, 75))
        self.fps_toggle = False

        self.img_arrow = pygame.image.load("row.png").convert_alpha()
        self.img_arrow_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) + 250, 75))
    
        self.img_arrow2 = pygame.image.load("row.png").convert_alpha()
        self.img_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.img_arrow2_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) - 250, 75))

        self.wage_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.wage_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 265))
        self.wage_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.wage_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 265))

        self.price_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.price_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 410))
        self.price_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.price_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 410))

        self.stock_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.stock_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 790))
        self.stock_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.stock_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 790))

        self.raw_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.raw_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 930))
        self.raw_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.raw_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 930))

        self.work_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.work_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 790))
        self.work_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.work_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 790))

        self.info_name = 0
        self.info_name_rect = 0
        
        self.info_price = 0
        self.info_price_rect = 0

        self.info_own = 0
        self.info_own_rect = 0
        
        self.border_width = border_width

        self.no_cursor = False

        self.info_operational = 0
        self.info_operational_rect = 0

        self.loan_page = False
        self.payment_page = False
        self.credit_score = 500
        self.interest_rate_flat = 5
        self.interest_penalty = 0
        self.interest_rate_list = []
        self.debt_list = []
        self.loan_text = 'Type Here'
        self.current_amount_typed = 0
        self.typing = False
        self.loan_rejected = False
        self.interest_reward = 1

        self.share_max = 100
        self.equity_num = 0
        self.equity_own_list = [self.share_max]
        self.equity_debt = []
        self.interest_rate = 0
        self.interest_rate_modifier = 1
        
        self.building_price_modifier = 1

        self.loan_cancel_confirm_deviation = 30

        self.debt_whole = 0

        self.index_num = 0
        self.index_num_max = 0

        self.payment_bank_group_text = []
        self.payment_bank_group_rect = []
        self.temp_text = 0
        self.temp_rect = 0
        self.no_payment = []
        self.x_payment = 0
        self.y_payment = 150
        self.current_list_num_bank = 0
        self.payemnt_page_pay = False

        self.payment_text = ''
        self.payment_text = 'Type Here'

        self.pause_sym = pygame.image.load("paused.png").convert_alpha()
        self.play_sym = pygame.image.load("row.png").convert_alpha()

        self.pause_play_sym_rect = self.play_sym.get_frect(topright = (-100, -100))

# RENDER FUNCTIONS

###################################################################################################################################################################################

######################################################
# THIS IS A BIG FUNCTION SO IT'S DIVIDED FOR CLARITY #
######################################################

###################################################################################################################################################################################

    def building_menu_render(self, dt): 
        self.display.fill(self.blue)
        self.display.blit(self.img_arrow, self.img_arrow_rect)
        self.display.blit(self.img_arrow2, self.img_arrow2_rect)

        self.display.blit(self.text_building_menu.sell_button, self.text_building_menu.sell_button_rect)
        self.display.blit(self.text_building_menu.leave_button, self.text_building_menu.leave_button_rect)
        keys = pygame.key.get_pressed()

        self.worker_title = self.fontlower.render("People Working", False, 'White')
        self.worker_t_rect = self.worker_title.get_frect(center = (self.win_w / 2, 730))

        self.stock_u = self.fontlower.render(f"0", False, 'White')
        self.stock_ur = self.stock_u.get_frect(center = (self.win_w / 2, 990))

        self.stockt = self.fontlower.render("Stock", False, 'White')
        self.stocktr = self.stockt.get_frect(center = (self.win_w / 2, 930))

        self.worker_content = self.fontlower.render("0", False, 'White')
        self.worker_c_rect = self.worker_content.get_frect(center = (self.win_w / 2, 790))

        if self.port_mouse.rect.colliderect(self.img_arrow_rect) and not self.menu_cooldown or self.img_arrow_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
            self.new_rect = pygame.draw.rect(self.display, 'White', self.img_arrow_rect, self.border_width)
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                for i in self.world.world_group:
                    if i.in_menu:
                        if i.arpartment_complex == False and i.house_2  == False and i.house_1 == False:
                            if self.building_menu_1:
                                self.building_menu_1 = False
                                self.building_menu_2 = True
                            elif self.building_menu_2:
                                self.building_menu_1 = True
                                self.building_menu_2 = False
                            else: self.building_menu_1 = True
                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()

                            self.noise.play()

        if self.port_mouse.rect.colliderect(self.img_arrow2_rect) and not self.menu_cooldown or self.img_arrow2_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
            self.new_rect = pygame.draw.rect(self.display, 'white', self.img_arrow2_rect, self.border_width)
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                for i in self.world.world_group:
                    if i.in_menu:
                        if i.arpartment_complex == False and i.house_2  == False and i.house_1 == False:
                            if self.building_menu_1:
                                self.building_menu_1 = False
                                self.building_menu_2 = True
                            elif self.building_menu_2:
                                self.building_menu_1 = True
                                self.building_menu_2 = False
                            else: self.building_menu_1 = True
                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()

                            self.noise.play()


        if self.port_mouse.rect.colliderect(self.text_building_menu.leave_button_rect) and not self.menu_cooldown or self.text_building_menu.leave_button_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
            self.new_rect = pygame.draw.rect(self.display, 'white', self.text_building_menu.leave_button_rect, self.border_width)
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                for i in self.world.world_group:
                    i.in_menu = False
                self.building_menu = False
                self.game = True
                self.menu = False
                self.bank_menu = False
                self.noise.play()

                self.menu_cooldown = True
                self.start_time = pygame.time.get_ticks()

        if self.port_mouse.rect.colliderect(self.text_building_menu.sell_button_rect) and not self.menu_cooldown or self.text_building_menu.sell_button_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
            self.new_rect = pygame.draw.rect(self.display, 'white', self.text_building_menu.sell_button_rect, self.border_width)
            for i in self.world.world_group:
                if i.in_menu:
                    self.info_price = self.fontlower.render(f"Price: ${round(i.price * 0.6)}", False, "White")
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                i.update(self.population.population, self.min_wage)
                self.menu_cooldown = True
                self.start_time = pygame.time.get_ticks()
                for i in self.world.world_group:
                    if i.in_menu and i.plr_owns:
                        self.money += i.price / 2
                        i.plr_owns = False
                    i.in_menu = False
                self.building_menu = False
                self.game = True
                self.menu = False
                self.ping.play()

        if self.building_menu_2:
            self.ult_render()
            self.work_arrow1 = pygame.image.load("row.png").convert_alpha()
            self.work_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 790))
            self.work_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
            self.work_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 790))

            self.display.blit(self.work_arrow1, self.work_arrow1_rect)
            self.display.blit(self.work_arrow2, self.work_arrow2_rect)

            self
            for i in self.world.world_group:
                if i.in_menu:
                    self.dist = 150
                    i.productivity = 0.0000430 * ((i.wage)**2)
                    if i.type == "Converter":
                        raw_stock = i.raw_unit
                    else: raw_stock = 0
                    stock_max = i.stock_unit_max
                    stock = i.stock_unit
                    if i.productivity < 0:
                        i.productivity = 0
                    if i.productivity > 1:
                        i.productivity = 1
                    if i.stock_unit_max > 1000:
                        self.dist = 225
                    elif i.stock_unit_max > 10000:
                        self.dist = 300
                    elif i.stock_unit_max > 100000:
                        self.dist = 375

                    if self.port_mouse.rect.colliderect(self.work_arrow1_rect) or self.work_arrow1_rect.collidepoint(pygame.mouse.get_pos()):
                        self.new_rect = pygame.draw.rect(self.display, 'white', self.work_arrow1_rect, self.border_width)
                        # +
                        if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                            i.worker_max += 1

                            self.noise.play()
                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()

                    if self.port_mouse.rect.colliderect(self.work_arrow2_rect) or self.work_arrow2_rect.collidepoint(pygame.mouse.get_pos()):
                        self.new_rect = pygame.draw.rect(self.display, 'white', self.work_arrow2_rect, self.border_width)
                        # -
                        if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                            if i.worker_max <= 0:
                                i.worker_max = 0
                            else:
                                i.worker_max -= 1
                            self.noise.play()
                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()
                    
                    self.worker_content = self.fontlower.render(f"{i.worker_max}", False, 'White')

                    #pro = round((round(((((i.slope) * (((i.item_cost) - (i.opt_price)) ** 2) + (self.population.workable  * (i.market_value / 100)) * i.item_cost)) * i.productivity) / i.extra_division) - i.expense) * i.tax)
                    pro = self.net_income = round(((i.income - i.expense)))
                    self.pg_2.update(i.wage, i.item_cost, pro, stock, raw_stock, stock_max)

            self.stock_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 790))
            self.stock_arrow2_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) - self.dist, 790))

            self.display.blit(self.worker_title, self.worker_t_rect)
            self.display.blit(self.worker_content, self.worker_c_rect)
            self.display.blit(self.stock_u, self.stock_ur)
            self.display.blit(self.stockt, self.stocktr)

            self.display.blit(self.pg_2.title, self.pg_2.title_rect)
            self.display.blit(self.pg_2.wage_title, self.pg_2.wage_title_rect)
            self.display.blit(self.pg_2.wage_content, self.pg_2.wage_content_rect)
            self.display.blit(self.pg_2.price_title, self.pg_2.price_title_rect)
            self.display.blit(self.pg_2.price, self.pg_2.price_rect)
            self.display.blit(self.pg_2.info_1_title_content, self.pg_2.info_1_title_content_rect)
            self.display.blit(self.pg_2.info_1_title, self.pg_2.info_1_title_rect)
            #self.display.blit(self.pg_2.title2, self.pg_2.title2_rect)

            self.display.blit(self.wage_arrow1, self.wage_arrow1_rect)
            self.display.blit(self.wage_arrow2, self.wage_arrow2_rect)
            self.display.blit(self.price_arrow1, self.price_arrow1_rect)
            self.display.blit(self.price_arrow2, self.price_arrow2_rect)

            self.img_arrow_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) + 300, 85))
            self.img_arrow2_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) - 300, 85))

            if self.port_mouse.rect.colliderect(self.wage_arrow1_rect) and not self.menu_cooldown or self.wage_arrow1_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.wage_arrow1_rect, self.border_width)
                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    for i in self.world.world_group:
                        if i.in_menu:
                            i.wage += 5
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.port_mouse.rect.colliderect(self.wage_arrow2_rect) and not self.menu_cooldown or self.wage_arrow2_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.wage_arrow2_rect, self.border_width)
                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    for i in self.world.world_group:
                        if i.in_menu:
                            i.wage -= 5
                            if i.wage < 10:
                                i.wage = 10
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.port_mouse.rect.colliderect(self.price_arrow1_rect) and not self.menu_cooldown or self.price_arrow1_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.price_arrow1_rect, self.border_width)
                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    for i in self.world.world_group:
                        if i.in_menu:
                            i.item_cost += 5
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.port_mouse.rect.colliderect(self.price_arrow2_rect) and not self.menu_cooldown or self.price_arrow2_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.price_arrow2_rect, self.border_width)
                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    for i in self.world.world_group:
                        if i.in_menu:
                            if i.item_cost - 5 > 0:
                                i.item_cost -= 5
                            else: 
                                self.noise.play()
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

        if self.building_menu_1:

            self.display.blit(self.text_building_menu.title, self.text_building_menu.title_rect)  

            self.display.blit(self.arrow_button, self.arrow_button_rect)

            self.img_arrow_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) + 250, 85))
            self.img_arrow2_rect = self.img_arrow.get_frect(center = ((self.win_w / 2) - 250, 85))

            if not self.next_page:
                self.display.blit(self.text_building_menu.building_shop, self.text_building_menu.building_shop_rect)
                self.display.blit(self.text_building_menu.building_shop_2, self.text_building_menu.building_shop_2_rect)
                self.display.blit(self.text_building_menu.building_shop_3, self.text_building_menu.building_shop_3_rect)
                self.display.blit(self.text_building_menu.house_1, self.text_building_menu.house_1_rect)
                self.display.blit(self.text_building_menu.house_2, self.text_building_menu.house_2_rect)
                self.display.blit(self.text_building_menu.apartment_complex, self.text_building_menu.apartment_complex_rect)
                self.display.blit(self.text_building_menu.hotel, self.text_building_menu.hotel_rect)
                self.display.blit(self.text_building_menu.industrial_brick, self.text_building_menu.industrial_brick_rect)
                self.display.blit(self.text_building_menu.industrial_computers, self.text_building_menu.industrial_computers_rect)
                self.display.blit(self.text_building_menu.industrial_graphics_card, self.text_building_menu.industrial_graphics_card_rect)
                self.display.blit(self.text_building_menu.industrial_CPU, self.text_building_menu.industrial_CPU_rect)

            if self.next_page:
                self.display.blit(self.text_building_menu.industrial_monitor, self.text_building_menu.industrial_monitor_rect)
                self.display.blit(self.text_building_menu.industrial_steel, self.text_building_menu.industrial_steel_rect)

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            self.ult_render()
            if not self.menu_cooldown:
                if self.port_mouse.rect.colliderect(self.arrow_button_rect) and not self.menu_cooldown or self.arrow_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.new_rect = pygame.draw.rect(self.display, 'white', self.arrow_button_rect, self.border_width)
                    if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        if self.next_page:
                            self.next_page = False
                        elif not self.next_page:
                            self.next_page = True

                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                        self.noise.play()

                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        for i in self.world.world_group:
                            if i.in_menu:
                                if i.plr_owns:
                                    self.money += i.price
                                    i.plr_owns = False
                                    self.ping.play()

                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()

                            i.in_menu = False

                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()

                        self.building_menu = False
                        self.game = True
                        self.menu = False

                if not self.next_page:
                    for r in self.text_building_menu.rect_list:
                        if self.port_mouse.rect.colliderect(r) and not self.menu_cooldown or r.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                            self.new_rect = pygame.draw.rect(self.display, 'white', r, self.border_width)

                #Buttons for changing type

                        for i in self.world.world_group:

                            if self.new_rect.colliderect(self.text_building_menu.building_shop_rect) and not self.menu_cooldown and not i.building_shop:
                                if i.in_menu:
                                    self.conversion_cost = round(78000 / 2)
                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = True
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()    
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)                      

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = True
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.update(self.population.population, self.min_wage)
                                            i.market_value + 0.1
                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.building_shop_2_rect) and not self.menu_cooldown and not i.building_shop2:
                                if i.in_menu:
                                    self.conversion_cost = round(70000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        
                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = True
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = True
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)
                                
                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.building_shop_3_rect) and not self.menu_cooldown and not i.building_shop3:
                                if i.in_menu:
                                    self.conversion_cost = round(600000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")

                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = True

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            i.in_menu = False
                                            self.building_menu = False
                                            self.game = True
                                            self.menu = False

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                            self.ping.play()

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = True

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            i.update(self.population.population, self.min_wage)
                                            i.market_value + 0.1

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.industrial_brick_rect) and not self.menu_cooldown and not i.industrial_brick:
                                if i.in_menu:
                                    self.conversion_cost = round(250000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                        
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:                            
                        
                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False
            
                                            i.industrial_steel = False
                                            i.industrial_brick = True
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            i.update(self.population.population, self.min_wage)
                                            i.market_value + 0.1

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                            self.ping.play()
                                            i.market_value + 0.1

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  True
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.update(self.population.population, self.min_wage)
                                            i.market_value + 0.1

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.industrial_computers_rect) and not self.menu_cooldown and not i.industrial_computers:
                                if i.in_menu:
                                    self.conversion_cost = round(75000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = True
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False
            
                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = True
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                            #i.in_menu = False
                                            #self.building_menu = False
                                            #self.game = True
                                            #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.industrial_graphics_card_rect) and not self.menu_cooldown and not i.industrial_graphics_card:
                                if i.in_menu:
                                    self.conversion_cost = round(60000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:


                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = True
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                            #i.in_menu = False
                                            #self.building_menu = False
                                            #self.game = True
                                            #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = True
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                            #i.in_menu = False
                                            #self.building_menu = False
                                            #self.game = True
                                            #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.industrial_CPU_rect) and not self.menu_cooldown and not i.industrial_CPU:
                                if i.in_menu:
                                    self.conversion_cost = round(50000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = True
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                            #i.in_menu = False
                                            #self.building_menu = False
                                            #self.game = True
                                            #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = True
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()

                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()
        
                            if self.new_rect.colliderect(self.text_building_menu.apartment_complex_rect) and not self.menu_cooldown and not i.arpartment_complex:
                                if i.in_menu:
                                    self.conversion_cost = round(500000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False
            
                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = True
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)
                            
                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = True
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False
                                        else: self.noise.play()

                            if self.new_rect.colliderect(self.text_building_menu.house_1_rect) and not self.menu_cooldown and not i.house_1:
                                if i.in_menu:
                                    self.conversion_cost = round(50000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                self.info_price_rect = self.info_price.get_frect(bottomright = (self.win_w, self.win_h))
                            
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = True
                                            i.house_2 = False
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = True
                                            i.house_2 = False
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        else: self.noise.play()

                                    #i.in_menu = False
                                    #self.building_menu = False
                                    #self.game = True
                                    #self.menu = False

                            if self.new_rect.colliderect(self.text_building_menu.house_2_rect) and not self.menu_cooldown and not i.house_2:
                                if i.in_menu:
                                    self.conversion_cost = round(97000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")

                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False
            
                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = True
                                            i.hotel = False

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                    #i.in_menu = False
                                    #self.building_menu = False
                                    #self.game = True
                                    #self.menu = False

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = True
                                            i.hotel = False

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        else: self.noise.play()

                                        #i.in_menu = False
                                        #self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                            if self.new_rect.colliderect(self.text_building_menu.hotel_rect) and not self.menu_cooldown and not i.hotel:
                                if i.in_menu:
                                    self.conversion_cost = round(200000 / 2)

                                self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")                        
                                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                                    if i.in_menu:
                                        if self.money > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = True

                                            self.money -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            self.ping.play()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)

                                        #i.in_menu = False
                                        ##self.building_menu = False
                                        #self.game = True
                                        #self.menu = False

                                    

                                        elif self.credit > self.conversion_cost:
                                            i.building_shop = False
                                            i.building_shop2 = False
                                            i.building_shop3 = False

                                            i.industrial_steel = False
                                            i.industrial_brick =  False
                                            i.industrial_computers = False
                                            i.industrial_graphics_card = False
                                            i.industrial_CPU = False
                                            i.industrial_monitor = False

                                            i.arpartment_complex = False
                                            i.house_1 = False
                                            i.house_2 = False
                                            i.hotel = True
                                            self.ping.play()

                                            self.credit -= self.conversion_cost

                                            self.menu_cooldown = True
                                            self.start_time = pygame.time.get_ticks()
                                            i.market_value + 0.1
                                            i.update(self.population.population, self.min_wage)
                                        else: self.noise.play()

                                    #i.in_menu = False
                                    #self.building_menu = False
                                    #self.game = True
                                    #self.menu = False
    #NEXT PAGE
                if self.next_page:
                    for r in self.text_building_menu.rect_list2:
                        if self.port_mouse.rect.colliderect(r) and not self.menu_cooldown or r.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                            self.new_rect = pygame.draw.rect(self.display, 'white', r, self.border_width)

                            for i in self.world.world_group:

                                if self.new_rect.colliderect(self.text_building_menu.industrial_monitor_rect) and not self.menu_cooldown and not i.industrial_monitor:
                                    if i.in_menu:
                                        self.conversion_cost = round(100000 / 2)

                                    self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")
                                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                                        if i.in_menu:
                                            self.conversion_cost = round(100000 / 2)

                                        if i.in_menu:
                                            if self.money > self.conversion_cost:
                                                i.building_shop = False
                                                i.building_shop2 = False
                                                i.building_shop3 = False

                                                i.industrial_steel = False
                                                i.industrial_brick =  False
                                                i.industrial_computers = False
                                                i.industrial_graphics_card = False
                                                i.industrial_CPU = False
                                                i.industrial_monitor = True

                                                i.arpartment_complex = False
                                                i.house_1 = False
                                                i.house_2 = False
                                                i.hotel = False

                                                self.money -= self.conversion_cost

                                                self.menu_cooldown = True
                                                self.start_time = pygame.time.get_ticks()
                                                self.ping.play()
                                                i.market_value + 0.1
                                                i.update(self.population.population, self.min_wage)

                                            #i.in_menu = False
                                            #self.building_menu = False
                                            #self.game = True
                                            #self.menu = False

                                            elif self.credit > self.conversion_cost:
                                                i.building_shop = False
                                                i.building_shop2 = False
                                                i.building_shop3 = False
                    
                                                i.industrial_steel = False
                                                i.industrial_brick =  False
                                                i.industrial_computers = False
                                                i.industrial_graphics_card = False
                                                i.industrial_CPU = False
                                                i.industrial_monitor = True

                                                i.arpartment_complex = False
                                                i.house_1 = False
                                                i.house_2 = False
                                                i.hotel = False

                                                self.credit -= self.conversion_cost

                                                self.menu_cooldown = True
                                                self.start_time = pygame.time.get_ticks()
                                                self.ping.play()
                                                i.market_value + 0.1
                                                i.update(self.population.population, self.min_wage)

                                                #i.in_menu = False
                                                #self.building_menu = False
                                                #self.game = True
                                                #self.menu = False
                                            else: self.noise.play()
            

                                if self.new_rect.colliderect(self.text_building_menu.industrial_steel_rect) and not self.menu_cooldown and not i.industrial_steel:
                                    if i.in_menu:
                                        self.conversion_cost = round(50000 / 2)
                                    self.info_price = self.fontlower.render(f"Price: ${self.conversion_cost}", False, "White")

                                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:

                                        if i.in_menu:
                                            if self.money > self.conversion_cost:
                                                i.building_shop = False
                                                i.building_shop2 = False
                                                i.building_shop3 = False

                                                i.industrial_steel = True
                                                i.industrial_brick =  False
                                                i.industrial_computers = False
                                                i.industrial_graphics_card = False
                                                i.industrial_CPU = False
                                                i.industrial_monitor = False

                                                i.arpartment_complex = False
                                                i.house_1 = False
                                                i.house_2 = False
                                                i.hotel = False

                                                self.money -= self.conversion_cost

                                                self.menu_cooldown = True
                                                self.start_time = pygame.time.get_ticks()

                                                self.ping.play()
                                                i.market_value + 0.1
                                                i.update(self.population.population, self.min_wage)

                                                #i.in_menu = False
                                                #self.building_menu = False
                                                #self.game = True
                                                #self.menu = False
                                        
                                            elif self.credit > self.conversion_cost:
                                                i.building_shop = False
                                                i.building_shop2 = False
                                                i.building_shop3 = False

                                                i.industrial_steel = True
                                                i.industrial_brick =  False
                                                i.industrial_computers = False
                                                i.industrial_graphics_card = False
                                                i.industrial_CPU = False
                                                i.industrial_monitor = False

                                                i.arpartment_complex = False
                                                i.house_1 = False
                                                i.house_2 = False
                                                i.hotel = False

                                                self.credit -= self.conversion_cost

                                                self.menu_cooldown = True
                                                self.start_time = pygame.time.get_ticks()

                                                self.ping.play()
                                                i.market_value + 0.1

                                                i.update(self.population.population, self.min_wage)

                                                #i.in_menu = False
                                                #self.building_menu = False
                                                #self.game = True
                                                #self.menu = False
                                            else: self.noise.play()
            
        self.info_name = 0
        self.info_name_rect = 0
        if self.info_price:
            self.info_price_rect = self.info_price.get_frect(bottomright = (self.win_w, self.win_h))
            self.display.blit(self.info_price, self.info_price_rect)
        self.cursor.draw(self.display)

        self.ult_render()
        self.essential_render()

        pygame.display.update()

###################################################################################################################################################################################

#######################################################
# ABOVE IS A BIG FUNCTION SO IT'S DIVIDED FOR CLARITY #
#######################################################

###################################################################################################################################################################################
    
    def game_render(self, dt):

        self.display.fill((0, 127, 14))
        self.world.world_group.draw(self.display)
        keys = pygame.key.get_pressed()
        self.loan_page = False

        self.next_page = False

        self.time_dislay = self.fontlower.render(f"{self.month_display}, {self.day}, {self.year}", False,"white")
        self.time_dislay_rect = self.time_dislay.get_frect(topleft = (0, 0))

        self.all_sprites.draw(self.display)
        self.display.blit(self.bank_text, self.bank_text_rect)

        if self.port_mouse.rect.colliderect(self.bank_text_rect) and not self.menu_cooldown  or self.bank_text_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
            self.new_rect = pygame.draw.rect(self.display, 'white', self.bank_text_rect, self.border_width)
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                self.bank_menu = True
                self.game = False
                self.equity_num = 0

                self.menu_cooldown = True
                self.start_time = pygame.time.get_ticks()

        for i in self.world.world_group:
            if self.port_mouse.rect.colliderect(i.rect) and not self.menu_cooldown  or i.rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                self.new_rect = pygame.draw.rect(self.display, 'white', i.rect, self.border_width)
                self.workable = self.population.workable

                if self.workable > 0:
                    self.workable -= i.worker_max
                    i.employee = i.worker_max

                if i.operational:
                    self.info_operational = self.fontlower.render("Operational", False, "White")
                else: self.info_operational = self.fontlower.render("Not Operational", False, "White")

                if i.building_shop:
                    self.info_name = self.fontlower.render("Small Shop", False, "White")

                if i.building_shop2:
                    self.info_name = self.fontlower.render("Medium Shop", False, "White")

                if i.building_shop3:
                    self.info_name = self.fontlower.render("Large Shop", False, "White")

                if i.house_1:
                    self.info_name = self.fontlower.render("Small House", False, "White")

                if i.house_2:
                    self.info_name = self.fontlower.render("Luxury House", False, "White")
        
                if i.hotel:
                    self.info_name = self.fontlower.render("Hotel", False, "White")

                if i.arpartment_complex:
                    self.info_name = self.fontlower.render("Apartment Complex", False, "White")

                if i.industrial_brick:
                    self.info_name = self.fontlower.render("Brick Factory", False, "White")

                if i.industrial_computers:
                    self.info_name = self.fontlower.render("Computer Factory", False, "White")

                if i.industrial_CPU:
                    self.info_name = self.fontlower.render("CPU Factory", False, "White")

                if i.industrial_graphics_card:
                    self.info_name = self.fontlower.render("GPU Factory", False, "White")

                if i.industrial_monitor:
                    self.info_name = self.fontlower.render("Monitor Factory", False, "White")

                if i.industrial_steel:
                    self.info_name = self.fontlower.render("Steel Factory", False, "White")

                if self.new_rect.colliderect(i.rect) and i.plr_owns == True:
                    if i.plr_owns:
                        self.info_own = self.fontlower.render(f"You Own This", False, "White")

                self.info_price = self.fontlower.render(f"Price: ${i.price}", False, "White")

                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    if not i.plr_owns:
                        if self.credit >= i.price or self.money >= i.price:
                            i.plr_owns = True
                            self.ping.play()

                            if self.money >= i.price:
                                self.money -= i.price
                            else: self.credit -= i.price

                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()
                    else:
                        self.noise.play()
                        self.menu_cooldown = True
                        i.in_menu = True
                        self.building_menu = True
                        self.game = False
                        self.bank_menu = False
                        self.building_menu_1 = True
                        self.building_menu_2 = False

                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()

        if self.info_name:
            self.info_name_rect = self.info_name.get_frect(bottomright = (self.win_w, self.win_h))

            if self.info_price:
                self.display.blit(self.info_name, self.info_name_rect)
                self.info_price_rect = self.info_price.get_frect(bottomright = (self.win_w, self.win_h - 65))
                self.display.blit(self.info_price, self.info_price_rect)
                
        if self.info_own:
            self.info_own_rect = self.info_own.get_frect(bottomright = (self.win_w, self.win_h - 130))
            self.display.blit(self.info_own, self.info_own_rect)

        if self.info_operational:

            self.info_operational_rect = self.info_operational.get_frect(topright = (self.win_w, 0))
            if self.info_own_rect:
                self.info_operational_rect = self.info_operational.get_frect(topright = (self.win_w, 0))
            #self.display.blit(self.info_operational, self.info_operational_rect)

        
        self.fps_rect = self.fps_text.get_frect(topleft = (0, 65))

        self.ult_render()
        self.essential_render()

                            
        pygame.display.update()

    def menu_render(self, dt):
        self.display.fill(self.blue)
        self.loan_page = False

        self.display.blit(self.play_button.text, self.play_button.rect)
        self.display.blit(self.exit_button.text, self.exit_button.rect)
        self.display.blit(self.toggle_cursor, self.toggle_cursor_rect)
        
        keys = pygame.key.get_pressed()

        pygame.event.pump()
        if not self.menu_cooldown:
            if self.port_mouse.rect.colliderect(self.play_button.rect) or self.play_button.rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                self.new_rect = pygame.draw.rect(self.display, 'white', self.play_button.rect, self.border_width)
                if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                    self.noise.play()
                    self.menu = False
                    self.game = True
                    self.building_menu = False

                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.port_mouse.rect.colliderect(self.exit_button.rect) or self.exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.exit_button.rect, self.border_width)
                if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                    self.noise.play()
                    self.running = False
                    pygame.quit()
                    pygame.mixer.quit()

            if self.running:
                if self.port_mouse.rect.colliderect(self.toggle_cursor_rect) or self.toggle_cursor_rect.collidepoint(pygame.mouse.get_pos()):
                    self.new_rect = pygame.draw.rect(self.display, 'white', self.toggle_cursor_rect, self.border_width)
                    if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                        if self.cursor_allowed:
                            self.cursor_allowed = False

                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()
                            self.noise.play()
                        else: 
                            self.cursor_allowed = True
                            self.port_mouse.rect.center = (self.win_w / 2, self.win_h / 2)

                            self.menu_cooldown = True
                            self.start_time = pygame.time.get_ticks()
                            self.noise.play()

            
        self.fps_rect = self.fps_text.get_frect(topleft = (0, 0))
                
        if self.running:
            self.ult_render()
            pygame.display.update()

    def ult_render(self):
        if self.fps_toggle:
            self.display.blit(self.fps_text, self.fps_rect)
            self.cursor.draw(self.display)
    
    def essential_render(self):
        self.display.blit(self.text_money.debt_text, self.text_money.debt_rect)
        self.display.blit(self.text_money.text, self.text_money.rect)
        self.text_money.update(self.money, self.credit, self.debt_whole)
        self.display.blit(self.time_dislay, self.time_dislay_rect)
        if self.pause == True:
            self.display.blit(self.pause_sym, self.pause_play_sym_rect)
        else:
            self.display.blit(self.play_sym, self.pause_play_sym_rect)
        
    def stock_render(self):
        self.display.fill(self.blue)
        self.ult_render()

        pygame.display.update()

    def bank_render(self):
        self.display.fill(self.blue)
        self.cursor.draw(self.display)

        self.x_payment = 0
        self.y_payment = 175

        self.temp_text = 0
        self.temp_rect = 0

        self.interest_reward = 0
        self.interest_rate = 0
        self.loan_rejected = False
        if self.interest_rate_modifier <= 0:
            self.interest_rate_modifier = 1

        self.rejected_loan_text = self.fontlower.render("Rejected", False, 'Red')
        self.rejected_loan_text_rect = self.rejected_loan_text.get_frect(bottomright = (self.win_w, self.win_h))

        self.loan_confirm_text = self.fontlower.render("Confirm", False, 'White')
        self.loan_confirm_rect = self.loan_confirm_text.get_frect(bottomright = ((self.win_w / 2) - self.loan_cancel_confirm_deviation, self.win_h))

        self.loan_cancel_text = self.fontlower.render("Cancel", False, "White")
        self.loan_cancel_rect = self.loan_cancel_text.get_frect(bottomleft = ((self.win_w / 2) + self.loan_cancel_confirm_deviation, self.win_h))

        self.payment_confirm_text = self.fontlower.render("Confirm", False, 'White')
        self.payment_confirm_rect = self.loan_confirm_text.get_frect(bottomright = ((self.win_w / 2) - self.loan_cancel_confirm_deviation, self.win_h))

        self.payment_cancel_text = self.fontlower.render("Cancel", False, "White")
        self.payment_cancel_rect = self.loan_cancel_text.get_frect(bottomleft = ((self.win_w / 2) + self.loan_cancel_confirm_deviation, self.win_h))

        self.accepted_loan_text = self.fontlower.render("Accepted", False, 'Green')
        self.accepted_loan_text_rect = self.accepted_loan_text.get_frect(bottomright = (self.win_w, self.win_h))

        self.bank_title = self.fontlower.render("Bank of Appleton Springs", False, 'White')
        self.bank_title_rect = self.bank_title.get_frect(midtop = (self.win_w / 2, 100))

        self.equity_title = self.fontlower.render("Shares", False, 'White')
        self.equity_title_rect = self.equity_title.get_frect(center = (self.win_w / 2, 350))

        self.equity_content = self.fontlower.render(f"{self.equity_num}/{self.share_max}", False, 'White')
        self.equity_content_rect = self.equity_content.get_frect(center = (self.win_w / 2, 425))

        self.equity_arrow1 = pygame.image.load("row.png").convert_alpha()
        self.equity_arrow1_rect = self.wage_arrow1.get_frect(center = ((self.win_w / 2) + self.dist, 425))
        self.equity_arrow2 = pygame.transform.flip(self.img_arrow, True, False)
        self.equity_arrow2_rect = self.wage_arrow2.get_frect(center = ((self.win_w / 2) - self.dist, 425))

        self.loan_app = self.fontlower.render("Appy For A Loan", False, 'White')
        self.loan_app_rect = self.loan_app.get_frect(center = (self.win_w / 2, 400))

        self.interest_rate_title = self.fontlower.render("Interest Rate", False, 'White')
        self.interest_rate_title_rect = self.interest_rate_title.get_frect(center = (self.win_w / 2, 800))

        self.leave_button = self.fontlower.render("Leave", False, 'White')
        self.leave_button_rect = self.leave_button.get_frect(topright = (self.win_w, 0))

        self.payment_button = self.fontlower.render("Payment", False, 'White')
        self.payment_button_rect = self.payment_button.get_frect(center = (self.win_w / 2, (self.win_h / 2) + 150))

        self.back_payment = self.fontlower.render("<< Back", False, 'White')
        self.back_payment_rect = self.back_payment.get_frect(bottomleft = (0, self.win_h - (65 * 2)))

        self.display.blit(self.bank_title, self.bank_title_rect)
        self.display.blit(self.leave_button, self.leave_button_rect)
 
        keys = pygame.key.get_pressed()

        if self.port_mouse.rect.colliderect(self.leave_button_rect) and not self.menu_cooldown or self.leave_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.new_rect = pygame.draw.rect(self.display, 'White', self.leave_button_rect, self.border_width)
            if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                self.payemnt_page_pay = False
                self.loan_page = False
                self.payment_page = False
                self.bank_menu = False
                self.building_menu = False
                self.game = True
                self.typing = False
                self.equity_num = False

                self.menu_cooldown = True
                self.noise.play()
                self.start_time = pygame.time.get_ticks()

        if not self.loan_page and not self.payment_page:
            self.display.blit(self.loan_app, self.loan_app_rect)
            self.display.blit(self.payment_button, self.payment_button_rect)
            if self.port_mouse.rect.colliderect(self.loan_app_rect) and not self.menu_cooldown or self.loan_app_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                self.new_rect = pygame.draw.rect(self.display, 'white', self.loan_app_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.loan_page = True
                    self.interest_rate = 0
                    self.menu_cooldown = True
                    self.noise.play()
                    self.start_time = pygame.time.get_ticks()
            if self.port_mouse.rect.colliderect(self.payment_button_rect) or self.payment_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.payment_button_rect, self.border_width)
                if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.payment_page = True
                    self.loan_page = False

                    self.noise.play()
                    self.menu_cooldown = False
                    self.start_time = pygame.time.get_ticks()
        
        if self.payment_page:
            self.index_num_max = 0
            self.index_num = 0
            len(self.debt_list)
            self.index_num = 0
            for i in self.debt_list:
                if self.debt_list:
                    self.index_num_max = len(self.debt_list) - 1
                    self.x_payment += 400
                    self.temp_text = self.fontlower.render(f"Debt No.{self.index_num + 1}", False, 'White')
                    self.temp_rect = self.temp_text.get_frect(topleft = (self.x_payment, self.y_payment))
                    self.index_num += 1
                    if self.x_payment > self.win_w:
                        self.x_payment = 0
                        self.y_payment += 125
                    if self.temp_rect.right > self.win_w:
                        self.temp_rect.x = 0
                        self.temp_rect.y += 125
                        self.x_payment = 400
                        self.y_payment += 125
                    if not self.payemnt_page_pay:
                        self.display.blit(self.temp_text, self.temp_rect)
                    self.payment_bank_group_rect.append(self.temp_rect)
                    self.payment_bank_group_text.append(self.temp_text)
            self.index_num = 0
            for i in self.payment_bank_group_rect:
                if self.port_mouse.rect.colliderect(i) and not self.payemnt_page_pay or i.collidepoint(pygame.mouse.get_pos()) and not self.payemnt_page_pay:
                    self.new_rect = pygame.draw.rect(self.display, 'White', i, self.border_width)
                    self.current_list_num_bank = self.payment_bank_group_rect.index(i)
                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        self.payemnt_page_pay = True
                        self.current_list_num_bank = self.payment_bank_group_rect.index(i)

                        self.noise.play()
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
            if self.payemnt_page_pay:
                if self.payment_text != 'Type Here' and not self.payment_text == '':
                    if float(self.payment_text) > self.debt_list[self.current_list_num_bank]:
                        self.payment_text = str(round(self.debt_list[self.current_list_num_bank]))
                self.text_payment_text = self.fontlower.render(f"{self.payment_text}", False, 'White')
                self.text_payment_rect = self.text_payment_text.get_frect(center = (self.win_w / 2, self.win_h /2))
                self.display.blit(self.text_payment_text, self.text_payment_rect)
                self.display.blit(self.payment_confirm_text, self.payment_confirm_rect)
                self.display.blit(self.payment_cancel_text, self.payment_cancel_rect)

                if self.port_mouse.rect.colliderect(self.payment_confirm_rect) or self.payment_confirm_rect.collidepoint(pygame.mouse.get_pos()):
                    self.new_rect = pygame.draw.rect(self.display, 'White', self.payment_confirm_rect, self.border_width)
                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        if self.payment_text != '' and self.payment_text != 'Type Here':
                            if self.money >= int(self.payment_text):
                                self.payemnt_page_pay = False
                                self.payment_page = False
                                self.ping.play()
                                self.debt_list[self.current_list_num_bank] -= int(self.payment_text)
                                self.money -= int(self.payment_text)
                                if self.debt_list[self.current_list_num_bank] <= 0:
                                    del self.debt_list[self.current_list_num_bank]
                                    del self.interest_rate_list[self.current_list_num_bank]
                            else:
                                self.noise.play()
                        else:
                            self.noise.play()
                        
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                
                if self.port_mouse.rect.colliderect(self.payment_cancel_rect) or self.payment_cancel_rect.collidepoint(pygame.mouse.get_pos()):
                    self.new_rect = pygame.draw.rect(self.display, 'White', self.payment_cancel_rect, self.border_width)
                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        self.payemnt_page_pay = False
                        self.payment_page = False
                        
                        self.noise.play()
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()

                if self.port_mouse.rect.colliderect(self.text_payment_rect) or self.text_payment_rect.collidepoint(pygame.mouse.get_pos()):
                    self.new_rect = pygame.draw.rect(self.display, 'White', self.text_payment_rect, self.border_width)
                    if keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                        if not self.typing:
                            self.typing = True
                        else:
                            self.typing = True
                        if self.payment_text == 'Type Here':
                            self.payment_text = ''

                        self.noise.play()
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()

                if self.typing:
                    if keys[pygame.K_0] and not self.menu_cooldown:
                        self.payment_text += '0'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_1] and not self.menu_cooldown:
                        self.payment_text += '1'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_2] and not self.menu_cooldown:
                        self.payment_text += '2'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_3] and not self.menu_cooldown:
                        self.payment_text += '3'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_4] and not self.menu_cooldown:
                        self.payment_text += '4'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_5] and not self.menu_cooldown:
                        self.payment_text += '5'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_6] and not self.menu_cooldown:
                        self.payment_text += '6'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_7] and not self.menu_cooldown:
                        self.payment_text += '7'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_8] and not self.menu_cooldown:
                        self.payment_text += '8'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_9] and not self.menu_cooldown:
                        self.payment_text += '9'
                        self.menu_cooldown = True
                        self.start_time = pygame.time.get_ticks()
                    if keys[pygame.K_BACKSPACE]:
                        self.payment_text = ''
                if not self.typing and not self.payment_text:
                    self.payment_text = 'Type Here'
                self.display.blit(self.text_payment_text, self.text_payment_rect)
            
        if self.loan_page:
            self.payment_page = False

            self.interest_rate = 0
            if self.equity_num < 0:
                self.equity_num = 0
            if self.equity_num > 100:
                self.equity_num = 100

            self.display.blit(self.loan_amount_text, self.loan_amount_text_rect)
            self.display.blit(self.loan_confirm_text, self.loan_confirm_rect)
            self.display.blit(self.loan_cancel_text, self.loan_cancel_rect)
            self.display.blit(self.interest_rate_title, self.interest_rate_title_rect)
            self.display.blit(self.equity_title, self.equity_title_rect)
            self.display.blit(self.equity_arrow1, self.equity_arrow1_rect)
            self.display.blit(self.equity_arrow2, self.equity_arrow2_rect)

            if self.port_mouse.rect.colliderect(self.equity_arrow1_rect) or self.equity_arrow1_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.equity_arrow1_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.equity_num += 1
                    if self.equity_num > round(self.equity_own_list[0] * 0.50):
                        self.equity_num = round(self.equity_own_list[0] * 0.50)

                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                    self.noise.play()
            if self.port_mouse.rect.colliderect(self.equity_arrow2_rect) and not self.menu_cooldown or self.equity_arrow2_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                self.new_rect = pygame.draw.rect(self.display, 'white', self.equity_arrow2_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.equity_num -= 1

                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                    self.noise.play()

            if self.port_mouse.rect.colliderect(self.loan_amount_text_rect) and not self.menu_cooldown or self.loan_amount_text_rect.collidepoint(pygame.mouse.get_pos()) and not self.menu_cooldown:
                self.new_rect = pygame.draw.rect(self.display, 'white', self.loan_amount_text_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.menu_cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.noise.play()
                    if self.typing == True:
                        self.typing = False
                    else: 
                        self.typing = True
                        self.loan_text = ''
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.typing:
                if keys[pygame.K_0] and not self.menu_cooldown:
                    self.loan_text += '0'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_1] and not self.menu_cooldown:
                    self.loan_text += '1'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_2] and not self.menu_cooldown:
                    self.loan_text += '2'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_3] and not self.menu_cooldown:
                    self.loan_text += '3'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_4] and not self.menu_cooldown:
                    self.loan_text += '4'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_5] and not self.menu_cooldown:
                    self.loan_text += '5'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_6] and not self.menu_cooldown:
                    self.loan_text += '6'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_7] and not self.menu_cooldown:
                    self.loan_text += '7'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_8] and not self.menu_cooldown:
                    self.loan_text += '8'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_9] and not self.menu_cooldown:
                    self.loan_text += '9'
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()
                if keys[pygame.K_BACKSPACE]:
                    self.loan_text = ''
            if not self.typing and not self.loan_text:
                self.loan_text = 'Type Here'

            if self.loan_text:
                if self.loan_text != 'Type Here':
                    self.current_amount_typed = int(self.loan_text)
                    self.loan_rejected = False
                else:
                    self.current_amount_typed = 0
            if self.current_amount_typed:
                if self.credit_score < 200:
                    self.interest_penalty = 7
                    self.loan_rejected = True
                if self.credit_score > 500:
                    self.interest_penalty = 5
                elif self.credit_score >= 500 and self.credit_score <= 680:
                    self.interest_penalty = 2
                elif self.credit_score >= 681:
                    self.interest_penalty = 0

                if ((self.money - self.debt_whole) * 2) < self.current_amount_typed:
                    self.interest_penalty += 15
                    self.loan_rejected = False
                if ((self.money - self.debt_whole) * 3) < self.current_amount_typed:
                    self.interest_penalty += 30
                    self.loan_rejected = False
                if ((self.money - self.debt_whole) * 5) < self.current_amount_typed:
                    self.interest_penalty +=35
                    self.loan_rejected = False
                if ((self.money - self.debt_whole) * 6) < self.current_amount_typed:
                    self.loan_rejected = True
            if self.equity_num == 100:
                self.loan_rejected = True

            if self.equity_num > self.equity_own_list[0]:
                if self.equity_own_list[0] - 10 <= 0:
                    self.equity_num = self.equity_own_list[0] - 1
                else:
                    self.equity_num = self.equity_own_list[0] - 10

            self.equity_content = self.fontlower.render(f"{self.equity_num}/{self.equity_own_list[0]}", False, 'White')
            self.equity_content_rect = self.equity_content.get_frect(center = (self.win_w / 2, 400 + 25))

            self.interest_reward += self.equity_num / 50

            self.interest_rate += round(((self.interest_rate_flat * self.interest_rate_modifier) + self.interest_penalty) - (((self.interest_rate_flat * self.interest_rate_modifier) + self.interest_penalty) * self.interest_reward))
            self.interest_rate_content = self.fontlower.render(f"{self.interest_rate}%", False, 'White')
            self.interest_rate_content_rect = self.interest_rate_content.get_frect(center = (self.win_w / 2, 875))
            self.display.blit(self.interest_rate_content, self.interest_rate_content_rect)
            self.display.blit(self.equity_content, self.equity_content_rect)

            if self.loan_rejected:
                self.display.blit(self.rejected_loan_text, self.rejected_loan_text_rect)
            elif not self.loan_rejected:
                self.display.blit(self.accepted_loan_text, self.accepted_loan_text_rect)

            if self.port_mouse.rect.colliderect(self.loan_confirm_rect) or self.loan_confirm_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.loan_confirm_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    if not self.loan_rejected:
                        self.debt_list.append(self.current_amount_typed)
                        self.interest_rate_list.append(self.interest_rate)
                        self.money += self.current_amount_typed
                        self.loan_page = False
                        if self.equity_num:
                            self.equity_own_list.append(self.equity_num)
                            self.equity_own_list[0] -= self.equity_num
                        else:
                            self.equity_debt.append(False)
                        if ((self.money - self.debt_whole) * 2) < self.current_amount_typed:
                            self.credit_score -= 100
                        if ((self.money - self.debt_whole) * 3) < self.current_amount_typed:
                            self.credit_score -= 200
                        if ((self.money - self.debt_whole) * 5) < self.current_amount_typed:
                            self.credit_score -= 250
                    self.noise.play()
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

            if self.port_mouse.rect.colliderect(self.loan_cancel_rect) or self.loan_cancel_rect.collidepoint(pygame.mouse.get_pos()):
                self.new_rect = pygame.draw.rect(self.display, 'white', self.loan_cancel_rect, self.border_width)
                if self.keys[pygame.K_RETURN] and not self.cooldown or pygame.mouse.get_pressed()[0] and not self.menu_cooldown:
                    self.loan_page = False
                    self.noise.play()
                    self.menu_cooldown = True
                    self.start_time = pygame.time.get_ticks()

        self.ult_render()
        self.essential_render()

        pygame.display.update()
        
        self.payment_bank_group_rect = []
        self.payment_bank_group_text = []

    def b_menu_render(self):
        self.display.fill(self.blue)
        self.ult_render()

        pygame.display.update()

# GAME LOOP

    def run(self):
        while self.running:

            self.temp_text = 0
            self.temp_rect = 0

            self.index_num_max = 0

            self.index_num = 0

            self.debt_whole = 0

            self.loan_amount_text = self.fontlower.render(self.loan_text, False, 'White')
            self.loan_amount_text_rect = self.loan_amount_text.get_frect(center = (self.win_w / 2, self.win_h / 2))

            self.new_rect = pygame.draw.rect(self.display, "white",(100, 100, -100, -150))
            self.workable = self.population.workable

            self.info_name = self.fontlower.render("Empty Land", True, "White")
            self.info_name_rect = 0

            self.info_price = 0
            self.info_price_rect = 0

            self.info_own = False
            self.info_own_rect = False

            self.info_operational = 0
            self.info_operational_rect = 0

            self.fps = round(self.clock.get_fps())
            self.fps_text = self.fontlower.render(str(self.fps), False, "White")

            self.current_time = pygame.time.get_ticks()

            self.mouse_pos = pygame.mouse.get_pos()
            dt = self.clock.tick() / 1000
            self.month_display = self.month_text[self.month_index]
            self.current_month = self.months[self.month_index]

            self.keys = pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            recent_keys = pygame.key.get_just_pressed()
            
            if self.debt_list:
                for i in self.debt_list:
                    self.debt_whole += i

            if self.credit_score < 250:
                self.credit_score = 100

            if not self.cursor_allowed:
                self.port_mouse.rect.center = (-100, -100)

            self.change += self.change * dt
            if self.music_index > self.music_max_index:
                    self.music_index = 0

            if not pygame.mixer.get_busy():
                self.music_index += 1
                if self.music_index > self.music_max_index:
                    self.music_index = 0
                self.current_music = pygame.mixer.Sound(self.music_list[self.music_index])
                self.current_music.play()
                self.current_music.set_volume(1)

            if self.current_time - self.start_time >= self.duration:
                self.menu_cooldown = False
                self.cooldown = False
            else: 
                self.menu_cooldown = True
                self.menu_cooldown = True

            if self.game:
                #Time Sys
                if not self.pause:
                    if round(self.change) >= self.max_time:
                        self.day += 1
                        self.change = 5

                        for i in self.world.world_group:
                            i.make_cash()
                            if self.workable > 0:
                                self.workable -= i.worker_max
                                i.employee = i.worker_max
                            if i.plr_owns:
                                i.make_cash()
                                self.money += i.net_income
                            i.computer_decrease += 1                            

                    if self.day > self.current_month:
                        self.day = 1

                        if self.month_index < 11:
                            self.month_index += 1
                        else: 
                            self.month_index = 0 
                            self.year += 1

                        if self.debt_list:
                            for i in self.debt_list:
                                self.debt_list[self.index_num] += (i*(self.interest_rate_list[self.index_num] / 100))
                                print(self.interest_rate_list[self.index_num])
                                self.index_num += 1
                                self.credit_score -= 25
                        self.index_num = 0

                if recent_keys[pygame.K_SPACE]:
                    self.ping.play()
                    if self.pause:
                        self.pause = False
                    else: self.pause = True

            #Exiting
            if game:
                if keys[pygame.K_ESCAPE]:
                    self.payemnt_page_pay = False
                    self.game = False
                    self.menu = True
                    self.building_menu = False
                    self.economics = False
                    self.bank_menu = False
                    self.stock_menu = False
                    self.typing = False
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if keys[pygame.K_F3] and not self.fps_toggle and not self.menu_cooldown:
                self.fps_toggle = True

                self.menu_cooldown = True
                self.start_time = pygame.time.get_ticks()

            elif keys[pygame.K_F3] and self.fps_toggle and not self.menu_cooldown:
                self.fps_toggle = False
                self.menu_cooldown = True
                self.start_time = pygame.time.get_ticks()

            self.port_mouse.move(dt)
            self.all_sprites.update()

            if self.game:
                for i in self.world.world_group:
                    if i.operational:
                        self.potential_positions += i.worker_max
                for i in self.world.world_group:
                    self.total_housing += i.housing_space

                self.population.update(self.total_housing, self.potential_positions)
                self.game_render(dt)
                
                self.world.world_group.update(self.total_housing, self.min_wage)

                #Reset
                self.potential_positions = 0
                self.total_housing = 0
            
            if self.building_menu:
                self.building_menu_render(dt)
            
            if self.stock_menu:
                self.stock_render()

            if self.bank_menu:
                self.bank_render()

            if self.menu:
                self.menu_render(dt)

        pygame.quit()
        pygame.mixer.quit()

game = Game(round(Border_width))
if __name__ == '__main__':
    game.run()

pygame.mixer.quit()
pygame.quit()