# -*- coding:cp936 -*-

"""
Purpose:本程序用于创建、查看、删除图纸上的批注
Author:IAN
Contact:knottech@163.com
"""

import kcs_ui
import kcs_util
import kcs_draft

from iknot.core import ktDraft
from KcsPoint2D import Point2D
from KcsRline2D import Rline2D
from KcsCircle2D import Circle2D
from KcsColour import Colour
from KcsRectangle2D import Rectangle2D
from KcsStringlist import Stringlist
from KcsText import Text

SUB_VIEW_NAME="KNOT_NOTE"

def AddNote():
    res=kcs_ui.string_req("请输入标注内容")
    if res[0]==kcs_util.ok():
        content=res[1]
        cor1=Point2D()
        cor2=Point2D()
        res=kcs_ui.point2D_req("请选择标注点",cor1)
        if res[0]==kcs_util.ok():
            res=kcs_ui.point2D_req("请选择标注文字位置",cor2)
            if res[0]==kcs_util.ok(): #开始标注
                #记录原来状态
                old=kcs_draft.subpicture_current_get()
                
                #创建component
                subView=ktDraft.GetKtSubView(SUB_VIEW_NAME)
                #检查是否在KNOT_VIEW下
                parent=kcs_draft.element_parent_get(subView)
                parentName=kcs_draft.subpicture_name_get(parent)
                if parentName!="KNOT_VIEW":
                    return
                kcs_draft.subpicture_current_set(subView)
                compName="NOTE_"+str(GetID(subView))
                comp=kcs_draft.component_new(compName)
                kcs_draft.subpicture_current_set(comp)
                
                #写文字
                txt=Text(content)
                txt.SetPosition(cor2)
                txt.SetColour(Colour("Red"))
                txt.SetFont("黑体")
                txt.SetHeight(5)
                hTxt=kcs_draft.text_new(txt)
                
                #画边框
                rect=Rectangle2D()
                rect=kcs_draft.element_extent_get(hTxt)
                offset=1
                rect.SetCorner1(Point2D(rect.Corner1.X-offset,rect.Corner1.Y-offset))
                rect.SetCorner2(Point2D(rect.Corner2.X+offset,rect.Corner2.Y+offset))
                hd=kcs_draft.rectangle_new(rect)
                kcs_draft.element_colour_set(hd,Colour("Red"))
                
                #画引线
                sta=cor1
                end=rect.GetCorner1()
                if end.X<sta.X:
                    end.SetX(end.X+rect.Corner2.X-rect.Corner1.X)
                if end.Y<sta.Y:
                    end.SetY(end.Y+rect.Corner2.Y-rect.Corner1.Y)
                line=Rline2D(sta,end)
                hd=kcs_draft.line_new(line)
                kcs_draft.element_colour_set(hd,Colour("Red"))
                
                #画圆圈
                circle=Circle2D(sta,2)
                hd=kcs_draft.circle_new(circle)
                kcs_draft.element_colour_set(hd,Colour("Red"))
                
                #恢复原来状态
                if len(old)==3:
                    kcs_draft.subpicture_current_set(old[2])
                else:
                    kcs_draft.subpicture_current_set()
        
def DeleteNote():
    pt=Point2D()
    res=kcs_ui.point2D_req("请选择要删除的批注",pt)
    if res[0]==kcs_util.ok():
        try:
            hText=kcs_draft.text_identify(pt)
            comp=kcs_draft.element_parent_get(hText)
            compName=kcs_draft.subpicture_name_get(comp)
            if compName.startswith("NOTE_"):
                kcs_draft.element_delete(comp)
        except Exception,e:
            kcs_ui.message_noconfirm(e.message)
            
def ShowNote():
    hNoteList=[] #获得note列表
    try:
        subView=ktDraft.GetKtSubView(SUB_VIEW_NAME)
        comp=kcs_draft.element_child_first_get(subView)
        compName=kcs_draft.subpicture_name_get(comp)
        if compName.startswith("NOTE_"):
            hNoteList.append(comp)
        while True:
            try:
                comp=kcs_draft.element_sibling_next_get(comp)
                compName=kcs_draft.subpicture_name_get(comp)
                if compName.startswith("NOTE_"):
                    hNoteList.append(comp)
            except:
                break
    except Exception,e:
        kcs_ui.message_noconfirm(e.message)
        return
    sList=Stringlist("ok") #获得批注内容列表
    for hNote in hNoteList: 
        noteName=kcs_draft.subpicture_name_get(hNote)
        #找到文字
        try:
            ee=kcs_draft.element_child_first_get(hNote)
            txt=Text()
            if kcs_draft.element_is_text(ee):
                txt=kcs_draft.text_properties_get(ee,txt)
                sList.AddString(noteName+" : "+txt.GetString())
                continue
            while True:
                ee=kcs_draft.element_sibling_next_get(ee)
                if kcs_draft.element_is_text(ee):
                    txt=kcs_draft.text_properties_get(ee.txt)
                    sList.AddString(noteName+" : "+txt.GetString())
                    break
        except Exception,e:
            kcs_ui.message_noconfirm(e.message)
    sList.StrList=sList.StrList[1:]
    res=kcs_ui.string_select("批注","批注列表","请选择批注",sList) #显示批注列表
    if res[0]==kcs_util.ok():
        index=res[1]
        hNote=hNoteList[index-1]
        rect=kcs_draft.element_extent_get(hNote) #缩放
        factor=50
        rect.SetCorner1(Point2D(rect.Corner1.X-factor,rect.Corner1.Y-factor))
        rect.SetCorner2(Point2D(rect.Corner2.X+factor,rect.Corner2.Y+factor))
        kcs_draft.dwg_zoom(rect)
                    
    
def GetID(hSubView):
    """获得批注编号"""
    index=1
    try:
        comp=kcs_draft.element_child_first_get(hSubView)
        name=kcs_draft.subpicture_name_get(comp)
        if name.startswith("NOTE_"):
            n=int(name[5:])
            index=max(index,n)
        while True:
            try:
                comp=kcs_draft.element_sibling_next_get(comp)
                name=kcs_draft.subpicture_name_get(comp)
                if name.startswith("NOTE_"):
                    n=int(name[5:])
                    index=max(index,n)
            except:
                break
    except:
        return index
    return index+1
            
def HideAll():
    try:
        subView=ktDraft.GetKtSubView(SUB_VIEW_NAME)
        kcs_draft.element_visibility_set(subView,0)
    except Exception,e:
        kcs_ui.message_noconfirm(e.message)

def DisplayAll():
    try:
        subView=ktDraft.GetKtSubView(SUB_VIEW_NAME)
        kcs_draft.element_visibility_set(subView,1)
    except Exception,e:
        kcs_ui.message_noconfirm(e.message)

if __name__=="__main__":
    AddNote()