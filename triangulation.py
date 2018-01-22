# triangulation
# a logic puzzle by Mark Silverman
# 2018/01/21
from tkinter import *
from tkinter import filedialog
import math

#up
#11,22,33
#left-bottom,right-bottom,middle-top

#down
#13,23,31
#left-top,right-top,middle-bottom

#x1 leftmost
#x3 middle
#x2 rightmost

#y1 bottom
#y2 = y1
#y3 top

length = 50
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
        self.answer = False
        self.dir = UP
        self.id = triangle.next_id
        triangle.next_id += 1
        self.xleft = self.xright = self.xmiddle = self.ybottom = self.ytop = 0

    def toggle(self, which=LEFT):
        if (which == LEFT):
            if  (self.state == FILLED):
                self.state = UNFILLED
            else:
                self.state = FILLED
        elif (which == RIGHT):
            if (self.state == FROZEN):
                self.state = UNFILLED
            else:
                self.state = FROZEN
        if (triangulation.play_mode == False):
            if (self.state == FILLED):
                self.answer = 1
            else:
                self.answer = 0

class triangulation(Frame):
    play_mode = False

    def left_click(self, event):
        self.click(event, LEFT)

    def right_click(self, event):
        self.click(event, RIGHT)

    def click(self, event, which):
        self.cx = event.x
        self.cy = event.y
        node = self.top
        if (event.y < node.ytop):
            return
        while (node):
            if (event.y > node.ybottom):
                node = node.child
            elif (event.x > node.xright):
                node = node.right
            elif (event.x < node.xleft):
                node = node.left
            else:
                # our bounding box always overlaps two triangles
                # need to see if the the click was above or below the side of the triangle
                # tangent(angle) = opposite / ajacent
                # we know the angle and the length of the ajacent side; need to find the opposite
                if (node.dir == UP):
                    if (event.x > node.xmiddle and node.right):
                        o = node.ybottom - (node.xright - event.x) * math.tan(math.radians(60))
                        if (event.y < o): node = node.right
                    elif (event.x < node.xmiddle and node.left):
                        o = node.ybottom - (event.x - node.xleft) * math.tan(math.radians(60))
                        if (event.y < o): node = node.left
                elif (node.dir == DOWN):
                    if (event.x > node.xmiddle and node.right):
                        o = node.ybottom - (event.x - node.xmiddle) * math.tan(math.radians(60))
                        if (event.y > o): node = node.right
                    elif (event.x < node.xmiddle and node.left):
                        o = node.ybottom - (node.xmiddle - event.x) * math.tan(math.radians(60))
                        if (event.y > o): node = node.left
                node.toggle(which)
                self.cursor = node
                self.draw()
                break
    
    def key(self, event):
        k = repr(event.keysym)
        # print(k)
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'i'"): self.insert()
        if (k == "'s'"): self.save()
        if (k == "'h'"):
           if (self.hide == True): self.hide = False
           else: self.hide = True
        if (k == "'r'"): self.more_rows()
        if (k == "'R'"): self.fewer_rows()
  
        if (k == "'7'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.dir == UP and self.cursor.left): self.cursor = self.cursor.left
            elif (self.cursor.dir == DOWN and self.cursor.parent): self.cursor = self.cursor.parent
        if (k == "'9'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.dir == UP and self.cursor.right): self.cursor = self.cursor.right
            elif (self.cursor.dir == DOWN and self.cursor.parent): self.cursor = self.cursor.parent
        if (k == "'1'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.dir == UP and self.cursor.child): self.cursor = self.cursor.child
            elif (self.cursor.dir == DOWN and self.cursor.left): self.cursor = self.cursor.left
        if (k == "'3'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.dir == UP and self.cursor.child): self.cursor = self.cursor.child
            elif (self.cursor.dir == DOWN and self.cursor.right): self.cursor = self.cursor.right
        if (k == "'Left'" or k == "'4'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.left):
                self.cursor = self.cursor.left
            elif (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'Right'" or k == "'6'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.right):
                self.cursor = self.cursor.right
            elif (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'Up'" or k == "'8'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.parent):
                self.cursor = self.cursor.parent
            elif (self.cursor.right and self.cursor.right.parent):
                self.cursor = self.cursor.right
            elif (self.cursor.left and self.cursor.left.parent):
                self.cursor = self.cursor.left
        if (k == "'Down'" or k == "'2'"):
            if (self.cursor == None): self.cursor = self.top
            if (self.cursor.child):
                self.cursor = self.cursor.child
        if (k == "'space'"):
            if (self.cursor == None): self.cursor = self.top
            self.cursor.toggle()
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

        self.open_button = Button(self, text="open")
        self.open_button["command"] = self.open
        self.open_button.pack({"side": "left"})

        self.save_button = Button(self, text="save")
        self.save_button["command"] = self.save
        self.save_button.pack({"side": "left"})

        self.quit_button = Button(self, text="quit")
        self.quit_button["command"] = self.quit
        self.quit_button.pack({"side": "left"})

        self.play_button = Button(self, text="play")
        self.play_button["command"] = self.play
        self.play_button.pack({"side": "left"})

        self.canvas = Canvas(self.master, width=w, height=h, bg='white')
        self.canvas.pack({"side": "left"})

    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        master.bind("<Key>", self.key)
        master.bind("<Button-1>", self.left_click)
        master.bind("<Button-3>", self.right_click)
        self.new()

    def play(self):
        if (triangulation.play_mode == False):
            triangulation.play_mode = True
            self.play_button.config(text="design")
            self.clear()
        else:
            triangulation.play_mode = False
            self.play_button.config(text="play")
            self.refill()
        self.draw()

    def new(self):
        self.cx = 0
        self.cy = 0
        triangulation.play_mode = False
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
    
    # clears the state but not the answer flag
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

    # sets the fill state based on the answer flag
    def refill(self):
        node = self.top
        dir = RIGHT
        while(node):
            if (node.answer == True):
                node.state = FILLED
            else:
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
        winner = True
        self.canvas.delete("all")
        if (triangulation.play_mode):
            self.canvas.create_text(100, 50, text="play mode", font="12x24")
        else:
            self.canvas.create_text(100, 50, text="design mode", font="12x24")
        node = self.top
        for row_idx in range(0, self.rows):
            start_of_row = node
            node.dir = UP
            node_idx = 0
            cnt = 0
            total_cnt = 0
            while (node):
                x1 = hw - length - (half_length * (row_idx + 1)) + (half_length * node_idx)
                y1 = (row_idx + 2) * altitude
                x2 = x1 + length
                y2 = y1
                x3 = x1 + half_length
                y3 = y1 - altitude

                if (node.answer == True):
                    cnt += 1
                    total_cnt += 1
                    if (triangulation.play_mode == True and node.state != FILLED): winner = False
                elif (triangulation.play_mode == True and node.state == FILLED):
                    winner = False

                if (node.state == FILLED):
                    color = "darkgreen" # "darkgray"
                    if (self.play_mode == True):
                        cnt -= 1
                        total_cnt -= 1
                elif (node.state == UNFILLED):
                    if (self.play_mode):
                        color = "lightgray"
                    else:
                        color = "white"
                elif (node.state == FROZEN):
                    color = "lightblue"

                if (self.hide == True):
                    color = "white"

                node.xleft = x1
                node.xright = x2
                node.xmiddle = x3
                node.ybottom = y1
                node.ytop = y3

                if (node.dir == UP):
                    if (node == self.cursor):
                        clist = ((x1,y1), (x2,y2), (x3, y3))
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x1, y1, outline="black", fill=color, width=3)
                    node = node.right
                    if (node): node.dir = DOWN
                else:
                    if (node == self.cursor):
                        clist = ((x1,y3), (x2,y3), (x3, y1))
                    self.canvas.create_polygon(x1, y3, x2, y3, x3, y1, x1, y3, outline="black", fill=color, width=3)
                    node = node.right
                    if (node): node.dir = UP
                node_idx += 1
            
            color = "black"
            if (cnt < 0):
                color = "red"
            elif (cnt == 0):
                color = "darkgreen"
            self.canvas.create_text(hw - 1.3 * length - (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude/2),
                                    fill=color, text=cnt, font="12x24")
            node = start_of_row.child
            if (node):
                node = node.left

        if (self.cursor and self.hide == False):
            self.canvas.create_polygon(clist, outline="darkred", fill="", width=8)

        if (triangulation.play_mode and winner):
            self.canvas.create_text(100, 100, text="winner!", font="12x24")

        # calculate the totals on the right
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = DOWN
            start_of_row = node
            while (node):
                if (node.answer):
                    cnt += 1
                    total_cnt += 1
                if (node.state == FILLED):
                    if (self.play_mode == True):
                        cnt -= 1
                        total_cnt -= 1
                if (dir == DOWN):
                    node = node.child
                    dir = LEFT
                else:
                    node = node.left
                    dir = DOWN
            color = "black"
            if (cnt < 0):
                color = "red"
            elif (cnt == 0):
                color = "darkgreen"
            self.canvas.create_text(hw - length + (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude),
                                    fill=color, text=cnt, font="12x24")
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
                if (node.answer):
                    cnt += 1
                    total_cnt += 1
                if (node.state == FILLED):
                    if (self.play_mode == True):
                        cnt -= 1
                        total_cnt -= 1
                if (dir == DOWN):
                    node = node.child
                    dir = RIGHT
                else:
                    node = node.right
                    dir = DOWN
            color = "black"
            if (cnt < 0):
                color = "red"
            elif (cnt == 0):
                color = "darkgreen"
            self.canvas.create_text(hw - (half_length/2) + self.rows * half_length - (length * (row_idx + 1)),
                                    (self.rows + 2) * altitude - (altitude / 2),
                                    fill=color, text=cnt, font="12x24")
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

        self.canvas.create_text(100, 150, text="total: " + str(total_cnt), font="12x24")
        # self.canvas.after(1, self.draw)
        # if (self.cx and self.cy):
            # self.canvas.create_oval(self.cx - 5, self.cy - 5, self.cx + 5, self.cy + 5, outline="black", fill="green")

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

        filename = filedialog.askopenfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
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
                    node.answer = True
                prev_node = node
        self.play_mode = True
        self.draw()

    def save(self):
        filename = filedialog.asksaveasfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        f = open(filename, 'w')
        node = self.top
        start_of_row = node
        while (node):
            if (node.state == FILLED):
                f.write(" X")
            else:
                f.write(" .")
            node = node.right
            if (node == None and start_of_row and start_of_row.child and start_of_row.child.left):
                node = start_of_row.child.left
                start_of_row = node
                f.write("\n")
        f.close()

root = Tk()
app = triangulation(master=root)
app.mainloop()
root.destroy()
