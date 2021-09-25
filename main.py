import random
import sys
import time

import PySide2
from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from numpy import sqrt

from untitled import Ui_MainWindow


class MainThread(QThread):
    finished_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        x = 0
        while True:
            time.sleep(0.05)
            x = x + 0.001
            y = 100 * (x - sqrt(x)) / (x - 1)
            self.finished_signal.emit(y)


# 检测ip
def validate_ip(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i, x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError:
            return False
    return True


class main_window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.thread = MainThread()
        self.thread.finished_signal.connect(self.set_progressbar_value)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0)
        self.ui.pushButton.clicked.connect(self.start)

    def set_progressbar_value(self, value):
        self.ui.progressBar.setValue(value)
        if value >= 100:
            self.ui.label.setText("黑入成功")
        elif value >= 99.101:
            self.ui.label.setText("正在加载视频预览")
        elif value >= 98.012:
            self.ui.label.setText("正在开启对方的摄像头")
        elif value >= 97.321:
            self.ui.label.setText("正在开启远程主机的权限")
        elif value >= 91.987:
            self.ui.label.setText("正在尝试登入系统并安装\r\n\r\n远程操控驱动")
        elif value >= 75.129:
            self.ui.label.setText("正在暴力破解对方的密码，这可能\r\n\r\n会花费一段时间")
        elif value >= 70.583:
            self.ui.label.setText("正在搜索合适的密码破解算法")
        elif value >= 64.257:
            self.ui.label.setText("正在扫描对方的漏洞")
        elif value >= 61.234:
            self.ui.label.setText("正在验证系统版本")
        elif value >= 55.123:
            self.ui.label.setText("正在建立网络连接")
        else:
            self.ui.label.setText("正在初始化")

    def start(self):
        ip_str = self.ui.lineEdit.text()
        if not validate_ip(ip_str):
            msg_box = QMessageBox(QMessageBox.Warning, '摄像头黑入器', 'ip地址不正确')
            msg_box.exec_()
        else:
            choice = QMessageBox.warning(self, '摄像头黑入器',
                                         '即将开始黑入远程主机！\r\n\r\n警告：利用系统漏洞黑入对方摄像头是违法行为，可能会被追踪法律责任！\r\n由此产生的一切责任与开发者无关！',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.thread.start()
                self.ui.pushButton.setEnabled(False)
                self.ui.lineEdit.setEnabled(False)
            elif choice == QMessageBox.No:
                print('取消')

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        if 100 > self.ui.progressBar.value() > 60:
            msg_box = QMessageBox(QMessageBox.Warning, '摄像头黑入器', '网络连接已建立，正在运行黑入计划……暂时无法退出。请稍后重试。')
            msg_box.exec_()
            event.ignore()
        else:
            super().closeEvent(event)
            self.thread.quit()
            self.thread.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.setWindowTitle("摄像头黑入器")
    window.setFixedWidth(window.width())
    window.setFixedHeight(window.height())
    window.show()
    sys.exit(app.exec_())
