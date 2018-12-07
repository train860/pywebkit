# -*- coding: utf-8 -*
import serial

'''客显'''
class Display():
 
    def __init__(self):
        self.ser=serial.Serial()
        self.ser.baudrate =2400
        self.ser.port = 'COM2'  # '/dev/tty.Bluetooth-Incoming-Port'
    #初始化
    def init(self):
        self.ser.open()
        data = b'\x1B\40'  # 初始化
        n = self.ser.write(data)
        self.ser.close()
        return n
    #清屏
    def clear(self):
        self.ser.open()
        data = b'\x0C'#清屏
        n = self.ser.write(data)
        self.ser.close()
        return n
    # 全暗
    def darkScreen(self):
        self.ser.open()
        data = b'\x1B\x73\x30'#全暗
        n = self.ser.write(data)
        self.ser.close()
        return n
    #单价
    def unitPrice(self,price):
        self.ser.open()
        data =b'\x1B\x73\x31'#单价
        num=b'\x1B\x51\x41' + (str(price)).encode('utf-8') + b'\x0D'  # 发送数据
        self.ser.write(data)
        n=self.ser.write(num)
        self.ser.close()
        return n

    # 应收
    def ablePrice(self, price):
        self.ser.open()
        data = b'\x1B\x73\x32'#应收
        num = b'\x1B\x51\x41' + (str(price)).encode('utf-8') + b'\x0D'  # 发送数据
        self.ser.write(data)
        n = self.ser.write(num)
        self.ser.close()
        return n

    # 实收
    def receivedPrice(self, price):
        self.ser.open()
        data = b'\x1B\x73\x33'#实收
        num = b'\x1B\x51\x41' + (str(price)).encode('utf-8') + b'\x0D'  # 发送数据
        self.ser.write(data)
        n = self.ser.write(num)
        self.ser.close()
        return n

    # 找回
    def backPrice(self, price):
        self.ser.open()
        data = b'\x1B\x73\x34'#找回
        num = b'\x1B\x51\x41' + (str(price)).encode('utf-8') + b'\x0D'  # 发送数据
        self.ser.write(data)
        n = self.ser.write(num)
        self.ser.close()
        return n

    #清除光标
    def clearPointer(self):
        self.ser.open()
        data = b'\x24'#清除光标
        n=self.ser.write(data)
        self.ser.close()
        return n

    # 移动光标
    def movePointer(self,num):
        self.ser.open()
        data = b'\x1B\x6C'+(str(num)).encode('utf-8')#移动光标
        n = self.ser.write(data)
        self.ser.close()
        return n
