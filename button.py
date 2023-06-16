import pygame
import sys

pygame.init()


class Button:
    def __init__(self, text_input, pos, font, base_color, hover_color, selected=False):
        self.text_input = text_input
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = font.render(text_input, True, base_color)
        self.rect = self.text.get_rect(center=pos)
        self.selected = selected

    def update(self, screen):
        screen.blit(self.text, self.rect)

    def check_hover(self, pos):
        if self.selected:
            self.text = self.font.render(self.text_input, True, self.base_color)
            return False
        elif pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
            return True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            return False
