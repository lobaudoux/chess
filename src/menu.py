from GUI import *
from button import *


class Menu:
    def __init__(self, button_texts):
        self.visible = False
        n_buttons = len(button_texts)
        centers = []
        for i in range(1, n_buttons+1):
            centers.append((board_x/2, board_y*(i+MENU_OFFSET/2)/(n_buttons+1+MENU_OFFSET)))
        self.buttons = [Button(centers[i], BUTTON_WIDTH, BUTTON_HEIGHT, button_texts[i]) for i in range(len(button_texts))]

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self):
        if self.visible:
            draw_menu(self)

    def collide(self, point):
        for button in self.buttons:
            if button.collide(point):
                return button

    def is_visible(self):
        return self.visible
