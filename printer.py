# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui,QtPrintSupport

class Printer():
    # 打印机列表
    @staticmethod
    def printerList():
        printer = []
        printerInfo = QtPrintSupport.QPrinterInfo()
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        return printer

    # 打印任务
    @staticmethod
    def printing(printer='defaultPrinter', context=''):

        printerInfo = QtPrintSupport.QPrinterInfo()
        p = QtPrintSupport.QPrinter()
        p.setResolution(96)
        p.setPageSize(QtPrintSupport.QPrinter.Letter)
        p.setPageMargins(0, 16, 0, 20, QtPrintSupport.QPrinter.Millimeter)
        for item in printerInfo.availablePrinters():
            if printer == item.printerName():
                p = QtPrintSupport.QPrinter(item)
        doc = QtGui.QTextDocument()
        doc.setHtml(u'%s' % context)
        doc.setPageSize(QtCore.QSizeF(p.pageRect().size()))
        #doc.setPageSize(QtCore.QSizeF(300,50))
        #doc.setPageSize(QtCore.QSizeF(p.logicalDpiX() * (80 / 25.4),
                                      #p.logicalDpiY() * (297 / 25.4)))
        p.setOutputFormat(QtPrintSupport.QPrinter.NativeFormat)
        doc.print_(p)