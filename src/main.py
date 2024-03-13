from src.import_modules import *


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):  # Subclass QMainWindow for tool main window
    # Define the paths as class variables
    APPDATA_LOCAL_PATH = os.path.join(os.environ['LOCALAPPDATA'])
    CONFIG_JSON_PATH = os.path.join(APPDATA_LOCAL_PATH, 'sds_tool_config.json')
    DOMAIN_NAME = None
    RUNNING_USER = None
    FAVORITES = []

    # Define main window and layout
    def __init__(self, parent=None):
        self.favorites_tree = None
        self.favorite_forms = None
        self.select_button = None
        self.form_selection = None
        self.tabs = QTabWidget()
        super(MainWindow, self).__init__(parent)

        # List to store instances of open forms
        self.current_form_instances = []

        # Main container for the window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set window properties
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("SDS User Management Tool")
        self.setWindowIcon(QtGui.QIcon(':/images/GE-Monogram.ico'))

        # Tab widget to hold multiple forms
        self.tabs.setStyleSheet("QTabWidget::pane { border-bottom-left-radius: 5px; border-bottom-right-radius: "
                                "5px; background-color: #4B4B4B}")
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.tabs)

        # Let's grab the domain this is being run on
        self.config_update()

        # Define the main tab that will be used
        self.tabs.setMovable(True)
        self.tabs.formsTab = QWidget()
        tab_index = self.tabs.addTab(self.tabs.formsTab, "Tools")
        self.tabs.setTabIcon(tab_index, QIcon(':/images/jake-head.png'))
        self.formsTabUI()

        # Now load the saved tab instances from the previous session if they exist
        self.load_app_state()

        # Add a context menu to the tabs bar
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

        # Install event filter
        self.installEventFilter(self)

    # Define the individual tabs and their content
    def formsTabUI(self):
        layout = QGridLayout()

        # Label for available tools
        forms_label = QLabel("Available Tools")
        font = forms_label.font()
        font.setPointSize(15)
        forms_label.setFont(font)
        forms_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(forms_label, 0, 0, 1, 4)  # Row 0, Column 0, Span 1 row, 1 column

        # Domain Label
        current_domain = QLabel(f"Domain: {self.DOMAIN_NAME}")
        current_domain.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(current_domain, 0, 4, 1, 1)

        # User Label
        current_user = QLabel(f"User: {self.RUNNING_USER}")
        current_user.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(current_user, 0, 5, 1, 1)

        # Date Label
        today = datetime.today().date()
        formatted_date = today.strftime("%m/%d/%Y")
        current_date = QLabel(f"Date: {formatted_date}")
        current_date.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(current_date, 0, 6, 1, 1)

        # List widget for displaying available forms
        self.form_selection = WatermarkTableWidget()

        # Add a context menu to the tabs bar
        self.form_selection.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.form_selection.customContextMenuRequested.connect(self.show_list_context_menu)

        # Populate the list widget
        self.populate_form_list()

        # Double-click an item to open the form
        # ^TODO: Why does this have to be held down on the second click to get the tooltip to display for the full time?
        self.form_selection.itemDoubleClicked.connect(
            lambda: self.open_form(self.form_selection.item(self.form_selection.currentRow(), 0).text()))
        self.form_selection.itemClicked.connect(self.enable_select_button)
        layout.addWidget(self.form_selection, 1, 0, 1, 7)

        # Button to select and open a form
        self.select_button = QPushButton("Select Form")
        self.select_button.setEnabled(False)
        # On clicking the select form button, send the selected text to open_form to handle opening the new tab
        self.select_button.clicked.connect(
            lambda: self.open_form(self.form_selection.item(self.form_selection.currentRow(), 0).text()))
        layout.addWidget(self.select_button, 2, 0, 1, 7)

        self.tabs.formsTab.setLayout(layout)

    def keyPressEvent(self, event):  # Capture Key Press Events to define some shortcuts
        try:
            # When 'ctrl+h' is pressed change the active tab to 'Tools'
            if event.key() == Qt.Key.Key_H and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self.tabs.setCurrentIndex(self.tabs.indexOf(self.tabs.formsTab))
            elif event.key() == Qt.Key.Key_N and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # If Ctrl+N is pressed, open a New User page
                self.open_form("New User")

            super(MainWindow, self).keyPressEvent(event)
        except Exception as e:
            print(f"That didn't work: {e}")

    # noinspection PyArgumentList
    def open_form(self, name=None, args=None):
        if name is not None and self.tabs.count() > 9:
            try:
                # Display a tooltip near the mouse cursor
                mouse_pos = QCursor.pos()
                self.show_tooltip("Max Number of Tabs Open!", mouse_pos, 2000)
            except Exception as e:
                print(f"There was an error displaying the tooltip: {e}")
        elif name is not None and name.replace('*  ', '') in mapping.keys():
            try:
                # Find the matching form instance in the 'mapping' tree
                form_info = mapping.get(name.replace('*  ', ''), {})
                form_call = form_info.get("function")
                if form_call:
                    if args is not None:  # If the form is being called with arguments, pass them to the form
                        form_instance = form_call(self, args)
                    else:
                        form_instance = form_call(self)
                    # Store the instance in a list
                    self.current_form_instances.append(form_instance)
            except Exception as e:
                print(f"There was an error opening the form: {e}")

    def enable_select_button(self):  # Enable the select button if an item becomes selected in form_selection
        self.select_button.setEnabled(True)

    def show_tooltip(self, text, pos, duration):
        QToolTip.showText(pos, text)
        timer = QTimer(self)
        timer.timeout.connect(QToolTip.hideText)
        timer.start(duration)

    def show_list_context_menu(self, point):
        # Get the currently selected item in form_selection
        current_row = self.form_selection.currentRow()

        if current_row >= 0:  # Check if any item is selected
            item = self.form_selection.item(self.form_selection.currentRow(), 0).text()
            list_context_menu = QMenu(self)

            # Add open_form action
            open_form_action = QAction("Open Form", self)
            # Pass the item to the open_form function
            open_form_action.triggered.connect(lambda: self.open_form(str(item).replace('*  ', '')))
            list_context_menu.addAction(open_form_action)

            # Seperator
            separator_action = QAction(self)
            separator_action.setSeparator(True)
            list_context_menu.addAction(separator_action)

            if self.FAVORITES is not None and str(item).replace('*  ', '') not in self.FAVORITES:
                # Add favorite action
                add_favorite_action = QAction("Add to Favorites", self)
                # Pass the item to the add_favorite function
                add_favorite_action.triggered.connect(lambda: self.add_favorite(item))
                list_context_menu.addAction(add_favorite_action)
            else:
                # Add favorite action
                remove_favorite_action = QAction("Remove from Favorites", self)
                # Pass the item to the add_favorite function
                remove_favorite_action.triggered.connect(lambda: self.remove_favorite(str(item).replace('*  ', '')))
                list_context_menu.addAction(remove_favorite_action)

            list_context_menu.exec(self.form_selection.mapToGlobal(point))

    def show_tab_context_menu(self, point):
        try:
            # Find the index of the tab at the right-clicked position
            index = self.tabs.tabBar().tabAt(point)

            # Only show the context menu if the right-clicked tab is not the 'Tools' tab
            if index >= 0 and self.tabs.tabText(index) != "Tools":
                # Show a context menu when right-clicking on a tab
                tab_context_menu = QMenu(self)

                # Close Tab action
                close_tab_action = QAction("Close Tab", self)
                # Pass the index as data to the triggered signal
                close_tab_action.triggered.connect(lambda: self.close_tab(index))
                tab_context_menu.addAction(close_tab_action)

                # Duplicate Tab action
                duplicate_tab_action = QAction("Duplicate Tab", self)
                # Pass the index as data to the triggered signal
                duplicate_tab_action.triggered.connect(lambda: self.duplicate_tab(index))
                tab_context_menu.addAction(duplicate_tab_action)

                # Seperator
                separator_action = QAction(self)
                separator_action.setSeparator(True)
                tab_context_menu.addAction(separator_action)

                if self.FAVORITES is not None and self.tabs.tabText(index) not in self.FAVORITES:
                    # Add favorite action
                    add_favorite_action = QAction("Add to Favorites", self)
                    # Pass the item to the add_favorite function
                    add_favorite_action.triggered.connect(lambda: self.add_favorite(self.tabs.tabText(index)))
                    tab_context_menu.addAction(add_favorite_action)
                else:
                    # Add favorite action
                    remove_favorite_action = QAction("Remove from Favorites", self)
                    # Pass the item to the add_favorite function
                    remove_favorite_action.triggered.connect(lambda: self.remove_favorite(self.tabs.tabText(index)))
                    tab_context_menu.addAction(remove_favorite_action)

                tab_context_menu.exec(self.tabs.mapToGlobal(point))
            elif index >= 0 and self.tabs.tabText(index) == "Tools":
                # Show a context menu when right-clicking on a tab
                tab_context_menu = QMenu(self)

                # Close all other tabs action
                if self.tabs.count() > 1:
                    close_all_tabs_action = QAction("Close All Tabs", self)
                    close_all_tabs_action.triggered.connect(lambda: self.close_all_tabs(index))
                    tab_context_menu.addAction(close_all_tabs_action)

                # Seperator
                separator_action = QAction(self)
                separator_action.setSeparator(True)
                tab_context_menu.addAction(separator_action)

                # About Info pop-up
                about_info_action = QAction("About", self)
                about_info_action.triggered.connect(self.open_about_info)
                tab_context_menu.addAction(about_info_action)

                tab_context_menu.exec(self.tabs.mapToGlobal(point))
        except Exception as e:
            print(f"Error showing tab context menu: {e}")

    def open_about_info(self):
        PopupWindow = AboutPopupWindow(self)
        PopupWindow.exec()

    def close_tab(self, index):
        try:
            # If index is not provided, get the currently selected tab index
            if index is None:
                index = self.tabs.currentIndex()

            if self.tabs.tabText(index) != "Tools":
                # Get the widget associated with the tab index
                widget = self.tabs.widget(index)
                if widget in self.current_form_instances:
                    # Remove the widget from the list
                    self.current_form_instances.remove(widget)

                # Remove the tab at the specified index
                self.tabs.removeTab(index)
        except Exception as e:
            print(f"Error when closing tab: {e}")

    def close_all_tabs(self, index):
        try:
            if self.tabs.tabText(index) == "Tools":
                # Get the total number of tabs
                total_tabs = self.tabs.count()

                # Iterate through all tabs (excluding the "Tools" tab)
                for i in range(total_tabs - 1, -1, -1):
                    if i != index:
                        # Get the widget associated with the tab index
                        widget = self.tabs.widget(i)
                        if widget in self.current_form_instances:
                            # Remove the widget from the list
                            self.current_form_instances.remove(widget)
                            # Remove the tab at the specified index
                            self.tabs.removeTab(i)
        except Exception as e:
            print(f"Error when closing all tabs: {e}")

    def duplicate_tab(self, index):
        try:
            # Get the widget associated with the tab index
            tab_name = self.tabs.tabText(index)
            self.open_form(tab_name)
        except Exception as e:
            print(f"Error when duplicating tab: {e}")

    def config_update(self):  # Make sure the domain is in the config file since we rely on that to speed up some logic
        try:
            # Open the existing JSON config file or create an empty dictionary if it doesn't exist
            with open(self.CONFIG_JSON_PATH, 'r') as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            config_data = {}

        # Check if "domain_name" key exists in config_data
        if "domain_name" not in config_data or config_data["domain_name"] is None:
            self.DOMAIN_NAME = str(PSquery("$env:UserDomain"), 'utf-8').strip()

            # Save the Domain Name to the config file
            config_data["domain_name"] = self.DOMAIN_NAME
            with open(self.CONFIG_JSON_PATH, 'w') as config_file:
                json.dump(config_data, config_file, indent=2)
        else:
            self.DOMAIN_NAME = config_data["domain_name"]

        # Check if "user_name" key exists in config_data
        if "user_name" not in config_data or config_data["user_name"] is None:
            self.RUNNING_USER = str(PSquery("$env:UserName"), 'utf-8').strip()

            # Save the username to the config file
            config_data["user_name"] = self.RUNNING_USER
            with open(self.CONFIG_JSON_PATH, 'w') as config_file:
                json.dump(config_data, config_file, indent=2)
        else:
            self.RUNNING_USER = config_data["user_name"]

        if "favorites" in config_data and config_data["favorites"] is not None:
            for favorite in config_data["favorites"]:
                self.FAVORITES.append(favorite)

    def closeEvent(self, event):
        # Save tab state to the configuration file when the application is closed
        self.save_app_state()
        event.accept()

    def populate_form_list(self):
        # Clear the form_selection list to repopulate it with the sorted favorites/non-favorites
        self.form_selection.clear()
        # Reset the row count
        self.form_selection.setRowCount(0)
        # Sort the list of form names
        all_form_names = sorted(mapping.keys())
        # Check for the global favorites variable
        if self.FAVORITES != "":
            favorites = self.FAVORITES
        else:
            favorites = None

        sorted_non_favorites = []
        sorted_favorites = []
        # Sort through the form names and separate out the favorites in a pre-sorted list
        for name in all_form_names:
            if name in favorites:
                sorted_favorites.append(f"*  {name}")
            else:
                sorted_non_favorites.append(name)

        sorted_form_names = []
        # Populate the full list with the favorite items on top
        for name in sorted_favorites:
            sorted_form_names.append(name)
        for name in sorted_non_favorites:
            sorted_form_names.append(name)

        # Add the available forms by pulling their names from mapping
        for row, form_name in enumerate(sorted_form_names):
            self.form_selection.insertRow(row)
            key_item = QTableWidgetItem(form_name)
            description_item = QTableWidgetItem(mapping[form_name.replace('*  ', '')]["description"])
            self.form_selection.setItem(row, 0, key_item)
            font = description_item.font()
            font.setItalic(True)
            description_item.setFont(font)
            description_item.setForeground(QColor(255, 255, 255, 96))
            self.form_selection.setItem(row, 1, description_item)

    def add_favorite(self, name):
        if name not in self.FAVORITES:
            self.FAVORITES.append(name)
            self.populate_form_list()
            self.manage_favorites(self.FAVORITES)

    def remove_favorite(self, name):
        try:
            if self.FAVORITES is not None and name in self.FAVORITES:
                self.FAVORITES.remove(name)
                self.populate_form_list()
                self.manage_favorites(self.FAVORITES)
        except Exception as e:
            print(f"Unable to remove: {e}")

    def manage_favorites(self, current_favorites=None):
        try:
            # Open the existing JSON config file or create an empty dictionary if it doesn't exist
            with open(self.CONFIG_JSON_PATH, 'r') as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            config_data = {}

        if current_favorites is not None:
            config_data["favorites"] = current_favorites

        # Save the updated information to the JSON file
        with open(self.CONFIG_JSON_PATH, 'w') as config_file:
            json.dump(config_data, config_file, indent=2)

    def save_app_state(self):
        # Get the currently open tabs
        open_tabs_info = []
        for index in range(self.tabs.count()):
            tab_title = self.tabs.tabText(index)
            if tab_title != "Tools" and tab_title in mapping:
                open_tabs_info.append(tab_title)

        try:
            # Open the existing JSON config file or create an empty dictionary if it doesn't exist
            with open(self.CONFIG_JSON_PATH, 'r') as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            config_data = {}

        # Update the "tabs" field with the information of open tabs
        config_data["tabs"] = open_tabs_info

        # Save the updated information to the JSON file
        with open(self.CONFIG_JSON_PATH, 'w') as config_file:
            json.dump(config_data, config_file, indent=2)

    def load_app_state(self):
        # Load tab state from the JSON file
        try:
            with open(self.CONFIG_JSON_PATH, 'r') as config_file:
                config_data = json.load(config_file)

            # Create tabs based on the loaded information
            # Check if "domain_name" key exists in config_data
            if "tabs" in config_data and config_data["tabs"] is not None:
                for tab_name in config_data["tabs"]:
                    self.open_form(tab_name)

            # Set the tab index back to '0' (The Forms Tab)
            self.tabs.setCurrentIndex(0)

        except FileNotFoundError:
            pass  # The file might not exist on the first run


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    loading_dialog = AppLoadingDialog()
    app.processEvents()
    loading_dialog.show()
    app.processEvents()
    main_app = MainWindow()
    app.processEvents()
    main_app.show()
    loading_dialog.accept()

    sys.exit(app.exec())
