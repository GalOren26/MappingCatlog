#################
#               #
#  Point Class  #
#               #
#################
import math, time
import line as Line
from graphics import canvas
class Point:
    "Create an object of type Point from two integers"
    def __init__(self,x,y=None,TileId=None ):
            self.x = x
            self.y = y
            self.WasHere=False
            self.TileId=TileId
    @staticmethod
    def Xcord(self):
           return self.x
    @staticmethod
    def Ycord(self):
           return self.y       
    def X(self):
        return self.x
    def Y(self):
        return self.y

    def move(self,dx,dy):
        "Move point by dx and dy"
        self.x += dx
        self.y += dy

    def show(self):
        print( "x = ", self.x,)
        print( "y = ", self.y)

    def rotate90(self,ox,oy):
        dx = self.x - ox
        dy = self.y - oy
        self.x, self.y = ox-dy , oy + dx

    def scale(self, sx, sy):
        self.x = sx * self.x
        self.y = sy * self.y


    def draw(self):
        x1 = self.x-2
        y1 = self.y-2
        x2 = self.x+2
        y2 = self.y+2
        id = canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="")
        return id


    def text(self,t,**kwargs):
        dx = kwargs.pop('dx', 0)
        dy = kwargs.pop('dy', -1)
        # kwargs.setdefault('anchor', 's')
        kwargs.setdefault('font', 'Consolas 4')
        kwargs.setdefault('tags', ['TEXT', 'POINT'])
        kwargs['text'] = t
        #id = canvas.create_text(self.x + dx, self.y + dy, **kwargs)
        id = canvas.create_text(self.x + dx, self.y + dy, anchor='s' ,text=t)
        return id
    # this is how a Point object will be printed with the Python print statement:
    def __str__(self):
        return "P(%.6f,%.6f)"  %  (self.x, self.y)
    def __repr__(self):
            return "P(%.6f,%.6f)"  %  (self.x, self.y)
    def __lt__(self,line):## inresiction is zero  point is "lower " than line!
        assert isinstance(line,Line.Line),"you must provide a Line as second argument!"
        if  line.p1.x==line.p2.x:
            Yminline=min(line.p1.y,line.p2.y)
            return True if self.y<Yminline else False 
        elif line.p1.y==line.p2.y:
            Xminline=min(line.p1.x,line.p2.x)
            return True if self.x<Xminline else False 
        raise Exception('Not horintal or vertical line!')

    def __gt__(self,line):## inresiction is zero point is "greater " than line!
        assert isinstance(line,Line.Line),"you must provide a Line as second argument!"
        if line.p1.x==line.p2.x:
            Ymaxline=max(line.p1.y,line.p2.y)
            return True if Ymaxline<self.y else False 
        elif line.p1.y==line.p2.y:
            Xmaxline=max(line.p1.x,line.p2.x)
            return True if Xmaxline<self.x else False 
        raise Exception('Not horizontal or vertical line!')
    def __eq__(self,point):
      assert isinstance(point,Point),"you must provide a point as second argument!"
      if (point.X()==self.X() and point.Y()==self.Y()):
        return True 
      else: 
        return False
    def __hash__(self):
        return hash((self.X(),self.Y()))
    def __add__(self,Mypoint):
        self.x+=Mypoint.X()
        self.y+=Mypoint.Y()
        return self
def test3():
    p1 =Point(400, 400)
    p1.draw()
    p1.text(p1)
    p1.move(100,100)
    p1.text(p1)
    p1.draw()
    p1.rotate90(400,400)
    p1.draw()
   # Tkinter.mainloop()

if __name__ == "__main__":
    test3()
