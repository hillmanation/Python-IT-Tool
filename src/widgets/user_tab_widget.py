from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QCheckBox, QSizePolicy, QLineEdit


class UserTabWidget(QTabWidget):
    def __init__(self, main_tabs):
        super(UserTabWidget, self).__init__()

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
