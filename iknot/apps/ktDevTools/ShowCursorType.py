# -*- coding:cp936 -*-

"""
Purpose:To display all the possible cursor types on current drawing.
Author:IAN
http://www.iknot.org
"""

import kcs_ui
import kcs_util
from kcs_ui import message_noconfirm as msg

from KcsPoint2D import Point2D
import KcsStat_point2D_req
from KcsCursorType import CursorType
from KcsHighlightSet import HighlightSet
from KcsButtonState import ButtonState

def run():
    stat=KcsStat_point2D_req.Stat_point2D_req()
    ct=CursorType()
    
    CursorTypes = {'CrossHair' : 1, 'RubberBand' : 2, 'RubberRectangle' : 3, 'RubberCircle' : 4, 'DragCursor' : 5}
    
    actions=CursorTypes.keys()
    
    bs=ButtonState()
    bs.EnableLock(1)
    bs.SetCheckedLock('V')
    
    pt=Point2D(2,3)
    while True:
        res=kcs_ui.choice_select('title','header',actions)
        if res[0]==kcs_util.ok():
            #msg("%s:%s"%(res[1],CursorTypes.keys()[res[1]-1]))
            if res[1]==1:
                ct.SetCrossHair()
            elif res[1]==2:
                ct.SetRubberBand(pt)
            elif res[1]==3:
                ct.SetRubberRectangle(pt)
            elif res[1]==4:
                ct.SetRubberCircle(pt)
            elif res[1]==5:
                pass
            stat.SetCursorType(ct)
            stat.SetDefMode('ModeMidPoint')
            stat.SetHelpPoint(Point2D(0,0))
            msg(ct)
            res,pt2=kcs_ui.point2D_req('msg',pt,stat,bs)
            msg(pt2)
        else:
            break
    