import src.assets.resources
from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from src.widgets.clearable_search_bar import ClearableSearchBar
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QTabWidget, QFormLayout, QListWidget, \
    QHBoxLayout, QCheckBox, QSizePolicy, QTableWidget, QPushButton, QStyle, QLayout, QGridLayout
from src.widgets.user_tab_widget import UserTabWidget


# noinspection PyUnresolvedReferences
class useraccount_ui(QWidget):
    def __init__(self, main_app):
        super(useraccount_ui, self).__init__(main_app)

        self.attribute_search_button = None
        self.attribute_layout = None
        self.attribute_search_box = None
        self.user_attributes = None
        self.member_of_info = None
        self.main_app = main_app
        self.setup_ui()

    def setup_ui(self):
        user_detail_layout = QVBoxLayout(self)

        user_detail_tabs = UserTabWidget(self.main_app.tabs)
        general_tab = QWidget()
        member_of_tab = QWidget()
        attribute_tab = QWidget()

        general_tab_index = user_detail_tabs.addEditableTab(general_tab, "General",
                                                            QIcon(':/material-icons/user_manage.png'))
        user_detail_tabs.addEditableTab(member_of_tab, "Groups", QIcon(':/material-icons/user_group_icon.png'))
        user_detail_tabs.addEditableTab(attribute_tab, "Attributes", QIcon(':/material-icons/user_attributes.png'))

        # Apply rounded corners to the bottom corners of QTabWidget
        user_detail_tabs.setStyleSheet(
            "QTabWidget::pane { border: 1.5px solid #1E1E1E; border-bottom-left-radius: "
            "5px; border-bottom-right-radius: 5px; }"
        )

        # General Tab
        general_layout = QFormLayout(general_tab)

        full_name = QLineEdit("John Doe")
        full_name.setReadOnly(True)
        full_name.setObjectName("full_name")
        logon_name = QLineEdit("johndoe")
        logon_name.setReadOnly(True)
        logon_name.setObjectName("logon_name")
        first_name = QLineEdit("John")
        first_name.setReadOnly(True)
        first_name.setObjectName("first_name")
        last_name = QLineEdit("Doe")
        last_name.setReadOnly(True)
        last_name.setObjectName("last_name")
        description = QLineEdit("Test User John Doe")
        description.setReadOnly(True)
        description.setObjectName("description")
        email = QLineEdit("john.doe@example.com")
        email.setReadOnly(True)
        email.setObjectName("email")

        general_layout.addRow(QLabel("Full Name:"), full_name)
        general_layout.addRow(QLabel("Logon Name:"), logon_name)
        general_layout.addRow(QLabel("First Name:"), first_name)
        general_layout.addRow(QLabel("Last Name:"), last_name)
        general_layout.addRow(QLabel("Description:"), description)
        general_layout.addRow(QLabel("Email:"), email)

        # Member Of Tab
        member_of_layout = QVBoxLayout(member_of_tab)

        self.member_of_info = QListWidget()

        group_names = ["Group 1", "Group 2", "Group 3"]
        for i in group_names:
            self.member_of_info.addItem(str(i))

        member_of_layout.addWidget(self.member_of_info)
        
        # Attribute Editor Tab
        self.attribute_layout = QGridLayout(attribute_tab)

        # Create a search bar to filter user attributes
        self.attribute_search_box = ClearableSearchBar(self, "Search for an Attribute...")
        self.attribute_layout.addWidget(self.attribute_search_box, 0, 0, 1, 1)

        # Search button
        self.attribute_search_button = QPushButton("Search")
        self.attribute_layout.addWidget(self.attribute_search_button, 0, 1, 1, 1)

        # Define the QTableWidget to hold user attributes
        self.user_attributes = QTableWidget()
        self.attribute_layout.addWidget(self.user_attributes, 1, 0, 1, 2)

        # Add tabs to the main layout
        user_detail_layout.addWidget(user_detail_tabs)
        user_detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        tab_name = full_name.text()

        tab_index = self.main_app.tabs.addTab(self, tab_name)
        self.main_app.tabs.setTabIcon(tab_index, QIcon(':/material-icons/user_icon.png'))
        self.main_app.tabs.setCurrentIndex(tab_index)
        full_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
        logon_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
        first_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
        last_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
        description.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
        email.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, self.main_app.tabs.indexOf(self),
                                                             general_tab))
