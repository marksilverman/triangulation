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
vertical_gap = 0
left_gap = 10;
right_gap =0;

_down = 0
_up = 1
_left = 2
_right = 3

_unfilled = 0
_filled = 1
_frozen = 2
# _next_id = 0

class triangle():
    next_id = 0
    def __init__(self):
        global _next_id, _unfilled
        self.parent = self.child = self.left = self.right = None
        self.state = _unfilled
        self.id = triangle.next_id
        self.selected = 0
        triangle.next_id += 1

class triangulation(Frame):
    def key(self, event):
        k = repr(event.keysym)
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'a'"): self.add()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'h'"):
           if (self.hide == True): self.hide = False
           else: self.hide = True
        if (k == "'r'"): self.more_rows()
        if (k == "'R'"): self.fewer_rows()
        if (k == "'Left'"):
            if (self.cursor.left):
                self.cursor = self.cursor.left
            elif (self.cursor.child):
                self.cursor = self.cursor.child.left
        if (k == "'Right'"):
            if (self.cursor.right):
                self.cursor = self.cursor.right
            elif (self.cursor.child):
                self.cursor = self.cursor.child.right
        if (k == "'Up'"):
            if (self.cursor.parent):
                self.cursor = self.cursor.parent
            elif (self.cursor.right and self.cursor.right.parent):
                self.cursor = self.cursor.right.parent
            elif (self.cursor.left and self.cursor.left.parent):
                self.cursor = self.cursor.left.parent
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

    def new(self):
        global _up, _down
        self.hide = False
        self.cursor = self.top = new_node = parent_node = triangle()
        for row_idx in range(1, self.rows):
            prev_node = None
            node_cnt = 1 + row_idx * 2
            for node_idx in range(0, node_cnt):
                new_node = triangle()
                if (node_idx % 2):
                    new_node.dir = _down
                else:
                    new_node.dir = _up
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
        global _unfilled, _filled, _frozen
        node = self.top
        node = node.child.child
        node.state = _filled
        node = node.child
        node.state = _filled
        node.left.state = _filled
        node.right.state = _filled

    def draw(self):
        global hw, length, half_length, altitude, vertical_gap, _unfilled, _filled, _frozen, _up, _down, _left, _right
        self.canvas.delete("all")
        node = self.top
        for row_idx in range(0, self.rows):
            start_of_row = node
            dir = _up
            node_idx = 0
            cnt = 0
            while (node):
                x1 = hw - length - (half_length * (row_idx + 1)) + (half_length * node_idx)
                y1 = (row_idx + 2) * (altitude + vertical_gap)
                x2 = x1 + length
                y2 = y1
                x3 = x1 + half_length
                y3 = y1 - altitude

                if (node.state == _filled):
                    color = "darkgray"
                    cnt += 1
                elif (node.state == _unfilled):
                    color = "white"
                elif (node.state == _frozen):
                    color = "pink"

                if (node == self.cursor):
                    color = "green"
                if (self.hide == True):
                    color = "white"

                if (dir == _up):
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x1, y1, outline="black", fill=color, width=3)
                    dir = _down
                else:
                    self.canvas.create_polygon(x1, y3, x2, y3, x3, y1, x1, y3, outline="black", fill=color, width=3)
                    dir = _up
                node = node.right
                node_idx += 1
            
            self.canvas.create_text(hw - 1.3 * length - (half_length * (row_idx + 1)),
                                    (row_idx + 2) * (altitude + vertical_gap) - (altitude/2),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.left

        # calculate the totals on the right
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = _down
            start_of_row = node
            while (node):
                if (node.state == _filled):
                    cnt += 1
                if (dir == _down):
                    node = node.child
                    dir = _left
                else:
                    node = node.left
                    dir = _down
            self.canvas.create_text(hw - .75 * length + (half_length * (row_idx + 1)),
                                    (row_idx + 2) * (altitude + vertical_gap) - (altitude/2),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.right

        # calculate the totals along the bottom
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = _down
            start_of_row = node
            while (node):
                if (node.state == _filled):
                    cnt += 1
                if (dir == _down):
                    node = node.child
                    dir = _right
                else:
                    node = node.right
                    dir = _down
            self.canvas.create_text(hw - half_length + self.rows * length / 2.0 - (length * (row_idx + 1)),
                                    (self.rows + 2) * (altitude + vertical_gap) - (altitude/2),
                                    text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.left
        # self.canvas.after(1, self.draw)

    def open(self):
        self.canvas.delete("all")

        numeric = re.compile("^[\d,]+$");
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select file")
        f = open(filename, 'r')

        row_num = 0
        for line in f:
            row_num = row_num + 1
            data = line.split()
        
            if (numeric.match(data[1])):
                for i in range(len(data)):
                    self.canvas.create_text(hw - (half_length * row_num) + (length * i),
                                            (row_num + 1) * altitude - (altitude/2), text=data[i], font="12x24")
                # horiz arrow
                self.canvas.create_line(hw - (half_length * row_num / 2) - 130, row_num * altitude / 2,
                                        hw - (half_length * row_num / 2) - 95, row_num * altitude / 2,
                                        fill="black", width=8, arrow="last", arrowshape=[12,12,8])
                # ne/sw arrow
                self.canvas.create_line(hw + (half_length * row_num / 2) + 30, (row_num - 1) * altitude / 2,
                                        hw + (half_length * row_num / 2), (row_num + 1) * altitude / 2,
                                        fill="black", width=8, arrow="last", arrowshape=[12,12,8])
                # nw/se arrow
                self.canvas.create_line(hw - 30, (row_num + 2) * altitude,
                                        hw - 55, (row_num + 1) * altitude,
                                        fill="black", width=8, arrow="last", arrowshape=[12,12,8])
                break
            
            up = 1
            triangle_list = data[1:-1]
            triangle_cnt = len(triangle_list)
            for triangle_idx in range(triangle_cnt):
                x1 = hw - length - (half_length * row_num) + (half_length * triangle_idx)
                y1 = (row_num + 1) * (altitude + vertical_gap)
                x2 = x1 + length
                y2 = y1
                x3 = x1 + half_length
                y3 = y1 - altitude

                triangle = triangle_list[triangle_idx]
                if (triangle == '.'):
                    color = "white"
                elif (triangle == "|"):
                    color = "pink"
                else:
                    color = "darkgray"

                if (triangle_idx == 0):
                    self.canvas.create_text(x1 - half_length // 2, y1 - (altitude/2), text=data[0], font="12x24")

                if (up == 1):
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x1, y1, outline="black", fill=color, width=3)
                    up = 0
                else:
                    self.canvas.create_polygon(x1, y3, x2, y3, x3, y1, x1, y3, outline="black", fill=color, width=3)
                    up = 1

                if (triangle_idx == triangle_cnt - 1):
                    self.canvas.create_text(x1 + 1.3 * length, y1 - (altitude/2), text=data[-1], font="12x24")

root = Tk()
app = triangulation(master=root)
app.mainloop()
root.destroy()
