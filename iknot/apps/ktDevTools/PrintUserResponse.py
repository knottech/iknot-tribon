# -*- coding:cp936 -*-

"""
Purpose:To print all the response value(integer).
Author:IAN
http://www.iknot.org
"""

import kcs_util as util
import kcs_ui
from kcs_ui import message_noconfirm as msg
from KcsPoint2D import Point2D

def PrintAll():
    msg("ok():%s" % util.ok())
    msg("cancel():%s" % util.cancel())
    msg("quit():%s" % util.quit())
    msg("options():%s" % util.options())
    msg("operation_complete():%s" % util.operation_complete())
    msg("yes():%s" % util.yes())
    msg("no():%s" % util.no())
    msg("all():%s" % util.all())
    msg("undo():%s" % util.undo())
    msg("reject():%s" % util.reject())
    msg("exit_function():%s" % util.exit_function())
    
def PrintUserResponse():
    while True:
        pt=Point2D()
        res=kcs_ui.point2D_req('Esc to quit.',pt)
        if res[0]==util.cancel():
            break
        else:
            msg('Your response is: %s'%res[0])
def run():
    res,action=kcs_ui.choice_select('User response','Choices',
        ['Print all','Response of point2D_req'])
    if res==util.ok():
        if action==1:
            PrintAll()
        elif action==2:
            PrintUserResponse()
    
if __name__ == "__main__":
    PrintAll()
