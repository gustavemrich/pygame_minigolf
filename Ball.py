import pygame

class Ball:
    def __init__(self, position, radius) -> None:
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.color = "white"
        self.radius = radius