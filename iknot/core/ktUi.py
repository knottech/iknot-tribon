# -*- coding:cp936 -*-

"""
Author:IAN
Contact:knottech@163.com
"""
from KcsPoint2D import Point2D
import kcs_ui
import kcs_util
from KcsStat_point2D_req import Stat_point2D_req

def Pick2DPoints(number=0,mode="ModeAuto"):
    """
    Pick points until reach the number.
    number=0 means unlimited number.
    """
    pts=[]
    index=0
    action=kcs_util.ok()
    while index<number or number==0:
        pt=Point2D()
        stp=Stat_point2D_req()
        stp.SetDefMode(mode)
        action,pt=kcs_ui.point2D_req('请选择第%s个点'%(index+1),pt,stp)
        if action==kcs_util.ok():
            pts.append(pt)
        elif action==kcs_util.operation_complete() and number==0:
            return pts
        elif action==kcs_util.cancel():
            print 'operation canceled'
            return None
        index+=1
    return pts

if __name__=='__main__':
    pass