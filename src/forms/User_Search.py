import datetime
import src.assets.resources
from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
import PyQt6.QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QWidget
from src.widgets.clearable_search_bar import ClearableSearchBar


# noinspection PyUnresolvedReferences
class usersearchform_ui(QWidget):
    def __init__(self, main_app):
        super(usersearchform_ui, self).__init__(main_app)  # Pass main_app as the parent

        self.results_box = None
        self.usersearch_box = None
        try:
            self.main_app = main_app
            self.setup_ui()
        except Exception as e:
            print(f"An error occurred: {e}")

    def setup_ui(self):
        try:
            title = "User Search"

            usersearch_layout = PyQt6.QtWidgets.QGridLayout(self)

            usersearch_label = PyQt6.QtWidgets.QLabel("Search for a User")
            font = usersearch_label.font()
            font.setPointSize(15)
            usersearch_label.setFont(font)
            usersearch_layout.addWidget(usersearch_label, 0, 0, 1, 1)

            self.usersearch_box = ClearableSearchBar(self, "Enter User Name or SSO")
            self.usersearch_box.returnPressed.connect(self.sample_user_find)
            usersearch_layout.addWidget(self.usersearch_box, 1, 0, 1, 1)

            search_button = PyQt6.QtWidgets.QPushButton("Search") # Row 1, Column 1, Span 1 row, 1 column
            search_button.clicked.connect(self.sample_user_find)
            usersearch_layout.addWidget(search_button, 1, 2, 1, 1)

            clear_button = PyQt6.QtWidgets.QPushButton("Clear")
            clear_button.clicked.connect(self.clear_page)
            usersearch_layout.addWidget(clear_button, 1, 3, 1, 1)

            spacer_cell = PyQt6.QtWidgets.QSpacerItem(300, 20)
            '''40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)'''
            usersearch_layout.addItem(spacer_cell, 1, 4, 1, 1)

            # Set Header names for the results_box
            header_names = ["Name", "SSO", "OU", "Enabled", "Locked?", "Expiration", "Annual Training"]

            self.results_box = PyQt6.QtWidgets.QTableWidget(2, 7, self)
            self.results_box.setAlternatingRowColors(True)
            self.results_box.horizontalHeader().setSectionResizeMode(PyQt6.QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.results_box.verticalHeader().setSectionResizeMode(PyQt6.QtWidgets.QHeaderView.ResizeMode.
                                                                   ResizeToContents)
            self.results_box.setSelectionBehavior(PyQt6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
            self.results_box.setEditTriggers(PyQt6.QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
            self.results_box.itemDoubleClicked.connect(self.results_item_dclicked)
            self.results_box.setHorizontalHeaderLabels(header_names)
            usersearch_layout.addWidget(self.results_box, 2, 0, 1, 5)

            usersearch_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            tab_index = self.main_app.tabs.addTab(self, title)
            self.main_app.tabs.setTabIcon(tab_index, QIcon(':/material-icons/user_search.png'))
            self.main_app.tabs.setCurrentIndex(tab_index)

        except Exception as e:
            print(f"The following error occurred: {e}")

    def clear_page(self):
        self.usersearch_box.clear()
        self.results_box.clearContents()
        self.results_box.setRowCount(0)

    '''def sample_user_find(self):
        search = self.usersearch_box.text()

        if search != "":
            results = PSquery(f"cmd.exe /c net user {search}")
            utf_convert = results.decode('utf-8')
            print(utf_convert)
            self.usersearch_box.clear()'''

    def results_item_dclicked(self):
        selected_row = self.results_box.currentRow()

        '''if selected_row >= 0:
            row_data = []
            for column in range(self.results_box.columnCount()):
                item = self.results_box.item(selected_row, column)
                if item is not None:
                    row_data.append(item.text())

            print(row_data)'''

        if selected_row >= 0:
            sso = self.results_box.item(selected_row, 1).text()
            self.main_app.open_form("User Account")

    def sample_user_find(self):
        search = self.usersearch_box.text()

        if search != "":
            # This is a placeholder for your actual search results
            # Replace this with your logic to retrieve and process the results

            # Test data
            test_data = [  # Test data for results_box
                {"Name": "Doe, John", "SSO": "123456789", "OU": "IT", "Enabled": True, "Locked": False,
                 "Expiration": "2024-12-31", "Annual Training": True},
                {"Name": "Smith, Jane", "SSO": "987654321", "OU": "HR", "Enabled": True, "Locked": True,
                 "Expiration": "2023-10-15", "Annual Training": False},
                {"Name": "Brown, Alex", "SSO": "555666777", "OU": "Finance", "Enabled": False, "Locked": False,
                 "Expiration": "2025-06-22", "Annual Training": True},
                {"Name": "Taylor, Emily", "SSO": "111222333", "OU": "Marketing", "Enabled": True, "Locked": True,
                 "Expiration": "2023-08-05", "Annual Training": False},
                {"Name": "Clark, Michael", "SSO": "444555666", "OU": "Sales", "Enabled": True, "Locked": False,
                 "Expiration": "2024-04-18", "Annual Training": True}
            ]

            self.results_box.setRowCount(0)  # Clear all existing rows

            try:
                for row_data in test_data:
                    self.results_box.insertRow(0)
                    for col, (key, value) in enumerate(row_data.items()):
                        item = QTableWidgetItem(str(value))
                        if col == 5:  # Assuming 'Expiration' is in the 6th column
                            item.setData(0, datetime.datetime.strptime(value, "%Y-%m-%d"))
                        self.results_box.setItem(0, col, item)
            except Exception as e:
                print(f"The following error occurred: {e}")

    def open_user(self, SSO):
        ui_name = name.lower()  # Force lowercase form name
        # form_call = self.main_app.mapping.get(str(ui_name))  # Find the matching form instance in the 'mapping' tree
        try:
            if form_call:
                # Store the instance in a list
                form_instance = form_call(self)
                self.main_app.current_form_instances.append(form_instance)
        except Exception as e:
            print(f"There was an error opening the form: {e}")