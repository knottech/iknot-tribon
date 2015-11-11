# -*- coding:cp936 -*-

"""
Author:IAN
www.iknot.org
Contact:knottech@163.com
"""

import kcs_ui
import kcs_util
from KcsPoint2D import Point2D
from iknot.core import ktDraft
from iknot.core.ktDraft import LineMaker
import kcs_draft
import math

class Page(object):
    def __init__(self):
        self.Location=Point2D(0,0)
        self.Width=420
        self.Height=297
        self.PaddingLeft=20
        self.PaddingRight=5
        self.PaddingTop=5
        self.PaddingBottom=5
        self.Index=0

    def Draw(self):
        "draw the drawing form on current drawing"
        #check whether view exist
        hd=kcs_draft.subview_new('KT_FORM%s'%(self.Index))
        kcs_draft.subpicture_current_set(hd)
        hd=kcs_draft.component_new('FORM_CONTOUR')
        kcs_draft.subpicture_current_set(hd)
        
        #drawing form lines
        #outer rectangle
        lm=LineMaker(self.Location.X,self.Location.Y)
        lm.LineX(self.Width)
        lm.LineY(self.Height)
        lm.LineX(-self.Width)
        lm.LineY(-self.Height)
        #inner rectangle
        lm.Move(self.PaddingLeft,self.PaddingBottom)
        lm.LineX(self.Width-self.PaddingRight-self.PaddingLeft)
        lm.LineY(self.Height-self.PaddingBottom-self.PaddingTop)
        lm.LineX(-self.Width+self.PaddingRight+self.PaddingLeft)
        lm.LineY(-self.Height+self.PaddingBottom+self.PaddingTop)
        #onter lines
        lm.MoveTo(self.Location.X+self.PaddingLeft, 
                  self.Location.Y+self.Height-self.PaddingTop-13)
        lm.LineX(60)
        lm.LineY(13)
        lm.MoveTo(self.Location.X+self.Width-self.PaddingRight,
                  self.Location.Y+self.Height-self.PaddingTop-13)
        lm.LineX(-14)
        lm.LineY(13)
        lm.MoveY(-13)
        lm.LineX(-46)
        lm.LineY(13)
        lm.MoveY(-13)
        lm.LineX(-65)
        lm.LineY(13)
        lm.Move(111,-13)
        lm.Line(14,13)
        
def CreateForm():
    "create a form with n pages."
    #check whether view exist.
    ViewName='KT_FORM'
    for view in ktDraft.GetViews():
        if view[1]=='KT_FORM':
            print 'view already exist.'
            return
    hd=kcs_draft.view_new(ViewName)
    res=kcs_ui.int_req("How many pages do you want?",1)
    if res[0]==kcs_util.ok():
        for i in range(res[1]):
            pg=Page()
            pg.Location=Point2D(i*420,0)
            pg.Index=i+1
            kcs_draft.subpicture_current_set(hd)
            pg.Draw()
    kcs_draft.dwg_purge()