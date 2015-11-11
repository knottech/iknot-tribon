# -*- coding:cp936 -*-

"""
Purpose:A tool to create and manipulate a table on current drawing.
Author:IAN
Contact:knottech@163.com
"""

menu=("表格",
        ("新建空白表格", "iknot.apps.ktTable.CreateEmptyTable",
         'Create an m x n table without text.'),
        ("从csv文件创建", "iknot.apps.ktTable.ShowLinetypes",
         'To display all the possible line type on current drawing'),
        ("设置列文本", "iknot.apps.ktTable.ChangeColumnText",
         'Set the column text'),
        ("设置列宽度", "iknot.apps.ktTable.ChangeColumnWidth",
         'Set the length of column'),
        ("修改单元格", "iknot.apps.ktTable.ChangeCellText",
        'Set the cell text.'),
        ("移动列", "iknot.apps.ktTable.MoveColumn",
          'move the column in x direction.'),
    )
