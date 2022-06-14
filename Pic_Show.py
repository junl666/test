from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
from rotate import Ui_MainWindow

'''定义主窗口'''


class PicShow(QtWidgets.QMainWindow, Ui_MainWindow):  # 不可用QMainWindow,因为QLabel继承自QWidget
    def __init__(self, img_path):
        super(PicShow, self).__init__()
        self.img_path = img_path
        self.setupUi(self)
        pic_width, pic_height = cv2.imread(img_path).shape[0], cv2.imread(img_path).shape[1]
        self.resize(pic_width, pic_height)  # 设定窗口大小(根据自己显示图片的大小，可更改)
        self.setWindowTitle("图片查看")  # 设定窗口名称

        self.imgPixmap = QPixmap(img_path)  # 载入图片
        self.scaledImg = self.imgPixmap.scaled(self.size())  # 初始化缩放图
        self.singleOffset = QPoint(0, 0)  # 初始化偏移值

        self.isLeftPressed = bool(False)  # 图片被点住(鼠标左键)标志位
        self.isImgLabelArea = bool(True)  # 鼠标进入label图片显示区域
        self.rotate.triggered.connect(self.slotRotate)
        self.rotateAnti.triggered.connect(self.slotRotateAnti)

    '''重载绘图: 动态绘图'''

    def paintEvent(self, event):
        self.imgPainter = QPainter()  # 用于动态绘制图片
        self.imgFramePainter = QPainter()  # 用于动态绘制图片外线框
        self.imgPainter.begin(self)  # 无begin和end,则将一直循环更新
        self.imgPainter.drawPixmap(self.singleOffset, self.scaledImg)  # 从图像文件提取Pixmap并显示在指定位置
        self.imgFramePainter.setPen(QColor(168, 34, 3))  # 不设置则为默认黑色   # 设置绘图颜色/大小/样式
        self.imgFramePainter.drawRect(10, 10, 480, 480)  # 为图片绘外线狂(向外延展1)
        self.imgPainter.end()  # 无begin和end,则将一直循环更新

    # =============================================================================
    # 图片移动: 首先,确定图片被点选(鼠标左键按下)且未左键释放;
    #          其次,确定鼠标移动;
    #          最后,更新偏移值,移动图片.
    # =============================================================================
    '''重载一下鼠标按下事件(单击)'''

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            print("鼠标左键单击")  # 响应测试语句
            self.isLeftPressed = True  # 左键按下(图片被点住),置Ture
            self.preMousePosition = event.pos()  # 获取鼠标当前位置
        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            print("鼠标右键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            print("鼠标中键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            print("鼠标左右键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            print("鼠标左中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            print("鼠标右中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
                | QtCore.Qt.RightButton:  # 左中右键同时按下
            print("鼠标左中右键同时单击")  # 响应测试语句

    '''重载一下滚轮滚动事件'''

    def wheelEvent(self, event):
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离
        if angleY > 0:  # 滚轮上滚
            print("鼠标中键上滚")  # 响应测试语句
            self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() + 5,
                                                   self.scaledImg.height() + 5)
            newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
                       / (self.scaledImg.width() - 5)
            newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
                        / (self.scaledImg.height() - 5)
            self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
            self.repaint()  # 重绘
        else:  # 滚轮下滚
            print("鼠标中键下滚")  # 响应测试语句
            self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() - 5,
                                                   self.scaledImg.height() - 5)
            newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
                       / (self.scaledImg.width() + 5)
            newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
                        / (self.scaledImg.height() + 5)
            self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
            self.repaint()  # 重绘

    '''重载一下鼠标键公开事件'''

    def mouseReleaseEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键释放
            self.isLeftPressed = False;  # 左键释放(图片被点住),置False
            print("鼠标左键松开")  # 响应测试语句
        elif event.button() == Qt.RightButton:  # 右键释放
            self.singleOffset = QPoint(0, 0)  # 置为初值
            self.scaledImg = self.imgPixmap.scaled(self.size())  # 置为初值
            self.repaint()  # 重绘
            print("鼠标右键松开")  # 响应测试语句

    '''重载一下鼠标移动事件'''

    def mouseMoveEvent(self, event):
        if self.isLeftPressed:  # 左键按下
            print("鼠标左键按下，移动鼠标")  # 响应测试语句
            self.endMousePosition = event.pos() - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
            self.singleOffset = self.singleOffset + self.endMousePosition  # 更新偏移量
            self.preMousePosition = event.pos()  # 更新当前鼠标在窗口上的位置，下次移动用
            self.repaint()  # 重绘

    def slotRotate(self):

        transform = QTransform()
        transform.rotate(90)
        self.imgPixmap = self.imgPixmap.transformed(transform)
        self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width(),
                                               self.scaledImg.height())
        self.repaint()

    def slotRotateAnti(self):

        transform = QTransform()
        transform.rotate(-90)
        self.imgPixmap = self.imgPixmap.transformed(transform)
        self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width(),
                                               self.scaledImg.height())
        self.repaint()


'''主函数'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = PicShow('result.jpg')
    myshow.show()
    sys.exit(app.exec_())
