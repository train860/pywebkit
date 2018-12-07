# -*- coding: utf-8 -*
from PyQt5.QtCore import *
import display
import printer
import sys
import json

'''Js 桥接'''
class PythonJS(QObject):
    '''供js调用'''
    __pyqtSignals__ = ("contentChanged(const QString &)")

    @pyqtSlot()
    def close(self):
        sys.exit()

    '''客显'''
    #初始化
    @pyqtSlot(result=int)
    def displayInit(self):
       return display.Display().init()

    #清屏
    @pyqtSlot(result=int)
    def displayClear(self):
        return display.Display().clear()

    # 全暗
    @pyqtSlot(result=int)
    def displayDarkScreen(self):
        return display.Display().darkScreen()

    # 单价
    @pyqtSlot(str,result=int)
    def displayUnitPrice(self,str):
        if not any(str):
            return 0
        return display.Display().unitPrice(str)

    # 应收
    @pyqtSlot(str,result=int)
    def displayAblePrice(self,str):
        if not any(str):
            return 0
        return display.Display().ablePrice(str)

    # 实收
    @pyqtSlot(str,result=int)
    def displayReceivedPrice(self,str):
        if not any(str):
            return 0
        return display.Display().receivedPrice(str)

    # 找回
    @pyqtSlot(str,result=int)
    def displayBackPrice(self,str):
        if not any(str):
            return 0
        return display.Display().backPrice(str)

    # 清除光标
    @pyqtSlot(result=int)
    def displayClearPointer(self):
        return display.Display().clearPointer()

    # 找回
    @pyqtSlot(str, result=int)
    def displayMovePointer(self, str):
        return display.Display().movePointer(str)
    #打印
    @pyqtSlot(str, result=int)
    def printer(self,str):
        if not any(str):
            return 0
        printer.Printer().printing(context=str)
        return 1;