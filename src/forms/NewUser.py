from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class newuserformUI(QWidget):  # Inherit from QWidget
    def __init__(self, main_app):
        super(newuserformUI, self).__init__(main_app)  # Pass main_app as the parent
        self.main_app = main_app
        self.setup_ui()

    def setup_ui(self):
        try:
            title = "New User"

            newuser_layout = QVBoxLayout(self)  # Set layout for self (which is a QWidget)

            newuser_label = QLabel("Create New User")
            font = newuser_label.font()
            font.setPointSize(15)
            newuser_label.setFont(font)
            newuser_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            newuser_layout.addWidget(newuser_label)

            tabindex = self.main_app.tabs.addTab(self, title)  # Add self to tabs instead of newuser_tab
            self.main_app.tabs.setCurrentIndex(tabindex)
        except Exception as e:
            print(f"The following error occurred: {e}")
