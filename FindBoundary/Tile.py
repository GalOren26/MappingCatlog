from line import Line 
from point import Point 
import tkinter as Tkinter
import random


class Tile(): 
     def __init__(self,Topleft,BottomRight,TileId=None):#Going to sweep from left to right and from top to bottom.
         # we do sweep from left to right and from top to bottom,there for we first counter left then right for x sweep
         #  and first top then bottom for y sweep
         self.Top=Line(Topleft  ,Point(BottomRight.X(),Topleft.Y()),TileId=TileId,type="1end",)#0 and 1 for sorting later 
         self.Bottom=Line(Point(Topleft.X(),BottomRight.Y()),  BottomRight,TileId=TileId, type="0start")
         self.Right=Line(Point(BottomRight.X(),Topleft.Y()),  BottomRight,TileId=TileId, type="1end")
         self.left=Line(Topleft  ,Point(Topleft.X(),BottomRight.Y()),TileId=TileId,type="0start")
     def draw(self,color=None,numerate=False):
         if (color==None):
             color= "#%03x" % random.randint(0, 0xFFF)
         self.Top.draw(color,numerate=numerate)
         self.Bottom.draw(color,numerate=numerate)
         self.Right.draw(color,numerate=numerate)
         self.left.draw(color,numerate=numerate)