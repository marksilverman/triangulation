# triangulation
# a logic puzzle by Mark Silverman
# 2018/01/21
from tkinter import *
from tkinter import filedialog
import math
import random

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

UNFILLED = 0
FILLED = 1
FROZEN = 2

def random_color():
    return "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')

class triangle():
    next_id = 0
    def __init__(self):
        self.parent = self.child = self.left = self.right = None
        self.xleft = self.xright = self.xmiddle = self.ybottom = self.ytop = 0
        self.state = UNFILLED
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

    def key(self, event):
        k = repr(event.keysym)
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'i'"): self.insert()
        if (k == "'s'"): self.save()
        if (k == "'p'"): self.play()
        if (k == "'r'"): self.draw()
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
        self.rows += 1
        self.tv_rows.set(str(self.rows))
        self.new()

    def fewer_rows(self):
        self.rows -= 1
        self.tv_rows.set(str(self.rows))
        self.new()

    def createWidgets(self):
        self.remove_row = Button(self, text="--")
        self.remove_row["command"] = self.fewer_rows
        self.remove_row.pack({"side": "left"})

        self.row_label = Label(self)
        self.row_label["text"] = "rows:"
        self.row_label.pack({"side": "left"})
        self.rows = 12
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

        self.error_button = Button(self, text="show errors")
        self.error_button["command"] = self.show_errors
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
        triangle.next_id = 0
        self.winner = False
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
        self.winner = False
        self.cursor = node = self.top
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

    def show_errors(self):
        self.cursor = node = self.top
        dir = RIGHT
        while(node):
            if ((node.answer == True and node.state != FILLED) or (node.answer == False and node.state == FILLED)):
                self.canvas.create_oval(node.xleft+18, node.ytop+15,
                                       node.xright-18, node.ybottom-15, fill="tomato", outline="tomato")
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
        node = self.top
        total_cnt = 0
        for row_idx in range(0, self.rows):
            node_idx = cnt = left_col_idx = alt_left_col_idx = 0
            right_col_idx = alt_right_col_idx = row_idx
            start_of_row = node
            node.dir = UP
            
            while (node):
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
                    (node.answer == True and node.state != FILLED) or (node.answer == False and node.state == FILLED)):
                    self.winner = False

                if (node.state == FILLED):
                    color = "medium sea green"
                    if (self.play_mode == True):
                        cnt -= 1
                elif (node.state == UNFILLED):
                    if (self.play_mode):
                        color = "ivory"
                    else:
                        color = "lavender"
                elif (node.state == FROZEN):
                    color = "lightblue"

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
                    node = node.right
                    if (node): node.dir = DOWN
                    right_col_idx -= 1
                    alt_left_col_idx += 1
                else:
                    node.xy = ((node.xleft, node.ytop), (node.xright, node.ytop), (node.xmiddle, node.ybottom))
                    mytags.append("downtriangle")
                    node.draw(self.canvas, color, mytags)
                    node = node.right
                    if (node): node.dir = UP
                    left_col_idx += 1
                    alt_right_col_idx -= 1
                node_idx += 1

            color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            self.canvas.create_text(center_x - 1.3 * length - (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude/2),
                                    fill=color, text=cnt, font="12x24", tags="text")
            node = start_of_row.child
            if (node): node = node.left

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
        node = self.top
        for row_idx in range(0, self.rows):
            cnt = 0
            dir = DOWN
            start_of_row = node
            while (node):
                if (node.answer): cnt += 1
                if (node.state == FILLED and self.play_mode == True): cnt -= 1
                if (dir == DOWN):
                    node = node.child
                    dir = LEFT
                else:
                    node = node.left
                    dir = DOWN
            color = "black"
            if (cnt < 0):
                color = "tomato"
            elif (cnt == 0):
                color = "darkgreen"
            self.canvas.create_text(center_x - length + (half_length * (row_idx + 1)),
                                    (row_idx + 2) * altitude - (altitude),
                                    fill=color, text=cnt, font="12x24", tags="text")
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
                if (node.answer): cnt += 1
                if (node.state == FILLED and self.play_mode == True): cnt -= 1
                if (dir == DOWN):
                    node = node.child
                    dir = RIGHT
                else:
                    node = node.right
                    dir = DOWN
            color = "black"
            if (cnt < 0):
                color = "tomato"
            elif (cnt == 0):
                color = "darkgreen"
            self.canvas.create_text(center_x - (half_length/2) + self.rows * half_length - (length * (row_idx + 1)),
                                    (self.rows + 2) * altitude - (altitude / 2),
                                    fill=color, text=cnt, font="12x24", tags="text")
            node = start_of_row.child
            if (node):
                node = node.left

        self.canvas.create_image(center_x - (half_length * self.rows / 2) - 130, self.rows * altitude / 2, image=self.right_arrow)
        self.canvas.create_image(center_x + (half_length * self.rows / 2) + 30, ((self.rows - 1) * altitude / 2) - altitude / 2, image=self.down_left_arrow)
        self.canvas.create_image(center_x - 15, (self.rows + 3) * altitude, image=self.up_left_arrow)

        self.canvas.create_text(100, 150, text="total shaded triangles: " + str(total_cnt), font="12x24", tags="text")

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
                if (s == 'X'): node.answer = True
                prev_node = node
        triangulation.play_mode = True
        self.draw()

    def scroll(self, letter):
        f = open(letter + ".txt", 'r')
        if (f == None): return
        more_rows = 0
        triangle.next_id = 0
        start_of_row = None
        letter_top = None
        for line in f:
            more_rows += 1
            triangle_list = line.split()
            triangle_cnt = len(triangle_list)
            if (triangle_cnt == 0):
                break
            parent_node = start_of_row
            prev_node = None
            for triangle_idx in range(triangle_cnt):
                node = triangle()
                if (triangle_idx == 0):
                    start_of_row = node
                    if (more_rows == 1):
                        letter_top = node
                else:
                    node.left = prev_node
                    prev_node.right = node
                    if (triangle_idx < triangle_cnt - 1):
                        node.parent = parent_node
                        parent_node.child = node
                        parent_node = parent_node.right
                s = triangle_list[triangle_idx]
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
        for j in range(0, self.rows):
            for i in range(0, 3):
                if (i == 0): mytags = "row"
                elif (i == 1): mytags = "left_col"
                elif (i == 2): mytags = "right_col"
                color = "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')
                self.canvas.itemconfig(mytags + str(random.randint(0, self.rows)), fill=color)
                self.canvas.update_idletasks()
                self.canvas.after(50)

        # row wipes
        mytags = "row"
        for i in range(0, 2):
            for j in range(0, self.rows):
                if (i == 0):
                    self.canvas.itemconfig(mytags + str(j), fill=random_color())
                else:
                    self.canvas.itemconfig(mytags + str(self.rows - j - 1), fill=random_color())
                self.canvas.update_idletasks()
                self.canvas.after(50)

        # column wipes
        for j in range(0, 4):
            for i in range(0, 2):
                if (j == 0): mytags = "left_col"
                elif (j == 1): mytags = "alt_left_col"
                elif (j == 2): mytags = "right_col"
                elif (j == 3): mytags = "alt_right_col"
                for k in range(0, self.rows):
                    if (i == 0):
                        self.canvas.itemconfig(mytags + str(k), fill=random_color())
                    else:
                        self.canvas.itemconfig(mytags + str(self.rows - k - 1), fill=random_color())
                    self.canvas.update_idletasks()
                    self.canvas.after(50)

root = Tk()
app = triangulation(master=root)
app.mainloop()
root.destroy()
