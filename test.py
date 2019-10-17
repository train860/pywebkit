
import sys
from io import BytesIO

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
from PIL import Image

class MyTextEdit(QTextEdit):
    mousePressSignal = pyqtSignal(str)
    contextMenuSignal = pyqtSignal(QMenu,QPoint)
    def __init__(self, *args):
        super(QTextEdit,self).__init__(*args)
    def mousePressEvent(self, event):
        self.mousePressSignal.emit("345")
        print(event.pos())
        QTextEdit.mouseMoveEvent(self,event)
    def contextMenuEvent(self,event):
        menu=self.createStandardContextMenu()
        print("contextMenuEvent",event.pos())
        self.contextMenuSignal.emit(menu,event.globalPos())

class MyImage(QImage):
    def __init__(self, *args):
        super(QImage,self).__init__(*args)
    def mousePressEvent(self,event):
        pass
class TextEditDemo(QWidget):
    def __init__(self,parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.setWindowTitle('QTextEdit 例子')

        #定义窗口的初始大小
        self.resize(300,270)
        #创建多行文本框

        w= QWidget()
        #self.textEdit = MyTextEdit(w)
        self.textEdit = MyTextEdit()
        #创建两个按钮
        self.btnPress1=QPushButton('显示文本')
        self.btnPress2=QPushButton('显示HTML')
        self.btnPress3 = QPushButton('删除table')
        '''
        self.label=QLabel(w)
        self.label.setText("test")
        self.label.setGeometry(0,0,50,20)
        self.label.setVisible(False)
        '''
        #实例化垂直布局
        layout=QVBoxLayout()
        #相关控件添加到垂直布局中
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress1)
        layout.addWidget(self.btnPress2)
        layout.addWidget(self.btnPress3)

        #设置布局
        self.setLayout(layout)

        #将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress1.clicked.connect(self.btnPress1_clicked)
        self.btnPress2.clicked.connect(self.btnPress2_clicked)
        self.btnPress3.clicked.connect(self.btnPress3_clicked)

        self.textEdit.selectionChanged.connect(self.onSelectionChanged)
        self.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)
        self.textEdit.mousePressSignal.connect(self.OnMousePressed)
        self.textEdit.contextMenuSignal.connect(self.OnContextMenuEvent)
    def isCursorInTable(self):
        textCursor = self.textEdit.textCursor()
        table = textCursor.currentTable()
        return table != None

    def onCursorPositionChanged(self):
        textCursor = self.textEdit.textCursor()
        table=textCursor.currentTable()
        if table!=None:
            pass
            '''
            #可以获取td的位置
            #print(textCursor.blockNumber())
            #layout().boundingRect()
            #print(textCursor.block() )
            if not self.label.isVisible():
                #self.label.setVisible(True)
                pass
            #r = self.textEdit.cursorRect()
            #self.label.move(r.x(), r.y())
            '''
    def onSelectionChanged(self):
        textCursor=self.textEdit.textCursor()
        selectedHtml=textCursor.selection().toHtml()
        print(selectedHtml)

    def btnPress1_clicked(self):
        html=self.textEdit.toHtml()
        print(html)
        print(self.textEdit.cursorRect())

        img=QImage("./test.jpg")

        cursor = self.textEdit.textCursor()
        #cursor.insertBlock()

        f=QTextFrameFormat()
        f.setBorder(1)
        f.setBorderStyle(QTextFrameFormat.BorderStyle_Solid)
        textFrame=cursor.insertFrame(f)
        textFrame.firstCursorPosition().insertImage(img, "myimage");
        #cursor.insertImage(img, "myimage");

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
        #cursor.movePosition(0);
        tableFormat=QTextTableFormat()
        tableFormat.setCellPadding(0)
        tableFormat.setCellSpacing(0)
        cursor.insertBlock()
        print("table",self.textEdit.cursorRect())
        #这个地方记住table的位置

        cursor.insertTable(2, 3,tableFormat);

    def btnPress3_clicked(self):
        self.deleteTable()

    def deleteTable(self):
        textCursor = self.textEdit.textCursor()
        table = textCursor.currentTable()
        if table != None:
            table.removeRows(0, table.rows())
    @pyqtSlot(str)
    def OnMousePressed(self,text):

        textCursor = self.textEdit.textCursor()
        print(self.textEdit.document().firstBlock().layout().boundingRect())

    @pyqtSlot(QMenu,QPoint)
    def OnContextMenuEvent(self,menu,point):
        textCursor = self.textEdit.textCursor()
        #print(textCursor.block().layout().boundingRect())
        if self.isCursorInTable():
            menu.addAction("test menu",self.deleteTable)
        menu.exec(point)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=TextEditDemo()
    win.show()
    sys.exit(app.exec_())