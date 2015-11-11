# -*- coding:cp936 -*-

"""
Author:IAN
www.iknot.org
Contact:knottech@163.com
"""

import kcs_ui
import kcs_util
import kcs_draft

from iknot.core import ktDraft
from KcsPoint2D import Point2D
from KcsVector2D import Vector2D
from KcsTransformation2D import Transformation2D
from KcsRline2D import Rline2D
from KcsColour import Colour
from KcsRectangle2D import Rectangle2D
from KcsStringlist import Stringlist
from KcsText import Text

class Table(object):
    "Every table "
    def __init__(self,hd=None):
        "init by view handle"
        
        self.NRow=0 #count of row.(n)
        self.NColumn=0  #count of column.(m)
        self.Cells=[]
        self.Handle=hd #handle of view
        self.Location=Point2D(0,0)  #left top corner of table
        self.RowHeight=3.8
        if hd!=None:
            self._set(hd)
    def Draw(self):
        "Draw table on current drawing"
        if self.Handle==None:   #create a new view for this table
            #get the max index and create view
            tbViews=ktDraft.GetViews(r'^KT_TABLE_.\d*$')
            maxIndex=1
            if len(tbViews)>0:
                maxIndex=max([int(i[1][9:]) for i in tbViews])+1
            viewName='KT_TABLE_%s'%(maxIndex)
            self.Handle=kcs_draft.view_new(viewName)
            kcs_draft.subpicture_current_set(self.Handle)
            
            #create subview
            subName='KT%sX%s'%(self.NColumn,self.NRow)
            hdSub=kcs_draft.subview_new(subName)
            
            #create component for cells
            for c in self.Cells:
                kcs_draft.subpicture_current_set(hdSub)
                c.Draw()
        else:
            for c in self.Cells:
                c.Draw()
        kcs_draft.subpicture_current_set()
    def _set(self,viewhandle):
        """Set table by handle of view
        view name like:KT_TABLE_1
        subview name like:KTmXn
        m:column number
        n:row number
        """
        self.Handle=viewhandle
        #get the size of table
        subview=ktDraft.GetSubviews(viewhandle, r'^KT\d*X\d*$')[0]
        self.NColumn,self.NRow=[int(i) for i in subview[1][2:].split('X')]
        #set the cells
        self.Cells=[]
        comps=ktDraft.GetComponents(subview[0], r'^KT\d*X\d*$')
        for comp in comps:
            c=Cell(comp[0])
            self.Cells.append(c)
    def ChangeColumnText(self,index,strText):
        """Set the column text by strText"""
        column=self.GetColumn(index)
        for c in column:
            c.String=strText
            c.Draw()
    def ChangeCellText(self,m,n,newString):
        "set the cell text by new string"
        c=self.GetCell(m, n)
        c.String=newString
        c.Draw()
    def ChangeColumnWidth(self,index,length):
        """Set the length of column of given index.
        first column's index is 1.
        """
        column=self.GetColumn(index)
        pre_length=abs(column[0].Rect.Corner1.X-column[0].Rect.Corner2.X)
        
        for c in column:
            c.Rect.Corner2.X=c.Rect.Corner1.X+length
            c.Draw()
        #move the columns bigger than index
        dx=length-pre_length
        for i in range(index,self.NColumn):
            self.MoveColumn(i+1, dx)
    def MoveColumn(self,index,offset_x):
        """move the column in x direction"""
        column=self.GetColumn(index)
        for c in column:
            c.Rect.Corner1.X+=offset_x
            c.Rect.Corner2.X+=offset_x
            
            c.Draw()
        #get column width
#         column[0].Rect.Corner2.X-column[0].Rect.Corner1.X
#     def MoveTo(self,pt):
#         "Move table to given point"
#         pass
    def Init(self,m,n,width=30,pos=Point2D(0,0)):
        """init a empty m x n table.
        m:column count
        n:row count
        width:width of each column.
        """
        self.Cells=[]
        self.NColumn=m
        self.NRow=n
        self.Location=pos
        for i in range(self.NColumn):
            for j in range(self.NRow):
                c=Cell()
                c.M=i+1
                c.N=j+1
                c.String=''
                c.Rect.SetCorner1(Point2D(i*width+self.Location.X,-(j+1)*self.RowHeight+self.Location.Y))
                c.Rect.SetCorner2(Point2D((i+1)*width+self.Location.X,-j*self.RowHeight+self.Location.Y))
                self.Cells.append(c)
    def ReadList(self,li):
        """Read from a python list. list should be 2 dimension.
        [(A11,A12,...Am),
         (A21,A22,...Am),
         ...
         (An1,An2,...Anm)]
        """
        self.Cells=[]
        self.NColumn=len(li[0])
        self.NRow=len(li)
        for i in range(self.NColumn):
            for j in range(self.NRow):
                c=Cell()
                c.M=i+1
                c.N=j+1
                c.String=li[j][i]
                self.Cells.append(c)
        #caculate the position
        dx=0 #x offset of cells
        for i in range(self.NColumn):
            column=self.GetColumn(i+1)
            maxLength=max([kcs_draft.text_length(c.GetText()) for c in column])+1
            for c in column:
                cor1=Point2D(self.Location.X+dx,self.Location.Y-self.RowHeight*c.N)
                cor2=Point2D(cor1.X+maxLength,cor1.Y+self.RowHeight)
                c.Rect.SetCorners(cor1,cor2)
            dx+=maxLength
                
    def GetRow(self,rowIndex):
        "return cells of row by given row index"
        return [c for c in self.Cells if c.N==rowIndex]
    def GetColumn(self,colIndex):
        "return cells of column by given column index"
        return [c for c in self.Cells if c.M==colIndex]
    def GetCell(self,m,n):
        """return cell.
        m:column number
        n:row number
        """
        for c in self.Cells:
            if c.M==m and c.N==n:
                return c
    def ReadCsv(self,fileName):
        "Read data from csv file"
        pass
    def SaveToCsv(self,fileName):
        "Save data to csv file"
        pass
    def Clear(self):
        "Delete all Text in the table"
        pass
    def __repr__(self):
        return 'table:%sx%s'%(self.NColumn,self.NRow)

class Cell(object):
    """
    Single cell of table.Each cell is a component of drawing.
    Cell name should like:KTmXn
    m:column index of cell
    n:row index of cell
    ! Set the rectangle before setting string.
    """
    def __init__(self,hd=None):
        self.String=''     #string
        self.Rect=Rectangle2D()
        self.Handle=hd
        self.M=0
        self.N=0
        if hd!=None:
            self._set(hd)
    def _set(self,hd):
        "set by a component handle"
        #set M,N
        name=kcs_draft.subpicture_name_get(self.Handle)
        self.M,self.N=[int(i) for i in name[2:].split('X')]
        #set Text and Rectangle
        ees=ktDraft.GetSubElements(hd)
        for ee in ees:
            if kcs_draft.element_is_text(ee):
                tempText=Text()
                kcs_draft.text_properties_get(ee,tempText)
                self.String=tempText.String
        self.Rect=kcs_draft.element_extent_get(hd)
    def GetCompName(self):
        "return component name of this cell. (KTmXn)"
        return 'KT%sX%s'%(self.M,self.N)
    def GetText(self):
        cor=self.Rect.Corner1
        txt=Text(self.String)
        txt.SetPosition(Point2D(cor.X+1,cor.Y+1))
        txt.SetColour(Colour("Black"))
        txt.SetFont("黑体")
        txt.SetHeight(2.5)
        return txt
    def Draw(self):
        "Draw the cell on drawing."
#         if self.Handle!=None: #clear the cell first
#             for ee in ktDraft.GetSubElements(self.Handle):
#                 print ee
#                 kcs_draft.element_delete(ee)
#         else:
#             # !make sure the parrent sub view is set current
        if self.Handle!=None:
            prt=kcs_draft.element_parent_get(self.Handle)
            kcs_draft.element_delete(self.Handle)
            kcs_draft.subpicture_current_set(prt)
        self.Handle=kcs_draft.component_new(self.GetCompName())
        kcs_draft.subpicture_current_set(self.Handle)
        if len(self.String)>0:
            kcs_draft.text_new(self.GetText())
        kcs_draft.rectangle_new(self.Rect)
        kcs_draft.subpicture_current_set()
    def __repr__(self):
        return 'Cell:%s x %s ,location:%s'%(self.M,self.N,self.Rect.Corner1)

def CreateTable(li):
    """create table from a python list"""
    pt=Point2D()
    res=kcs_ui.point2D_req('Please pick the left-top corner of table.',pt)
    if res[0]==kcs_util.ok():
        t=Table()
        t.ReadList(li)
        t.Draw()

def CreateTableFromCsv(csvfile):
    """Read data from csv file."""
    
    pass
def ChangeColumnWidth():
    pt=Point2D()
    res=kcs_ui.point2D_req('Please select the column',pt)
    if res[0]==kcs_util.ok():
        hdView=kcs_draft.view_identify(res[1])
        comp=kcs_draft.component_identify(res[1])
        #get column index from comp name
        name=kcs_draft.subpicture_name_get(comp)
        colIndex=int(name[2:].split('X')[0])
        table=Table(hdView)
        res=kcs_ui.int_req('Please enter the width',100)
        if res[0]==kcs_util.ok():
            table.ChangeColumnWidth(colIndex, res[1])
def ChangeColumnText():
    pt=Point2D()
    res=kcs_ui.point2D_req('Please select the column',pt)
    if res[0]==kcs_util.ok():
        hdView=kcs_draft.view_identify(res[1])
        comp=kcs_draft.component_identify(res[1])
        #get column index from comp name
        name=kcs_draft.subpicture_name_get(comp)
        colIndex=int(name[2:].split('X')[0])
        table=Table(hdView)
        res=kcs_ui.string_req('Please enter the string','iknot')
        if res[0]==kcs_util.ok():
            table.ChangeColumnText(colIndex, res[1])
def ChangeCellText():
    pt=Point2D()
    res=kcs_ui.point2D_req('Please select the column',pt)
    if res[0]==kcs_util.ok():
        hdView=kcs_draft.view_identify(res[1])
        comp=kcs_draft.component_identify(res[1])
        #get column index from comp name
        name=kcs_draft.subpicture_name_get(comp)
        colIndex=int(name[2:].split('X')[0])
        rowIndex=int(name[2:].split('X')[1])
        table=Table(hdView)
        res=kcs_ui.string_req('Please enter the string','iknot')
        if res[0]==kcs_util.ok():
            table.ChangeCellText(colIndex, rowIndex, res[1])
def CreateEmptyTable():
    """
    Create an m x n table without text.
    
    """
    res=kcs_ui.string_req('please enter the column number,row number and the width of each cell',
                          '5,3,30')
    if res[0]==kcs_util.ok():
        li=res[1].split(',')
        m,n,width=int(li[0]),int(li[1]),float(li[2])
        pt=Point2D()
        res=kcs_ui.point2D_req('Please pick the left-top corner of table.',pt)
        if res[0]==kcs_util.ok():
            t=Table()
            t.Init(m, n, width, res[1])
            t.Draw()
def MoveColumn():
    pt=Point2D()
    res=kcs_ui.point2D_req('Please select the column',pt)
    if res[0]==kcs_util.ok():
        hdView=kcs_draft.view_identify(res[1])
        comp=kcs_draft.component_identify(res[1])
        
        #get column index from comp name
        name=kcs_draft.subpicture_name_get(comp)
        colIndex=int(name[2:].split('X')[0])
        table=Table(hdView)
        res=kcs_ui.int_req('Please enter the offset',100)
        if res[0]==kcs_util.ok():
            table.MoveColumn(colIndex, res[1])
if __name__=='__main__':
    li=[('IAN','23','shanghai','13482488167'),
        ('jiang','32','jiangsu','13469952399'),
        ('hua','24','xuhui,shanghai,china','64685500')]
#     t=Table()
#     t.ReadList(li)
#     t.Draw()
#     MoveColumn()
#     ChangeColumnWidth()
    kcs_draft.dwg_purge()
    kcs_draft.dwg_repaint()