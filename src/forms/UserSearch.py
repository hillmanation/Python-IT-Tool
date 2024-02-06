from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QGridLayout

'''def usersearchformUI():
    title = "User Search"

    layout = QGridLayout()

    newuserLabel = QLabel("User Search")

    font = newuserLabel.font()
    font.setPointSize(15)
    newuserLabel.setFont(font)
    newuserLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    layout.addWidget(newuserLabel)



    return layout, title
'''


class usersearchformUI:
    def __init__(self, main_app):
        # print("Initializing usersearchformUI")
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "User Search"

            usersearch_tab = QWidget()
            usersearch_layout = QVBoxLayout(usersearch_tab)

            usersearch_label = QLabel("Search for a User")
            font = usersearch_label.font()
            font.setPointSize(15)
            usersearch_label.setFont(font)
            usersearch_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            usersearch_layout.addWidget(usersearch_label)

            tabindex = self.main_app.tabs.addTab(usersearch_tab, title)
            self.main_app.tabs.setCurrentIndex(tabindex)

        except Exception as e:
            print(f"The following error occurred: {e}")

