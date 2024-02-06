from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class newuserformUI:
    def __init__(self, main_app):
        ##print("Initializing newuserformUI")
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "New User"

            newuser_tab = QWidget()
            newuser_layout = QVBoxLayout(newuser_tab)

            newuser_label = QLabel("Create New User")
            font = newuser_label.font()
            font.setPointSize(15)
            newuser_label.setFont(font)
            newuser_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            newuser_layout.addWidget(newuser_label)

            tabindex = self.main_app.tabs.addTab(newuser_tab, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")