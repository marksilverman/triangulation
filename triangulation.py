# pyramid
# a logic puzzle by Mark Silverman
# 2018/01/21
from triangle import *
from tkinter import *
from tkinter import filedialog
import math
import random

canvas_width = 900
canvas_height = 700
center_x = canvas_width // 2

def random_color():
    return "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')

class pyramid(Frame):
    play_mode = False

    def click(self, event):
        self.cursor = None
        self.draw()

    def left_click(self, event, node):
        self.cursor = node
        node.toggle(dir.LEFT, self.play_mode)
        self.draw()

    def right_click(self, event, node):
        self.cursor = node
        node.toggle(dir.RIGHT, self.play_mode)
        self.draw()

    def rotate(self):
        if (self.rlist == self.rlist_a):
            self.rlist = self.rlist_b
        elif (self.rlist == self.rlist_b):
            self.rlist = self.rlist_c
        else:
            self.rlist = self.rlist_a
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.draw()

    # fill in the easy stuff
    def easy_fill(self, rlist):
        did_something = 0
        for ridx in range(0, self.rcnt):
            answer_cnt = filled_cnt = empty_cnt = frozen_cnt = 0
            nlist = rlist[ridx]
            for nidx in range(0, len(nlist)):
                node = nlist[nidx]
                if (node.answer == True): answer_cnt += 1
                if (node.state == state.filled): filled_cnt += 1
                if (node.state == state.blank): empty_cnt += 1
                if (node.state == state.frozen): frozen_cnt += 1
            if (answer_cnt == filled_cnt):
                # freeze what's left in this row
                for nidx in range(0, len(nlist)):
                    node = nlist[nidx]
                    if (node.state != state.filled and node.state != state.frozen):
                        node.state = state.frozen
                        node.draw(self.canvas, "green", "temp")
                        self.canvas.update_idletasks()
                        self.canvas.after(10)
                        did_something += 1
            if (answer_cnt == filled_cnt + empty_cnt):
                # fill in what's left in this row
                for nidx in range(0, len(nlist)):
                    node = nlist[nidx]
                    if (node.state != state.frozen and node.state != state.filled):
                        node.state = state.filled
                        node.draw(self.canvas, "black", "temp")
                        self.canvas.update_idletasks()
                        self.canvas.after(10)
                        did_something += 1
        return did_something

    # free any triangles which can't be part of a pyramid
    def medium_fill(self, rlist):
        did_something = False
        for ridx in range(0, self.rcnt):
            nlist = rlist[ridx]
            for nidx in range(0, len(nlist)):
                node = nlist[nidx]
                if (node.state != state.blank): continue

                child_left = child_right = parent_left = parent_right = right_right = left_left = None
                left = node.left
                right = node.right
                child = node.child
                parent = node.parent

                # see if anything is possible
                if (node.direction == dir.UP):
                    # see if this triangle is a center
                    if (child and child.state == state.blank):
                        # look center
                        if (child.left and child.left.state == state.blank and
                            child.right and child.right.state == state.blank):
                                continue
                        # look down
                        if (left and left.state == state.blank and
                            right and right.state == state.blank):
                                continue
                    # look left
                    if (left and left.state == state.blank and
                        left.left and left.left.state == state.blank and
                        left.parent and left.parent.state == state.blank):
                            continue

                    # look right
                    if (right and right.state == state.blank and
                        right.right and right.right.state == state.blank and
                        right.parent and right.parent.state == state.blank):
                            continue
                elif (node.direction == dir.DOWN):
                    if (parent and parent.state == state.blank):
                        # look center
                        if (left and left.state == state.blank and
                            right and right.state == state.blank):
                                continue
                        # look up
                        if (parent.left and parent.left.state == state.blank and
                            parent.right and parent.right.state == state.blank):
                                continue
                    # look left
                    if (left and left.state == state.blank and
                        left.left and left.left.state == state.blank and
                        left.child and left.child.state == state.blank):
                            continue
                    # look right
                    if (right and right.state == state.blank and
                        right.right and right.right.state == state.blank and
                        right.child and right.child.state == state.blank):
                            continue
                # if we reach here there are no possible pyramids with this triangle
                node.state = state.frozen
                did_something = True
        return did_something

    def solve(self):
        did_something = True
        while (did_something):
            did_something = False
            for i in range(0, 3):
                if i == 0: rlist = self.rlist_a
                elif i == 1: rlist = self.rlist_b
                elif i == 2: rlist = self.rlist_c
                did_something |= self.easy_fill(rlist)
                did_something |= self.medium_fill(rlist)
        self.canvas.delete("temp")

    def key(self, event):
        k = repr(event.keysym)
        # print(k)
        if (k == "'r'"):
            self.rotate()
            return
        if (k == "'F1'"): self.solve()
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'s'"): self.save()
        if (k == "'p'"): self.play()
        if (k == "'l'"):
            msg = "triangulation"
            for i in range(0, len(msg)):
                self.scroll(msg[i:i+1])
        if (k == "'h'"): self.hide = not self.hide
        if (k == "'equal'" or k == "'plus'"): self.more_rows()
        if (k == "'minus'" or k == "'underscore'"): self.fewer_rows()
        if (k == "'Home'" or k == "'Prior'"): self.cursor = self.top
        if (k == "'End'" or k == "'Next'"): self.cursor = self.rlist[self.rcnt-1][self.cidx+self.rcnt-self.ridx-1]

        if (k == "'Left'" or k == "'4'"):
            self.cidx -= 1
            if (self.cidx < 0): self.cidx = len(self.rlist[self.ridx]) - 1
            self.cursor = self.rlist[self.ridx][self.cidx]

        if (k == "'Right'" or k == "'6'"):
            self.cidx += 1
            if (self.cidx == len(self.rlist[self.ridx])): self.cidx = 0
            self.cursor = self.rlist[self.ridx][self.cidx]

        if (k == "'Up'" or k == "'8'"):
            if (self.ridx > 0):
                if (self.cidx == 0):
                    self.cidx = 1
                elif (self.cidx == (len(self.rlist[self.ridx]) - 1)):
                    self.cidx -= 1
                else:
                    self.ridx -= 1
                    self.cidx -= 1
                self.cursor = self.rlist[self.ridx][self.cidx]

        if (k == "'Down'" or k == "'2'"):
            if (self.ridx < (self.rcnt - 1)):
                self.ridx += 1
                self.cidx += 1
                self.cursor = self.rlist[self.ridx][self.cidx]

        if (k == "'space'"): # fill
            if (self.cursor == None): self.cursor = self.rlist[self.ridx][self.cidx]
            self.cursor.toggle(dir.LEFT, self.play_mode)

        if (k == "'f'"): # freeze
            if (self.cursor == None): self.cursor = self.top
            self.cursor.toggle(dir.RIGHT, self.play_mode)

        self.draw()

    def more_rows(self):
        self.rcnt += 1
        if (self.rcnt == 15):
            self.length -= 5
            self.half_length = self.length // 2
            self.altitude = self.length * math.sqrt(3) / 2.0
        self.tv_rows.set(str(self.rcnt))
        self.new()

    def fewer_rows(self):
        if (self.rcnt < 3): return
        self.rcnt -= 1
        if (self.rcnt == 15):
            self.length += 5
            self.half_length = self.length // 2
            self.altitude = self.length * math.sqrt(3) / 2.0
        self.tv_rows.set(str(self.rcnt))
        self.new()

    def createWidgets(self):
        self.remove_row = Button(self, text="--")
        self.remove_row["command"] = self.fewer_rows
        self.remove_row.pack({"side": "left"})

        self.row_label = Label(self)
        self.row_label["text"] = "rows:"
        self.row_label.pack({"side": "left"})
        self.rcnt = 12
        self.tv_rows = StringVar()
        self.tv_rows.set(str(self.rcnt))
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
        self.rlist = None
        self.ridx = 0
        self.cidx = 0
        self.length = 40
        self.half_length = self.length // 2
        self.altitude = self.length * math.sqrt(3) / 2.0
        self.new()

    def play(self):
        if (pyramid.play_mode == False):
            pyramid.play_mode = True
            self.play_button.config(text="design")
            self.clear()
        else:
            pyramid.play_mode = False
            self.play_button.config(text="play")
            self.refill()
        self.draw()

    # create a new pyramid
    def new(self):
        triangle.next_id = 0
        self.winner = False
        pyramid.play_mode = False
        self.hide = False
        self.cursor = self.top = node = parent_node = triangle()
        self.rlist_a = [None for x in range(self.rcnt)]
        self.rlist_a[0] = [node]
        for ridx in range(1, self.rcnt):
            prev_node = None
            ccnt = 1 + ridx * 2
            self.rlist_a[ridx] = [None for x in range(ccnt)]
            for cidx in range(0, ccnt):
                node = triangle()
                self.rlist_a[ridx][cidx] = node

                if (cidx % 2):
                    node.direction = dir.DOWN
                else:
                    node.direction = dir.UP
                if (cidx == 0):
                    start_of_current_row = node
                if (prev_node):
                    prev_node.right = node
                    node.left = prev_node
                prev_node = node

                if (cidx > 0 and cidx < (ccnt- 1)):
                    node.parent = parent_node
                    parent_node.child = node
                    parent_node = parent_node.right
            parent_node = start_of_current_row;
        
        # rlist is the list of rows at the top of the pyramid
        self.rlist = self.rlist_a

        # b goes from bottom-right to the top-left
        self.rlist_b = [None for x in range(self.rcnt)]
        node = self.top
        ridx = self.rcnt - 1
        while(ridx >= 0):
            cidx = 0
            ccnt = 1 + ridx * 2
            self.rlist_b[ridx] = [None for x in range(ccnt)]
            start_of_row = node
            direction = dir.DOWN
            while(node):
                self.rlist_b[ridx][cidx] = node
                cidx += 1
                if (direction == dir.DOWN):
                    node = node.child
                    direction = dir.LEFT
                elif (direction == dir.LEFT):
                    node = node.left
                    direction = dir.DOWN
            node = start_of_row
            node = node.child
            if (node): node = node.right
            direction = dir.DOWN
            ridx -= 1

        self.rlist_c = [None for x in range(self.rcnt)]
        node = self.top
        ridx = self.rcnt - 1
        while(ridx >= 0):
            ccnt = 1 + ridx * 2
            cidx = ccnt - 1
            self.rlist_c[ridx] = [None for x in range(ccnt)]
            start_of_row = node
            direction = dir.DOWN
            while(node):
                self.rlist_c[ridx][cidx] = node
                cidx -= 1
                if (direction == dir.DOWN):
                    node = node.child
                    direction = dir.RIGHT
                elif (direction == dir.RIGHT):
                    node = node.right
                    direction = dir.DOWN
            node = start_of_row
            node = node.child
            if (node): node = node.left
            direction = dir.DOWN
            ridx -= 1
        ridx = cidx = 0
        self.draw()
    
    # clears the state but not the answer flag
    def clear(self):
        self.winner = False
        for ridx in range(0, self.rcnt):
            for cidx in range(0, len(self.rlist[ridx])):
                self.rlist[ridx][cidx].state = state.blank

    def show_errors(self):
        for ridx in range(0, self.rcnt):
            for cidx in range(0, len(self.rlist[ridx])):
                node = self.rlist[ridx][cidx]
                if ((node.answer == True and node.state != state.filled) or
                    (node.answer == False and node.state == state.filled)):
                    self.canvas.create_oval(node.xleft+18, node.ytop+15, node.xright-18, node.ybottom-15, fill="tomato", outline="tomato")

    # sets the fill state based on the answer flag
    def refill(self):
        for ridx in range(0, self.rcnt):
            for cidx in range(0, len(self.rlist[ridx])):
                node = self.rlist[ridx][cidx]
                if (node.answer == True):
                    node.state = state.filled
                else:
                    node.state = state.blank

    def draw(self):
        already_won = False
        if (self.winner): already_won = True
            
        self.winner = True
        self.canvas.delete("all")
        msg = "design mode"
        if (pyramid.play_mode): msg = "play mode"
        self.canvas.create_text(100, 50, text=msg, font="12x24", tags="text")
        
        total_cnt = 0
        for ridx in range(0, self.rcnt):
            cnt = left_col_idx = alt_left_col_idx = 0
            right_col_idx = alt_right_col_idx = ridx
            nlist = self.rlist[ridx]
            for cidx in range(0, len(nlist)):
                node = nlist[cidx]
                node.xleft = center_x - self.length - (self.half_length * (ridx + 1)) + (self.half_length * cidx)
                node.ybottom = (ridx + 2) * self.altitude
                node.xright = node.xleft + self.length
                node.ybottom = node.ybottom
                node.xmiddle = node.xleft + self.half_length
                node.ytop = node.ybottom - self.altitude

                if (node == self.cursor):
                    self.ridx = ridx
                    self.cidx = cidx
                    msg = "row " + str(ridx+1)
                    self.canvas.create_text(800, 50, text=msg, font="12x24", tags="text")
                    msg = "column " + str(cidx+1)
                    self.canvas.create_text(800, 80, text=msg, font="12x24", tags="text")

                if (node.answer == True):
                    cnt += 1
                    total_cnt += 1

                if (pyramid.play_mode == True and
                    (node.answer == True and node.state != state.filled) or
                    (node.answer == False and node.state == state.filled)):
                    self.winner = False

                color = "ivory"
                if (node.state == state.filled):
                    color = "medium sea green"
                    if (pyramid.play_mode == True): cnt -= 1
                elif (node.state == state.blank and pyramid.play_mode): color = "thistle1"
                elif (node.state == state.frozen): color = "gray"
                if (self.hide == True): color = "white"

                mytags = ["all"]
                mytags.append(str("triangle") + str(node.id))
                mytags.append(str("row") + str(ridx))
                mytags.append(str("left_col") + str(left_col_idx))
                mytags.append(str("right_col") + str(right_col_idx))
                mytags.append(str("alt_left_col") + str(alt_left_col_idx))
                mytags.append(str("alt_right_col") + str(alt_right_col_idx))

                self.canvas.tag_bind(str("triangle") + str(node.id), "<Button-1>", lambda event, n=node: self.left_click(event, n))
                self.canvas.tag_bind(str("triangle") + str(node.id), "<Button-3>", lambda event, n=node: self.right_click(event, n))
            
                if (node.direction == dir.UP):
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
            x = center_x - 1.3 * self.length - (self.half_length * (ridx + 1))
            y = (ridx + 2) * self.altitude - (self.altitude/2)
            if (self.hide == False and self.cursor != None and ridx == self.ridx):
                self.canvas.create_oval(x-12, y-12, x+12, y+12, fill='gold', tags="text")
            self.canvas.create_text(x, y, fill=color, text=cnt, font="12x24", tags="text")

        if (self.cursor and self.hide == False and (already_won == True or pyramid.play_mode == False or self.winner == False)):
            self.cursor.outline(self.canvas)

        # winner?
        if (already_won == False and pyramid.play_mode and self.winner == True):
            self.canvas.delete("text")
            self.chicken_dinner()
            return

        # calculate totals on the right
        if (self.rlist == self.rlist_a): next_list = self.rlist_b
        elif (self.rlist == self.rlist_b): next_list = self.rlist_c
        else: next_list = self.rlist_a
        for ridx in range(0, len(next_list)):
            nlist = next_list[len(next_list) - ridx - 1]
            cnt = 0
            this_one = False
            for cidx in range(0, len(nlist)):
                node = nlist[cidx]
                if (node == self.cursor):
                    this_one = True
                if (node.answer): cnt += 1
                if (node.state == state.filled and pyramid.play_mode == True): cnt -= 1
            color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            x = center_x - self.length + (self.half_length * (ridx + 1))
            y =  (ridx + 2) * self.altitude - (self.altitude)
            if (self.hide == False and this_one):
                self.canvas.create_oval(x-12, y-12, x+12, y+12, fill='gold')
            self.canvas.create_text(x, y, fill=color, text=cnt, font="12x24", tags="text")

        # calculate the totals along the bottom
        if (next_list == self.rlist_a): next_list = self.rlist_b
        elif (next_list == self.rlist_b): next_list = self.rlist_c
        else: next_list = self.rlist_a
        for ridx in range(0, len(next_list)):
            nlist = next_list[len(next_list) - ridx - 1]
            cnt = 0
            this_one = False
            for cidx in range(0, len(nlist)):
                node = nlist[len(nlist) - cidx - 1]
                if (node == self.cursor):
                    this_one = True
                if (node.answer): cnt += 1
                if (node.state == state.filled and pyramid.play_mode == True): cnt -= 1
                color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            x = center_x - (self.half_length/2) + self.rcnt * self.half_length - (self.length * (ridx + 1))
            y = (self.rcnt + 2) * self.altitude - (self.altitude / 2)
            if (self.hide == False and this_one):
                self.canvas.create_oval(x-12, y-12, x+12, y+12, fill='gold')
            self.canvas.create_text(x, y, fill=color, text=cnt, font="12x24", tags="text")

        self.canvas.create_image(center_x - (self.half_length * self.rcnt / 2) - 130, self.rcnt * self.altitude / 2, image=self.right_arrow)
        self.canvas.create_image(center_x + (self.half_length * self.rcnt / 2) + 30, ((self.rcnt - 1) * self.altitude / 2) - self.altitude / 2, image=self.down_left_arrow)
        self.canvas.create_image(center_x - 15, (self.rcnt + 3) * self.altitude, image=self.up_left_arrow)

        self.canvas.create_text(100, 150, text="total shaded triangles: " + str(total_cnt), font="12x24", tags="text")

    def open(self):
        filename = filedialog.askopenfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        if len(filename) == 0: return
        f = open(filename, 'r')
        data = list(f)
        if (len(data) != self.rcnt):
            self.rcnt = len(data)
            self.new()
        for ridx in range(0, self.rcnt):
            line = data[ridx]
            nlist = line.split()
            ccnt = len(nlist)
            for cidx in range(ccnt):
                node = self.rlist[ridx][cidx]
                if (nlist[cidx][:1] == 'X'): node.answer = True
                if (nlist[cidx][-1:] == 'f'): node.state = state.filled
                if (nlist[cidx][-1:] == '!'): node.state = state.frozen
        pyramid.play_mode = True
        self.draw()

    # X - answer
    # f - filled
    # ! - frozen
    # . - blank
    def save(self):
        filename = filedialog.asksaveasfilename(initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        if (len(filename) == 0): return
        f = open(filename, 'w')
        for ridx in range(0, self.rcnt):
            for cidx in range(0, len(self.rlist[ridx])):
                node = self.rlist[ridx][cidx]
                f.write(" ")
                if (node.answer): f.write("X")
                if (node.state == state.filled): f.write("f")
                elif (node.state == state.frozen): f.write("!")
                elif (node.state == state.blank): f.write(".")
            if (ridx < self.rcnt - 1): f.write("\n")
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
            nlist = line.split()
            ccnt = len(nlist)
            if (ccnt == 0):
                break
            parent_node = start_of_row
            prev_node = None
            for cidx in range(ccnt):
                node = triangle()
                if (cidx == 0):
                    start_of_row = node
                    if (more_rows == 1):
                        letter_top = node
                else:
                    node.left = prev_node
                    prev_node.right = node
                    if (cidx < ccnt - 1):
                        node.parent = parent_node
                        parent_node.child = node
                        parent_node = parent_node.right
                s = nlist[cidx]
                if (s == 'X'): node.answer = True
                prev_node = node
        node = self.top
        while (node.child): node = node.child
        while (node.right): node = node.right
        node = node.left.left
        if (node.direction != dir.UP): node = node.left
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
        direction = dir.LEFT
        last_letter = None
        while (node and letter_node):
            if (letter_node != last_letter and letter_node.answer):
                node.draw(self.canvas, "red", "temp")
            last_letter = letter_node
            if (direction == dir.LEFT):
                if (node.left and letter_node.left):
                    node = node.left
                    letter_node = letter_node.left
                else:
                    node = center_node
                    letter_node = center_letter
                    direction = dir.RIGHT
            elif (direction == dir.RIGHT):
                if (node.right and letter_node.right):
                    node = node.right
                    letter_node = letter_node.right
                else:
                    center_node = node = center_node.child
                    center_letter = letter_node = center_letter.child
                    direction = dir.LEFT
            else:
                node = None
                letter_node = None
        self.canvas.update_idletasks()
        self.canvas.after(100)

    # winner, winner
    def chicken_dinner(self):
        # the entire pyramid
        #for i in range(0, 8):
        #    color = random_color()
        #    self.canvas.itemconfig("all", fill=color)
        #    self.canvas.update_idletasks()
        #    self.canvas.after(100)

        # the up and down triangles
        #for i in range(0, 6):
        #    for j in range(0, 2):
        #        color = random_color()
        #        if (j == 0): self.canvas.itemconfig("uptriangle", fill=color)
        #        elif (j == 1): self.canvas.itemconfig("downtriangle", fill=color)
        #        self.canvas.update_idletasks()
        #        self.canvas.after(100)

        # twinkles
        for i in range(0, 5):
            for j in range(0, 30):
                color = random_color()
                mytags = "triangle"
                mytags += str(random.randint(0, triangle.next_id))
                self.canvas.itemconfig(mytags, fill=color)
            self.canvas.update_idletasks()
            self.canvas.after(50)
        self.draw()
        return
        # random wipes
        #for j in range(0, self.rcnt):
        #    for i in range(0, 3):
        #        if (i == 0): mytags = "row"
        #        elif (i == 1): mytags = "left_col"
        #        elif (i == 2): mytags = "right_col"
        #        color = "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')
        #        self.canvas.itemconfig(mytags + str(random.randint(0, self.rcnt)), fill=color)
        #        self.canvas.update_idletasks()
        #        self.canvas.after(50)

        # row wipes
        mytags = "row"
        for i in range(0, self.rcnt):
            self.canvas.itemconfig(mytags + str(i), fill=random_color())
            self.canvas.update_idletasks()
            self.canvas.after(50)

        # column wipes
        for i in range(0, 4):
            if (i == 0): mytags = "left_col"
            elif (i == 1): mytags = "right_col"
            elif (i == 2): mytags = "alt_left_col"
            elif (i == 3): mytags = "alt_right_col"
            for j in range(0, self.rcnt):
                self.canvas.itemconfig(mytags + str(j), fill=random_color())
                self.canvas.update_idletasks()
                self.canvas.after(50)

root = Tk()
app = pyramid(master=root)
app.mainloop()
root.destroy()
