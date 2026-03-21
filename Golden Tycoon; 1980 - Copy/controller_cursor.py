import pygame

class cursor(pygame.sprite.Sprite):
    def __init__(self, width, height, groups):
        super().__init__(groups)
        self.screen_w = width
        self.screen_h = height
        self.direction = pygame.math.Vector2(0,0) 
        self.speed = 1500 / 2
        self.image = pygame.image.load("cursor.png").convert()
        self.rect = self.image.get_frect(center = (width / 2, height / 2))

    def move(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        self.rect.center += self.direction * self.speed * dt