
import sys
from io import BytesIO

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
from PIL import Image
import chardet

class MyTextEdit(QTextEdit):
    mousePressSignal = pyqtSignal(str)
    contextMenuSignal = pyqtSignal(QMenu,QPoint)

    def __init__(self, key):
        super(QTextEdit,self).__init__()
        self.key=key
        self.setFrameStyle(QFrame.NoFrame)
    def mousePressEvent(self, event):
        self.mousePressSignal.emit("345")
        print(event.pos())
        QTextEdit.mousePressEvent(self,event)
    def contextMenuEvent(self,event):
        menu=self.createStandardContextMenu()
        print("contextMenuEvent",event.pos())
        self.contextMenuSignal.emit(menu,event.globalPos())

class MyLabel(QLabel):
    def __init__(self, *args):
        super(QLabel,self).__init__(*args)
    def mousePressEvent(self,event):
        print("label pos",self.geometry())
        pass
class MyImage(QImage):
    def __init__(self, *args):
        super(QImage,self).__init__(*args)

class TextEditDemo(QWidget):
    def __init__(self,parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.setWindowTitle('QTextEdit 例子')

        #定义窗口的初始大小
        self.resize(300,270)
        #创建多行文本框
        self.scroll=QScrollArea(objectName="ScrollView")
        w= QWidget()
        #self.textEdit = MyTextEdit(w)
        self.textEdit = MyTextEdit("test1")
        self.textEdit.setContentsMargins(QMargins(0,0,0,0))
        self.textEdit.setPlaceholderText("type your text")

        #创建两个按钮
        self.btnPress1=QPushButton('显示文本')
        self.btnPress2=QPushButton('显示HTML')
        self.btnPress3 = QPushButton('删除table')
        self.btnPress4 = QPushButton('添加label')
        '''
        self.label=QLabel(w)
        self.label.setText("test")
        self.label.setGeometry(0,0,50,20)
        self.label.setVisible(False)
        '''
        #实例化垂直布局
        self.layout=QVBoxLayout()

        self.layout.setContentsMargins(QMargins(0,0,0,0))
        self.layout.setSpacing(0)
        #相关控件添加到垂直布局中

        self.mylayout=QVBoxLayout()
        self.mylayout.setContentsMargins(QMargins(0,0,0,0))
        self.mylayout.setSpacing(0)
        self.mylayout.addWidget(self.textEdit)
        self.mylayout.insertStretch(-1,0)
        #w.setStyleSheet("background:grey")
        w.setLayout(self.mylayout)
        w.setContentsMargins(0,0,0,0)
        self.scroll.setFrameStyle(QFrame.NoFrame)
        self.scroll.setWidget(w)
        self.scroll.setWidgetResizable(True)
        self.scroll.setContentsMargins(0,0,0,0)

        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        self.scroll.setStyleSheet(content)
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        l2=QHBoxLayout()
        l2.addWidget(self.btnPress1)
        l2.addWidget(self.btnPress2)
        l2.addWidget(self.btnPress3)
        l2.addWidget(self.btnPress4)
        w2=QWidget()
        w2.setLayout(l2)

        self.layout.addWidget(w2)
        self.layout.addWidget(self.scroll)
        #设置布局
        self.setLayout(self.layout)


        #将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress1.clicked.connect(self.btnPress1_clicked)
        self.btnPress2.clicked.connect(self.btnPress2_clicked)
        self.btnPress3.clicked.connect(self.btnPress3_clicked)
        self.btnPress4.clicked.connect(self.btnPress4_clicked)

        self.addEventListener(self.textEdit)

    def addEventListener(self,textEdit):

        textEdit.setFixedHeight(28)
        textEdit.textChanged.connect(lambda: self.onTextChanged(textEdit.key))
        textEdit.selectionChanged.connect(lambda:self.onSelectionChanged(textEdit.key))
        textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)
        textEdit.mousePressSignal.connect(self.OnMousePressed)
        textEdit.contextMenuSignal.connect(self.OnContextMenuEvent)
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

    def onTextChanged(self,key):

        document=self.textEdit.document()
        newHeight = document.size().height()+5
        if newHeight != self.textEdit.height():
            self.textEdit.setFixedHeight(newHeight)

        #self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum() + 100)

    def onSelectionChanged(self,name):
        print("onSelectionChanged",name)
        textCursor=self.textEdit.textCursor()
        selectedHtml=textCursor.selection().toHtml()
        #print(selectedHtml)

    def btnPress1_clicked(self):
        '''
        textEdit= MyTextEdit("test2")
        self.addEventListener(textEdit)
        self.layout.insertWidget(1,textEdit)
        #self.layout.removeWidget(self.btnPress3)

        html=self.textEdit.toHtml()
        print(html)
        print(self.textEdit.cursorRect())

        img=QImage("./test.jpg")

        cursor = self.textEdit.textCursor()
        cursor.insertBlock()

        cursor.insertImage(img, "myimage");
        '''
        self.insertImage()
    def insertImage(self):
        url = "http://photocdn.sohu.com/20120128/Img333056814.jpg"
        res = requests.get(url)
        img = QImage.fromData(res.content)

        img=img.scaled(QSize(50,50),Qt.KeepAspectRatio);
        pixmap = QPixmap.fromImage(img)
        l1 = MyLabel(self)
        l1.setPixmap(pixmap)
        l1.setStyleSheet("background:white")
        l1.setAlignment(Qt.AlignCenter)
        self.mylayout.insertWidget(1, l1)
        textEdit = MyTextEdit("test2")
        self.addEventListener(textEdit)
        self.mylayout.insertWidget(2, textEdit)
        textEdit.setFocus()

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
    def btnPress4_clicked(self):
        self.insertLabel()
    def deleteTable(self):
        textCursor = self.textEdit.textCursor()
        table = textCursor.currentTable()
        if table != None:
            table.removeRows(0, table.rows())

    def insertLabel(self):
        img = QImage("./test.jpg")

        cursor = self.textEdit.textCursor()
        cursor.insertBlock()

        cursor.insertImage(img, "myimage");
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