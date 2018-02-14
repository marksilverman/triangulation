from enum import Enum

class dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class state(Enum):
    blank = 0
    filled = 1
    frozen = 2

class triangle():
    next_id = 0

    def __init__(self):
        self.parent = self.child = self.left = self.right = None
        self.xleft = self.xright = self.xmiddle = self.ybottom = self.ytop = 0
        self.state = state.blank
        self.answer = False
        self.direction = dir.UP
        self.xy = None
        self.id = triangle.next_id
        triangle.next_id += 1

    def outline(self, canvas):
        canvas.create_polygon(self.xy, outline="SlateBlue1", fill="", width=6)

    def draw(self, canvas, color, mytags):
        self.tags = mytags
        canvas.create_polygon(self.xy, outline="black", fill=color, activefill="gold", width=3, tags=mytags)

    def toggle(self, which, play_mode):
        if (which == dir.LEFT):
            if  (self.state == state.filled):
                self.state = state.blank
            else:
                self.state = state.filled
        elif (which == dir.RIGHT):
            if (self.state == state.frozen):
                self.state = state.blank
            else:
                self.state = state.frozen
        if (play_mode == False):
            if (self.state == state.filled):
                self.answer = 1
            else:
                self.answer = 0

