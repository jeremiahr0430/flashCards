import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QInputDialog

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.checkbox = QCheckBox('Initial Text', self)

        btn_update = QPushButton('Update Text', self)
        btn_update.clicked.connect(self.show_input_dialog)

        layout = QVBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(btn_update)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Checkbox Text Updater')
        self.show()

    def show_input_dialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter new text:')
        if ok:
            self.checkbox.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())
