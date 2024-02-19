import subprocess
import src.assets.resources
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit, QPlainTextEdit
from src.widgets.powershell_classes import PSStyleOutput, PowershellStylePrompt


class psform_ui(QWidget):

    def __init__(self, main_app):
        super(psform_ui, self).__init__(main_app)  # Pass main_app as the parent
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

            self.output_box = PSStyleOutput()
            self.output_box.setReadOnly(True)
            self.output_box.setFont(QFont("Lucida Console"))
            self.output_box.resize(QSize(400, 580))
            psform_layout.addWidget(self.output_box)

            get_button = QPushButton("Enter")
            get_button.clicked.connect(self.runPS)
            psform_layout.addWidget(get_button)

            tab_index = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setTabIcon(tab_index, QIcon(':/material-icons/ps_icon.png'))
            self.main_app.tabs.setCurrentIndex(tab_index)
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