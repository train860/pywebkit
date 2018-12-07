# -*- coding: utf-8 -*
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import *

#import jsnative
import sys

class CustomQwebview(QWebEngineView):
    def __init__(self,parent=None):
        super(CustomQwebview,self).__init__(parent)
        # when you want to destroy the dialog set this to True
        self._want_to_close = False
        self.loadFinished.connect(self._on_loadFinished)
        self.page().featurePermissionRequested.connect(self._on_feature_permission_requested)

    #捕捉窗口关闭事件
    def closeEvent(self, event):
        if self._want_to_close:
            super(CustomQwebview, self).closeEvent(event)
        else:
            event.ignore()
            self.setWindowState(Qt.WindowMinimized)

    def resizeEvent(self, event):
        pass

    @pyqtSlot()
    def _on_loadFinished(self):
        pass

    @pyqtSlot(QUrl, 'QWebEnginePage::Feature')
    def _on_feature_permission_requested(self,url,feature):
        self.page().setFeaturePermission(url, feature,QWebEnginePage.PermissionGrantedByUser)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    url = QUrl("http://www.baidu.com/")
    # url = QUrl("http://localhost")
    wv = CustomQwebview()
    wv._want_to_close = True
    # 去掉标题栏
    # wv.setWindowFlags(Qt.FramelessWindowHint)
    # wv.setWindowFlags(Qt.WindowTitleHint)
    # 全屏
    wv.showMaximized()
    # screen = QDesktopWidget().availableGeometry()
    # wv.setFixedSize(screen.width(), screen.height())
    '''
    pjs = jsnative.PythonJS()

    page = wv.page()
    channel = QWebChannel(page)
    channel.registerObject('python', pjs)
    page.setWebChannel(channel)
    '''
    # wv.page().setUrl(url)
    wv.load(url)
    wv.show()
    sys.exit(app.exec_())
