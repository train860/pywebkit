from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QDialog):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton('退出', self, clicked=self.doClose))

        # 窗口透明度动画类

        self.animation = QPropertyAnimation(self,b'pos')
        self.animation.setDuration(200)  # 持续时间1秒

        # 执行淡入
        self.doShow()

    def doShow(self):
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(QPoint(0,0))
        self.animation.setEndValue(QPoint(20,20))
        self.animation.start()

    def doClose(self):
        dialog=Window()
        dialog.exec()
        return
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())