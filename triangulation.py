# pyramid
# a logic puzzle by Mark Silverman
# 2018/01/21

from triangle import *
from tkinter import *
from tkinter import filedialog
import random

sqrt3 = 1.732
canvas_width = 900
canvas_height = 800
center_x = canvas_width // 2
default_length = 40

def random_rgb():
    return random.randint(0, 0xFF), random.randint(0, 0xFF), random.randint(0, 0xFF)

def new_color(r, g, b):
    r = (r + random.randint(0, 0xFF)) % 0xFF
    g = (g + random.randint(0, 0xFF)) % 0xFF
    b = (b + random.randint(0, 0xFF)) % 0xFF
    return r, g, b

def make_color(r, g, b):
    return "#" + format(int(r), '02x') + format(int(g), '02x') + format(int(b), '02x')

def random_color():
    return "#" + format(int(random.randint(0, 0xFFFFFF)), '06x')

class pyramid(Frame):
    def click(self, event):
        self.cursor = None
        self.draw()

    def left_click(self, event, node):
        self.cursor = node
        node.toggle(dir.LEFT)
        self.draw()

    def right_click(self, event, node):
        self.cursor = node
        node.toggle(dir.RIGHT)
        self.draw()

    def rotate(self):
        if (self.rlist == self.rlist_a):
            self.rlist = self.rlist_b
            self.count_list = self.count_list_b
        elif (self.rlist == self.rlist_b):
            self.rlist = self.rlist_c
            self.count_list = self.count_list_c
        else:
            self.rlist = self.rlist_a
            self.count_list = self.count_list_a
        self.top = self.rlist[0][0]
        self.left = self.rlist[self.rcnt-1][0]
        self.right = self.rlist[self.rcnt-1][len(self.rlist[self.rcnt-1])-1]
        self.draw()

    # fill in the easy stuff
    def easy_fill(self, rlist):
        did_something = 0
        for ridx in range(0, self.rcnt):
            answer_cnt = filled_cnt = empty_cnt = frozen_cnt = 0
            clist = rlist[ridx]
            for cidx in range(0, len(clist)):
                node = clist[cidx]
                if (node.answer == True): answer_cnt += 1
                if (node.state == state.filled): filled_cnt += 1
                if (node.state == state.blank): empty_cnt += 1
                if (node.state == state.frozen): frozen_cnt += 1
            if (answer_cnt == filled_cnt):
                # freeze what's left in this row
                for cidx in range(0, len(clist)):
                    node = clist[cidx]
                    if (node.state != state.filled and node.state != state.frozen):
                        node.freeze()
                        node.draw(self.canvas, "black", "temp")
                        self.canvas.update_idletasks()
                        self.canvas.after(10)
                        did_something += 1
            if (answer_cnt == filled_cnt + empty_cnt):
                # fill in what's left in this row
                for cidx in range(0, len(clist)):
                    node = clist[cidx]
                    if (node.state != state.frozen and node.state != state.filled):
                        node.fill()
                        node.draw(self.canvas, "green", "temp")
                        self.canvas.update_idletasks()
                        self.canvas.after(10)
                        did_something += 1
        return did_something

    def find_family(self, rlist, clist, ridx, cidx):
        p = c = l = r = ll = lp = lc = rr = rp = rc = None
        #parents
        if ridx-1 >= 0:
            if cidx-1 >= 0 and cidx-1 < len(rlist[ridx-1]): p  = rlist[ridx-1][cidx-1]
            if cidx-2 >= 0 and cidx-2 < len(rlist[ridx-1]): lp = rlist[ridx-1][cidx-2]
            if cidx < len(rlist[ridx-1]): rp = rlist[ridx-1][cidx]
        #children
        if ridx+1 < len(rlist):
           c = rlist[ridx+1][cidx+1]
           lc = rlist[ridx+1][cidx]
           rc = rlist[ridx+1][cidx+2]
        #lefts
        if cidx-1 >= 0: l = clist[cidx-1]
        if cidx-2 >= 0: ll = clist[cidx-2]
        #rights
        if cidx+1 < len(clist): r = clist[cidx+1]
        if cidx+2 < len(clist): rr = clist[cidx+2]
        return p, c, l, r, ll, lp, lc, rr, rp, rc

    # freeze any triangles which can't be part of a pyramid
    def freeze_impossibles(self, rlist, count_list):
        did_something = False
        for ridx in range(0, self.rcnt):
            clist = rlist[ridx]
            for cidx in range(0, len(clist)):
                node = clist[cidx]
                if (node.isNotBlank()): continue
                if (count_list[ridx] == 0):
                    node.freeze()
                    did_something = True
                    continue
                p, c, l, r, ll, lp, lc, rr, rp, rc = self.find_family(rlist, clist, ridx, cidx)
                # see if anything is possible
                if node.direction == dir.UP:
                    # look down
                    if c and c.isNotFrozen() and (c.isFilled() or count_list[ridx+1] > 0):
                        if l and r and l.isNotFrozen() and r.isNotFrozen():
                            need = 0
                            if (l.isBlank()): need += 1
                            if (r.isBlank()): need += 1
                            if (count_list[ridx] >= need): continue
                        if lc and rc and lc.isNotFrozen() and rc.isNotFrozen():
                           need = 0
                           if lc.isBlank(): need += 1
                           if rc.isBlank(): need += 1
                           if count_list[ridx+1] >= need: continue
                    # look left
                    if lp and lp.isNotFrozen() and (lp.isFilled() or count_list[ridx-1] > 0):
                        if l and ll and l.isNotFrozen() and ll.isNotFrozen():
                            need = 0
                            if l.isBlank(): need += 1
                            if ll.isBlank(): need += 1
                            if count_list[ridx] >= need: continue
                    # look right
                    if rp and rp.isNotFrozen() and (rp.isFilled() or count_list[ridx-1] > 0):
                        if r and rr and r.isNotFrozen() and rr.isNotFrozen():
                            need = 0
                            if r.isBlank(): need += 1
                            if rr.isBlank(): need += 1
                            if count_list[ridx] >= need: continue
                elif node.direction == dir.DOWN:
                    # look up
                    if p and p.isNotFrozen() and (p.isFilled() or count_list[ridx-1] > 0):
                        if l and r and l.isNotFrozen() and r.isNotFrozen():
                            need = 0
                            if l.isBlank(): need += 1
                            if r.isBlank(): need += 1
                            if count_list[ridx] >= need: continue
                        if lp and rp and lp.isNotFrozen() and rp.isNotFrozen():
                           need = 0
                           if lp.isBlank(): need += 1
                           if rp.isBlank(): need += 1
                           if count_list[ridx-1] >= need: continue
                    # look left
                    if lc and lc.isNotFrozen() and (lc.isFilled() or count_list[ridx+1] > 0):
                        if l and ll and l.isNotFrozen() and ll.isNotFrozen():
                            need = 0
                            if l.isBlank(): need += 1
                            if ll.isBlank(): need += 1
                            if count_list[ridx] >= need: continue
                    # look right
                    if rc and rc.isNotFrozen() and (rc.isFilled() or count_list[ridx+1] > 0):
                        if r and rr and r.isNotFrozen() and rr.isNotFrozen():
                            need = 0
                            if r.isBlank(): need += 1
                            if rr.isBlank(): need += 1
                            if count_list[ridx] >= need: continue
                # if we reach here there are no possible pyramids with this triangle
                node.freeze()
                did_something = True
        return did_something

    def extend_singles(self, rlist, count_list):
        did_something = False
        for ridx in range(0, self.rcnt):
            clist = rlist[ridx]
            for cidx in range(0, len(clist)):
                node = clist[cidx]
                if (node.isNotFilled()): continue
                p, c, l, r, ll, lp, lc, rr, rp, rc = self.find_family(rlist, clist, ridx, cidx)
                need_these = []
                found_one = False

                # look for a unique solution
                if node.direction == dir.UP:
                    # look down
                    if c and c.isNotFrozen() and (c.isFilled() or count_list[ridx+1] > 0):
                        if l and r and l.isNotFrozen() and r.isNotFrozen():
                            need = 0
                            if l.isBlank(): need += 1
                            if r.isBlank(): need += 1
                            if count_list[ridx] >= need:
                                if c.isBlank(): need_these.append(c)
                                if l.isBlank(): need_these.append(l)
                                if r.isBlank(): need_these.append(r)
                                found_one = True
                        if lc and rc and lc.isNotFrozen() and rc.isNotFrozen():
                           need = 0
                           if lc.isBlank(): need += 1
                           if rc.isBlank(): need += 1
                           if count_list[ridx+1] >= need:
                                if found_one: continue
                                if c.isBlank(): need_these.append(c)
                                if lc.isBlank(): need_these.append(lc)
                                if rc.isBlank(): need_these.append(rc)
                                found_one = True
                    # look left
                    if lp and lp.isNotFrozen() and (lp.isFilled() or count_list[ridx-1] > 0):
                        if l and ll and l.isNotFrozen() and ll.isNotFrozen():
                            need = 0
                            if l.isBlank(): need += 1
                            if ll.isBlank(): need += 1
                            if count_list[ridx] >= need:
                                if found_one: continue
                                if lp.isBlank(): need_these.append(lp)
                                if l.isBlank(): need_these.append(l)
                                if ll.isBlank(): need_these.append(ll)
                                found_one = True
                    # look right
                    if rp and rp.isNotFrozen() and (rp.isFilled() or count_list[ridx-1] > 0):
                        if r and rr and r.isNotFrozen() and rr.isNotFrozen():
                            need = 0
                            if r.isBlank(): need += 1
                            if rr.isBlank(): need += 1
                            if count_list[ridx] >= need:
                                if found_one: continue
                                if rp.isBlank(): need_these.append(rp)
                                if r.isBlank(): need_these.append(r)
                                if rr.isBlank(): need_these.append(rr)
                                found_one = True
                    if len(need_these): did_something = True
                    for n in need_these: n.fill()
                    continue
                elif (node.direction == dir.DOWN):
                    # look up
                    if (p and p.isNotFrozen() and (p.isFilled() or count_list[ridx-1] > 0)):
                        if (l and r and l.isNotFrozen() and r.isNotFrozen()):
                            need = 0
                            if (l.isBlank()): need += 1
                            if (r.isBlank()): need += 1
                            if (count_list[ridx] >= need):
                                if found_one: continue
                                if p.isBlank(): need_these.append(p)
                                if l.isBlank(): need_these.append(l)
                                if r.isBlank(): need_these.append(r)
                                found_one = True
                        if (lp and rp and lp.isNotFrozen() and rp.isNotFrozen()):
                           need = 0
                           if (lp.isBlank()): need += 1
                           if (rp.isBlank()): need += 1
                           if (count_list[ridx-1] >= need):
                                if found_one: continue
                                if p.isBlank(): need_these.append(p)
                                if lp.isBlank(): need_these.append(lp)
                                if rp.isBlank(): need_these.append(rp)
                                found_one = True
                    # look left
                    if (lc and lc.isNotFrozen() and (lc.isFilled() or count_list[ridx+1] > 0)):
                        if (l and ll and l.isNotFrozen() and ll.isNotFrozen()):
                            need = 0
                            if (l.isBlank()): need += 1
                            if (ll.isBlank()): need += 1
                            if (count_list[ridx] >= need):
                                if found_one: continue
                                if lc.isBlank(): need_these.append(lc)
                                if l.isBlank(): need_these.append(l)
                                if ll.isBlank(): need_these.append(ll)
                                found_one = True
                    # look right
                    if (rc and rc.isNotFrozen() and (rc.isFilled() or count_list[ridx+1] > 0)):
                        if (r and rr and r.isNotFrozen() and rr.isNotFrozen()):
                            need = 0
                            if (r.isBlank()): need += 1
                            if (rr.isBlank()): need += 1
                            if (count_list[ridx] >= need):
                                if found_one: continue
                                if rc.isBlank(): need_these.append(rc)
                                if r.isBlank(): need_these.append(r)
                                if rr.isBlank(): need_these.append(rr)
                                found_one = True
                    if len(need_these): did_something = True
                    for n in need_these: n.fill()
                    continue
        return did_something

    def solve(self):
        self.auto_solve = True
        did_something = True
        while (did_something):
            did_something = False
            for i in range(0, 3):
                if i == 0: rlist = self.rlist_a
                elif i == 1: rlist = self.rlist_b
                elif i == 2: rlist = self.rlist_c
                did_something |= self.easy_fill(rlist)
            did_something |= self.freeze_impossibles(self.rlist_a, self.count_list_a)
            did_something |= self.extend_singles(self.rlist_a, self.count_list_a)
        self.canvas.delete("temp")
    
    def ctrl_left(self, event):
        if (self.cursor == None): return
        self.cidx = 0
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.draw()
    
    def ctrl_right(self, event):
        if (self.cursor == None): return
        self.cidx = len(self.rlist[self.ridx])-1
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.draw()
    
    def ctrl_up(self, event):
        if (self.cursor == None): return
        while self.cidx > 0 and len(self.rlist[self.ridx-1]) >= self.cidx:
            self.ridx -= 1
            self.cidx -= 1
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.draw()
    
    def ctrl_down(self, event):
        if (self.cursor == None): return
        while (self.ridx < self.rcnt-1):
            self.ridx += 1
            self.cidx += 1
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.draw()

    def shift_left(self, event):
        if (self.cursor == None): return
        self.cursor.fill()
        self.cidx -= 1
        if (self.cidx < 0): self.cidx = len(self.rlist[self.ridx]) - 1
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.cursor.fill()
        self.draw()

    def shift_right(self, event):
        if (self.cursor == None): return
        self.cursor.fill()
        self.cidx += 1
        if (self.cidx == len(self.rlist[self.ridx])): self.cidx = 0
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.cursor.fill()
        self.draw()

    def shift_up(self, event):
        if (self.cursor == None): return
        self.cursor.fill()
        if (self.ridx > 0):
            if (self.cidx == 0):
                self.cidx = 1
            elif (self.cidx == (len(self.rlist[self.ridx]) - 1)):
                self.cidx -= 1
            else:
                self.ridx -= 1
                self.cidx -= 1
            self.cursor = self.rlist[self.ridx][self.cidx]
            self.cursor.fill()
        self.draw()

    def shift_down(self, event):
        if (self.cursor == None): return
        self.cursor.fill()
        if (self.ridx < (self.rcnt - 1)):
            self.ridx += 1
            self.cidx += 1
            self.cursor = self.rlist[self.ridx][self.cidx]
            self.cursor.fill()
        self.draw()

    def alt_left(self, event):
        if (self.cursor == None): return
        self.cursor.freeze()
        self.cidx -= 1
        if (self.cidx < 0): self.cidx = len(self.rlist[self.ridx]) - 1
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.cursor.freeze()
        self.draw()

    def alt_right(self, event):
        if (self.cursor == None): return
        self.cursor.freeze()
        self.cidx += 1
        if (self.cidx == len(self.rlist[self.ridx])): self.cidx = 0
        self.cursor = self.rlist[self.ridx][self.cidx]
        self.cursor.freeze()
        self.draw()

    def alt_up(self, event):
        if (self.cursor == None): return
        self.cursor.freeze()
        if (self.ridx > 0):
            if (self.cidx == 0):
                self.cidx = 1
            elif (self.cidx == (len(self.rlist[self.ridx]) - 1)):
                self.cidx -= 1
            else:
                self.ridx -= 1
                self.cidx -= 1
            self.cursor = self.rlist[self.ridx][self.cidx]
            self.cursor.freeze()
        self.draw()

    def alt_down(self, event):
        if (self.cursor == None): return
        self.cursor.freeze()
        if (self.ridx < (self.rcnt - 1)):
            self.ridx += 1
            self.cidx += 1
            self.cursor = self.rlist[self.ridx][self.cidx]
            self.cursor.freeze()
        self.draw()

    def undo(self):
        cmd.undo()
        self.draw()

    def redo(self):
        cmd.redo()
        self.draw()

    def key(self, event):
        k = repr(event.keysym)
        # print(k)
        if (k == "'z'"): return self.undo()
        if (k == "'x'"): return self.redo()
        if (k == "'r'"): return self.rotate()
        if (k == "'F1'"):
            if cmd.play_mode:
                self.solve()
        if (k == "'q'"): self.quit()
        if (k == "'n'"): self.new()
        if (k == "'o'"): self.open()
        if (k == "'c'"): self.clear()
        if (k == "'s'"): self.save()
        if (k == "'p'"): self.play()
        if (k == "'h'"): self.hide = not self.hide
        if (k == "'equal'" or k == "'plus'"): self.more_rows()
        if (k == "'minus'" or k == "'underscore'"): self.fewer_rows()

        if (k == "'Home'"): self.cursor = self.top
        if (k == "'End'"): self.cursor = self.rlist[self.rcnt-1][self.cidx+self.rcnt-self.ridx-1]

        if (k == "'Prior'"):
            if (self.cursor == self.top):
                self.cursor = self.left
            elif (self.cursor == self.left):
                self.cursor = self.right
            else: self.cursor = self.top

        if (k == "'Next'"):
            if (self.cursor == self.top):
                self.cursor = self.right
            elif (self.cursor == self.right):
                self.cursor = self.left
            else: self.cursor = self.top

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
            self.cursor.toggle(dir.LEFT)

        if (k == "'f'"): # freeze
            if (self.cursor == None): self.cursor = self.top
            self.cursor.toggle(dir.RIGHT)

        self.draw()

    def more_rows(self):
        self.rcnt += 1
        if (self.rcnt >= 15):
            self.length -= self.rcnt - 15
            self.half_length = self.length // 2
            self.altitude = self.length * sqrt3 / 2.0
        self.tv_rows.set(str(self.rcnt))
        self.new()

    def fewer_rows(self):
        if (self.rcnt < 3): return
        self.rcnt -= 1
        if (self.rcnt == 15):
            self.length = default_length
            self.half_length = self.length // 2
            self.altitude = self.length * sqrt3 / 2.0
        self.tv_rows.set(str(self.rcnt))
        self.new()

    def createWidgets(self):
        self.winfo_toplevel().title("Triangulation")

        self.remove_row = Button(self, text="--")
        self.remove_row["command"] = self.fewer_rows
        self.remove_row.pack({"side": "left"})

        self.row_label = Label(self)
        self.row_label["text"] = "rows:"
        self.row_label.pack({"side": "left"})
        self.rcnt = 14
        self.tv_rows = StringVar()
        self.tv_rows.set(str(self.rcnt))
        self.row_count = Label(self)
        self.row_count["textvariable"] = self.tv_rows
        self.row_count.pack({"side": "left"})

        self.add_row = Button(self, text="++")
        self.add_row["command"] = self.more_rows
        self.add_row.pack({"side": "left"})

        self.undo_button = Button(self, text="undo")
        self.undo_button["command"] = self.undo
        self.undo_button.pack({"side": "left"})

        self.redo_button = Button(self, text="redo")
        self.redo_button["command"] = self.redo
        self.redo_button.pack({"side": "left"})

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
        self.file_name = "save.txt"
        self.dir_name = "."
        self.auto_solve = False
        self.pack()
        self.createWidgets()
        master.bind("<Key>", self.key)
        master.bind("<Control-Left>", self.ctrl_left)
        master.bind("<Control-Right>", self.ctrl_right)
        master.bind("<Control-Up>", self.ctrl_up)
        master.bind("<Control-Down>", self.ctrl_down)
        master.bind("<Shift-Left>", self.shift_left)
        master.bind("<Shift-Right>", self.shift_right)
        master.bind("<Shift-Up>", self.shift_up)
        master.bind("<Shift-Down>", self.shift_down)
        master.bind("<Alt-Left>", self.alt_left)
        master.bind("<Alt-Right>", self.alt_right)
        master.bind("<Alt-Up>", self.alt_up)
        master.bind("<Alt-Down>", self.alt_down)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.click)
        self.right_arrow = PhotoImage(file="right arrow.gif")
        self.up_left_arrow = PhotoImage(file="up left arrow.gif")
        self.down_left_arrow = PhotoImage(file="down left arrow.gif")
        self.rlist = None
        self.ridx = 0
        self.cidx = 0
        self.length = default_length
        self.half_length = self.length // 2
        self.altitude = self.length * sqrt3 / 2.0
        self.new()

    def play(self):
        if (cmd.play_mode == False):
            cmd.play_mode = True
            self.play_button.config(text="play mode")
            self.clear()
            cmd.reset()
        else:
            self.refill()
            cmd.play_mode = False
            self.play_button.config(text="design mode")
        self.draw()

    # create a new pyramid
    def new(self):
        if self.rcnt == 0: return
        triangle.next_id = 0
        self.winner = False
        self.hide = False
        # we maintain three arrays of rows
        # one starting on each corner (a, b, and c)
        # this makes rotation easier
        #
        # we fill all three arrays at the same time
        # which requires some juggling of indices
        #
        self.rlist_a = [None for x in range(self.rcnt)]
        self.rlist_b = [None for x in range(self.rcnt)]
        self.rlist_c = [None for x in range(self.rcnt)]
        self.count_list_a = [0 for x in range(self.rcnt)]
        self.count_list_b = [0 for x in range(self.rcnt)]
        self.count_list_c = [0 for x in range(self.rcnt)]

        for ridx in range(0, self.rcnt):
            ccnt = ridx * 2 + 1
            self.rlist_a[ridx] = [None for x in range(ccnt)]
            self.rlist_b[ridx] = [None for x in range(ccnt)]
            self.rlist_c[ridx] = [None for x in range(ccnt)]

        for a_ridx in range(0, self.rcnt):
            b_ridx = self.rcnt - 1
            b_cidx = a_ridx * 2
            c_ridx = self.rcnt - a_ridx - 1
            c_cidx = (self.rcnt - a_ridx - 1) * 2
            ccnt = a_ridx * 2 + 1

            for a_cidx in range(0, ccnt):
                node = triangle()
                if (a_ridx == 0 and a_cidx == 0):
                    self.cursor = self.top = node

                node.a_ridx = a_ridx
                node.a_cidx = a_cidx
                node.b_ridx = b_ridx
                node.b_cidx = b_cidx
                node.c_ridx = c_ridx
                node.c_cidx = c_cidx
                self.rlist_a[a_ridx][a_cidx] = node
                self.rlist_b[b_ridx][b_cidx] = node
                self.rlist_c[c_ridx][c_cidx] = node
                b_cidx -= 1
                if (a_cidx % 2):
                    b_ridx -= 1
                    c_cidx -= 1
                    node.direction = dir.DOWN
                else:
                    c_cidx += 1
                    c_ridx += 1
                    node.direction = dir.UP
        
        self.left = self.rlist_b[0][0]
        self.right = self.rlist_c[0][0]

        self.rlist = self.rlist_a
        self.count_list = self.count_list_a
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
        if (cmd.play_mode): msg = "play mode"
        self.canvas.create_text(100, 50, text=msg, font="12x24", tags="text")
        
        total_cnt = 0
        for ridx in range(0, self.rcnt):
            cnt = 0
            clist = self.rlist[ridx]
            for cidx in range(0, len(clist)):
                node = clist[cidx]
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

                if (cmd.play_mode == True and (node.answer == True and node.state != state.filled) or (node.answer == False and node.state == state.filled)):
                    self.winner = False

                color = "ivory"
                if (node.state == state.filled):
                    color = "medium sea green"
                    if (cmd.play_mode == True): cnt -= 1
                elif (node.state == state.blank and cmd.play_mode): color = "thistle1"
                elif (node.state == state.frozen): color = "gray"
                if (self.hide == True): color = "white"

                mytags = ["all"]
                mytags.append(str("id") + str(node.id))
                mytags.append(str("arow") + str(node.a_ridx))
                mytags.append(str("acol") + str(node.a_cidx))
                mytags.append(str("brow") + str(node.b_ridx))
                mytags.append(str("bcol") + str(node.b_cidx))
                mytags.append(str("crow") + str(node.c_ridx))
                mytags.append(str("ccol") + str(node.c_cidx))

                self.canvas.tag_bind(str("id") + str(node.id), "<Button-1>", lambda event, n=node: self.left_click(event, n))
                self.canvas.tag_bind(str("id") + str(node.id), "<Button-3>", lambda event, n=node: self.right_click(event, n))
            
                if (node.direction == dir.UP):
                    node.xy = ((node.xleft, node.ybottom), (node.xright, node.ybottom), (node.xmiddle, node.ytop))
                    mytags.append("up")
                else:
                    node.xy = ((node.xleft, node.ytop), (node.xright, node.ytop), (node.xmiddle, node.ybottom))
                    mytags.append("down")
                node.draw(self.canvas, color, mytags)

            color = "black"
            if (cnt < 0): color = "tomato"
            elif (cnt == 0): color = "darkgreen"
            x = center_x - 1.3 * self.length - (self.half_length * (ridx + 1))
            y = (ridx + 2) * self.altitude - (self.altitude/2)
            if (self.hide == False and self.cursor != None and ridx == self.ridx):
                self.canvas.create_oval(x-12, y-12, x+12, y+12, fill='gold', tags="text")
            self.canvas.create_text(x, y, fill=color, text=cnt, font="12x24", tags="text")
            self.count_list[ridx] = cnt

        if (self.cursor and self.hide == False and (already_won == True or cmd.play_mode == False or self.winner == False)):
            self.cursor.outline(self.canvas)

        # winner?
        if (total_cnt and already_won == False and cmd.play_mode and self.winner):
            self.canvas.delete("text")
            self.chicken_dinner()
            return

        # calculate more totals
        next_list = self.rlist
        for i in range(0, 2):
            if (next_list == self.rlist_a):
                next_list = self.rlist_b
                next_count_list = self.count_list_b
            elif (next_list == self.rlist_b):
                next_list = self.rlist_c
                next_count_list = self.count_list_c
            else:
                next_list = self.rlist_a
                next_count_list = self.count_list_a

            for ridx in range(0, len(next_list)):
                clist = next_list[len(next_list) - ridx - 1]
                cnt = 0
                this_one = False
                for cidx in range(0, len(clist)):
                    node = clist[cidx]
                    if (node == self.cursor):
                        this_one = True
                    if (node.answer): cnt += 1
                    if (node.state == state.filled and cmd.play_mode == True): cnt -= 1
                color = "black"
                if (cnt < 0): color = "tomato"
                elif (cnt == 0): color = "darkgreen"
                if i == 0:
                    x = center_x - self.length + (self.half_length * (ridx + 1))
                    y =  (ridx + 2) * self.altitude - (self.altitude)
                else:
                    x = center_x - (self.half_length/2) + self.rcnt * self.half_length - (self.length * (ridx + 1))
                    y = (self.rcnt + 2) * self.altitude - (self.altitude / 2)
                if (self.hide == False and this_one):
                    self.canvas.create_oval(x-12, y-12, x+12, y+12, fill='gold')
                self.canvas.create_text(x, y, fill=color, text=cnt, font="12x24", tags="text")
                next_count_list[len(next_list) - ridx - 1] = cnt

        # arrows
        self.canvas.create_image(center_x - (self.half_length * self.rcnt / 2) - 130, self.rcnt * self.altitude / 2, image=self.right_arrow)
        self.canvas.create_image(center_x + (self.half_length * self.rcnt / 2) + 30, ((self.rcnt - 1) * self.altitude / 2) - self.altitude / 2, image=self.down_left_arrow)
        self.canvas.create_image(center_x - 15, (self.rcnt + 3) * self.altitude, image=self.up_left_arrow)
        self.canvas.create_text(100, 150, text="total shaded triangles: " + str(total_cnt), font="12x24", tags="text")

    def open(self):
        f = filedialog.askopenfile(initialdir = self.dir_name, filetypes = (("text","*.txt"), ("all files","*.*")))
        if f == None: return
        data = list(f)
        self.rcnt = len(data)
        self.new()
        for ridx in range(0, self.rcnt):
            line = data[ridx]
            clist = line.split()
            ccnt = len(clist)
            for cidx in range(ccnt):
                node = self.rlist[ridx][cidx]
                if (clist[cidx][:1] == 'X'): node.answer = True
                if (clist[cidx][-1:] == 'f'): node.state = state.filled
                if (clist[cidx][-1:] == '!'): node.state = state.frozen
        cmd.play_mode = True
        cmd.reset()
        self.draw()
        self.file_name = f.name[f.name.rfind('/')+1:]
        self.dir_name = f.name[:f.name.rfind('/')]
        self.winfo_toplevel().title("Triangulation - " + self.file_name)

    # X - answer
    # f - filled
    # ! - frozen
    # . - blank
    def save(self):
        f = filedialog.asksaveasfile(initialfile = self.file_name, initialdir = ".", filetypes = (("text","*.txt"), ("all files","*.*")))
        if f == None: return
        for ridx in range(0, self.rcnt):
            for cidx in range(0, len(self.rlist[ridx])):
                node = self.rlist[ridx][cidx]
                f.write(" ")
                if (node.answer): f.write("X")
                if (cmd.play_mode == True and node.state == state.filled): f.write("f")
                elif (node.state == state.frozen): f.write("!")
                elif (node.state == state.blank): f.write(".")
            if (ridx < self.rcnt - 1): f.write("\n")
        f.close()
        self.file_name = f.name[f.name.rfind('/')+1:]
        self.dir_name = f.name[:f.name.rfind('/')]
        self.winfo_toplevel().title("Triangulation - " + self.file_name)

    # winner, winner
    def chicken_dinner(self):
        # the entire pyramid
        for i in range(0, 3):
            color = random_color()
            self.canvas.itemconfig("all", fill=color)
            self.canvas.update_idletasks()
            self.canvas.after(100)

        # the up and down triangles
        for i in range(0, 3):
            for j in range(0, 4):
                c = random_color()
                if j < 2: self.canvas.itemconfig("up", fill=c)
                else: self.canvas.itemconfig("down", fill=c)
                self.canvas.update_idletasks()
                self.canvas.after(100)

        # twinkles
        for i in range(0, 0):
            for j in range(0, triangle.next_id//3):
                color = random_color()
                mytags = "id"
                mytags += str(random.randint(0, triangle.next_id))
                self.canvas.itemconfig(mytags, fill=color)
            self.canvas.update_idletasks()
            self.canvas.after(10)

        # row wipes
        atags = "arow"
        btags = "brow"
        ctags = "crow"
        for i in range(0, 3):
            r, g, b = random_rgb()
            c1 = make_color(r, g, b)
            r, g, b = new_color(r, g, b)
            c2 = make_color(r, g, b)
            r, g, b = new_color(r, g, b)
            c3 = make_color(r, g, b)
            for k in range(0, self.rcnt):
                self.canvas.itemconfig(atags + str(k), fill=c1)
                self.canvas.itemconfig(btags + str(k), fill=c2)
                self.canvas.itemconfig(ctags + str(k), fill=c3)
                #self.canvas.itemconfig(atags + str(self.rcnt-k+1), fill=c2a)
                self.canvas.update_idletasks()
                self.canvas.after(50)
        self.draw()

root = Tk()
app = pyramid(master=root)
app.mainloop()
root.destroy()
