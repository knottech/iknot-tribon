# -*- coding:cp936 -*-

"""
Purpose:To display information of view,subview,subpicture on current drawing.
Author:IAN
http://www.iknot.org
"""

import kcs_ui
import kcs_util
from iknot.core import ktDraft
from kcs_ui import message_noconfirm as msg
from KcsPoint2D import Point2D
import kcs_draft

def run():
    actions=['View','Subview','Component','Element']
    res,act=kcs_ui.choice_select('View info','Select the type',actions)
    if res==kcs_util.ok():
        pt=Point2D()
        if act==1:
            ees=ktDraft.GetViews()
            printElements(ees)
        elif act==2:
            kcs_ui.point2D_req('Select',pt)
            hd=kcs_draft.view_identify(pt)
            ees=ktDraft.GetSubviews(hd)
            printElements(ees)
        elif act==3:
            kcs_ui.point2D_req('Select',pt)
            hd=kcs_draft.subview_identify(pt)
            ees=ktDraft.GetComponents(hd)
            printElements(ees)
        elif act==4:
            kcs_ui.point2D_req('Select',pt)
            hd=kcs_draft.component_identify(pt)
            ees=ktDraft.GetSubElements(hd)
            printElements(ees)
def printElements(ees):
    print 'contains:'
    for ee in ees:
        print ee