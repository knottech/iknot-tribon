# -*- coding:cp936 -*-

"""
Author:IAN
www.iknot.org
Contact:knottech@163.com
"""

import kcs_util
from iknot.core import ktGui
from iknot.apps import ktText,ktAuxLine
from iknot.apps import ktMeasure
from iknot.apps import ktNote
from iknot.apps import ktDevTools
from iknot.apps import ktTable
from iknot.apps import ktDwgForm
from iknot.apps import ktWebsite


if not ktGui.IsMenuExist():
    _ktMenu=[]
    if kcs_util.app_basic_design():
        pass
    elif kcs_util.app_cable():
        pass
    elif kcs_util.app_curved_hull():
        pass
    elif kcs_util.app_diagram():
        pass
    elif kcs_util.app_drafting():
        pass
    elif kcs_util.app_planar_hull():
        from iknot.apps import ktHull
        _ktMenu.append(ktHull.menu)
    elif kcs_util.app_nesting():
        pass
    elif kcs_util.app_pipe():
        pass
    elif kcs_util.app_structure():
        pass
    elif kcs_util.app_ventilation():
        pass
    else:
        print 'can not identify the current application.'
    _ktMenu.append(ktDwgForm.menu)
    _ktMenu.append(ktText.menu)
    _ktMenu.append(ktMeasure.menu)
    _ktMenu.append(ktNote.menu)
    _ktMenu.append(ktTable.menu)
    _ktMenu.append(ktDevTools.menu)
    _ktMenu.append(ktWebsite.menu)
    _ktMenu.append(('',-1))
    _ktMenu.append(('About','iknot.about'))
    
    ktGui.AddMenu('iKnot', _ktMenu)