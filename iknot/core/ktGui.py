# -*- coding:cp936 -*-

"""
purpose:to create menu and toolbar for apps.
author:IAN
contact:knottech@163.com
"""

import kcs_gui

def AddKnotSubMenu(name,menu):
    """add items on Knot sub menu.
    name:sub menu name
    menu: ((caption,script,message),(caption,script,message),...)
    """
    ktmenu=GetKnotMenu()
    m=kcs_gui.menu_add(ktmenu,0,name)
    subIndex=0
    for item in menu:
        kcs_gui.menu_item_usr_add(m,subIndex,item[0],item[1],item[2])
        subIndex += 1
    
def AddKnotItem(caption,script,message=''):
    """add a item on knot menu."""
    menu=GetKnotMenu()
    kcs_gui.menu_item_usr_add(menu,0,caption,script,message)

def GetMenu(menuName):
    """
    return menu object by given name.
    if the name is not exist, create a new one and return.
    """
    main_menu = kcs_gui.menu_get(None, 0)
    index=0
    while True:
        menu=kcs_gui.menu_item_get(main_menu, index)
        if menu[0]==menuName:
            return kcs_gui.menu_get(main_menu,index)
        elif menu[0]=='&Help':
            return kcs_gui.menu_add(main_menu,index+1,menuName)
        elif index>100:
            return None
        else:
            index+=1
def GetMenus():
    main_menu = kcs_gui.menu_get(None, 0)
    index=0
    menus=[]
    while True:
        try:
            m=kcs_gui.menu_item_get(main_menu, index)
            menus.append((m[0],m[1],kcs_gui.menu_get(main_menu,index)))
            index+=1
        except 'kcs_IndexError':
            print 'error----------'
        except:
            return menus
def IsMenuExist(menuName='iKnot'):
    main_menu = kcs_gui.menu_get(None, 0)
    index=0
    while True:
        try:
            menu=kcs_gui.menu_item_get(main_menu, index)
            if menu[0]==menuName:
                return True
            index+=1
        except:
            return False
def GetKnotMenu():
    """return 'iKnot' menu object"""
    return GetMenu('iKnot')

def AddMenu(menuName, menuList):
    """initiate the menu.
    menuName:menu name
    menuList:[("sub menu name",
                ("caption", "script",'message'),
                ("caption", "script",'message'),
            ),
            ]
    """
    try:
        main_menu = kcs_gui.menu_get(None, 0)
        index = 0
        while 1:
            if kcs_gui.menu_item_get(main_menu, index)[0] == "&Help":
                break;
            elif kcs_gui.menu_item_get(main_menu, index)[0] == menuName:
                return
            else:
                index = index + 1;
                
        ktMenu = kcs_gui.menu_add(main_menu, index + 1, menuName)
        menuIndex = 0
        for menu in menuList:
            if len(menu) == 2 and isinstance(menu[1], str): 
                kcs_gui.menu_item_usr_add(ktMenu, menuIndex, menu[0], menu[1])
                menuIndex += 1
            elif len(menu) == 2 and menu[1] == -1:  # 分隔线
                kcs_gui.menu_item_std_add(ktMenu, menuIndex, menu[0], menu[1])
                menuIndex += 1
            else:
                m = kcs_gui.menu_add(ktMenu, menuIndex, menu[0])
                subIndex = 0
                for submenu in menu[1:]:
                    kcs_gui.menu_item_usr_add(m, subIndex, submenu[0], submenu[1])
                    subIndex += 1
                menuIndex += 1
    except Exception, e:
        print e
        
if __name__=="__main__":
    pass