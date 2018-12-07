# -*- coding: utf-8 -*
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtWebEngineWidgets import *

import configparser
import sys
import glob
import serial
import serial.tools.list_ports

''' 串口工具 '''
class SerialTool():
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.parity = "N"
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.timeout = 0.25

    def getId(self,port):

        self.ser.port = port

        data = b'AT$DTUID?'
        str=""
        try:
            self.ser.open()
            self.ser.write(data)
            str = self.ser.readline()
            self.ser.close()
        except serial.SerialException:
            pass
        if str=="":
            return str
        else:
            return str.decode("utf-8")  # +DTUID:cypyzx001


'''Js 桥接'''
'''前端html需要引入qwebchannel.js'''
'''http://doc.qt.io/archives/qt-5.10/qtwebengine-webenginewidgets-markdowneditor-example.html'''
class PythonJS(QObject):
    '''供js调用'''
    __pyqtSignals__ = ("contentChanged(const QString &)")

    #初始化
    @pyqtSlot(str,result=str)
    def testJs(self, text):
        data = "";
        #platform = sys.platform  # .lower()
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        serialTool = SerialTool()
        for port in ports:
            try:
                ser = serial.Serial(port)
                # 向串口发送指令
                data = serialTool.getId(ser.portstr)
                if data != "":
                    break
                ser.close()
            except (OSError, serial.SerialException):
                pass
        return data

class CustomQwebview(QWebEngineView):
    def __init__(self,parent=None):
        super(CustomQwebview,self).__init__(parent)
        # when you want to destroy the dialog set this to True
        self._want_to_close = False
        self.loadFinished.connect(self._on_loadFinished)

        self.page().featurePermissionRequested.connect(self._on_feature_permission_requested)
    #需要重载，否则url无法跳转
    def createWindow(self, QWebEnginePage_WebWindowType):
        return self
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
    app.setApplicationName("webview")
    cf = configparser.ConfigParser()
    cf.read("config.conf")
    serverUri = cf.get("common", "server_uri")
    #url=QUrl("http://192.168.199.135:8090/cect29_guard/")
    url = QUrl(serverUri)
    wv =CustomQwebview()
    wv._want_to_close=True
    #去掉标题栏
    #wv.setWindowFlags(Qt.FramelessWindowHint)
    #wv.setWindowFlags(Qt.WindowTitleHint)
    #全屏
    wv.showMaximized()
    #screen = QDesktopWidget().availableGeometry()
    #wv.setFixedSize(screen.width(), screen.height())

    pjs = PythonJS()

    page=wv.page()
    channel = QWebChannel(page)
    channel.registerObject('bridge', pjs)
    page.setWebChannel(channel)
    wv.page().setUrl(url)
    wv.show()
    app.exec()