################
#              #
#  Line Class  #
#              #
################
import point 
import math
from graphics import canvas
import random
class Line:
    def __init__(self, p1, p2,TileId=None,type="0start"):
        self.p1 = point.Point(p1.X(),p1.Y(),TileId)
        self.p2 = point.Point(p2.X(),p2.Y(),TileId)
        self.type=type
        if (TileId!=None):
            self.TileId=TileId
        if( self.p1.X()==self.p2.X()):
            self.direction="vertical"
        elif self.p1.Y()==self.p2.Y():
              self.direction="horizontal"
        else:
              raise Exception("line iss neither horizontal nor vertical")
#------line metheods--------
    def move(self,dx,dy):
        "Move line by dx and dy"
        self.p1.move(dx,dy)
        self.p2.move(dx,dy)

    def length(self):
        x1 = self.p1.X()
        y1 = self.p1.Y()
        x2 = self.p2.X()
        y2 = self.p2.Y()
        len = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return len

    def middle(self):
        x = (self.p1.X() + self.p2.X()) / 2
        y = (self.p1.Y() + self.p2.Y()) / 2
        return point.Point(x,y)
    def interval(self):#(min,max)
        if (self.direction=="vertical"):
            return (min(self.p1.Y(),self.p2.Y()),max(self.p1.Y(),self.p2.Y()))
        else:
            return (min(self.p1.X(),self.p2.X()),max(self.p1.X(),self.p2.X()))
    def orderPoints(self):
        if (self.direction=="vertical"):
                maxpoint=max([self.p1,self.p2],key=lambda  point :point.Y())
                minpoint= self.p2 if maxpoint is self.p1 else self.p1
        else:
                maxpoint=max([self.p1,self.p2],key=lambda  point :point.X())
                minpoint= self.p2 if maxpoint is self.p1 else self.p1
        return (minpoint,maxpoint)
#--------math methods------------
    @staticmethod
    def UnionLines(lines):
        union=[] 
        i,j=0,0
        while(i<len(lines) ):
            while((i+j+1)<len(lines)):
                if(lines[i+j][1]>lines[i+j+1][0]):
                    j+=1
                    continue
                else: break
            top=max([line[1] for line in lines[i:i+j+1]])
            union.append((lines[i][0],top))
            i=i+j+1
            j=0
        return union

    def intersection(self,unionlines):
        selfinterval=self.interval()
        intersect=[]
        for segmant in unionlines: 
            if(segmant[1]<selfinterval[0] or segmant[0]>selfinterval[1]):
                 continue
            intersect.append((max(segmant[0],selfinterval[0]),min(segmant[1],selfinterval[1])))
        return intersect

    def DiffIntersection(self,intersectlines):
        diff=[]
        selfinterval=self.interval()
        if len(intersectlines)==0: 
            diff.append(selfinterval)
            return diff 
        if (intersectlines[0][0]>selfinterval[0]):
            diff.append((selfinterval[0],intersectlines[0][0])) 
        for i in range(len(intersectlines)-1): 
            if intersectlines[i][1]<intersectlines[i+1][0]:
                diff.append((intersectlines[i][1],intersectlines[i+1][0]))
        if intersectlines[-1][1]<selfinterval[1]:
            diff.append((intersectlines[-1][1],selfinterval[1]))
        return diff


#------print methods ------------

    def show(self):
        self.p1.show()
        self.p2.show()

    def draw(self,color="#000",numerate=False,ShowData=False,font="Times 8 bold" ):
        # if (color==None):
        #    color= "#%03x" % random.randint(0, 0xFFF)
        canvas.create_line(self.p1.X(), self.p1.Y(), self.p2.X(), self.p2.Y(), width=1, fill=color)
        if numerate:
          middle=self.middle()
          if(self.type=="0start"):
            if(self.direction=="vertical"):
                canvas.create_text(middle.X()+10,middle.Y(),fill=f"{color}",font=font,text=f"{self.TileId}")
            else: 
                canvas.create_text(middle.X(),middle.Y()+10,fill=f"{color}",font=font,text=f"{self.TileId}")           
          else:
                if(self.direction=="vertical"):
                   canvas.create_text(middle.X()-10,middle.Y(),fill=f"{color}",font=font,text=f"{self.TileId}")
                else: 
                   canvas.create_text(middle.X(),middle.Y()-10,fill=f"{color}",font=font,text=f"{self.TileId}")      
        if ShowData:
          middle=self.middle()  
          canvas.create_text(middle.X()+10,middle.Y(),fill=f"{color}",font=font,text=f"x({int(self.p1.X())}),t({self.type})")
    # this is how a Line object will be printed with the Python print statement:

    def __str__(self):
        return "Line(%s,%s)"  %  (str(self.p1) , str(self.p2))
    def __repr__(self):
        return "Line(%s,%s)"  %  (str(self.p1) , str(self.p2))
#-------------------------------------------------



def test3():
    p1 =point.Point(0,50)
    p2 =point.Point(10,50)
    l = Line(p1,p2)
    l.draw()

   # p2.rotate90(200,200)
   # l.draw()
if __name__ == "__main__":
    test3()






    # def __lt__(self,other):## inresiction is zero  line is "lower " than other line 
    #     assert isinstance(other,self),"Other is NOT A Line!"
    #     if self.p1.X()==self.p2.X():
    #         YmaxSelf=max( self.p1.Y(),self.p2.Y())
    #         YminOther=min(other.p1.Y(),other.p2.Y())
    #         return True if YmaxSelf<YminOther else False 
    #     elif self.p1.Y()==self.p2.Y():
    #         XmaxSelf=max( self.p1.X(),self.p2.X())
    #         XminOther=min(other.p1.X(),other.p2.X())
    #         return True if XmaxSelf<XminOther else False 
    #     raise Exception('Not horintal or vertical line!')

    # def __gt__(self,other):## inresiction is zero  line is "greater " than other line 
    #     assert isinstance(other,self),"Other is NOT A Line!"
    #     if self.p1.X()==self.p2.X():
    #         assert other.p1.X()== other.p2.X(),"second line not horizontal!"
    #         YminSelf=min( self.p1.Y(),self.p2.Y())
    #         YmaxOther=max(other.p1.Y(),other.p2.Y())
    #         return True if  YmaxOther<YminSelf else False 
    #     elif self.p1.Y()==self.p2.Y():
    #         assert other.p1.Y()== other.p2.Y(),"second line not vertical!"
    #         XminSelf=min( self.p1.X(),self.p2.X())
    #         XmaxOther=max(other.p1.X(),other.p2.X())
    #         return True if XmaxOther<XminSelf else False 
    #     raise Exception('Not horizontal or vertical line!')
#--------------------------------------------------