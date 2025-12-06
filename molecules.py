# molecules.py
import pygame
import math
from settings import *

# Цвета атомов в молекуле
ELEMENT_COLORS = {
    "C": (80, 80, 80),       # Углерод
    "N": (50, 100, 200),     # Азот
    "O": (200, 50, 50),      # Кислород
    "H": (220, 220, 220),    # Водород
    "S": (220, 180, 0),      # Сера
}

'''AMINO_ACIDS = {
    "аланин": "draw_alanine",
    "глицин": "draw_glycine",
    "валин": "draw_valine",
    "лейцин": "draw_leucine",
    "изолейцин": "draw_isoleucine",
    "пролин": "draw_proline",
    "фенилаланин": "draw_phenylalanine",
    "триптофан": "draw_tryptophan",
    "серин": "draw_serine",
    "треонин": "draw_threonine",
    "цистеин": "draw_cysteine",
    "метионин": "draw_methionine",
    "аспарагин": "draw_asparagine",
    "глутамин": "draw_glutamine",
    "аспартат": "draw_aspartate",
    "глутамат": "draw_glutamate",
    "лизин": "draw_lysine",
    "аргинин": "draw_arginine",
    "гистидин": "draw_histidine",
    "тирозин": "draw_tyrosine",
}'''

AMINO_ACIDS = {
    "глицин": "draw_glycine" }


def draw_atom(surface, x, y, element, r=10):
    '''рисует атом в виде круга с подписью'''
    # рисует круг атома
    color = ELEMENT_COLORS.get(element, (150, 150, 150))
    pygame.draw.circle(surface, color, (x, y), r)
    pygame.draw.circle(surface, BLACK, (x, y), r, 2)
    
    # создаёт подпись атома
    label = element
    font = pygame.font.SysFont("arial", 11, bold=True)
    text_color = WHITE if element != "H" else BLACK
    text = font.render(label, True, text_color)
    rect = text.get_rect(center=(x, y))
    surface.blit(text, rect)

def draw_bond(surface, x1, y1, x2, y2, double=False):
    '''рисует связи'''
    if double:
        # рисование двойной связи
        dx = (y2 - y1) * 0.08
        dy = (x2 - x1) * 0.08
        pygame.draw.line(surface, BLACK, (x1 + dx, y1 - dy), (x2 + dx, y2 - dy), 2)
        pygame.draw.line(surface, BLACK, (x1 - dx, y1 + dy), (x2 - dx, y2 + dy), 2)
    else:
        # рисование одинарной связи
        pygame.draw.line(surface, BLACK, (x1, y1), (x2, y2), 3)

def draw_backbone(surface, x, y):
    '''Рисует общий скелет аминокислоты N-C-C'''
    positions = {}
    
    ca_x, ca_y = x, y
    positions["CA"] = (ca_x, ca_y)  # координаты альфа-углерода
    
    n_x, n_y = ca_x - 60, ca_y
    positions["N"] = (n_x, n_y)
    
    c_x, c_y = ca_x + 60, ca_y
    positions["C"] = (c_x, c_y)

    # рисует связи скелета от альфа-C
    draw_bond(surface, n_x, n_y, ca_x, ca_y)
    draw_bond(surface, ca_x, ca_y, c_x, c_y)
    
    # рисует связь C=O скелета
    o1_x, o1_y = c_x, c_y - 50
    draw_bond(surface, c_x, c_y, o1_x, o1_y, double=True)
    
    # рисует связь C-OH скелета
    oh_x, oh_y = c_x + 40, c_y + 20
    draw_bond(surface, c_x, c_y, oh_x, oh_y)
    
    # рисует связь с H при альфа-C
    ha_x, ha_y = ca_x, ca_y - 40
    draw_bond(surface, ca_x, ca_y, ha_x, ha_y)
    
    # рисует связи 2 H при N
    hn1_x, hn1_y = n_x - 30, n_y - 20
    hn2_x, hn2_y = n_x - 30, n_y + 20
    draw_bond(surface, n_x, n_y, hn1_x, hn1_y)
    draw_bond(surface, n_x, n_y, hn2_x, hn2_y)
    
    # рисует связь H при OH
    hoh_x, hoh_y = oh_x + 20, oh_y
    draw_bond(surface, oh_x, oh_y, hoh_x, hoh_y)

    # Рисуем атомы поверх связей
    draw_atom(surface, ca_x, ca_y, "C")
    draw_atom(surface, n_x, n_y, "N")
    draw_atom(surface, c_x, c_y, "C")
    draw_atom(surface, o1_x, o1_y, "O")
    draw_atom(surface, oh_x, oh_y, "O")
    draw_atom(surface, ha_x, ha_y, "H", 7)
    draw_atom(surface, hn1_x, hn1_y, "H", 7)
    draw_atom(surface, hn2_x, hn2_y, "H", 7)
    draw_atom(surface, hoh_x, hoh_y, "H", 7)
    
    return positions

def get_poly_points(cx, cy, r, sides, start_deg=0):
    '''функция для создания списка вершин правильного многоугольника'''
    points = []
    for i in range(sides):
        angle = math.radians(start_deg + i * (360 / sides))
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    return points

def draw_amino_acid(surface, name, x, y):
    '''отрисовка аминокислоты'''
    func_name = AMINO_ACIDS.get(name)
    if func_name:
        globals()[func_name](surface, x, y)

def draw_glycine(surface, x, y):
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    h_x, h_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, h_x, h_y)
    draw_atom(surface, h_x, h_y, "H", 7)
