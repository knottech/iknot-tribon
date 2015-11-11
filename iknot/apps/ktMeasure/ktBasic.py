# -*- coding:cp936 -*-

"""
本程序用于查询点坐标信息
Author:IAN
www.iknot.org
Contact:iknot@qq.com
"""

import kcs_ui
import kcs_util
import string
from KcsPoint2D import Point2D
from KcsPoint3D import Point3D
from iknot.core import ktUi

width = 10

def Point3DCoord():
    "show the coordinate of selected point"
    pt = Point2D()
    res = kcs_ui.point2D_req("请选择要查询的点", pt)

    if res[0] == kcs_util.ok():
        res = kcs_util.tra_coord_ship(pt.X, pt.Y, "")
        if res[0] == 0:
            pt3d = Point3D(res[1], res[2], res[3])
            res, fr, fr_offset = kcs_util.coord_to_pos(1, pt3d.X)
            res, lp_y, lp_y_offset = kcs_util.coord_to_pos(2, pt3d.Y)
            res, lp_z, lp_z_offset = kcs_util.coord_to_pos(3, pt3d.Z)
            fr_offset=round(fr_offset,2)
            lp_y_offset=round(lp_y_offset,2)
            lp_z_offset=round(lp_z_offset,2)
            x=round(pt3d.X,2)
            y=round(pt3d.Y,2)
            z=round(pt3d.Z,2)

            Msg("--"*25)
            Msg("二维点：" + str(pt))
            Msg("三维坐标信息：")
            Msg("X: %s,FR%s %s" % (string.ljust(str(x), width), str(fr), _fmt(fr_offset)))
            Msg("Y: %s,LP%s %s" % (string.ljust(str(y), width), str(lp_y), _fmt(lp_y_offset)))
            Msg("Z: %s,LP%s %s" % (string.ljust(str(z), width), str(lp_z), _fmt(lp_z_offset)))
            Msg("--"*25)
def Distance3D():
    "show the distance between selected points"
    sta,end=ktUi.Pick2DPoints(2)
    res1 = kcs_util.tra_coord_ship(sta.X, sta.Y, "")
    res2 = kcs_util.tra_coord_ship(end.X, end.Y, "")
    if res1[0]==0 and res2[0]==0:
        pt1=Point3D(res1[1],res1[2],res1[3])
        pt2=Point3D(res2[1],res2[2],res2[3])
        d=pt1.DistanceToPoint(pt2)
        Msg('--'*25)
        Msg('dx:%s'%(round(pt1.X-pt2.X)))
        Msg('dy:%s'%(round(pt1.Y-pt2.Y)))
        Msg('dz:%s'%(round(pt1.Z-pt2.Z)))
        Msg('distance:%s'%(round(d)))

def _fmt(x):
    if x==0:
        return ''
    elif x>0:
        return '+'+str(x)
    else:
        return str(x)
            
def Msg(message):
    kcs_ui.message_noconfirm(message)
        
if __name__ == "__main__":
    pass
