from pygame import *
import os

try:
    from settings import Settings, settings_loop
except ImportError:
    print("УВАГА: файл settings.py не знайдено. Використовуються тестові налаштування.")

    class Settings:
        def __init__(self):
            self.music_enabled = False
            self.volume = 0.5

    def settings_loop(screen, w, h, s):
        print("Відкрито вікно налаштувань (Тест)")

PURPLE = (142, 36, 108)
ORANGE = (225, 108, 68)
BLUE = (85, 118, 201)
WHITE = (255, 255, 255)

BUTTONS = ["ПОЧАТИ", "НАЛАШТУВАННЯ", "ВИХІД"]

class Button:
    def __init__(self, text, font, width, height, pos, round_top=False, round_bottom=False):
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.pos = pos
        self.round_top = round_top
        self.round_bottom = round_bottom
        self.rect = Rect(pos[0], pos[1], width, height)

    def draw(self, screen, selected=False):
        if self.text == "ПОЧАТИ":
            color = ORANGE if selected else PURPLE
        elif self.text == "НАЛАШТУВАННЯ":
            color = ORANGE if selected else BLUE
        else:
            color = ORANGE if selected else BLUE

        border_radius = 20
        top_left = border_radius if self.round_top else 0
        top_right = border_radius if self.round_top else 0
        bottom_left = border_radius if self.round_bottom else 0
        bottom_right = border_radius if self.round_bottom else 0

        draw.rect(screen, color, self.rect,
                  border_top_left_radius=top_left,
                  border_top_right_radius=top_right,
                  border_bottom_left_radius=bottom_left,
                  border_bottom_right_radius=bottom_right)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

def load_sound_safe(path):
    if os.path.exists(path):
        return mixer.Sound(path)
    else:
        class DummySound:
            def play(self): pass

        return DummySound()


def menu_loop(screen_width, screen_height, screen, settings):
    # init() краще викликати в головному блоці, але тут лишимо для надійності
    init()
    display.set_caption("Меню")
    clock = time.Clock()
    mixer.init()

    play_menu_music(settings)

    MENU_CHOICE_SOUND = load_sound_safe('sounds/Menu Choice.mp3')

    font_obj = font.Font(None, 40)
    button_width = 400
    button_height = 70
    gap = 10
    total_height = len(BUTTONS) * button_height + (len(BUTTONS) - 1) * gap
    start_y = (screen_height - total_height) // 2

    buttons = []
    for i, text in enumerate(BUTTONS):
        x = (screen_width - button_width) // 2
        y = start_y + i * (button_height + gap)
        round_top = i == 0
        round_bottom = i == len(BUTTONS) - 1
        buttons.append(Button(text, font_obj, button_width, button_height, (x, y), round_top, round_bottom))

    selected_index = 0

    running = True
    while running:
        screen.fill((30, 30, 30))

        for e in event.get():
            if e.type == QUIT:
                quit()

            if e.type == KEYDOWN:
                if e.key == K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                    MENU_CHOICE_SOUND.play()
                elif e.key == K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                    MENU_CHOICE_SOUND.play()
                elif e.key == K_RETURN:

                    if buttons[selected_index].text == 'ПОЧАТИ':
                        mixer.music.stop()
                        print("Натиснуто: ПОЧАТИ")  # Для тесту
                        return  # Вихід з меню в гру

                    if buttons[selected_index].text == "ВИХІД":
                        quit()

                    if buttons[selected_index].text == 'НАЛАШТУВАННЯ':
                        mixer.music.stop()
                        settings_loop(screen, screen_width, screen_height, settings)
                        play_menu_music(settings)

        for i, button in enumerate(buttons):
            button.draw(screen, selected=(i == selected_index))

        display.flip()
        clock.tick(60)

def play_menu_music(settings):
    if settings.music_enabled:
        path = 'sounds/menu.mp3'
        if os.path.exists(path):
            mixer.music.set_volume(settings.volume)
            mixer.music.load(path)
            mixer.music.play(-1)
        else:
            print(f"Музика не знайдена: {path}")

def stop_music():
    mixer.music.stop()

def start_menu(WIDTH, HEIGHT, screen):
    settings = Settings()
    menu_loop(WIDTH, HEIGHT, screen, settings)
    return settings

if __name__ == "__main__":
    init()
    TEST_WIDTH, TEST_HEIGHT = 800, 600
    test_screen = display.set_mode((TEST_WIDTH, TEST_HEIGHT))

    print("Запуск тестового режиму меню...")

    try:
        final_settings = start_menu(TEST_WIDTH, TEST_HEIGHT, test_screen)
        print("Меню закрито, перехід до гри.")
    except Exception as e:
        print(f"Сталася помилка під час виконання: {e}")