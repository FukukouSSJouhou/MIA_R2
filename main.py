# これはサンプルの Python スクリプトです。
import sys
import os
from PySide2 import QtCore, QtWidgets, QtQml,QtGui
# Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。
from PySide2.QtWidgets import QApplication, QLabel

from MainWindow import MainWindowConnect


def main():
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    print ("Detamon")
    app=QtWidgets.QApplication(sys.argv)
    mainwinconnect=MainWindowConnect()
    engine=QtQml.QQmlApplicationEngine()
    ctx=engine.rootContext()
    ctx.setContextProperty("mainwinconnect",mainwinconnect)
    engine.load('MIA_R2.qml')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    main()

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
