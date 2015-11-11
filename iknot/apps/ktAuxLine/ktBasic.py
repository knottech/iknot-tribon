# -*- coding:cp936 -*-

"""
Author:IAN
www.iknot.org
Contact:knottech@163.com
"""

import math
from KcsRline2D import Rline2D
import kcs_draft
import kcs_ui
import kcs_util
from KcsPoint2D import Point2D
from KcsCircle2D import Circle2D
from KcsPolygon2D import Polygon2D
from iknot.core.ktDraft import CurrentSubpictureManager
from iknot.core import ktUi

def Arrow(start,end,size=2.5,angle=15):
    #distance can't less than size
    if start.DistanceToPoint(end)<=size:
        raise 'Given points is too close.'
    length=start.DistanceToPoint(end)
    scale=(length-size)/size
    x=(start.X+scale*end.X)/(1+scale)
    y=(start.Y+scale*end.Y)/(1+scale)
    theta=GetAngle(start, end)
    d=size*math.tan(math.radians(angle))
    dx=d*math.sin(theta)
    dy=d*math.cos(theta)
    p3=Point2D(x+dx,y-dy)
    p4=Point2D(x-dx,y+dy)
    
    kcs_draft.line_new(Rline2D(start, end))
    kcs_draft.line_new(Rline2D(p3, end))
    kcs_draft.line_new(Rline2D(p4, end))
    kcs_draft.line_new(Rline2D(p3, p4))
def CircleArrow(start,end,size=1.2):
    """draw a arrow with circle at the end."""
    #distance can't less than size
    if start.DistanceToPoint(end)<=size:
        raise 'Given points is too close.'
    kcs_draft.line_new(Rline2D(start, end))
    c=Circle2D(end,size)
    kcs_draft.circle_new(c)
def Polygon(center,radius,number,angle=0.0):
    """
    center:center point of polygon.
    radius:radius of out circle.
    number:count of sides.
    angle:rotation angle of polygon.
    """
    if number<3:
        raise 'number can not less than 3.'
    pts=[]
    index=0
    alpha=math.pi*2/number
    while index<number:
        beta=alpha*index+math.radians(angle)
        print beta
        dx=radius*math.cos(beta)
        dy=radius*math.sin(beta)
        pts.append(Point2D(center.X+dx,center.Y+dy))
        index+=1
    DrawLines(pts)
def Diamond(center,width,height):
    """
    center:center point.
    width:x direction length
    height:y direction length
    """
    dx=width*1.0/2
    dy=height*1.0/2
    p1=Point2D(center.X+dx,center.Y)
    p2=Point2D(center.X,center.Y-dy)
    p3=Point2D(center.X-dx,center.Y)
    p4=Point2D(center.X,center.Y+dy)
    DrawLines([p1,p2,p3,p4])

def Grid():
    """Create a grid on a new view"""
    res=kcs_ui.string_req('请输入格子的长，宽、列数，行数','30,10,8,5')
    if res[0]==kcs_util.ok():
        w,h,m,n=[float(i) for i in res[1].split(',')]
        pt=Point2D()
        res=kcs_ui.point2D_req('请选择Grid左上角位置,回车设为原点',pt)
        if res[0]==kcs_util.ok():
            csm=CurrentSubpictureManager()
            hd=kcs_draft.view_new('')
            csm.Set(hd)
            for i in range(n+1):    #horizontal line
                p1=Point2D(pt.X,pt.Y-h*i)
                p2=Point2D(pt.X+w*m,pt.Y-h*i)
                kcs_draft.line_new(Rline2D(p1,p2))
            for j in range(m+1):    #vertical line
                p1=Point2D(pt.X+j*w,pt.Y)
                p2=Point2D(pt.X+j*w,pt.Y-h*n)
                kcs_draft.line_new(Rline2D(p1,p2))
            csm.Back()
        elif res[0]==kcs_util.operation_complete():
            pt=Point2D(0,0)
            csm=CurrentSubpictureManager()
            hd=kcs_draft.view_new('')
            csm.Set(hd)
            for i in range(n+1):    #horizontal line
                p1=Point2D(pt.X,pt.Y-h*i)
                p2=Point2D(pt.X+w*m,pt.Y-h*i)
                kcs_draft.line_new(Rline2D(p1,p2))
            for j in range(m+1):    #vertical line
                p1=Point2D(pt.X+j*w,pt.Y)
                p2=Point2D(pt.X+j*w,pt.Y-h*n)
                kcs_draft.line_new(Rline2D(p1,p2))
            csm.Back()

def DrawLines(pts):
    """connect all points"""
    for i in range(len(pts)-1):
        kcs_draft.line_new(Rline2D(pts[i],pts[i+1]))
    kcs_draft.line_new(Rline2D(pts[0],pts[-1]))
def GetAngle(p1,p2):
    """return the angle of vector made up by p1 and p2."""
    if p1.X==p2.X:
        if p1.Y==p2.Y:
            raise 'Given points have same position.'
        if p1.Y<p2.Y:
            return math.pi*0.5
        elif p1.Y>p2.Y:
            return -math.pi*0.5
    else:
        return math.atan2(p2.Y-p1.Y, p2.X-p1.X)
    
if __name__=='__main__':
    Grid()