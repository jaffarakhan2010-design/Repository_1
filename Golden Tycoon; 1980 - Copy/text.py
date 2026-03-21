class Text_Money():
    def __init__(self, font, money, win_w, win_h):
        self.money = money
        self.credit = 0
        self.debt = 0
        self.text = font.render(f"Money: {self.money}", False,'white')
        self.rect = self.text.get_frect(bottomleft = (0, win_h))
        self.debt_text = font.render(f"Debt: ${self.debt}", False, "white")
        self.debt_rect = self.debt_text.get_frect(bottomleft = (0, win_h - 65))
        self.win_h = win_h
        self.font = font

        self.text = self.font.render(f"Credit: {self.credit}", False,'white')
        self.rect = self.text.get_frect(bottomleft = (0, self.win_h))

        self.next = False

    def update(self, new_cash, credit, debt):
        self.money = round(new_cash)
        self.credit = round(credit)
        self.debt = round(debt)

        self.text = self.font.render(f"Money: ${self.money}", False,'white')
        self.rect = self.text.get_frect(bottomleft = (0, self.win_h))
        self.text2 = self.font.render(f"Credit: ${self.credit}", False,'white')
        self.rect2 = self.text.get_frect(bottomleft = (0, self.win_h - 65))
        self.debt_text = self.font.render(f"Debt: ${self.debt}", False, "white")
        self.debt_rect = self.debt_text.get_frect(bottomleft = (0, self.win_h - 65))

class Building_Menu_Text():
    def __init__(self, font, win_w, win_h):

        e = 247.5
        s = 75

        self.rect_list = []
        self.rect_list2 = []
        self.text_list = []

        self.title = font.render("Building Menu", False, "White")
        self.title_rect = self.title.get_frect(center = (win_w / 2, 85))

        self.sell_button = font.render("Sell", False, "White")
        self.sell_button_rect = self.sell_button.get_frect(topright = (win_w, 0)) #1440, 1080

        self.rect_list.append(self.sell_button_rect)
        self.text_list.append(self.sell_button)

        self.leave_button = font.render("Leave", False, "White")
        self.leave_button_rect = self.leave_button.get_frect(topright = (win_w, 75))

        self.rect_list.append(self.leave_button_rect)
        self.text_list.append(self.leave_button)

        self.industrial_CPU = font.render("CPU Factory", False, "White")
        self.industrial_CPU_rect = self.industrial_CPU.get_frect(center = (win_w / 2, e - s))

        self.rect_list.append(self.industrial_CPU_rect)
        self.text_list.append(self.industrial_CPU_rect)

        self.building_shop = font.render("Small Shop", False, "White")
        self.building_shop_rect = self.building_shop.get_frect(center = (win_w / 2, e))

        self.rect_list.append(self.building_shop_rect)
        self.text_list.append(self.building_shop_rect)

        self.building_shop_2 = font.render("Medium Shop", False, "White")
        self.building_shop_2_rect = self.building_shop_2.get_frect(center = (win_w / 2, e + s))

        self.rect_list.append(self.building_shop_2_rect)
        self.text_list.append(self.building_shop_2_rect)

        self.building_shop_3 = font.render("Large Shop", False, "White")
        self.building_shop_3_rect = self.building_shop_3.get_frect(center = (win_w / 2, e + (s * 2)))

        self.rect_list.append(self.building_shop_3_rect)
        self.text_list.append(self.building_shop_3_rect)

        self.house_1 = font.render("Small House", False, "White")
        self.house_1_rect = self.house_1.get_frect(center = (win_w / 2, e + (s * 3)))

        self.rect_list.append(self.house_1_rect)
        self.text_list.append(self.house_1_rect)
        
        self.house_2 = font.render("Luxury House", False, "White")
        self.house_2_rect = self.house_2.get_frect(center = (win_w / 2, e + (s * 4)))

        self.rect_list.append(self.house_2_rect)
        self.text_list.append(self.house_2_rect)

        self.hotel = font.render("Hotel", False, "White")
        self.hotel_rect = self.hotel.get_frect(center = (win_w / 2, e + (s * 5)))

        self.rect_list.append(self.hotel_rect)
        self.text_list.append(self.hotel_rect)

        self.apartment_complex = font.render("Apartment Complex", False, "White")
        self.apartment_complex_rect = self.apartment_complex.get_frect(center = (win_w / 2, e + (s * 6)))

        self.rect_list.append(self.apartment_complex_rect)
        self.text_list.append(self.apartment_complex_rect)

        self.industrial_brick = font.render("Brick Factory", False, "White")
        self.industrial_brick_rect = self.industrial_brick.get_frect(center = (win_w / 2, e + (s * 7)))

        self.rect_list.append(self.industrial_brick_rect)
        self.text_list.append(self.industrial_brick_rect)

        self.industrial_computers = font.render("Computer Factory", False, "White")
        self.industrial_computers_rect = self.industrial_computers.get_frect(center = (win_w / 2, e + (s * 8)))

        self.rect_list.append(self.industrial_computers_rect)
        self.text_list.append(self.industrial_computers_rect)

        self.industrial_graphics_card = font.render("GPU Factory", False, "White")
        self.industrial_graphics_card_rect = self.industrial_graphics_card.get_frect(center = (win_w / 2, e + (s * 9)))

        self.rect_list.append(self.industrial_graphics_card_rect)
        self.text_list.append(self.industrial_graphics_card_rect)

        self.industrial_monitor = font.render("Monitor Factory", False, "White")
        self.industrial_monitor_rect = self.industrial_monitor.get_frect(center = (win_w / 2, ( e - s)))

        self.rect_list2.append(self.industrial_monitor_rect)
        self.text_list.append(self.industrial_monitor_rect)

        self.industrial_steel = font.render("Steel Factory", False, "White")
        self.industrial_steel_rect = self.industrial_steel.get_frect(center = (win_w / 2, (e)))

        self.rect_list2.append(self.industrial_steel_rect)
        self.text_list.append(self.industrial_steel_rect)

class Building_page_2():
    def __init__(self, font, w, h, wage, product_price):
        self.font = font
        self.example_num = 0
        self.w = w

        self.title = font.render("Management Menu", False, "White")
        self.title_rect = self.title.get_frect(center = (w / 2, 85))

        self.wage_title = font.render("Wages", False, "White")
        self.wage_title_rect = self.wage_title.get_frect(center = (w / 2, 200))

        self.wage_content = font.render(str(wage), False, "white")
        self.wage_content_rect = self.wage_content.get_frect(center = (w / 2, 265))

        self.price_title = font.render("Product Price", False, "white")
        self.price_title_rect = self.price_title.get_frect(center = (w / 2, 350))

        self.price = font.render(str(product_price), False, "white")
        self.price_rect = self.price.get_frect(center = (w / 2, 410))

        self.info_1_title = font.render("Estimated Profit", False, "White")
        self.info_1_title_rect = self.info_1_title.get_frect(center = (w / 2, 600))

        self.info_1_title_content = font.render(str(self.example_num), False, "White")
        self.info_1_title_content_rect = self.info_1_title_content.get_frect(center = ((w / 2), 660))

        self.title2 = font.render("Stock", False, "White")
        self.title2_rect = self.title2.get_frect(center = (w / 2, 730))
        self.title2_content = font.render(f"{0}/{0}", False, "White")
        self.title2_content_rect = self.title2.get_frect(center = ((w / 2) + 37.5, 790))

        self.title2r = font.render("Raw Unit", False, "White")
        self.title2r_rect = self.title2.get_frect(center = ((w / 2) - 37.5, 870))
        self.title2r_content = font.render(f"{0}/{0}", False, "white")
        self.title2r_content_rect = self.title2.get_frect(center = ((w / 2) + 37.5, 930))



    def update(self, wage, product_price, profit, stock, raw, s_max):
        self.wage_content = self.font.render(str(wage), False, "white")
        self.price = self.font.render(str(product_price), False, "white")
        self.info_1_title_content = self.font.render(str(profit), False, "White")
        self.info_1_title_content_rect = self.info_1_title_content.get_frect(center = ((self.w / 2), 660))
        self.title2r_content = self.font.render(str(round(raw)), False, "white")
        self.title2_content = self.font.render(str(round(stock)), False, "white")
        self.title2r_content_rect = self.title2.get_frect(center = ((self.w / 2) + 37.5, 930))
        self.title2_content_rect = self.title2.get_frect(center = ((self.w / 2) + 37.5, 790))

        self.title2r_rect = self.title2.get_frect(center = ((self.w / 2) - 37.5, 870))
        self.title2_rect = self.title2.get_frect(center = (self.w / 2, 730))

class text():
    def __init__(self, w, h, font):
        self.stock_title = font.render("Stock Market", False, "white")