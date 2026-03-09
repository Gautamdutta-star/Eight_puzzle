from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
import random
import time
import heapq


GOAL = (1,2,3,4,5,6,7,8,0)


# ---------- A* SOLVER ----------
def heuristic(state):
    d = 0
    for i in range(9):
        if state[i] != 0:
            x1,y1 = divmod(i,3)
            x2,y2 = divmod(state[i]-1,3)
            d += abs(x1-x2)+abs(y1-y2)
    return d


def neighbors(state):
    res=[]
    blank=state.index(0)
    r,c=divmod(blank,3)

    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc=r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            idx=nr*3+nc
            new=list(state)
            new[blank],new[idx]=new[idx],new[blank]
            res.append(tuple(new))
    return res


def solve(start):
    pq=[]
    heapq.heappush(pq,(0,start))
    parent={start:None}
    cost={start:0}

    while pq:
        _,cur=heapq.heappop(pq)

        if cur==GOAL:
            path=[]
            while cur:
                path.append(cur)
                cur=parent[cur]
            return path[::-1]

        for nxt in neighbors(cur):
            nc=cost[cur]+1
            if nxt not in cost or nc<cost[nxt]:
                cost[nxt]=nc
                f=nc+heuristic(nxt)
                heapq.heappush(pq,(f,nxt))
                parent[nxt]=cur
    return None


# ---------- MAIN GAME ----------
class PuzzleApp(App):

    def build(self):

        self.moves=0
        self.start_time=time.time()

        self.board=list(GOAL)
        random.shuffle(self.board)

        self.root=GridLayout(cols=1)

        self.info=Label(text="Swipe to Play 8-Puzzle 📱",
                        size_hint=(1,.1))
        self.root.add_widget(self.info)

        self.timer=Label(text="Time: 0",
                         size_hint=(1,.1))
        self.root.add_widget(self.timer)

        self.move_lbl=Label(text="Moves: 0",
                            size_hint=(1,.1))
        self.root.add_widget(self.move_lbl)

        self.grid=GridLayout(cols=3,
                             size_hint=(1,.6))

        self.btns=[]

        for i in range(9):
            b=Button(font_size=24)
            self.grid.add_widget(b)
            self.btns.append(b)

        self.root.add_widget(self.grid)

        self.solve_btn=Button(text="Auto Solve 🤖",
                              size_hint=(1,.1))
        self.solve_btn.bind(on_press=self.auto_solve)
        self.root.add_widget(self.solve_btn)

        self.refresh()

        # Swipe detection
        Window.bind(on_touch_down=self.touch_start,
                    on_touch_up=self.touch_end)

        self.sx=self.sy=0

        Clock.schedule_interval(self.update_time,1)

        return self.root


    # ---------- Touch Start ----------
    def touch_start(self,win,touch):
        self.sx=touch.x
        self.sy=touch.y


    # ---------- Touch End ----------
    def touch_end(self,win,touch):

        dx=touch.x-self.sx
        dy=touch.y-self.sy

        if abs(dx)<40 and abs(dy)<40:
            return

        if abs(dx)>abs(dy):
            if dx>0:
                self.move_blank("right")
            else:
                self.move_blank("left")
        else:
            if dy>0:
                self.move_blank("up")
            else:
                self.move_blank("down")


    # ---------- Move Blank ----------
    def move_blank(self,dir):

        blank=self.board.index(0)
        r,c=divmod(blank,3)

        target=None

        if dir=="up" and r<2:
            target=(r+1)*3+c
        elif dir=="down" and r>0:
            target=(r-1)*3+c
        elif dir=="left" and c<2:
            target=r*3+(c+1)
        elif dir=="right" and c>0:
            target=r*3+(c-1)

        if target is not None:

            self.board[blank],self.board[target]=\
            self.board[target],self.board[blank]

            self.moves+=1
            self.refresh()

            if tuple(self.board)==GOAL:
                self.info.text="🎉 Solved!"


    # ---------- Refresh ----------
    def refresh(self):

        for i in range(9):

            self.btns[i].text = \
            str(self.board[i]) if self.board[i]!=0 else ""

        self.move_lbl.text=f"Moves: {self.moves}"


    # ---------- Timer ----------
    def update_time(self,dt):

        t=int(time.time()-self.start_time)
        self.timer.text=f"Time: {t}"


    # ---------- Auto Solve ----------
    def auto_solve(self,btn):

        sol=solve(tuple(self.board))

        if sol:
            self.animate(sol,0)


    def animate(self,sol,i):

        if i>=len(sol):
            return

        self.board=list(sol[i])
        self.refresh()

        Clock.schedule_once(
            lambda dt:self.animate(sol,i+1),.3)


# ---------- RUN ----------
if __name__=="__main__":
    PuzzleApp().run()