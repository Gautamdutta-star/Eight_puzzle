import tkinter as tk
from tkinter import messagebox
import random
import time
import heapq
import winsound
import os


GOAL = (1,2,3,4,5,6,7,8,0)
SCORE_FILE = "highscore.txt"


# ----------------- SOUND -----------------
def play_move():
    winsound.Beep(800, 100)

def play_win():
    winsound.Beep(1500, 500)


# ----------------- HEURISTIC -----------------
def heuristic(state):

    dist = 0

    for i in range(9):

        if state[i] != 0:

            x1, y1 = divmod(i,3)
            x2, y2 = divmod(state[i]-1,3)

            dist += abs(x1-x2) + abs(y1-y2)

    return dist


# ----------------- NEIGHBOURS -----------------
def neighbors(state):

    result = []
    blank = state.index(0)

    r, c = divmod(blank,3)

    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr,dc in moves:

        nr,nc = r+dr, c+dc

        if 0<=nr<3 and 0<=nc<3:

            idx = nr*3+nc
            new = list(state)

            new[blank],new[idx] = new[idx],new[blank]

            result.append(tuple(new))

    return result


# ----------------- A* SOLVER -----------------
def solve(start):

    pq = []
    heapq.heappush(pq,(0,start))

    parent = {start:None}
    cost = {start:0}

    while pq:

        _,cur = heapq.heappop(pq)

        if cur == GOAL:
            return path(parent,cur)

        for nxt in neighbors(cur):

            new_cost = cost[cur]+1

            if nxt not in cost or new_cost < cost[nxt]:

                cost[nxt] = new_cost
                f = new_cost + heuristic(nxt)

                heapq.heappush(pq,(f,nxt))
                parent[nxt] = cur

    return None


def path(parent,node):

    p=[]

    while node:
        p.append(node)
        node=parent[node]

    return p[::-1]


# ----------------- GAME CLASS -----------------
class Puzzle:

    def __init__(self):

        self.win = tk.Tk()
        self.win.title("8 Puzzle Pro Version")
        self.win.geometry("380x560")

        self.moves = 0
        self.start = time.time()

        self.board = list(GOAL)
        self.shuffle()

        self.btns=[]

        self.ui()
        self.timer()

        self.win.mainloop()


    # ----------------- SHUFFLE -----------------
    def shuffle(self):

        while True:

            temp=list(GOAL)
            random.shuffle(temp)

            if temp!=list(GOAL):
                self.board=temp
                break


    # ----------------- UI -----------------
    def ui(self):

        self.info=tk.Label(self.win,text="8 Puzzle Game",
                           font=("Arial",16,"bold"))
        self.info.pack(pady=5)


        self.time_lbl=tk.Label(self.win,text="Time: 0 sec",
                               font=("Arial",12))
        self.time_lbl.pack()


        self.move_lbl=tk.Label(self.win,text="Moves: 0",
                               font=("Arial",12))
        self.move_lbl.pack()


        self.manhattan_lbl=tk.Label(self.win,text="Manhattan: 0",
                                    font=("Arial",12))
        self.manhattan_lbl.pack()


        frame=tk.Frame(self.win)
        frame.pack(pady=10)


        for i in range(9):

            b=tk.Button(frame,width=6,height=3,
                        font=("Arial",14),
                        command=lambda i=i:self.click(i))

            b.grid(row=i//3,column=i%3,padx=5,pady=5)

            self.btns.append(b)


        self.solve_btn=tk.Button(self.win,text="Auto Solve 🤖",
                                 bg="lightgreen",
                                 command=self.auto)

        self.solve_btn.pack(pady=5)


        self.reset_btn=tk.Button(self.win,text="Restart",
                                 bg="lightblue",
                                 command=self.restart)

        self.reset_btn.pack(pady=5)


        self.high_btn=tk.Button(self.win,text="View High Score",
                                bg="orange",
                                command=self.show_score)

        self.high_btn.pack(pady=5)


        self.refresh()


    # ----------------- DISPLAY -----------------
    def refresh(self):

        for i in range(9):

            if self.board[i]==0:

                self.btns[i]["text"]=""
                self.btns[i]["bg"]="white"

            else:

                self.btns[i]["text"]=self.board[i]
                self.btns[i]["bg"]="lightyellow"


        self.move_lbl.config(text=f"Moves: {self.moves}")

        dist = heuristic(tuple(self.board))
        self.manhattan_lbl.config(text=f"Manhattan: {dist}")


    # ----------------- CLICK -----------------
    def click(self,i):

        blank=self.board.index(0)

        r1,c1=divmod(i,3)
        r2,c2=divmod(blank,3)

        if abs(r1-r2)+abs(c1-c2)==1:

            self.board[i],self.board[blank]=\
            self.board[blank],self.board[i]

            self.moves+=1
            play_move()

            self.refresh()

            if tuple(self.board)==GOAL:
                self.win_game()


    # ----------------- TIMER -----------------
    def timer(self):

        t=int(time.time()-self.start)

        self.time_lbl.config(text=f"Time: {t} sec")

        self.win.after(1000,self.timer)


    # ----------------- WIN -----------------
    def win_game(self):

        play_win()

        t=int(time.time()-self.start)

        self.save_score(self.moves,t)

        msg=f"""
Solved 🎉

Moves: {self.moves}
Time: {t} sec
"""

        messagebox.showinfo("Winner",msg)


    # ----------------- AUTO SOLVE -----------------
    def auto(self):

        self.solve_btn["state"]="disabled"

        sol=solve(tuple(self.board))

        self.animate(sol,0)


    def animate(self,sol,i):

        if i>=len(sol):

            if tuple(self.board)==GOAL:
                self.win_game()

            return

        self.board=list(sol[i])
        self.refresh()

        self.win.after(300,
            lambda:self.animate(sol,i+1))


    # ----------------- HIGH SCORE -----------------
    def save_score(self,moves,time):

        record=f"Moves:{moves} Time:{time}"

        with open(SCORE_FILE,"w") as f:
            f.write(record)


    def show_score(self):

        if os.path.exists(SCORE_FILE):

            with open(SCORE_FILE) as f:
                data=f.read()

        else:
            data="No Record Yet"

        messagebox.showinfo("High Score",data)


    # ----------------- RESET -----------------
    def restart(self):

        self.moves=0
        self.start=time.time()

        self.shuffle()
        self.refresh()

        self.solve_btn["state"]="normal"



# ----------------- RUN -----------------

if __name__=="__main__":
    Puzzle()
