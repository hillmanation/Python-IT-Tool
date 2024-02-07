from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout


class usersearchformUI(QWidget):
    def __init__(self, main_app):
        super(usersearchformUI, self).__init__(main_app)  # Pass main_app as the parent
        # print("Initializing usersearchformUI")
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "User Search"

            usersearch_layout = QVBoxLayout(self)

            usersearch_label = QLabel("Search for a User")
            font = usersearch_label.font()
            font.setPointSize(15)
            usersearch_label.setFont(font)
            usersearch_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            usersearch_layout.addWidget(usersearch_label)

            tabindex = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")

