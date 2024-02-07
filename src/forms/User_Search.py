from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy


class usersearchformUI(QWidget):
    def __init__(self, main_app):
        super(usersearchformUI, self).__init__(main_app)  # Pass main_app as the parent

        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "User Search"

            usersearch_layout = QGridLayout(self)

            usersearch_label = QLabel("Search for a User")
            font = usersearch_label.font()
            font.setPointSize(15)
            usersearch_label.setFont(font)
            usersearch_layout.addWidget(usersearch_label, 0, 0, 1, 1)

            self.usersearch_box = QLineEdit()
            self.usersearch_box.setPlaceholderText("Enter User Name or SSO")

            # Add a search icon to usersearch_box
            search_icon = QIcon.fromTheme("edit-find", QIcon('assets/material-icons/search_icon.png'))
            self.usersearch_box.addAction(search_icon, QLineEdit.ActionPosition.TrailingPosition)
            usersearch_layout.addWidget(self.usersearch_box, 1, 0, 1, 1)

            search_button = QPushButton("Search") # Row 1, Column 1, Span 1 row, 1 column
            usersearch_layout.addWidget(search_button, 1, 2, 1, 1)

            clear_button = QPushButton("Clear")
            clear_button.clicked.connect(self.clear_page)
            usersearch_layout.addWidget(clear_button, 1, 3, 1, 1)

            spacer_cell = QSpacerItem(300, 20)
            '''40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)'''
            usersearch_layout.addItem(spacer_cell, 1, 4, 1, 1)

            usersearch_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            tabindex = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")

    def clear_page(self):
        self.usersearch_box.clear()
