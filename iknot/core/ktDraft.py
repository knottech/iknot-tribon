# -*- coding:cp936 -*-

"""
Author:IAN
Contact:knottech@163.com
"""

import kcs_draft
import kcs_ui
import kcs_util
from KcsPoint2D import Point2D
from KcsArc2D import Arc2D
from KcsCircle2D import Circle2D
from KcsVector2D import Vector2D
from KcsRline2D import Rline2D
import math
import re
#----------------------------------------------------------------------
def ViewToRect(viewHandle, rectangle, fixScale=True):
    """将视图缩放到给定矩形内
    Return: scale"""
    viewRec = kcs_draft.element_extent_get(viewHandle)
    scale_x = abs((viewRec.Corner2.X - viewRec.Corner1.X) / (rectangle.Corner2.X - rectangle.Corner1.X))
    scale_y = abs((viewRec.Corner2.Y - viewRec.Corner1.Y) / (rectangle.Corner2.Y - rectangle.Corner1.Y))
    scale = max(scale_x, scale_y)
    if fixScale:  # 修改比例(50,75,100)
        if scale < 50:
            scale = 50.0
        elif scale < 75:
            scale = 75.0
        elif scale < 100:
            scale = 100.0
    kcs_draft.view_scale(viewHandle, 1.0 / scale, viewRec.Corner1)
    
    # 移动到页面中心位置
    viewRec = kcs_draft.element_extent_get(viewHandle)
    viewCenter = Point2D((viewRec.Corner1.X + viewRec.Corner2.X) / 2, (viewRec.Corner1.Y + viewRec.Corner2.Y) / 2)
    recCenter = Point2D((rectangle.Corner1.X + rectangle.Corner2.X) / 2, (rectangle.Corner1.Y + rectangle.Corner2.Y) / 2)
    moveVec = Vector2D(recCenter.X - viewCenter.X, recCenter.Y - viewCenter.Y)
    kcs_draft.view_move(viewHandle, moveVec)
    
    return scale

def NewArrow(start, end, size=2.5, angle=15):
    """画水平箭头"""
    arrowHeight = math.tan(angle * math.pi / 180) * size
    
    line = Rline2D(start, end)
    kcs_draft.line_new(line)
    
    pt = Point2D()
    pt.X = end.X - size
    pt.Y = end.Y + arrowHeight
    line = Rline2D(end, pt)
    kcs_draft.line_new(line)
    
    pt2 = Point2D()
    pt2.X = pt.X
    pt2.Y = pt.Y - 2 * arrowHeight
    line = Rline2D(pt, pt2)
    kcs_draft.line_new(line)
    
    line = Rline2D(pt2, end)
    kcs_draft.line_new(line)
    
def GetKtView(): #obsolete, do not use it.
    """返回KNOT_VIEW handle"""
    try:
        return kcs_draft.view_identify("KNOT_VIEW")
    except:
        return kcs_draft.view_new("KNOT_VIEW")
    
def GetKtSubView(subViewName): #obsolete, do not use it.
    view=GetKtView()
    print view
    """返回指定名称的subview，若没有则新建一个"""
    try:
        subView = kcs_draft.element_child_first_get(view)
        name = kcs_draft.subpicture_name_get(subView)
        if name == subViewName:
            return subView
        while True:
            subView = kcs_draft.element_sibling_next_get(subView)
            name = kcs_draft.subpicture_name_get(subView)
            if name == subViewName:
                return subView
    except:
        csm=CurrentSubpictureManager()
        csm.Set(view)
        subView = kcs_draft.subview_new(subViewName)
        csm.Back()
        return subView
    
def GetKtComponent(compName, subView): #obsolete, do not use it.
    """返回指定名称的component，若没有则新建一个"""
    # subView=GetTitSubView(subViewName)
    name = kcs_draft.subpicture_name_get(subView)
    try:
        comp = kcs_draft.element_child_first_get(subView)
        name = kcs_draft.subpicture_name_get(comp)
        if name == compName:
            return comp
        while True:
            comp = kcs_draft.element_sibling_next_get(comp)
            name = kcs_draft.subpicture_name_get(comp)
            kcs_ui.message_noconfirm(name)
            if name == compName:
                return comp
    except:
        old = kcs_draft.subpicture_current_get()
        kcs_draft.subpicture_current_set(subView)
        comp = kcs_draft.component_new(compName)
        if len(old) == 3:
            kcs_draft.subpicture_current_set(old[2])
        return comp
    
def GetSubElements(superElement):
    """Return handles of all the sub elements satisfy the regular pattern
    """
    ees = []
    try:
        ee = kcs_draft.element_child_first_get(superElement)
        ees.append(ee)
        while True:
            try:
                ee = kcs_draft.element_sibling_next_get(ee)
                ees.append(ee)
            except:
                break
    except:
        return []
    return ees
def GetSubpictures(father=None,pattern='.*'):
    """Return handles and names of all the subpictures satisfy the regular pattern
    subpicture means view,subview or component.
    father: parent handle of subpicture.
    return views if father is None.
    return: [(handle,name),(handle,name)...]
    """
    ees = []
    try:
        if father==None:
            ee = kcs_draft.element_child_first_get()
        else:
            ee = kcs_draft.element_child_first_get(father)
        name=kcs_draft.subpicture_name_get(ee)
        ees.append((ee,name))
        while True:
            try:
                ee = kcs_draft.element_sibling_next_get(ee)
                name=kcs_draft.subpicture_name_get(ee)
                ees.append((ee,name))
            except:
                break
    except:
        return []
    return [ee for ee in ees if re.match(pattern,ee[1])!=None]
def GetViews(pattern='.*'):
    """Return handles of all the views satisfy the regular pattern
     on current drawing.
    """
    return GetSubpictures(None, pattern)
def GetSubviews(viewhandle,pattern='.*'):
    return GetSubpictures(viewhandle, pattern)
def GetComponents(subviewhandle,pattern='.*'):
    return GetSubpictures(subviewhandle, pattern)
def CleanDwg():
    oldSize = kcs_draft.dwg_size_get()  # in Kbyes
    name = kcs_draft.dwg_name_get()
    
    kcs_draft.dwg_pack()
    kcs_draft.dwg_purge()
    kcs_util.clean_workspace()
    
    newSize = kcs_draft.dwg_size_get()
    
    msg = """图纸：%s清理完毕
清理前大小：%s Kbytes
清理后大小：%s Kbytes
""" % (name, oldSize, newSize)
    
    kcs_ui.message_noconfirm(msg)
    
class LineMaker(object):
    """A class to help drawing lines on current drawing."""
    def __init__(self,x=0.0,y=0.0):
        self.Sta=Point2D(x,y)
    def SetPoint(self,pt):
        "set current point by Point2D"
        self.Sta=pt
    def Line(self,dx,dy):
        "create new line by given offset distance."
        x=self.Sta.X+dx
        y=self.Sta.Y+dy
        self.LineTo(x, y)
    def LineX(self,dx):
        "create new horizontal line  by dx"
        self.Line(dx, 0)
    def LineY(self,dy):
        "create new vertical line by dy"
        self.Line(0, dy)
    def LineTo(self,x,y):
        "create new line from current point to given x and y"
        end=Point2D(x,y)
        line=Rline2D(self.Sta,end)
        kcs_draft.line_new(line)
        self.Sta=end
    def Arc(self,dx,dy,dz=1):
        """
        create arc by given offset distance.
        if dz==1:arc will on the right side.
        if dz==-1:arc will on the left side.
        """
        x=self.Sta.X+dx
        y=self.Sta.Y+dy
        self.ArcTo(x, y, dz)
    def ArcTo(self,x,y,dz=1):
        "create arc to given x and y"
        end=Point2D(x,y)
        amp=self.Sta.DistanceToPoint(end)/2
        arc=Arc2D(self.Sta,end,amp*dz)
        kcs_draft.arc_new(arc)
        self.Sta=end
    def Circle(self,r):
        "create a circle at current point."
        c=Circle2D(self.Sta,r)
        kcs_draft.circle_new(c)
    def Move(self,dx,dy):
        "move current point by given offset distance"
        self.Sta=Point2D(self.Sta.X+dx,self.Sta.Y+dy)
    def MoveX(self,dx):
        "move maker on horizontal"
        self.Sta+=dx
    def MoveY(self,dy):
        "move maker on vertical"
        self.Sta.Y+=dy
    def MoveTo(self,x,y):
        "move current point to given x and y. "
        self.Sta=Point2D(x,y)
class CurrentSubpictureManager(object):
    "Manage the current subpicture for user to add something on drawing"
    def __init__(self):
        self.Pre=kcs_draft.subpicture_current_get()
    def Set(self,hd):
        """
        User it before draw operation.
        Or the subpicture of the drawing will be chaos.
        """
        #set current subpicture same as given handle.
        if not kcs_draft.element_is_subpicture(hd):
            father=kcs_draft.element_parent_get(hd)
            kcs_draft.subpicture_current_set(father)
        #only subpicture can be set as current.
        else:
            kcs_draft.subpicture_current_set(hd)
    def Back(self):
        """
        Use it after operation is done.
        Set previous current subpicture before operation.
        if view was set as current,subview and component would be created automatically
        """
        if len(self.Pre)==0:    #Empty: Define as automatic
            kcs_draft.subpicture_current_set()
        else:
            kcs_draft.subpicture_current_set(self.Pre[2])
if __name__ == "__main__":
    print GetViews('KNOT.*')