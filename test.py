
import sys
from io import BytesIO

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
from PIL import Image

class TextEditDemo(QWidget):
    def __init__(self,parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.setWindowTitle('QTextEdit 例子')

        #定义窗口的初始大小
        self.resize(300,270)
        #创建多行文本框
        self.textEdit=QTextEdit()

        #创建两个按钮
        self.btnPress1=QPushButton('显示文本')
        self.btnPress2=QPushButton('显示HTML')

        #实例化垂直布局
        layout=QVBoxLayout()
        #相关控件添加到垂直布局中
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress1)
        layout.addWidget(self.btnPress2)

        #设置布局
        self.setLayout(layout)

        #将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress1.clicked.connect(self.btnPress1_clicked)
        self.btnPress2.clicked.connect(self.btnPress2_clicked)

    def btnPress1_clicked(self):
        #以文本的形式输出到多行文本框
        self.textEdit.setPlainText('Hello PyQt5!\n单击按钮')

    def btnPress2_clicked(self):
        '''
        response = requests.get("http://www.sipbory.com/upload/201612/2.jpg")  # 使用requests库进行网络请求获取内容
        image1 = Image.open(BytesIO(response.content))  # 对得到的二进制数据进行操作
        image1.save('./test.jpg')  # 保存网络图片到本地
        del image1  # 删除图片对象(虽说会自己释放)，没有这个，会出现各种问题
        #image = QImage('xxx.png')
        #self.textEdit.append("<img src = \"./test.jpg\" />")
        self.textEdit.setHtml("<img src = \"./test.jpg\" />")
        '''

        #self.textEdit.setHtml("<table border=1 width=400><tr><td>1111</td></tr><tr><td>222</td></tr></table>")

        #cursor=QTextCursor()

        cursor=self.textEdit.textCursor()
        cursor.movePosition(0);

        table = cursor.insertTable(2, 3);


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=TextEditDemo()
    win.show()
    sys.exit(app.exec_())