import cx_Freeze as cx
import platform
import os

if platform.system()=="Windows":
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))

os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR,'tcl','tk8.6')

include_files = ["tic-tac-toe.ico", (os.path.join(PYTHON_DIR,'DLLs','tcl86t.dll'),''), (os.path.join(PYTHON_DIR,'DLLs','tk86t.dll'),'')]


target_name = None
base = None
if platform.system()=="Windows":
    base = "Win32GUI"
    target_name = 'Tic Tac Toe.exe'

shortcut_data = [
    ('DesktopShortcut','DesktopFolder','Tic Tac Toe','TARGETDIR',
        '[TARGETDIR]'+target_name,None,'It is a 1 vs 1 game',None,None,None,None,'TARGETDIR'
        ),(
            'MenuShortcut','ProgramMenuFolder','Tic Tac Toe','TARGETDIR','[TARGETDIR]'+target_name,None,
            'It is a 1 vs 1 game',None,None,None,None,'TARGETDIR'
        )
]

cx.setup(name = "Tic Tac Toe",
         version = "1.0",
         author = "Harshvardhan Singh",
         author_email = "harshvardhansingh458@gmail.com",
         description = "It is a 1 vs 1 game",
         options = {'build_exe':{'packages':["tkinter"],'include_files':include_files},
                    'bdist_msi':{
                        'upgrade_code':'{83A4FBB5-5727-4195-ADA6-2765FB571421}','data':{'Shortcut':shortcut_data}
                    }},
         executables = [cx.Executable("main.py",base = base,targetName=target_name,icon="tic-tac-toe.ico")])
