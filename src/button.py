from GUI import *


class Button:
    def __init__(self, center, w, h, text):
        self.center = center
        self.w = w
        self.h = h
        self.text = text

    def draw(self):
        draw_button(self)

    def collide(self, point):
        px, py = point
        cx, cy = self.center
        return cx-self.w/2 < px < cx+self.w/2 and cy-self.h/2 < py < cy+self.h/2
