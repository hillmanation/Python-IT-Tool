from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import src.assets.resources
from PyQt6.QtWidgets import QLineEdit, QSizePolicy


class ClearableSearchBar(QLineEdit):
    def __init__(self, parent=None, text="Search..."):
        super(ClearableSearchBar, self).__init__(parent)

        self.setPlaceholderText(text)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Add a search icon to search bar
        self.search_icon = QIcon.fromTheme("edit-find", QIcon(':/material-icons/search_icon.png'))
        self.clear_icon = QIcon.fromTheme("edit-find", QIcon(':/material-icons/cancel_search.png'))

        # Connect signals
        self.textChanged.connect(self.update_clear_button_visibility)
        self.addAction(self.search_icon, QLineEdit.ActionPosition.TrailingPosition).triggered.connect(self.clear_search)

    def update_clear_button_visibility(self):
        if not self.text():
            self.actions()[0].setIcon(self.search_icon)
        else:
            self.actions()[0].setIcon(self.clear_icon)

    def clear_search(self):
        self.clear()
