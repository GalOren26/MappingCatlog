import  line as Line
from point import Point 
from Tile import Tile 
from graphics import canvas
import tkinter as Tkinter
import random
from pyproj import Proj, transform,itransform, Transformer
class Outline():
    def __init__(self,fillename="list",origin=None):
        # data structures
        if(origin is not None):
            self.origin=origin
        self.tiles = []
        self.XSortedLines = []
        self.YSortedLines = []
        self.right={}
        self.left={}
        self.up={}
        self.down={}
        self.BoundaryPoints=[]
        self.FileName=fillename
    def FindOutline(self):
        self.ExtractTilesfromCSV()
        self.XSortedLines = self.SortLines("X")
        self.YSortedLines = self.SortLines("Y")
        SweepX=self.SweepLine("X",self.XSortedLines)
        SweepX.Sweep()
        SweepY=self.SweepLine("Y",self.YSortedLines)
        SweepY.Sweep()
        ##-----fill dictionary in order to traverse over the boundary 
        self.FillDirectionDict(SweepY.OutlineLines,self.right,self.left)
        self.FillDirectionDict(SweepX.OutlineLines,self.up,self.down)    
        self.FindOrderedPointsBoundary(SweepY)
        self.WriteToCSV()
        # ------- debug----------- 
        for tile in  self.tiles:
            tile.draw(color="black",numerate=True)
        for idx in range(len(self.BoundaryPoints)-1): 
             canvas.create_line(self.BoundaryPoints[idx].X(), self.BoundaryPoints[idx].Y(), self.BoundaryPoints[idx+1].X(), self.BoundaryPoints[idx+1].Y(), width=2, fill="blue")
      
        # for line in SweepX.OutlineLines:
        #     line.draw(font="Times 50 bold",color="red")
        # for line in SweepY.OutlineLines:
        #     line.draw(font="Times 50 bold",color="red")
        boundary=[]
        boundary.extend(canvas.bbox('all'))
        boundary[0]-=100
        boundary[1]-=100
        boundary[2]+=100
        boundary[3]+=100
        canvas.configure(scrollregion=boundary)
        canvas.mainloop()
        # canvas.configure(scrollregion=canvas.bbox('all'))
        # canvas.configure(scrollregion=canvas.bbox('all'))
      
        # ------- debug-----------
    def ExtractTilesfromCSV(self):
        try:
            with open(self.FileName, 'r') as file:

                for idx,line in enumerate(file):    
                    x1, y1, x2, y2 = [float(val) for val in line.strip().split(",")[1:]]
                    # --get all the Tiles
                    maxX=max( x1,x2)
                    minX=min( x1,x2)
                    maxY=max( y1,y2)
                    minY=min( y1,y2)
                    self.tiles.append(Tile(Point(minX,maxY), Point(maxX, minY),TileId=idx))  # cheak the multiply of x and y!!!!
                  #  self.tiles[-1].draw()
        except Exception as myerror:
            print("\n"+str(myerror))
            pass
    def WriteToCSV(self):
        namefile=self.FileName[self.FileName.rfind("/")+1:-4]
        with open(namefile+'_BoundaryPoints.csv', 'w') as out_file:
            out_file.write("X,Y,Long,Lat" + "\n")
            UTMpoints=[[point.X()+ self.origin.X(),point.Y()+ self.origin.Y()] for point in self.BoundaryPoints]
            transformer = Transformer.from_crs("epsg:32636", "epsg:4326")
            DD=[transformer.transform(pt[0],pt[1]) for pt in UTMpoints]
            for idx,point in enumerate(self.BoundaryPoints):
                # out_file.write(",".join([str(point.X()) ,str(point.Y()),[str(DD[idx][0] ),str( DD[idx][1])]])+ "\n")
                 out_file.write(",".join( [ "["+str(DD[idx][0]),str( DD[idx][1])+"]"])+ "\n")
    def SortLines(self, axis="Y"):
        if(axis == "X"):
            XLines = []
            for tile in self.tiles:
                XLines.extend([tile.Right, tile.left])
            return sorted(XLines, key=lambda XLine: (XLine.p1.X(), XLine.type))
        if(axis == "Y"):
            YLines = []
            for tile in self.tiles:
                YLines.extend([tile.Top, tile.Bottom])
            return sorted(YLines, key=lambda YLine: (YLine.p1.Y(), YLine.type))

    def DrawByClick(self, source):
        # its generator for draw line in form like list comprehension.
        self.DrawGen = (shape.draw(ShowData=True) for shape in source)
        canvas.bind('<Button-1>', self.drawcallback)

    def drawcallback(self, event):
        next(self.DrawGen)
        canvas.configure(scrollregion=canvas.bbox('all'))
    def FillDirectionDict(self,OutlineLines,direction,OppDirection):
        '''fill the dictionary of direction and oppsite direction in ordere to traverse on the boundary'''
        for line in OutlineLines:
                linepoints=line.orderPoints()
                direction[linepoints[0]]=linepoints[1]
                OppDirection[linepoints[1]]=linepoints[0]   
    def FindOrderedPointsBoundary(self,SweepY):
        Maxhorizontal=max(SweepY.OutlineLines,key=lambda line : line.p1.Y()).orderPoints()
        self.BoundaryPoints.extend(Maxhorizontal)
        point=Maxhorizontal[1]
        notcheck=False
        while(point!=Maxhorizontal[0]): 
            if (point in self.right):
                if(self.left[self.right[point]].WasHere==False or notcheck):
                      notcheck=False
                      self.right[point].WasHere=True
                      self.BoundaryPoints.append(self.right[point]) 
                      point=self.right[point]
                      continue
            if (point in self.down):
                if(self.up[self.down[point]].WasHere==False or notcheck ):
                    notcheck=False
                    self.down[point].WasHere=True
                    self.BoundaryPoints.append(self.down[point]) 
                    point=self.down[point]
                    continue
            if (point in self.left):
                  if(self.right[self.left[point]].WasHere==False or notcheck):
                    notcheck=False
                    self.left[point].WasHere=True
                    self.BoundaryPoints.append(self.left[point]) 
                    point=self.left[point]
                    continue
            if (point in self.up):
                   if(self.down[self.up[point]].WasHere==False or notcheck):
                        notcheck=False
                        self.up[point].WasHere=True
                        self.BoundaryPoints.append(self.up[point]) 
                        point=self.up[point]
            else: #case incontinueity     
                def distance(p1, p2):
                        return ( (  (p1.X() - p2.X()) ** 2 + (p1.Y() - p2.Y()) ** 2 ) )** (1 / 2) 
                searchlist=[self.up.keys(),self.up.values(),self.left.keys(),self.left.values()]   
                searchlist2=[]  
                ## bug fix- distance was serached amonng all the points of boundry include those we already been,so fix was to exclude them. 
                for direction in searchlist:
                    for el in direction:
                        if el not in self.BoundaryPoints:
                           searchlist2.append(el)
                dists=[distance(point,BoundaryPoint) for BoundaryPoint in  searchlist2]
                dists_new=[dist for dist in enumerate(dists)]#attach indexe s to list 
                closest2=sorted(dists_new, key=lambda dist: dist[1])[0][0]#not take himself the nearst neighbor to him
                searchlist2[closest2].WasHere=True
                point= searchlist2[closest2]
                notcheck=True 

    class SweepLine():
        '''Run on each axis with sweep line and add parts to boundary.

           x axis example-> run with sweep over x axis if meet"start line"(left side of  rectangle) check if its y-interval (ytop-ybootom)
           is continuously contained in the y-intervals of active lines if not add the missing part to border,
           either yes or no add the line to active list.
           if meet "finish line" remove it from active list then check if its y-interval continuously contained in active list
           if not add the missing part ''' 
        def __init__(self,axis,SortedLines):
            self.active = []
            self.OutlineLines=[]
            self.SortedLines=SortedLines
            assert axis=='y' or axis=='Y' or axis=='x' or axis=='X' ,'axis must be one of X x Y y'
            self.axis=axis
            if self.axis== 'x' or self.axis=='X':
                    self.XorY=Point.Xcord
                    self.oppXorY=Point.Ycord
            else:
                    self.XorY=Point.Ycord
                    self.oppXorY=Point.Xcord
        def Sweep(self):
                for line in self.SortedLines:
                    if line.type == "0start":
                        lineSegment=self.FindBoundaryPart(line) 
                        if lineSegment is not None :
                            self.OutlineLines.extend(lineSegment)
                        self.active.append(line)
                        self.active.sort(key=lambda line:(line.interval()[0],line.interval()[1]))
                    elif line.type == "1end":
                        #delete the start line from active list, #TO-DO find efficeant wat rather then run on all active list 
                        for idx in range(len(self.active)):
                            if line.TileId==self.active[idx].TileId:
                                self.active=  self.active[:idx]+  self.active[idx+1:]
                                break
                        lineSegment=self.FindBoundaryPart(line)
                        if lineSegment is not None :
                            self.OutlineLines.extend(lineSegment)                
                    else:
                        raise Exception('illegal Type of line')
        def FindBoundaryPart(self,line):#need to return the segment line or none
                Lineinterval=line.interval()
                if (len(self.active))==0:
                    boundarylines=[Lineinterval]
                else:
                    maxpoint= line.p1 if self.oppXorY(line.p1)>self.oppXorY(line.p2) else line.p2
                    minpoint= line.p2 if maxpoint==line.p1 else line.p1 
                    idx1 =self.BinarySearchPointInLine(minpoint,edge="min")
                    idx2 =self.BinarySearchPointInLine(maxpoint,edge="max")
                    ActiveSegments=[ self.active[idx].interval() for idx in range(idx1,idx2+1)]
                    ActiveUnion=Line.Line.UnionLines(ActiveSegments)
                    Activeintersction=line.intersection(ActiveUnion)
                    boundarylines=line.DiffIntersection(Activeintersction)
                 #   print(f"Current Line:\n{Lineinterval}\n Allactive:\n{self.active}\n RealventActive:\n{ ActiveSegments }\n  idx1:{idx1},idx2:{idx2}\n  boundarylines:\n {boundarylines} ")
                if len(boundarylines)==0:
                    return None 
                elif self.axis== 'x' or self.axis=='X':
                    return [Line.Line( Point(line.p1.X(),boundaryline[0],),Point(line.p1.X(),boundaryline[1])) for  boundaryline in boundarylines]
                else: 
                    return [Line.Line(Point(boundaryline[0],line.p1.Y()),Point(boundaryline[1],line.p1.Y())) for  boundaryline in boundarylines]

        def BinarySearchPointInLine(self,Point,low=0, high=None,edge=None ): 
            '''return touple (indexOfLine,Find(True/False)) the operation are overload'''
            if(high==None):
                high=len(self.active)-1
            if(Point < self.active[low]):
                return low
            if(Point > self.active[high]):
                return  high   
            while (low <= high):
                mid = (high + low) // 2
                if (Point < self.active[mid]): 
                    high = mid - 1
                elif (Point > self.active[mid]): 
                    low = mid + 1
                else:
                    if (edge==None):## we get to the end 
                          return mid
                    #to take the most left or most right 
                    elif(edge=="max"):
                        if(high-low<=1):
                            return  high if not Point < self.active[high] else  low 
                        low=mid
                    elif(edge=="min"):
                        if(high==low):
                              return low  
                        high=mid
            ## low == high + 1
            return low


Outline=Outline("list.csv",Point(694800,3486100))
Outline.FindOutline()




# ------------------ debug--------------------------------------------
#     self.drawbyclick(self.XLines)
#  for idx in range(len(self.XLines)-1):
#     if self.XLines[idx].p1.x==self.XLines[idx+1].p1.x and self.XLines[idx].type!=self.XLines[idx+1].type:
#       print("x:({}),type({}".format(self.XLines[idx].p1.x,self.XLines[idx].type))
