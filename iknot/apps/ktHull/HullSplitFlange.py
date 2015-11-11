# -*- coding:cp936 -*-

"""
Purpose:Split flange.
Author:IAN
http://www.iknot.org
"""

import kcs_ui
import CommonSample
import kcs_util
import kcs_hullpan


def GetFlange():
    while 1:
        panel = CommonSample.SelectModel('plane panel', 'select panel')
        if panel.PartType == 'flange':
            return panel

def GetPosition():
    actions = ('X', 'Y', 'Z')
    (res, index) = kcs_ui.choice_select('select', \
                                     'Please select line position', actions)
    if res == kcs_util.ok():
        (res, d) = kcs_ui.real_req('Please enter the number')
        if res == kcs_util.ok():
            if index == 1:
                return ('X', d)
            elif index == 2:
                return ('Y', d)
            elif index == 3:
                return ('Z', d)
    else:
        return 0

def GetNewStmt(stmt, pos, number):
    index1 = stmt.index('CON=')
    s1 = stmt[0:index1] + pos + '1=' + str(number) + ', ' + stmt[index1:]   
    index2 = stmt.index('CON=', index1 + 1)
    s2 = stmt[0:index2] + pos + '2=' + str(number) + ', ' + stmt[index2:]
    kcs_ui.message_noconfirm(s1)
    kcs_ui.message_noconfirm(s2)
    return (s1, s2)

def SpliteFlange():
    flange = GetFlange()
    group = kcs_hullpan.group_get(flange.Name, flange.PartId)
    stmt = kcs_hullpan.stmt_get(flange.Name, group)
    pos = GetPosition()
    newStmt = GetNewStmt(stmt, pos[0], pos[1])
    kcs_ui.message_confirm(stmt + '\n' + newStmt[0] + '\n' + newStmt[1])
    kcs_hullpan.stmt_exec(0, newStmt[0])
    kcs_hullpan.stmt_exec(0, newStmt[1])
    stmt2 = 'DEL, ' + stmt
    kcs_hullpan.stmt_exec(group, stmt2)

# You need to active a panel before using this function
def run():
    if not kcs_util.app_planar_hull():
        kcs_ui.message_confirm('该功能只能在Plannar Hull模块下使用.')
        return
    
    SpliteFlange()
# kcs_draft.highlight_off(0)

run()
