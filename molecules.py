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

AMINO_ACIDS = {
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
}


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
    '''рисует глицин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    h_x, h_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, h_x, h_y)
    draw_atom(surface, h_x, h_y, "H", 7)

def draw_alanine(surface, x, y):
    '''рисует аланин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 45
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")

def draw_phenylalanine(surface, x, y):
    '''рисует фенилаланин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    
    # CB (бета-углерод)
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    
    # бензольное кольцо

    r = 35
    cx, cy = cb_x, cb_y + r + 15 # сдвигает центр вниз на радиус + длина связи
    
    # start_deg=-90 - вершина 0 смотрит строго вверх
    pts = get_poly_points(cx, cy, r, 6, start_deg=-90)
    
    # связь CB - вершина 0
    draw_bond(surface, cb_x, cb_y, pts[0][0], pts[0][1])
    
    # рисует кольцо, двойные связи между вершинами 0-1, 2-3, 4-5
    for i in range(6):
        p1 = pts[i]
        p2 = pts[(i+1)%6]
        is_double = (i % 2 == 0) 
        draw_bond(surface, p1[0], p1[1], p2[0], p2[1], is_double)
    
    # рисует атом CB
    draw_atom(surface, cb_x, cb_y, "C")

def draw_tyrosine(surface, x, y):
    '''рисует тирозин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    
    # CB
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    
    # бензольное кольцо
    r = 35
    cx, cy = cb_x, cb_y + r + 15
    pts = get_poly_points(cx, cy, r, 6, start_deg=-90)
    
    # связь CB - вершина 0
    draw_bond(surface, cb_x, cb_y, pts[0][0], pts[0][1])
    
    # рисует кольцо
    for i in range(6):
        p1 = pts[i]
        p2 = pts[(i+1)%6]
        is_double = (i % 2 == 0)
        draw_bond(surface, p1[0], p1[1], p2[0], p2[1], is_double)
        
    # OH группа к кольцу (вершина 3)
    oh_x, oh_y = pts[3][0], pts[3][1] + 30
    draw_bond(surface, pts[3][0], pts[3][1], oh_x, oh_y)
    draw_atom(surface, oh_x, oh_y, "O")
    
    # водород при OH
    h_x, h_y = oh_x + 20, oh_y
    draw_bond(surface, oh_x, oh_y, h_x, h_y)
    draw_atom(surface, h_x, h_y, "H", 7)

    # рисует атом CB
    draw_atom(surface, cb_x, cb_y, "C")

def draw_tryptophan(surface, x, y):
    '''рисует триптофан'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    
    # CB
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    # рисует индол
    # C1 - верхняя точка пиррольного кольца, куда приходит связь от CB
    c1_x, c1_y = cb_x, cb_y + 30
    draw_bond(surface, cb_x, cb_y, c1_x, c1_y)
    
    # размеры пиррольного кольца
    pyrrole_w = 25 # половина ширины
    pyrrole_h = 35 # высота
    
    # координаты 5-членного пиррольного цикла
    # c1 (верхний), c2 (левый), n1 (азот пиррольного кольца), c3 (правый перед N), c4 (правый)
    
    p_c1   = (c1_x, c1_y) # C1
    p_c4 = (c1_x + pyrrole_w, c1_y + 15) # C4 (общий с бензолом)
    p_c3 = (c1_x + pyrrole_w, c1_y + 45) # C3 (общий с бензолом)
    p_n1 = (c1_x - pyrrole_w + 5, c1_y + 45) # N1
    p_c2  = (c1_x - pyrrole_w, c1_y + 15) # C2
    
    # рисует пиррол
    draw_bond(surface, p_c1[0], p_c1[1], p_c2[0], p_c2[1], True)  # C1=C2 (двойная)
    draw_bond(surface, p_c2[0], p_c2[1], p_n1[0], p_n1[1])    # C2-N1
    draw_bond(surface, p_n1[0], p_n1[1], p_c3[0], p_c3[1])  # N1-C3
    draw_bond(surface, p_c3[0], p_c3[1], p_c4[0], p_c4[1], True) # C3=C4 (общая с бензолом, двойная)
    draw_bond(surface, p_c4[0], p_c4[1], p_c1[0], p_c1[1])      # C4-C1
    
    # рисует N в вершине p_n1
    draw_atom(surface, p_n1[0], p_n1[1], "N")
    # H при азоте
    nh_x, nh_y = p_n1[0] - 15, p_n1[1] + 10
    draw_bond(surface, p_n1[0], p_n1[1], nh_x, nh_y)
    draw_atom(surface, nh_x, nh_y, "H", 7)
    
    # бензольное кольцо (6-членное) приклеено справа к грани p_с4 - p_с3
    # рисует 4 вершины справа
    benz_w = 30 #размер шага в кольце
    # верхняя вершина бензола
    b_top = (p_c4[0] + benz_w//2, p_c4[1] - 20)
    # правая верхняя
    b_top_r = (p_c4[0] + benz_w, p_c4[1] - 10)
    # правая нижняя
    b_bot_r = (p_c4[0] + benz_w, p_c3[1] + 10)
    # нижняя
    b_bot = (p_c4[0] + benz_w//2, p_c3[1] + 20)
    
    # cвязи бензола
    # p_c4 - b_top
    draw_bond(surface, p_c4[0], p_c4[1], b_top[0], b_top[1])
    # b_top - b_top_r (=)
    draw_bond(surface, b_top[0], b_top[1], b_top_r[0], b_top_r[1], True)
    # b_top_r - b_bot_r
    draw_bond(surface, b_top_r[0], b_top_r[1], b_bot_r[0], b_bot_r[1])
    # b_bot_r - b_bot (=)
    draw_bond(surface, b_bot_r[0], b_bot_r[1], b_bot[0], b_bot[1], True)
    # b_bot - p_c3 
    draw_bond(surface, b_bot[0], b_bot[1], p_c3[0], p_c3[1])

def draw_histidine(surface, x, y):
    '''рисует гистидин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    

    cx, cy = cb_x, cb_y + 45
    r = 30
    pts = get_poly_points(cx, cy, r, 5, start_deg=-90)

    draw_bond(surface, cb_x, cb_y, pts[0][0], pts[0][1])
    
    # Контур кольца
    draw_bond(surface, pts[0][0], pts[0][1], pts[1][0], pts[1][1])

    draw_bond(surface, pts[1][0], pts[1][1], pts[2][0], pts[2][1], True)

    draw_bond(surface, pts[2][0], pts[2][1], pts[3][0], pts[3][1])

    draw_bond(surface, pts[3][0], pts[3][1], pts[4][0], pts[4][1])

    draw_bond(surface, pts[4][0], pts[4][1], pts[0][0], pts[0][1], True)
    

    draw_atom(surface, pts[1][0], pts[1][1], "N") 
    draw_atom(surface, pts[3][0], pts[3][1], "N") 
    
    h_x, h_y = pts[3][0] - 20, pts[3][1] + 10
    draw_bond(surface, pts[3][0], pts[3][1], h_x, h_y)
    draw_atom(surface, h_x, h_y, "H", 7)

def draw_valine(surface, x, y):
    '''рисует валин'''
    pos = draw_backbone(surface, x, y)

    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    c1_x, c1_y = cb_x - 30, cb_y + 35
    c2_x, c2_y = cb_x + 30, cb_y + 35
    draw_bond(surface, cb_x, cb_y, c1_x, c1_y)
    draw_bond(surface, cb_x, cb_y, c2_x, c2_y)
    draw_atom(surface, c1_x, c1_y, "C")
    draw_atom(surface, c2_x, c2_y, "C")

def draw_leucine(surface, x, y):
    '''рисует лейцин'''
    pos = draw_backbone(surface, x, y)

    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")

    cg_x, cg_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")

    c1_x, c1_y = cg_x - 30, cg_y + 35
    c2_x, c2_y = cg_x + 30, cg_y + 35
    draw_bond(surface, cg_x, cg_y, c1_x, c1_y)
    draw_bond(surface, cg_x, cg_y, c2_x, c2_y)
    draw_atom(surface, c1_x, c1_y, "C")
    draw_atom(surface, c2_x, c2_y, "C")

def draw_isoleucine(surface, x, y):
    '''рисует изолейцин'''
    pos = draw_backbone(surface, x, y)

    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg2_x, cg2_y = cb_x - 30, cb_y + 35
    draw_bond(surface, cb_x, cb_y, cg2_x, cg2_y)
    draw_atom(surface, cg2_x, cg2_y, "C")
    
    cg1_x, cg1_y = cb_x + 30, cb_y + 35
    draw_bond(surface, cb_x, cb_y, cg1_x, cg1_y)
    draw_atom(surface, cg1_x, cg1_y, "C")
    
    cd1_x, cd1_y = cg1_x + 25, cg1_y + 35
    draw_bond(surface, cg1_x, cg1_y, cd1_x, cd1_y)
    draw_atom(surface, cd1_x, cd1_y, "C")

def draw_proline(surface, x, y):
    '''рисует пролин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    n_x, n_y = pos["N"]
    
    cb_x, cb_y = ca_x, ca_y + 40
    cd_x, cd_y = n_x, n_y + 40
    cg_x, cg_y = (cb_x + cd_x) // 2, cb_y + 25
    
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_bond(surface, cg_x, cg_y, cd_x, cd_y)
    draw_bond(surface, cd_x, cd_y, n_x, n_y)

def draw_serine(surface, x, y):
    '''рисует серин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    o_x, o_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, o_x, o_y)
    draw_atom(surface, o_x, o_y, "O")

def draw_threonine(surface, x, y):
    '''рисует треонин'''
    pos = draw_backbone(surface, x, y)
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x + 20, ca_y + 35
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    o_x, o_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, o_x, o_y)
    draw_atom(surface, o_x, o_y, "O")
    c_x, c_y = ca_x - 20, ca_y + 45
    draw_bond(surface, ca_x, ca_y, c_x, c_y)
    draw_atom(surface, c_x, c_y, "C")

def draw_cysteine(surface, x, y):
    '''рисует цистеин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    s_x, s_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, s_x, s_y)
    draw_atom(surface, s_x, s_y, "S")

def draw_methionine(surface, x, y):
    '''рисует метионин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x + 35, cb_y + 35
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    s_x, s_y = cg_x + 35, cg_y
    draw_bond(surface, cg_x, cg_y, s_x, s_y)
    draw_atom(surface, s_x, s_y, "S")
    
    ce_x, ce_y = s_x + 35, s_y
    draw_bond(surface, s_x, s_y, ce_x, ce_y)
    draw_atom(surface, ce_x, ce_y, "C")

def draw_asparagine(surface, x, y):
    '''рисует аспарагин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    o_x, o_y = cg_x - 30, cg_y + 30
    n_x, n_y = cg_x + 30, cg_y + 30
    draw_bond(surface, cg_x, cg_y, o_x, o_y, double=True)
    draw_bond(surface, cg_x, cg_y, n_x, n_y)
    draw_atom(surface, o_x, o_y, "O")
    draw_atom(surface, n_x, n_y, "N")

def draw_glutamine(surface, x, y):
    '''рисует глутамин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]

    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    cd_x, cd_y = cg_x, cg_y + 40
    draw_bond(surface, cg_x, cg_y, cd_x, cd_y)
    draw_atom(surface, cd_x, cd_y, "C")
    
    o_x, o_y = cd_x - 30, cd_y + 30
    n_x, n_y = cd_x + 30, cd_y + 30
    draw_bond(surface, cd_x, cd_y, o_x, o_y, double=True)
    draw_bond(surface, cd_x, cd_y, n_x, n_y)
    draw_atom(surface, o_x, o_y, "O")
    draw_atom(surface, n_x, n_y, "N")

def draw_aspartate(surface, x, y):
    '''рисует аспартат'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    o1_x, o1_y = cg_x - 30, cg_y + 30
    o2_x, o2_y = cg_x + 30, cg_y + 30
    draw_bond(surface, cg_x, cg_y, o1_x, o1_y, double=True)
    draw_bond(surface, cg_x, cg_y, o2_x, o2_y)
    draw_atom(surface, o1_x, o1_y, "O")
    draw_atom(surface, o2_x, o2_y, "O")

def draw_glutamate(surface, x, y):
    '''рисует глутамат'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 40
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 40
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    cd_x, cd_y = cg_x, cg_y + 40
    draw_bond(surface, cg_x, cg_y, cd_x, cd_y)
    draw_atom(surface, cd_x, cd_y, "C")
    
    o1_x, o1_y = cd_x - 30, cd_y + 30
    o2_x, o2_y = cd_x + 30, cd_y + 30
    draw_bond(surface, cd_x, cd_y, o1_x, o1_y, double=True)
    draw_bond(surface, cd_x, cd_y, o2_x, o2_y)
    draw_atom(surface, o1_x, o1_y, "O")
    draw_atom(surface, o2_x, o2_y, "O")

def draw_lysine(surface, x, y):
    '''рисует лизин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 35
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 35
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    cd_x, cd_y = cg_x, cg_y + 35
    draw_bond(surface, cg_x, cg_y, cd_x, cd_y)
    draw_atom(surface, cd_x, cd_y, "C")
    
    ce_x, ce_y = cd_x, cd_y + 35
    draw_bond(surface, cd_x, cd_y, ce_x, ce_y)
    draw_atom(surface, ce_x, ce_y, "C")
    
    n_x, n_y = ce_x, ce_y + 35
    draw_bond(surface, ce_x, ce_y, n_x, n_y)
    draw_atom(surface, n_x, n_y, "N")

def draw_arginine(surface, x, y):
    '''рисует аргинин'''
    pos = draw_backbone(surface, x, y)
    
    ca_x, ca_y = pos["CA"]
    cb_x, cb_y = ca_x, ca_y + 35
    draw_bond(surface, ca_x, ca_y, cb_x, cb_y)
    draw_atom(surface, cb_x, cb_y, "C")
    
    cg_x, cg_y = cb_x, cb_y + 35
    draw_bond(surface, cb_x, cb_y, cg_x, cg_y)
    draw_atom(surface, cg_x, cg_y, "C")
    
    cd_x, cd_y = cg_x, cg_y + 35
    draw_bond(surface, cg_x, cg_y, cd_x, cd_y)
    draw_atom(surface, cd_x, cd_y, "C")
    
    c_x, c_y = cd_x, cd_y + 35
    draw_bond(surface, cd_x, cd_y, c_x, c_y)
    draw_atom(surface, c_x, c_y, "C")
    
    n1_x, n1_y = c_x - 25, c_y + 25
    n2_x, n2_y = c_x + 25, c_y + 25
    draw_bond(surface, c_x, c_y, n1_x, n1_y)
    draw_bond(surface, c_x, c_y, n2_x, n2_y)
    draw_atom(surface, n1_x, n1_y, "N")
    draw_atom(surface, n2_x, n2_y, "N")

