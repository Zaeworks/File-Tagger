from dialog import AddTagDialog, ManageDialog
import sys
import os
from PyQt5 import QtWidgets

'''
参数
-a 快速标签 -f/-d 文件/目录
-m 管理
'''

if __name__ == "__main__":
    argv = sys.argv
    FILEPATH = argv[0]
    app = QtWidgets.QApplication(sys.argv)
    print(app.libraryPaths())
    app.addLibraryPath(".")
    if argv[1:] and argv[1] == '-a':
        isFile = True if argv[2] == '-f' else False
        path = ' '.join(argv[3:])
        dialog = AddTagDialog(path, isFile)
    elif argv[1:] and argv[1] == '-m':
        path = ' '.join(argv[2:])
        dialog = ManageDialog(path)
    else:
        path = os.path.abspath('')
        dialog = ManageDialog(path)
    dialog.show()
    sys.exit(app.exec_())
