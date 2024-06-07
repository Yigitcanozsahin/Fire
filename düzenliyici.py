from PyQt6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QApplication, QVBoxLayout, QPushButton, QWidget
import sys
from PyQt6.QtGui import QAction



class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Code Editor')
        self.setGeometry(100, 100, 800, 600)

        # Metin düzenleyiciyi oluştur
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Dosya menüsü oluştur
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Dosya menüsü eylemleri
        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save &As', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        # Butonlar
        button_layout = QVBoxLayout()

        run_button = QPushButton('Run')
        run_button.clicked.connect(self.run_code)
        button_layout.addWidget(run_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Python Files (*.py);;Text Files (*.txt);;All Files (*.*)')
        if file_name:
            with open(file_name, 'r') as file:
                self.text_edit.setPlainText(file.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Python Files (*.py);;Text Files (*.txt);;All Files (*.*)')
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save As', '', 'Python Files (*.py);;Text Files (*.txt);;All Files (*.*)')
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def run_code(self):
        # Burada, kodu çalıştırmak için terminal kısmındaki kodunuzu çağırabilirsiniz
        pass


def main():
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
