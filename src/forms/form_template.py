from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class templateUI(QWidget):
    def __init__(self, main_app):
        super(templateUI, self).__init__(main_app)  # Pass main_app as the parent
        ##print("Initializing templateUI")
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "Template"

            template_layout = QVBoxLayout(self)

            template_label = QLabel("Template")
            font = template_label.font()
            font.setPointSize(15)
            template_label.setFont(font)
            template_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            template_layout.addWidget(template_label)

            tabindex = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")