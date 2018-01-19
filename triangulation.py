from tkinter import *
from tkinter import filedialog
import math

length = 40
altitude = length * math.sqrt(3) / 2.0
half_length = length // 2
w = 900
h = 700
hw = w // 2
hh = h // 2

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

UNFILLED = 0
FILLED = 1
FROZEN = 2

class triangle():
    next_id = 0
    def __init__(self):
        self.parent = self.child = self.left = self.right = None
        self.state = UNFILLED
        self.selected = 0
        self.dir = UP
        self.id = triangle.next_id
        triangle.next_id += 1

class triangulation(Frame):
    def key(self, event):
        k = repr(event.keysym)
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'a'"): self.add()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'i'"): self.insert()
        if (k == "'h'"):
           if (self.hide == True): self.hide = False
           else: self.hide = True
        if (k == "'r'"): self.more_rows()
        if (k == "'R'"): self.fewer_rows()
        if (k == "'Left'"):
            if (self.cursor.left):
                self.cursor = self.cursor.left
            elif (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'Right'"):
            if (self.cursor.right):
                self.cursor = self.cursor.right
            elif (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'Up'"):
            if (self.cursor.parent):
                self.cursor = self.cursor.parent
            elif (self.cursor.right and self.cursor.right.parent):
                self.cursor = self.cursor.right
            elif (self.cursor.left and self.cursor.left.parent):
                self.cursor = self.cursor.left
        if (k == "'Down'"):
            if (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'space'"):
            self.cursor.state += 1
            if (self.cursor.state > 1):
                self.cursor.state = 0
        self.draw()

    def more_rows(self):
        self.rows += 1
        self.tv_rows.set(str(self.rows))

    def fewer_rows(self):
        self.rows -= 1
        self.tv_rows.set(str(self.rows))

    def createWidgets(self):
        self.remove_row = Button(self, text="--")
        self.remove_row["command"] = self.fewer_rows
        self.remove_row.pack({"side": "left"})

        self.row_label = Label(self)
        self.row_label["text"] = "rows:"
        self.row_label.pack({"side": "left"})
        self.rows = 8
        self.tv_rows = StringVar()
        self.tv_rows.set(str(self.rows))
        self.row_count = Label(self)
        self.row_count["textvariable"] = self.tv_rows
        self.row_count.pack({"side": "left"})

        self.add_row = Button(self, text="++")
        self.add_row["command"] = self.more_rows
        self.add_row.pack({"side": "left"})

        self.new_button = Button(self, text="new")
        self.new_button["command"] = self.new
        self.new_button.pack({"side": "left"})

        self.add_button = Button(self, text="add")
        self.add_button["command"] = self.add
        self.add_button.pack({"side": "left"})

        self.open_button = Button(self, text="open")
        self.open_button["command"] = self.open
        self.open_button.pack({"side": "left"})

        self.quit_button = Button(self, text="quit")
        self.quit_button["command"] = self.quit
        self.quit_button.pack({"side": "left"})

        self.canvas = Canvas(self.master, width=w, height=h, bg='white')
        self.canvas.pack({"side": "left"})

    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        master.bind("<Key>", self.key)
        self.new()

    def new(self):
        self.hide = False
        self.cursor = self.top = new_node = parent_node = triangle()
        for row_idx in range(1, self.rows):
            prev_node = None
            node_cnt = 1 + row_idx * 2
            for node_idx in range(0, node_cnt):
                new_node = triangle()
                if (node_idx % 2):
                    new_node.dir = DOWN
                else:
                    new_node.dir = UP
                if (node_idx == 0):
                    start_of_current_row = new_node
                if (prev_node):
                    prev_node.right = new_node
                    new_node.left = prev_node
                prev_node = new_node

                if (node_idx > 0 and node_idx < (node_cnt- 1)):
                    new_node.parent = parent_node
                    parent_node.child = new_node
                    parent_node = parent_node.right
            parent_node = start_of_current_row;
        self.draw()
    
    def add(self):
        node = self.top
        node = node.child.child
        node.state = FILLED
        node = node.child
        node.state = FILLED
        node.left.state = FILLED
        node.right.state = FILLED

    def clear(self):
        node = self.top
        dir = RIGHT
        while(node):
            node.state = UNFILLED
            if (dir == RIGHT):
               if (node.right):
                    node = node.right
               else:
                    node = node.child
                    if (node): node = node.right
                    dir = LEFT
            elif (dir == LEFT):
                if (node.left):
                    node = node.left
                else:
                    node = node.child
                    if (node): node = node.left
                    dir = RIGHT

    def draw(self):
        self.canvas.delete("all")
        node = self.top
        for row_idx in range(0, self.rows):
            start_of_row = node
            dir = UP
            node_idx = 0
            cnt = 0
            while (node):
                x1 = hw - length - (half_length * (row_idx + 1)) + (half_length * node_idx)
                y1 = (row_idx + 2) * altitude
                x2 = x1 + length
                y2 = y1
                x3 = x1 + half_length
                y3 = y1 - altitude

                if (node.state == FILLED):
                    color = "darkgray"
                    cnt += 1
                elif (node.state == UNFILLED):
                    color = "white"
                elif (node.state == FROZEN):
                    color = "pink"

                if (node == self.cursor):
                    color = "green"
                if (self.hide == True):
                    color = "white"

                if (dir == UP):
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x1, y1, outline="black", fill=color, width=3)
                    dir = DOWN
                else:
                    self.canvas.create_polygon(x1, y3, x2, y3, x3, y1, x1, y3, outline="black", fill=color, width=3)
                    dir = UP
                node = node.right
                node_idx += 1
            
            self.canvas.create_text(hw - 1.3 * length - (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude/2),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.left

        # calculate the totals on the right
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = DOWN
            start_of_row = node
            while (node):
                if (node.state == FILLED):
                    cnt += 1
                if (dir == DOWN):
                    node = node.child
                    dir = LEFT
                else:
                    node = node.left
                    dir = DOWN
            self.canvas.create_text(hw - length + (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.right

        # calculate the totals along the bottom
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = DOWN
            start_of_row = node
            while (node):
                if (node.state == FILLED):
                    cnt += 1
                if (dir == DOWN):
                    node = node.child
                    dir = RIGHT
                else:
                    node = node.right
                    dir = DOWN
            self.canvas.create_text(hw - (half_length/2) + self.rows * half_length - (length * (row_idx + 1)),
                                    (self.rows + 2) * altitude - (altitude / 2),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.left

            # horiz arrow
            self.canvas.create_line(hw - (half_length * self.rows / 2) - 130, self.rows * altitude / 2,
                                    hw - (half_length * self.rows / 2) - 95, self.rows * altitude / 2,
                                    fill="black", width=8, arrow="last", arrowshape=[12,12,8])
            # ne/sw arrow
            self.canvas.create_line(hw + (half_length * self.rows / 2) + 30, ((self.rows - 1) * altitude / 2) - altitude / 2,
                                    hw + (half_length * self.rows / 2), (self.rows + 1) * altitude / 2,
                                    fill="black", width=8, arrow="last", arrowshape=[12,12,8])
            # nw/se arrow
            self.canvas.create_line(hw - 15, (self.rows + 3) * altitude,
                                    hw - 35, (self.rows + 2) * altitude,
                                    fill="black", width=8, arrow="last", arrowshape=[12,12,8])

        # self.canvas.after(1, self.draw)

    def insert(self):
        node = self.cursor
        node.state = FILLED
        if (node.dir == DOWN):
            if (node.parent and node.parent.left and node.parent.right):
                node.parent.state = node.parent.left.state = node.parent.right.state = FILLED
            elif (node.parent and node.left and node.right):
                node.parent.state = node.left.state = node.right.state = FILLED
            elif (node.right and node.right.right and node.right.parent):
                node.right.state = node.right.right.state = node.right.parent.state = FILLED
            elif (node.left and node.left.left and node.left.parent):
                node.left.state = node.left.left.state = node.left.parent.state = FILLED
        elif (node.dir == UP):
            if (node.child and node.child.left and node.child.right):
                node.child.state = node.child.left.state = node.child.right.state = FILLED
            elif (node.child and node.left and node.right):
                node.child.state = node.left.state = node.right.state = FILLED
            elif (node.right and node.right.right and node.right.parent):
                node.right.state = node.right.right.state = node.right.parent.state = FILLED
            elif (node.left and node.left.left and node.left.parent):
                node.left.state = node.left.left.state = node.left.parent.state = FILLED

    def open(self):
        self.canvas.delete("all")

        numeric = re.compile("^[\d,]+$");
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select file")
        f = open(filename, 'r')

        triangle.next_id = 0
        self.rows = 0
        start_of_row = None
        for line in f:
            triangle_list = line.split()
            triangle_cnt = len(triangle_list)
            if (triangle_cnt == 0):
                break
            self.rows = self.rows + 1
            parent_node = start_of_row
            prev_node = None
            for triangle_idx in range(triangle_cnt):
                node = triangle()
                if (triangle_idx == 0):
                    start_of_row = node
                    if (self.rows == 1):
                        self.top = self.cursor = node
                else:
                    node.left = prev_node
                    prev_node.right = node
                    if (triangle_idx < triangle_cnt - 1):
                        node.parent = parent_node
                        parent_node.child = node
                        parent_node = parent_node.right
                s = triangle_list[triangle_idx]
                if (s == '.'):
                    node.state = UNFILLED
                elif (s == "|"):
                    node.state = FROZEN
                else:
                    node.state = FILLED
                prev_node = node
        self.draw()

root = Tk()
app = triangulation(master=root)
app.mainloop()
root.destroy()
