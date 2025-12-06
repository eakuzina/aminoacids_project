# main.py
import pygame
import random
from settings import *
#from molecules import AMINO_ACIDS, draw_amino_acid
from ui import InputBox

MESSAGE_DURATION_MS = 1500  # 1.5 секунды

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(FONT_NAME, 36, bold=True)
    font_small = pygame.font.SysFont(FONT_NAME, SMALL_FONT)
    font_1 = pygame.font.SysFont(FONT_NAME, 20)

    # Список всех аминокислот в случайном порядке
    '''keys = list(AMINO_ACIDS.keys())
    random.shuffle(keys)'''

    current_index = 0
    score = 0
    message = ""
    message_color = BLACK
    message_timer_ms = 0  

    # Поле ввода
    input_box = InputBox(WIDTH // 2 - 150, 550, 300, 50)

    # Текущая аминокислота
    #current_key = keys[current_index]

    running = True
    while running:
        dt = clock.tick(FPS)
        #обновляем таймер сообщения
        if message:
            message_timer_ms += dt
            '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            result = input_box.handle_event(event)

            if result is not None:
                user_answer = result.lower().strip()

                is_correct = (user_answer == current_key)

                if is_correct:
                    score += 1
                    message = f"ВЕРНО! Это {current_key.upper()}"
                    message_color = GREEN
                else:
                    message = f"НЕВЕРНО! Это {current_key.upper()}"
                    message_color = RED

                #следующеая аминокислота
                current_index = (current_index + 1) % len(keys)
                current_key = keys[current_index]
                input_box.clear()
                # перезапуск таймера
                message_timer_ms = 0 

'''
        # Отрисовка
        screen.fill(BG_COLOR)

        # Заголовок
        title_text = font_title.render("Угадай аминокислоту!", True, DARK_BLUE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 15))

        # Область для молекулы
        frame_rect = pygame.Rect(WIDTH // 2 - 200, 90, 400, 340)
        pygame.draw.rect(screen, DARK_BLUE, frame_rect, 3)

        #draw_amino_acid(screen, current_key, WIDTH // 2, 230)

        # Поле ввода
        input_box.draw(screen)

        '''     # Счёт
        score_text = font_small.render(f"Счёт: {score}/{len(keys)}", True, DARK_BLUE)
        screen.blit(score_text, (20, 15))
'''

        text1 = font_1.render(
            "Введите название аминокислоты и нажмите Enter",
            True,
            GRAY,
        )
        screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 510))

        # Окно с результатом (держим минимум MESSAGE_DURATION_MS)
        if message and message_timer_ms < MESSAGE_DURATION_MS:
            msg_text = font_small.render(message, True, message_color)
            msg_bg_rect = pygame.Rect(
                WIDTH // 2 - msg_text.get_width() // 2 - 20,
                450,
                msg_text.get_width() + 40,
                msg_text.get_height() + 10,
            )
            pygame.draw.rect(screen, WHITE, msg_bg_rect)
            pygame.draw.rect(screen, message_color, msg_bg_rect, 3)
            screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, 455))

        pygame.display.flip()

    #pygame.quit()
    #print(f"Игра закончена. Финальный счёт: {score}/{len(keys)}")


if __name__ == "__main__":
    main()



#СПИСОК АМИНОКИСЛОТ AMINO_ACIDS И ИХ ОТРИСОВКА draw_amino_acid.