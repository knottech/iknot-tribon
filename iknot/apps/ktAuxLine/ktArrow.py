import ktBasic
from iknot.core import ktUi
def run():
    pts=ktUi.Pick2DPoints(2)
    ktBasic.Arrow(pts[0], pts[1])