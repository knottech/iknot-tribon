# -*- coding:cp936 -*-

"""
Purpose:Generate FakeVitesse for developer.
Author:IAN
http://www.iknot.org
"""

# import the module first.
# make sure the imported module is valid for current application.

import sys
import os

# Please refer 'vitesse_access.xls' in document for availability of modules.
import kcs_ui
import kcs_dex
import kcs_att
import kcs_gui
import kcs_draft
import kcs_equip
import kcs_vol
import kcs_placvol
import kcs_assembly
import kcs_model
import kcs_modelstruct
import kcs_db
import kcs_weld
# import kcs_ic

import kcs_util
if kcs_util.app_basic_design() or kcs_util.app_planar_hull():
    import kcs_hullpan
    import kcs_chm
    import kcs_struct
elif kcs_util.app_cable():
    import kcs_hullpan
    import kcs_struct
    import kcs_cable
elif kcs_util.app_curved_hull():
    import kcs_chm
elif kcs_util.app_drafting():
    pass
#     import kcs_cway
elif kcs_util.app_nesting():
    pass
elif kcs_util.app_pipe() or kcs_util.app_ventilation():
    import kcs_hullpan
    import kcs_struct
    import kcs_pipe
    import kcs_spec
elif kcs_util.app_structure():
    import kcs_hullpan
    import kcs_struct
    
modList = [sys.modules.get(i) for i in sys.modules if i.startswith("kcs")]

def run():
    """
Do not place the fake vitesse file at python path.
Place it at 'external libraries' of eclipse is recommended
"""
    names=[i.__name__ for i in modList]
    res,action=kcs_ui.string_select('fake vitesse generator',
        'Please select the module you want to generate fake vitesse py.',
        'Press option to generate for all modules.',
        names)
    if res==kcs_util.ok():
        mod=modList[action-1]
        des=kcs_ui.string_req('Where do you want to place the file?',r'C:\temp')
        if des[0]==kcs_util.ok():
#         des = os.path.join(os.path.join(os.getcwd(), "FakeVitesse"))
            fname = des[1] + "\\" + mod.__name__ + ".py"
            GenPy(mod, fname)
    elif res==kcs_util.options():
        des=kcs_ui.string_req('Where do you want to place the file?',r'C:\temp')
        if des[0]==kcs_util.ok():
            for mod in modList:
                fname = des[1] + "\\" + mod.__name__ + ".py"
                GenPy(mod, fname)
def GenPy(mod,fname):
    """generate py file from given module.
    mod:module object.
    fname:file full path.
    """
    f = open(fname, 'w')
    title = """#
# This file is generated automatically
# Author:IAN
# http://www.iknot.org
"""
    f.write(title)
    for i in mod.__dict__.keys():
        s = "def " + i + "():" + "\n"
        f.write(s)
        s = "    return"
        f.write(s + "\n")
    f.close()
    kcs_ui.message_noconfirm('py file saved to:%s'%(fname))
if __name__=='__main__':
    run()