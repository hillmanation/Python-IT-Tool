from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class templateUI:
    def __init__(self, main_app):
        ##print("Initializing templateUI")
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "Template"

            template_tab = QWidget()
            template_layout = QVBoxLayout(template_tab)

            template_label = QLabel("Template")
            font = template_label.font()
            font.setPointSize(15)
            template_label.setFont(font)
            template_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            template_layout.addWidget(template_label)

            tabindex = self.main_app.tabs.addTab(template_tab, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")
