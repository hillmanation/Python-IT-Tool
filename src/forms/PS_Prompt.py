import subprocess
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit, QPlainTextEdit


class CustomOutputBox(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: white; background-color: MidnightBlue")
    def appendPlainTextNoScroll(self, text):
        # Save the current scrollbar value
        scrollbar = self.verticalScrollBar()
        scroll_position = scrollbar.value()

        # Append the text
        self.appendPlainText(text)

        # Restore the scrollbar value
        scrollbar.setValue(scroll_position)


class PowershellStylePrompt(QPlainTextEdit):
    enterKeyPressed = pyqtSignal()

    def keyPressEvent(self, event):
        try:
            if event.key() in {Qt.Key.Key_Return, Qt.Key.Key_Enter}:
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    cursor = self.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfBlock)
                    cursor.insertBlock()
                else:
                    self.enterKeyPressed.emit()
            else:
                super().keyPressEvent(event)
        except Exception as e:
            print(f"Key press error: {e}")

    def setPlainText(self, text):
        self.clear()
        self.insertPlainText(text)


class psformUI(QWidget):

    def __init__(self, main_app):
        super(psformUI, self).__init__(main_app)  # Pass main_app as the parent
        self.output_box = None
        self.command_input = None
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "Powershell Console"

            psform_layout = QVBoxLayout(self)

            newuser_label = QLabel("Powershell Prompt")
            font = newuser_label.font()
            font.setPointSize(15)
            newuser_label.setFont(font)
            newuser_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            psform_layout.addWidget(newuser_label)

            self.command_input = PowershellStylePrompt()
            self.command_input.enterKeyPressed.connect(self.runPS)
            psform_layout.addWidget(self.command_input)

            self.output_box = CustomOutputBox()
            self.output_box.setReadOnly(True)
            self.output_box.setFont(QFont("Lucida Console"))
            self.output_box.resize(QSize(400, 580))
            psform_layout.addWidget(self.output_box)

            get_button = QPushButton("Enter")
            get_button.clicked.connect(self.runPS)
            psform_layout.addWidget(get_button)

            tabindex = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setCurrentIndex(tabindex)
        except Exception as e:
            print(f"An error occurred during UI setup: {e}")

    def runPS(self):
        # print("Running PS command")
        try:
            cmd = self.command_input.toPlainText()
            # print(cmd)
            self.command_input.clear()
            completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            output = str(completed.stdout, 'utf-8')
            # print(f"Prompt> {cmd}")
            self.output_box.clear()
            self.output_box.appendPlainText(f"PS> {cmd}")
            self.output_box.appendPlainTextNoScroll(output)
        except Exception as e:
            print(f"There was an issue with {e}")