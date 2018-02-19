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

class cmd():
    play_mode = False
    queue = []
    idx = -1
    def __init__(self, node, new_state):
        if (node.state == new_state):
            return
        self.node = node
        self.old_state = node.state
        self.new_state = new_state
        node.state = new_state
        while (len(cmd.queue) > cmd.idx + 1):
            cmd.queue.pop()
        cmd.queue.append(self)
        cmd.idx += 1

    @staticmethod
    def reset():
        while len(cmd.queue): cmd.queue.pop()
        cmd.idx = -1

    @staticmethod
    def undo():
        if (cmd.idx < 0): return
        this_cmd = cmd.queue[cmd.idx]
        this_cmd.node.state = this_cmd.old_state
        cmd.idx -= 1

    @staticmethod
    def redo():
        print("redo")
        if (cmd.idx + 1 >= len(cmd.queue)): return
        cmd.idx += 1
        this_cmd = cmd.queue[cmd.idx]
        this_cmd.node.state = this_cmd.new_state

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

    def freeze(self):
        cmd(self, state.frozen)
        if (cmd.play_mode == False): self.answer = False

    def fill(self):
        cmd(self, state.filled)
        if (cmd.play_mode == False): self.answer = True

    def blank(self):
        cmd(self, state.blank)
        if (cmd.play_mode == False): self.answer = False

    def isFrozen(self): return self.state == state.frozen
    def isFilled(self): return self.state == state.filled
    def isBlank(self): return self.state == state.blank
    def isNotFrozen(self): return self.state != state.frozen
    def isNotFilled(self): return self.state != state.filled
    def isNotBlank(self): return self.state != state.blank

    def outline(self, canvas):
        canvas.create_polygon(self.xy, outline="SlateBlue1", fill="", width=6)

    def draw(self, canvas, color, mytags):
        self.tags = mytags
        canvas.create_polygon(self.xy, outline="black", fill=color, activefill="gold", width=3, tags=mytags)

    def toggle(self, which):
        if (which == dir.LEFT):
            if  (self.isFilled()):
                self.blank()
            else:
                self.fill()
        elif (which == dir.RIGHT):
            if (self.isFrozen()):
                self.blank()
            else:
                self.freeze()
