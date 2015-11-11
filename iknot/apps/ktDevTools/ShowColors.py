# -*- coding:cp936 -*-

"""
Purpose:To display all the possible colors on current drawing.
Author:IAN
http://www.iknot.org
"""

import kcs_draft
import KcsColour
from KcsPoint2D import Point2D
from KcsRline2D import Rline2D

def PrintColors():
    colors=KcsColour.ColourStrings
    pos=0
    for i in range(len(colors)):
        col=KcsColour.Colour(colors[i])
        kcs_draft.colour_set(col)
        
        p1=Point2D(0,pos)
        p2=Point2D(100,pos)
        ln=Rline2D(p1,p2)
        kcs_draft.line_new(ln)
        kcs_draft.text_new(colors[i],Point2D(p2.X+20,p2.Y))
        
        pos+=20
        
def run():
    PrintColors()

if __name__=="__main__":
    run()