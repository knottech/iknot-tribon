import ktBasic
import kcs_ui
import kcs_util
from KcsPoint2D import Point2D
def run():
    pt=Point2D()
    res=kcs_ui.point2D_req('��ѡ�����ĵ�',pt)
    if res[0]==kcs_util.ok():
        res2=kcs_ui.string_req('���������εĳߴ�','300,100')
        if res2[0]==kcs_util.ok():
            li=[float(s) for s in res2[1].split(',')]
            if len(li)==2:
                a,b=li
            else:
                raise 'wrong input'
            ktBasic.Diamond(res[1], a, b)
if __name__=='__main__':
    run()