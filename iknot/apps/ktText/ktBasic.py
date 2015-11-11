# -*- coding:cp936 -*-

"""
Author:IAN
www.iknot.org
Contact:knottech@163.com
"""

import kcs_ui
import kcs_util
import kcs_draft
from KcsPoint2D import Point2D
from KcsPolygon2D import Polygon2D
from KcsCaptureRegion2D import CaptureRegion2D
from KcsRectangle2D import Rectangle2D
from KcsText import Text
from KcsRline2D import Rline2D
from iknot.core import ktDraft

def GetRegion():  # ��õ�ǰͼֽ���Χ
    # �������View
    viewList = []
    try:
        view = kcs_draft.element_child_first_get()
        viewList.append(view)
        while True:
            try:
                view = kcs_draft.element_sibling_next_get(view)
                viewList.append(view)
            except:
                break
    except:  # û���ҵ��κ���ͼ
        return None
    rect = kcs_draft.element_extent_get(viewList[0])
    for view in viewList[1:]:
        rect2 = kcs_draft.element_extent_get(view)
        rect.SetCorner1(Point2D(min(rect.Corner1.X, rect2.Corner1.X), min(rect.Corner1.Y, rect2.Corner1.Y)))
        rect.SetCorner2(Point2D(max(rect.Corner2.X, rect2.Corner2.X), max(rect.Corner2.Y, rect2.Corner2.Y)))
    
    region = CaptureRegion2D()
    region.SetRectangle(rect)
    region.Inside = 1
    region.Cut = 0
    return region
   

def FindString(content):
    """��������ƥ���Text handle"""
    region = GetRegion()
    hds = []
    try:
        hds = kcs_draft.text_capture(region)
    except:
        kcs_ui.message_noconfirm("û���ҵ�����")
        return []
    txtList = []
    for hd in hds[1:]:
        txt = Text()
        kcs_draft.text_properties_get(hd, txt)
        if txt.GetString().upper() == content.upper():
            txtList.append(hd)
    return txtList
      
def ZoomElement(element):
    try:
        rect = kcs_draft.element_extent_get(element)
        rect.SetCorner1(Point2D(rect.Corner1.X - 100, rect.Corner1.Y - 100))
        rect.SetCorner2(Point2D(rect.Corner2.X + 100, rect.Corner2.Y + 100))
        kcs_draft.dwg_zoom(rect)
    except:
        kcs_ui.message_noconfirm('Failed to zoom text')
      
def Replace(hdList):
    res = kcs_ui.answer_req("�����滻", "�Ƿ�Ҫ�滻���֣�")
    if res == kcs_util.yes():
        txt = Text()
        kcs_draft.text_properties_get(hdList[0], txt)
        res = kcs_ui.string_req("������Ҫ�滻������", txt.GetString())
        if res[0] == kcs_util.ok():
            content = res[1]
            old = kcs_draft.subpicture_current_get()
            for hd in hdList:
                father = kcs_draft.element_parent_get(hd)  # ��������ͼ��
                kcs_draft.text_properties_get(hd, txt)
                txt.SetString(content)
                kcs_draft.element_delete(hd)  # ɾ��ԭ����
                kcs_draft.subpicture_current_set(father)  # ����ͼ��
                kcs_draft.text_new(txt)  # д����
            if len(old) == 3:
                kcs_draft.subpicture_current_set(old[2])
            else:
                kcs_draft.subpicture_current_set()
def ReplaceOne(hdText):
    "replace one text"
    txt=Text()
    kcs_draft.text_properties_get(hdText,txt)
    res=kcs_ui.string_req('������Ҫ�滻���ı�',txt.String)
    if res[0]==kcs_util.ok():
        old = kcs_draft.subpicture_current_get() #make the old subpicture
        father = kcs_draft.element_parent_get(hdText)  # ��������ͼ��
        txt.SetString(res[1])
        kcs_draft.element_delete(hdText)  # ɾ��ԭ����
        kcs_draft.subpicture_current_set(father)  # ����ͼ��
        kcs_draft.text_new(txt)  # д����
        if len(old) == 3:
            kcs_draft.subpicture_current_set(old[2])
        else:
            kcs_draft.subpicture_current_set()
def FindText():
    res=kcs_ui.string_req('��������Ҫ���ҵ�����','')
    if res[0]==kcs_util.ok():
        hdList=FindString(res[1])
        if len(hdList) == 1:
            ZoomElement(hdList[0])
            res=kcs_ui.answer_req('Find','�Ƿ�Ҫ�滻�ı���')
            if res[0]==kcs_util.yes():
                ReplaceOne(hdList[0])
        elif len(hdList) > 1:
            ZoomElement(hdList[0])
            index=1
            while True:
                if index>len(hdList):
                    kcs_ui.message_noconfirm("�Ѿ������һ��")
                    return
                res=kcs_ui.answer_req(r'���ҵ�%s������ǰ��%s��'%(len(hdList),index),'�Ƿ�Ҫ�滻�ı���')
                if res==kcs_util.yes():
                    ReplaceOne(hdList[index-1])
                    index+=1
                    continue
                elif res==kcs_util.no():
                    ZoomElement(hdList[index])
                    index+=1
                    continue
                else:
                    return
        elif len(hdList) == 0:
            kcs_ui.message_confirm("û���ҵ��κ�ƥ�������")
def FindAndReplace():
    res, txt = kcs_ui.string_req("��������Ҫ���ҵ�����", "")
    if res == kcs_util.ok():
        hdList = FindString(txt)
        if len(hdList) == 1:
            ZoomElement(hdList[0])
            Replace(hdList)
        elif len(hdList) > 1:
            kcs_ui.message_noconfirm("�ҵ�" + str(len(hdList)) + "��ƥ������֣�����ʾ��һ��")
            ZoomElement(hdList[0])
            Replace(hdList)
        elif len(hdList) == 0:
            kcs_ui.message_confirm("û���ҵ��κ�ƥ�������")
def SelectTexts():
    cor1 = Point2D()
    cor2 = Point2D()
    res = kcs_ui.point2D_req("��ѡ���������Ͻ�", cor1)
    if res[0] == kcs_util.ok():
        res = kcs_ui.point2D_req("��ѡ���������½�", cor2)
        if res[0] == kcs_util.ok():
            rect = Rectangle2D(cor1, cor2)
            region = CaptureRegion2D()
            region.SetRectangle(rect)
            region.Inside = 1
            region.Cut = 1
            hds = kcs_draft.text_capture(region)
            return hds
    return
def SelectText():
    "select a text from drawing"
    pt=Point2D()
    res=kcs_ui.point2D_req('��ѡ������',pt)
    if res[0]==kcs_util.ok():
        try:
            hdText=kcs_draft.text_identify(res[1])
            return hdText
        except:
            return None
def SetUnderline():
    "add underline for text"
    hdText=SelectText()
    if hdText!=None:
        csm=ktDraft.CurrentSubpictureManager()
        rect=kcs_draft.element_extent_get(hdText)
        #begin to draw underline
        x1=min(rect.Corner1.X,rect.Corner2.X)
        x2=max(rect.Corner1.X,rect.Corner2.X)
        y=min(rect.Corner1.Y,rect.Corner2.Y)-1
        csm.Set(hdText)
        line=Rline2D(Point2D(x1,y),Point2D(x2,y))
        kcs_draft.line_new(line)
        csm.Back()
def SetUndeeline():
    "add undee(wave) line for text"
    hdText=SelectText()
    if hdText!=None:
        csm=ktDraft.CurrentSubpictureManager()
        rect=kcs_draft.element_extent_get(hdText)
        #begin to draw underline
        x1=min(rect.Corner1.X,rect.Corner2.X)
        x2=max(rect.Corner1.X,rect.Corner2.X)
        y=min(rect.Corner1.Y,rect.Corner2.Y)-1
        pt=Point2D(x1,y)
        poly=Polygon2D(pt)
        dy=0.55
        while pt.X<x2:
            pt.X+=1
            pt.Y+=dy
            dy=-dy
            poly.AddPoint(pt)
        csm.Set(hdText)
        kcs_draft.spline_new(poly)
        csm.Back()
def Amplifier(step):
    "set the text bigger or smaller by given step"
    while True:
        hdText=SelectText()
        if hdText!=None:
            csm=ktDraft.CurrentSubpictureManager()
            t = Text()
            kcs_draft.text_properties_get(hdText, t)
            if t.GetHeight()<2:
                print 'can not be smaller'
                return
            else:
                csm.Set(hdText)
                kcs_draft.element_delete(hdText)
                t.SetHeight(t.GetHeight()+step)
                kcs_draft.text_new(t)
            csm.Back()
        else:
            break
def SetRectangle():
    "Add a rectangle around text"
    hdText=SelectText()
    if hdText!=None:
        csm=ktDraft.CurrentSubpictureManager()
        csm.Set(hdText)
        rect=kcs_draft.element_extent_get(hdText)
        rect.Corner1.X-=1
        rect.Corner1.Y-=1
        rect.Corner2.X+=1
        rect.Corner2.Y+=1
        kcs_draft.rectangle_new(rect)
        csm.Back()
def AlignLeft():
    "Align texts to the left."
    hds=SelectTexts()
    tList=[]
    for hd in hds[1:]:
        t=Text()
        kcs_draft.text_properties_get(hd,t)
        tList.append((hd,t))
    x=min([t[1].GetPosition().X for t in tList])
    csm=ktDraft.CurrentSubpictureManager()
    for hd,t in tList:
        csm.Set(hd)
        kcs_draft.element_delete(hd)
        t.Position.X=x
        kcs_draft.text_new(t)
    csm.Back()
def AlignRight():
    "Align texts to the left."
    hds=SelectTexts()
    tList=[]
    for hd in hds[1:]:
        t=Text()
        kcs_draft.text_properties_get(hd,t)
        tList.append((hd,t))
    x=max([t[1].GetPosition().X for t in tList])
    csm=ktDraft.CurrentSubpictureManager()
    for hd,t in tList:
        csm.Set(hd)
        rect=kcs_draft.element_extent_get(hd)
        width=abs(rect.Corner1.X-rect.Corner2.X)
        kcs_draft.element_delete(hd)
        t.Position.X=x-width
        kcs_draft.text_new(t)
    csm.Back()
def AlignTop():
    "Align texts to the left."
    hds=SelectTexts()
    tList=[]
    for hd in hds[1:]:
        t=Text()
        kcs_draft.text_properties_get(hd,t)
        tList.append((hd,t))
    y=max([t[1].GetPosition().Y for t in tList])
    csm=ktDraft.CurrentSubpictureManager()
    for hd,t in tList:
        csm.Set(hd)
        kcs_draft.element_delete(hd)
        t.Position.Y=y
        kcs_draft.text_new(t)
    csm.Back()
def AlignBottom():
    "Align texts to the left."
    hds=SelectTexts()
    tList=[]
    for hd in hds[1:]:
        t=Text()
        kcs_draft.text_properties_get(hd,t)
        tList.append((hd,t))
    y=min([t[1].GetPosition().Y for t in tList])
    csm=ktDraft.CurrentSubpictureManager()
    for hd,t in tList:
        csm.Set(hd)
        kcs_draft.element_delete(hd)
        t.Position.Y=y
        kcs_draft.text_new(t)
    csm.Back()
def FormatRegion():
    pt = Point2D()
    res = kcs_ui.point2D_req("��ѡ�����ֻ�ȡ��������", pt)
    if res[0] == kcs_util.ok():
        hd = kcs_draft.text_identify(pt)
        ori = Text()
        kcs_draft.text_properties_get(hd, ori)
        objs = SelectTexts()
        old = kcs_draft.subpicture_current_get()  # ��ǰͼ��
        for obj in objs[1:]:  # ��д����
            father = kcs_draft.element_parent_get(obj)  # ��������ͼ��
            t = Text()
            kcs_draft.text_properties_get(obj, t)
            ori.SetString(t.GetString())
            ori.SetPosition(t.GetPosition())
            kcs_draft.element_delete(obj)  # ɾ��ԭ����
            kcs_draft.subpicture_current_set(father)  # ����ͼ��
            kcs_draft.text_new(ori)  # д����
        if len(old) == 3:
            kcs_draft.subpicture_current_set(old[2])
        else:
            kcs_draft.subpicture_current_set()
        # except:
            # kcs_ui.message_noconfirm("Format brush command failed.")
def FormatSingle():
    pt = Point2D()
    res = kcs_ui.point2D_req("��ѡ�����ֻ�ȡ��������", pt)
    if res[0] == kcs_util.ok():
        hd = kcs_draft.text_identify(pt)
        ori = Text()
        kcs_draft.text_properties_get(hd, ori)
#         old = kcs_draft.subpicture_current_get()  # ��ǰͼ��
        while True:
            "select single text"
            pt2=Point2D()
            res = kcs_ui.point2D_req("��ѡ��Ҫ�滻������", pt2)
            if res[0]==kcs_util.ok():
                hdText=kcs_draft.text_identify(pt2)
                father = kcs_draft.element_parent_get(hdText)  # ��������ͼ��
                t = Text()
                kcs_draft.text_properties_get(hdText, t)
                ori.SetString(t.GetString())
                ori.SetPosition(t.GetPosition())
                kcs_draft.element_delete(hdText)  # ɾ��ԭ����
                kcs_draft.subpicture_current_set(father)  # ����ͼ��
                kcs_draft.text_new(ori)  # д����
            else:
                break
if __name__ == '__main__':
    AlignRight()
#     print kcs_draft.elemen    t_is_view(hd)
#     print kcs_draft.element_is_subpicture(hd)
#     print kcs_draft.element_is_subview(hd)
#     print kcs_draft.element_is_component(hd)
