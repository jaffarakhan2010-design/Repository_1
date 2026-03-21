import pygame

class Play_Button():
    def __init__(self, font, win_w, win_h):
        self.text = font.render("Play", False, 'White')
        self.rect = self.text.get_frect(center = (win_w / 2, win_h / 2))
class Exit_Button():
    def __init__(self, font, win_w, win_h):
        self.text = font.render("Exit", False, "white")
        self.rect = self.text.get_frect(center = (win_w / 2, (win_h / 2) + 100))