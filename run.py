from PyQt5 import QtWidgets
from imageprocess import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
from imageedit import ImageEdit
from bottombutton import button_self
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
from Pic_Show import PicShow


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()  # 继承父类的 __init__ 方法。但是在这里好像是多余的？？？
        self.setupUi(self)
        self.open.triggered.connect(self.read_file)  # 打开
        self.save.triggered.connect(self.save_file)  # 保存
        # 编辑
        self.zoomin.triggered.connect(self.zoomin_file)  # 放大
        self.zoomout.triggered.connect(self.zoomout_file)  # 缩小
        self.gray.triggered.connect(self.gray_file)  # 灰度
        self.light.triggered.connect(self.light_file)  # 亮度
        self.rotate.triggered.connect(self.rotate_file)  # 旋转
        self.screenshots.triggered.connect(self.screenshots_file)  # 截图
        # 按钮功能
        # 浏览
        self.Scan.clicked.connect(self.scan_file)

    def read_file(self):
        # 选取文件
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "E:/pythonProject3/qt5manager-master",
                                                         "All Files(*);;Text Files(*.png)")

        print(self.label_pic.size())
        self.lineEdit.setText(filename)

        self.captured = cv2.imread(str(filename))
        # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
        self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)

        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.label_pic.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.label_pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.picShow = PicShow(filename)
        self.picShow.show()

    def save_file(self):
        # 获取文件路径
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            # 用全局变量保存所有需要保存的变量在内存中的值。
            file_name = QFileDialog.getSaveFileName(self, "文件保存", "D:/imagetest/save",
                                                    "All Files (*);;Text Files (*.png)")
            print(file_name[0])
            btn = button_self()
            btn.file_save(file_path, file_name[0])

    def zoomin_file(self):  # 放大
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imageMagnification(file_path)

    def zoomout_file(self):  # 缩小
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imageReduction(file_path)

    def gray_file(self):  # 灰度
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imagegray(file_path)

    def light_file(self):  # 亮度
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imageBrightness(file_path, 1.3, 3)

    def rotate_file(self):  # 旋转
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imagerotate(file_path)

    def screenshots_file(self):  # 截图
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            ImageEdit.imagegrab(file_path)

    # 按钮功能
    # 浏览
    def scan_file(self):
        file_path = self.lineEdit.text()
        if file_path == '':
            self.showMessageBox()
        else:
            btn = button_self()
            btn.scan_pic(file_path)  #

    def showMessageBox(self):
        res_3 = QMessageBox.warning(self, "警告", "请选择文件，再执行该操作！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def resizePicToLabel(self, label_width, label_height, pic_width, pic_height):
        max_ratio = max(pic_width / label_width, pic_height / label_height)
        return pic_width / max_ratio, pic_height / max_ratio


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())
