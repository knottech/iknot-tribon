# -*- coding:cp936 -*-

"""
Purpose:Copy parts between panel.
Author:IAN
http://www.iknot.org
"""

import kcs_ui
import CommonSample
import kcs_hullpan

def run():
    model = CommonSample.SelectModel('plane panel', 'select part')
    group = kcs_hullpan.group_get(model.Name, model.PartId)
    stmt = kcs_hullpan.stmt_get(model.Name, group)
    
    kcs_ui.message_confirm(stmt)
    panel2 = CommonSample.SelectModel('plane panel', 'select part')
    kcs_hullpan.pan_activate([panel2.Name])
    kcs_hullpan.stmt_exec_single(0, stmt, panel2.Name)
    kcs_hullpan.pan_store([panel2.Name])
    kcs_hullpan.pan_skip([panel2.Name])
