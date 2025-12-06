# ui.py
import pygame
from settings import *

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.txt_surface = self.font.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        """Обрабатывает нажатия на мышь и клавиатуру"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active

            else:
                self.active = False
            self.color = BLUE if self.active else GRAY

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    result = self.text
                    return result
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 30:
                        self.text += event.unicode
                
                self.txt_surface = self.font.render(self.text, True, BLACK)

        return None


    def draw(self, screen):
        """Рисует поле ввода"""
        pygame.draw.rect(screen, self.color, self.rect, 3)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 3, self.rect.y + 3, 
                                         self.rect.width - 6, self.rect.height - 6))
        
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 8))
        
        
    def clear(self):
        """Очищает поле ввода"""
        self.text = ""
        self.txt_surface = self.font.render("", True, BLACK)

