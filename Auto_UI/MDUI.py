from PySide2.QtWidgets import QMainWindow,QWidget,QPushButton,QApplication,QPlainTextEdit
from PySide2.QtGui import QFont
import sys

class MD_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600,600)
        self.setWindowTitle("MD_get_data_tool")
        msg_font=QFont("Arial", 16, QFont.Black)
        self.msg = QPlainTextEdit(self)
        self.msg.setGeometry(10,10,580,520)
        self.msg.setFont(msg_font)


        Btn_font =QFont("Arial", 20, QFont.Black)

        self.btn_start = QPushButton(self)
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setGeometry(10, 540, 180, 50)
        self.btn_start.setText("start")
        self.btn_start.setFont(Btn_font)


        self.btn_clear = QPushButton(self)
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.setGeometry(210, 540, 180, 50)
        self.btn_clear.setText("clear")
        self.btn_clear.setFont(Btn_font)


        self.btn_stop = QPushButton(self)
        self.btn_stop.setObjectName("btn_end")
        self.btn_stop.setGeometry(410, 540, 180, 50)
        self.btn_stop.setText("stop")
        self.btn_stop.setFont(Btn_font)


    def test(self):
        print("123456")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MD_UI()
    ui.show()
    sys.exit(app.exec_())