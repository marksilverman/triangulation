# triangulation
# a logic puzzle by Mark Silverman
# 2018/01/21
from tkinter import *
from tkinter import filedialog
import math
import random
from enum import Enum

length = 40
altitude = length * math.sqrt(3) / 2.0
half_length = length // 2
canvas_width = 900
canvas_height = 700
center_x = canvas_width // 2

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class state(Enum):
    empty = 0
    filled = 1
    frozen = 2

def random_color():
    return "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')

class triangle():
    next_id = 0

    def __init__(self):
        self.parent = self.child = self.left = self.right = None
        self.xleft = self.xright = self.xmiddle = self.ybottom = self.ytop = 0
        self.state = state.empty
        self.answer = False
        self.dir = UP
        self.xy = None
        self.id = triangle.next_id
        triangle.next_id += 1

    def outline(self, canvas):
        canvas.create_polygon(self.xy, outline="SlateBlue1", fill="", width=6)

    def draw(self, canvas, color, mytags):
        canvas.create_polygon(self.xy, outline="black", fill=color, activefill="gold", width=3, tags=mytags)

    def toggle(self, which=LEFT):
        if (which == LEFT):
            if  (self.state == state.filled):
                self.state = state.empty
            else:
                self.state = state.filled
        elif (which == RIGHT):
            if (self.state == state.frozen):
                self.state = state.empty
            else:
                self.state = state.frozen
        if (triangulation.play_mode == False):
            if (self.state == state.filled):
                self.answer = 1
            else:
                self.answer = 0

class triangulation(Frame):
    play_mode = False

    def click(self, event):
        self.cursor = None
        self.draw()

    def left_click(self, event, node):
        self.cursor = None
        node.toggle(LEFT)
        self.draw()

    def right_click(self, event, node):
        self.cursor = None
        node.toggle(RIGHT)
        self.draw()

    def rotate(self):
        if (self.row_list == self.a_rows):
            self.row_list = self.b_rows
        elif (self.row_list == self.b_rows):
            self.row_list = self.c_rows
        else:
            self.row_list = self.a_rows
        self.draw()

    def key(self, event):
        k = repr(event.keysym)
        if (k == "'r'"):
            self.rotate()
            return
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'i'"): self.insert()
        if (k == "'s'"): self.save()
        if (k == "'p'"): self.play()
        if (k == "'l'"):
            msg = "triangulation"
            for i in range(0, len(msg)):
                self.scroll(msg[i:i+1])
        if (k == "'h'"):
           if (self.hide == True): self.hide = False
           else: self.hide = True
        if (k == "'equal'" or k == "'plus'"): self.more_rows()
        if (k == "'minus'" or k == "'underscore'"): self.fewer_rows()
  
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
            self.cursor.toggle(LEFT)
        if (k == "'f'"):
            if (self.cursor == None): self.cursor = self.top
            self.cursor.toggle(RIGHT)
        self.draw()

    def more_rows(self):
        self.row_cnt += 1
        self.tv_rows.set(str(self.row_cnt))
        self.new()

    def fewer_rows(self):
        self.row_cnt -= 1
        self.tv_rows.set(str(self.row_cnt))
        self.new()

    def createWidgets(self):
        self.remove_row = Button(self, text="--")
        self.remove_row["command"] = self.fewer_rows
        self.remove_row.pack({"side": "left"})

        self.row_label = Label(self)
        self.row_label["text"] = "rows:"
        self.row_label.pack({"side": "left"})
        self.row_cnt = 12
        self.tv_rows = StringVar()
        self.tv_rows.set(str(self.row_cnt))
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

        self.error_button = Button(self, text="show errors")
        self.error_button["command"] = self.show_errors
        self.error_button.pack({"side": "left"})

        self.error_button = Button(self, text="rotate")
        self.error_button["command"] = self.rotate
        self.error_button.pack({"side": "left"})

        self.canvas = Canvas(self.master, width=canvas_width, height=canvas_height, bg='navajo white')
        self.canvas.pack({"side": "left"})

    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        master.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.click)
        self.right_arrow = PhotoImage(file="right arrow.gif")
        self.up_left_arrow = PhotoImage(file="up left arrow.gif")
        self.down_left_arrow = PhotoImage(file="down left arrow.gif")
        self.row_list = None
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

    # create a new pyramid
    def new(self):
        triangle.next_id = 0
        self.winner = False
        self.play_mode = False
        self.hide = False
        self.cursor = self.top = node = parent_node = triangle()
        self.a_rows = [None for x in range(self.row_cnt)]
        self.a_rows[0] = [node]
        for row_idx in range(1, self.row_cnt):
            prev_node = None
            node_cnt = 1 + row_idx * 2
            self.a_rows[row_idx] = [None for x in range(node_cnt)]
            for node_idx in range(0, node_cnt):
                node = triangle()
                self.a_rows[row_idx][node_idx] = node

                if (node_idx % 2):
                    node.dir = DOWN
                else:
                    node.dir = UP
                if (node_idx == 0):
                    start_of_current_row = node
                if (prev_node):
                    prev_node.right = node
                    node.left = prev_node
                prev_node = node

                if (node_idx > 0 and node_idx < (node_cnt- 1)):
                    node.parent = parent_node
                    parent_node.child = node
                    parent_node = parent_node.right
            parent_node = start_of_current_row;
        
        # row_list is the list of rows at the top of the pyramid
        self.row_list = self.a_rows

        # b goes from bottom-right to the top-left
        self.b_rows = [None for x in range(self.row_cnt)]
        node = self.top
        row_idx = self.row_cnt - 1
        while(row_idx >= 0):
            node_idx = 0
            node_cnt = 1 + row_idx * 2
            self.b_rows[row_idx] = [None for x in range(node_cnt)]
            start_of_row = node
            dir = DOWN
            while(node):
                self.b_rows[row_idx][node_idx] = node
                node_idx += 1
                if (dir == DOWN):
                    node = node.child
                    dir = LEFT
                elif (dir == LEFT):
                    node = node.left
                    dir = DOWN
            node = start_of_row
            node = node.child
            if (node): node = node.right
            dir = DOWN
            row_idx -= 1

        self.c_rows = [None for x in range(self.row_cnt)]
        node = self.top
        row_idx = self.row_cnt - 1
        while(row_idx >= 0):
            node_cnt = 1 + row_idx * 2
            node_idx = node_cnt - 1
            self.c_rows[row_idx] = [None for x in range(node_cnt)]
            start_of_row = node
            dir = DOWN
            while(node):
                self.c_rows[row_idx][node_idx] = node
                node_idx -= 1
                if (dir == DOWN):
                    node = node.child
                    dir = RIGHT
                elif (dir == RIGHT):
                    node = node.right
                    dir = DOWN
            node = start_of_row
            node = node.child
            if (node): node = node.left
            dir = DOWN
            row_idx -= 1

        self.draw()
    
    # clears the state but not the answer flag
    def clear(self):
        self.winner = False
        for row_idx in range(0, self.row_cnt):
            for node_idx in range(0, len(self.row_list[row_idx])):
                self.row_list[row_idx][node_idx].state = state.empty

    def show_errors(self):
        for row_idx in range(0, self.row_cnt):
            for node_idx in range(0, len(self.row_list[row_idx])):
                node = self.row_list[row_idx][node_idx]
                if ((node.answer == True and node.state != state.filled) or
                    (node.answer == False and node.state == state.filled)):
                    self.canvas.create_oval(node.xleft+18, node.ytop+15, node.xright-18, node.ybottom-15, fill="tomato", outline="tomato")

    # sets the fill state based on the answer flag
    def refill(self):
        for row_idx in range(0, self.row_cnt):
            for node_idx in range(0, len(self.row_list[row_idx])):
                node = self.row_list[row_idx][node_idx]
                if (node.answer == True):
                    node.state = state.filled
                else:
                    node.state = state.empty

    def draw(self):
        if (self.winner):
            already_won = True
        else:
            already_won = False
        self.winner = True
        self.canvas.delete("all")
        if (triangulation.play_mode):
            self.canvas.create_text(100, 50, text="play mode", font="12x24", tags="text")
        else:
            self.canvas.create_text(100, 50, text="design mode", font="12x24", tags="text")
        
        total_cnt = 0
        for row_idx in range(0, self.row_cnt):
            node_list = self.row_list[row_idx]
            cnt = left_col_idx = alt_left_col_idx = 0
            right_col_idx = alt_right_col_idx = row_idx

            for node_idx in range(0, len(node_list)):
                node = node_list[node_idx]
                node.xleft = center_x - length - (half_length * (row_idx + 1)) + (half_length * node_idx)
                node.ybottom = (row_idx + 2) * altitude
                node.xright = node.xleft + length
                node.ybottom = node.ybottom
                node.xmiddle = node.xleft + half_length
                node.ytop = node.ybottom - altitude

                if (node.answer == True):
                    cnt += 1
                    total_cnt += 1

                if (triangulation.play_mode == True and
                    (node.answer == True and node.state != state.filled) or (node.answer == False and node.state == state.filled)):
                    self.winner = False

                color = "ivory"
                if (node.state == state.filled):
                    color = "medium sea green"
                    if (self.play_mode == True): cnt -= 1
                elif (node.state == state.empty and self.play_mode): color = "lavender"
                elif (node.state == state.frozen): color = "lightblue"
                if (self.hide == True): color = "white"

                mytags = ["all"]
                mytags.append(str("triangle") + str(node.id))
                mytags.append(str("row") + str(row_idx))
                mytags.append(str("left_col") + str(left_col_idx))
                mytags.append(str("right_col") + str(right_col_idx))
                mytags.append(str("alt_left_col") + str(alt_left_col_idx))
                mytags.append(str("alt_right_col") + str(alt_right_col_idx))

                self.canvas.tag_bind(str("triangle") + str(node.id), "<Button-1>", lambda event, n=node: self.left_click(event, n))
                self.canvas.tag_bind(str("triangle") + str(node.id), "<Button-3>", lambda event, n=node: self.right_click(event, n))
            
                if (node.dir == UP):
                    node.xy = ((node.xleft, node.ybottom), (node.xright, node.ybottom), (node.xmiddle, node.ytop))
                    mytags.append("uptriangle")
                    node.draw(self.canvas, color, mytags)
                    right_col_idx -= 1
                    alt_left_col_idx += 1
                else:
                    node.xy = ((node.xleft, node.ytop), (node.xright, node.ytop), (node.xmiddle, node.ybottom))
                    mytags.append("downtriangle")
                    node.draw(self.canvas, color, mytags)
                    left_col_idx += 1
                    alt_right_col_idx -= 1

            color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            self.canvas.create_text(center_x - 1.3 * length - (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude/2),
                                    fill=color, text=cnt, font="12x24", tags="text")

        #self.canvas.tag_bind("all", "<Button-1>", self.left_click)
        #self.canvas.tag_bind("all", "<Button-3>", self.right_click)

        if (self.cursor and self.hide == False and (already_won == True or triangulation.play_mode == False or self.winner == False)):
            self.cursor.outline(self.canvas)

        # winner!
        if (already_won == False and triangulation.play_mode and self.winner == True):
            self.canvas.delete("text")
            self.chicken_dinner()
            return

        # calculate the totals on the right
        if (self.row_list == self.a_rows): next_list = self.b_rows
        elif (self.row_list == self.b_rows): next_list = self.c_rows
        else: next_list = self.a_rows
        for row_idx in range(0, len(next_list)):
            node_list = next_list[len(next_list) - row_idx - 1]
            cnt = 0
            for node_idx in range(0, len(node_list)):
                node = node_list[node_idx]
                if (node.answer): cnt += 1
                if (node.state == state.filled and self.play_mode == True): cnt -= 1
            color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            self.canvas.create_text(center_x - length + (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude),
                                    fill=color, text=cnt, font="12x24", tags="text")

        # calculate the totals along the bottom
        if (next_list == self.a_rows): next_list = self.b_rows
        elif (next_list == self.b_rows): next_list = self.c_rows
        else: next_list = self.a_rows
        for row_idx in range(0, len(next_list)):
            node_list = next_list[len(next_list) - row_idx - 1]
            cnt = 0
            for node_idx in range(0, len(node_list)):
                node = node_list[len(node_list) - node_idx - 1]
                if (node.answer): cnt += 1
                if (node.state == state.filled and self.play_mode == True): cnt -= 1
                color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            self.canvas.create_text(center_x - (half_length/2) + self.row_cnt * half_length - (length * (row_idx + 1)),
                                    (self.row_cnt + 2) * altitude - (altitude / 2),
                                    fill=color, text=cnt, font="12x24", tags="text")

        self.canvas.create_image(center_x - (half_length * self.row_cnt / 2) - 130, self.row_cnt * altitude / 2, image=self.right_arrow)
        self.canvas.create_image(center_x + (half_length * self.row_cnt / 2) + 30, ((self.row_cnt - 1) * altitude / 2) - altitude / 2, image=self.down_left_arrow)
        self.canvas.create_image(center_x - 15, (self.row_cnt + 3) * altitude, image=self.up_left_arrow)

        self.canvas.create_text(100, 150, text="total shaded triangles: " + str(total_cnt), font="12x24", tags="text")

    def insert(self):
        node = self.cursor
        node.state = state.filled
        if (node.dir == DOWN):
            if (node.parent and node.parent.left and node.parent.right):
                node.parent.state = node.parent.left.state = node.parent.right.state = state.filled
            elif (node.parent and node.left and node.right):
                node.parent.state = node.left.state = node.right.state = state.filled
            elif (node.right and node.right.right and node.right.parent):
                node.right.state = node.right.right.state = node.right.parent.state = state.filled
            elif (node.left and node.left.left and node.left.parent):
                node.left.state = node.left.left.state = node.left.parent.state = state.filled
        elif (node.dir == UP):
            if (node.child and node.child.left and node.child.right):
                node.child.state = node.child.left.state = node.child.right.state = state.filled
            elif (node.child and node.left and node.right):
                node.child.state = node.left.state = node.right.state = state.filled
            elif (node.right and node.right.right and node.right.parent):
                node.right.state = node.right.right.state = node.right.parent.state = state.filled
            elif (node.left and node.left.left and node.left.parent):
                node.left.state = node.left.left.state = node.left.parent.state = state.filled

    def open(self):
        filename = filedialog.askopenfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        f = open(filename, 'r')
        data = list(f)
        if (len(data) != self.row_cnt):
            self.row_cnt = len(data)
            self.new()
        triangle.next_id = 0
        for ridx in range(0, self.row_cnt):
            line = data[ridx]
            node_list = line.split()
            node_cnt = len(node_list)
            for nidx in range(node_cnt):
                node = self.row_list[ridx][nidx]
                if (node_list[nidx] == 'X'): node.answer = True
        triangulation.play_mode = True
        self.draw()

    def save(self):
        filename = filedialog.asksaveasfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        f = open(filename, 'w')
        for ridx in range(0, self.row_cnt):
            for nidx in range(0, len(self.row_list[ridx])):
                if (self.row_list[ridx][nidx].state == state.filled):
                    f.write(" X")
                else:
                    f.write(" .")
            if (ridx < self.row_cnt - 1): f.write("\n")
        f.close()

    def scroll(self, letter):
        f = open(letter + ".txt", 'r')
        if (f == None): return
        more_rows = 0
        triangle.next_id = 0
        start_of_row = None
        letter_top = None
        for line in f:
            more_rows += 1
            node_list = line.split()
            node_cnt = len(node_list)
            if (node_cnt == 0):
                break
            parent_node = start_of_row
            prev_node = None
            for nidx in range(node_cnt):
                node = triangle()
                if (nidx == 0):
                    start_of_row = node
                    if (more_rows == 1):
                        letter_top = node
                else:
                    node.left = prev_node
                    prev_node.right = node
                    if (nidx < node_cnt - 1):
                        node.parent = parent_node
                        parent_node.child = node
                        parent_node = parent_node.right
                s = node_list[nidx]
                if (s == 'X'): node.answer = True
                prev_node = node
        node = self.top
        while (node.child): node = node.child
        while (node.right): node = node.right
        node = node.left.left
        if (node.dir != UP): node = node.left
        while (node):
            last_node = node
            self.show(node, letter_top)
            if (node.parent == None or node.parent.left == None):
                if (letter_top):
                    letter_top = letter_top.child
                    if (letter_top): letter_top = letter_top.right
                    if (letter_top == None):
                        break
            else:
                node = node.parent.left
            if (node == None): node = last_node
            self.canvas.delete("temp")
            self.canvas.update_idletasks()

    # this function shows letter_node at node
    def show(self, node, letter_node):
        center_node = node
        center_letter = letter_node
        dir = LEFT
        last_letter = None
        while (node and letter_node):
            if (letter_node != last_letter and letter_node.answer):
                node.draw(self.canvas, "red", "temp")
            last_letter = letter_node
            if (dir == LEFT):
                if (node.left and letter_node.left):
                    node = node.left
                    letter_node = letter_node.left
                else:
                    node = center_node
                    letter_node = center_letter
                    dir = RIGHT
            elif (dir == RIGHT):
                if (node.right and letter_node.right):
                    node = node.right
                    letter_node = letter_node.right
                else:
                    center_node = node = center_node.child
                    center_letter = letter_node = center_letter.child
                    dir = LEFT
            else:
                node = None
                letter_node = None
        self.canvas.update_idletasks()
        self.canvas.after(100)

    # winner, winner
    def chicken_dinner(self):
        # the entire pyramid
        for i in range(0, 4):
            color = random_color()
            self.canvas.itemconfig("all", fill=color)
            self.canvas.update_idletasks()
            self.canvas.after(50)

        # the up and down triangles
        for i in range(0, 2):
            for j in range(0, 2):
                color = "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')
                if (j == 0): self.canvas.itemconfig("uptriangle", fill=color)
                elif (j == 1): self.canvas.itemconfig("downtriangle", fill=color)
                self.canvas.update_idletasks()
                self.canvas.after(50)

        # twinkles
        for i in range(0, 16):
            for j in range(0, 30):
                color = "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')
                mytags = "triangle"
                mytags += str(random.randint(0, triangle.next_id))
                self.canvas.itemconfig(mytags, fill=color)
            self.canvas.update_idletasks()
            self.canvas.after(50)

        # random wipes
        for j in range(0, self.row_cnt):
            for i in range(0, 3):
                if (i == 0): mytags = "row"
                elif (i == 1): mytags = "left_col"
                elif (i == 2): mytags = "right_col"
                color = "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')
                self.canvas.itemconfig(mytags + str(random.randint(0, self.row_cnt)), fill=color)
                self.canvas.update_idletasks()
                self.canvas.after(50)

        # row wipes
        mytags = "row"
        for i in range(0, 2):
            for j in range(0, self.row_cnt):
                if (i == 0):
                    self.canvas.itemconfig(mytags + str(j), fill=random_color())
                else:
                    self.canvas.itemconfig(mytags + str(self.row_cnt - j - 1), fill=random_color())
                self.canvas.update_idletasks()
                self.canvas.after(50)

        # column wipes
        for j in range(0, 4):
            for i in range(0, 2):
                if (j == 0): mytags = "left_col"
                elif (j == 1): mytags = "alt_left_col"
                elif (j == 2): mytags = "right_col"
                elif (j == 3): mytags = "alt_right_col"
                for k in range(0, self.row_cnt):
                    if (i == 0):
                        self.canvas.itemconfig(mytags + str(k), fill=random_color())
                    else:
                        self.canvas.itemconfig(mytags + str(self.row_cnt - k - 1), fill=random_color())
                    self.canvas.update_idletasks()
                    self.canvas.after(50)

root = Tk()
app = triangulation(master=root)
app.mainloop()
root.destroy()
