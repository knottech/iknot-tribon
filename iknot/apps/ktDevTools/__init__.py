# -*- coding:cp936 -*-

"""
Purpose:Some gadget for developer to understand vitesse.
Author:IAN
Contact:knottech@163.com
"""

menu=("开发者工具",
        ("User response", "iknot.apps.ktDevTools.PrintUserResponse",
         'to print all possible user response.'),
        ("KcsLinetype", "iknot.apps.ktDevTools.ShowLinetypes",
         'To display all the possible line type on current drawing'),
        ("KcsColour", "iknot.apps.ktDevTools.ShowColors",
         'To display all the possible colors on current drawing'),
        ("KcsCursorType", "iknot.apps.ktDevTools.ShowCursorType",
         'To display all the possible cursor types on current drawing'),
        ("Generate fake vitesse", "iknot.apps.ktDevTools.GenFakeKcs",
        'Generate FakeVitesse for developer.'),
        ("Show dwg info", "iknot.apps.ktDevTools.ShowElements",
          'Display information of view,subview,subpicture'),
        ("Experiment", "iknot.apps.ktDevTools.Experiment",
          'For developer to test their temporary code.'),
    )
