from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, QTabWidget, QFormLayout, QListWidget, \
    QHBoxLayout, QCheckBox, QSizePolicy


class CustomTabWidget(QTabWidget):
    def __init__(self, main_tabs):
        super(CustomTabWidget, self).__init__()

        self.main_tabs = main_tabs

        # Create a custom widget with a checkbox
        self.checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(self.checkbox_widget)
        self.checkbox = QCheckBox("Enable Editing")
        checkbox_layout.addWidget(self.checkbox)

        # Set size policy to expand horizontally and vertically
        self.checkbox_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Set a specific size for the checkbox widget
        self.checkbox_widget.setFixedSize(130, 40)
        # Add the custom widget to the top-right corner
        self.setCornerWidget(self.checkbox_widget, Qt.Corner.TopRightCorner)

        # Connect the signal to the slot for toggling edit mode
        self.checkbox.stateChanged.connect(self.toggle_edit_mode)

        # Keep track of tabs that should be affected by checkbox state
        self.editable_tabs = []
        # Dictionary to store initial text values of QLineEdit fields in each tab
        self.initial_text_values = {}
        # Dictionary to store current text values of QLineEdit fields in each tab
        self.current_text_values = {}

    def addEditableTab(self, tab, title, icon=None):
        tab_index = self.addTab(tab, title)
        self.editable_tabs.append(tab_index)

        # Set the tab icon if provided
        if icon:
            self.setTabIcon(tab_index, icon)

        return tab_index

    def toggle_edit_mode(self, state):
        # Enable or disable editing for each text field in editable tabs
        for tab_index in self.editable_tabs:
            tab_widget = self.widget(tab_index)
            for widget in tab_widget.findChildren(QLineEdit):
                widget.setReadOnly(not state)

            self.set_initial_values(tab_index, tab_widget)

    def set_initial_values(self, tab_index, tab_widget):
        # Store the initial text values of QLineEdit fields in this tab if not already defined
        if tab_index not in self.initial_text_values:
            initial_text_values = {}
            for widget in tab_widget.findChildren(QLineEdit):
                if widget.objectName():
                    initial_text_values[widget.objectName()] = widget.text()
            self.initial_text_values[tab_index] = initial_text_values

    def get_current_values(self, tab_index, main_tab_index, tab_widget):
        # Store the current text values of QLineEdit fields in this tab
        current_text_values = {}
        for widget in tab_widget.findChildren(QLineEdit):
            if widget.objectName():
                current_text_values[widget.objectName()] = widget.text()
        self.current_text_values[tab_index] = current_text_values

        # Check if the current values are different from the initial values
        if tab_index in self.initial_text_values and tab_index in self.current_text_values:
            if self.initial_text_values[tab_index] != self.current_text_values[tab_index]:
                # If they are different, add '*' to the main_app.tabs tab text
                tab_text = self.main_tabs.tabText(main_tab_index)
                if not tab_text.endswith('*'):
                    self.main_tabs.setTabText(main_tab_index, f"{tab_text}*")
            elif self.initial_text_values[tab_index] == self.current_text_values[tab_index] \
                    and self.main_tabs.tabText(main_tab_index).endswith('*'):
                self.main_tabs.setTabText(main_tab_index, f"{self.main_tabs.tabText(main_tab_index).replace('*', '')}")


class useraccountUI(QWidget):
    def __init__(self, main_app):
        super(useraccountUI, self).__init__(main_app)

        self.member_of_info = None
        self.main_app = main_app
        self.setup_ui()

    def setup_ui(self):
        user_detail_layout = QVBoxLayout(self)

        user_detail_tabs = CustomTabWidget(self.main_app.tabs)
        general_tab = QWidget()
        member_of_tab = QWidget()

        general_tab_index = user_detail_tabs.addEditableTab(general_tab, "General", QIcon('assets/material-icons/user_manage.png'))
        user_detail_tabs.addEditableTab(member_of_tab, "Groups", QIcon('assets/material-icons/user_group_icon.png'))

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
        member_of_layout = QHBoxLayout(member_of_tab)

        self.member_of_info = QListWidget()

        group_names = ["Group 1", "Group 2", "Group 3"]
        for i in group_names:
            self.member_of_info.addItem(str(i))

        member_of_layout.addWidget(self.member_of_info)

        # Add tabs to the main layout
        user_detail_layout.addWidget(user_detail_tabs)
        user_detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        tab_index = self.main_app.tabs.addTab(self, full_name.text())
        full_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        logon_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        first_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        last_name.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        description.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        email.textChanged.connect(
            lambda text: user_detail_tabs.get_current_values(general_tab_index, tab_index, general_tab))
        self.main_app.tabs.setTabIcon(tab_index, QIcon('assets/material-icons/user_icon.png'))
        self.main_app.tabs.setCurrentIndex(tab_index)
