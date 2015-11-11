import ktBasic
import kcs_ui
import kcs_util
from KcsPoint2D import Point2D
def run():
    pt=Point2D()
    res=kcs_ui.point2D_req('��ѡ�����ĵ�',pt)
    if res[0]==kcs_util.ok():
        res2=kcs_ui.string_req('���������Բ�뾶����������ת�Ƕȣ�Ĭ��Ϊ0��','100,6,0')
        if res2[0]==kcs_util.ok():
            li=[float(s) for s in res2[1].split(',')]
            radius,number,angle=0.0,0.0,0.0
            if len(li)==2:
                radius,number=li
            elif len(li)==3:
                radius,number,angle=li
            else:
                raise 'wrong input'
            ktBasic.Polygon(res[1], radius, number, angle)
if __name__=='__main__':
    run()