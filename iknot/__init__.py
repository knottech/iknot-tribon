# -*- coding:cp936 -*-

"""
Author:IAN
Contact:knottech@163.com
"""

import kcs_util
from iknot.core import ktGui
from iknot.apps import ktText, ktSymbol
from iknot.apps import ktMeasure
from iknot.apps import ktNote

if not ktGui.IsMenuExist():
    _ktMenu=[]
    if kcs_util.app_basic_design():
        print 'basic design'
    elif kcs_util.app_cable():
        print 'app_cable'
    elif kcs_util.app_curved_hull():
        print 'curved hull'
    elif kcs_util.app_diagram():
        print 'diagram'
    elif kcs_util.app_drafting():
        _ktMenu.append(ktText.menu)
        _ktMenu.append(ktMeasure.menu)
        _ktMenu.append(ktSymbol.menu)
        _ktMenu.append(ktNote.menu)
    elif kcs_util.app_planar_hull():
        ktGui.AddKnotSubMenu(ktText.menu_name, ktText.menu)
    elif kcs_util.app_nesting():
        print 'nesting'
    elif kcs_util.app_pipe():
        print 'pipe'
    elif kcs_util.app_structure():
        print 'structure'
    elif kcs_util.app_ventilation():
        print 'ventilation'
    else:
        print 'can not identify the current application.'
    ktGui.AddMenu('iKnot', _ktMenu)