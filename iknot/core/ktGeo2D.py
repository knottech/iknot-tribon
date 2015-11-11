import math
from KcsPoint2D import Point2D

def GetAngle(p1,p2):
    """return the angle of vector made up by p1 and p2."""
    if p1.X==p2.X:
        if p1.Y==p2.Y:
            raise 'Given points have same position.'
        if p1.Y<p2.Y:
            return math.pi*0.5
        elif p1.Y>p2.Y:
            return -math.pi*0.5
    else:
        return math.atan2(p2.Y-p1.Y, p2.X-p1.X)
    
if __name__=='__main__':
    p1=Point2D(0,0)
    p2=Point2D(1,-1)
    a=GetAngle(p1, p2)
    
    print a,math.degrees(a)