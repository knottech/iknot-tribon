# -*- coding:cp936 -*-

"""
Purpose:To display all the possible line type on current drawing.
Author:IAN
http://www.iknot.org
"""

import kcs_draft
import KcsLinetype
from KcsPoint2D import Point2D
from KcsRline2D import Rline2D
from kcs_ui import message_noconfirm as msg

def PrintLinetypes():
    tps=KcsLinetype.GetLinetypes()
    pos=0
    for i in range(len(tps)):
        msg(i)
        tp=tps.keys()[i]
        name=KcsLinetype.GetSystemName(tp)
        lt=KcsLinetype.Linetype(name)
        kcs_draft.linetype_set(lt)
        
        p1=Point2D(0,pos)
        p2=Point2D(100,pos)
        ln=Rline2D(p1,p2)
        kcs_draft.line_new(ln)
        kcs_draft.text_new(name,Point2D(p2.X+20,p2.Y))
        
        pos+=20
        
def run():
#     kcs_draft.dwg_new()
    PrintLinetypes()

if __name__=="__main__":
    run()