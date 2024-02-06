from import_modules import *

mapping = {  # Map plain text to match a function we will call as a new tab
    "newuserUI": newuserformUI,
    "usersearchUI": usersearchformUI,
    "pspromptUI": psformUI
}

class MainWindow(QMainWindow):  # Subclass QMainWindow for tool main window
    # Define main window and layout
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # List to store instances of open forms
        self.current_form_instances = []

        # Main container for the window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set window properties
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("SDS User Management Tool")
        self.setWindowIcon(QtGui.QIcon('assets/images/jake-head-icon.ico'))

        # Tab widget to hold multiple forms
        self.tabs = QTabWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.tabs)

        # Define the main tab that will be used
        self.tabs.setMovable(True)
        self.tabs.formsTab = QWidget()
        self.tabs.addTab(self.tabs.formsTab, "Tools")
        self.formsTabUI()

        # Add a context menu to the tabs bar
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

    # Define the individual tabs and their content
    def formsTabUI(self):
        layout = QVBoxLayout()

        # Label for available tools
        formslabel = QLabel("Available Tools:")
        font = formslabel.font()
        font.setPointSize(15)
        formslabel.setFont(font)
        formslabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(formslabel)

        # List widget for displaying available forms
        self.formselection = QListWidget()

        formnames = (os.listdir('forms'))
        for i in formnames:
            if i != "__pycache__" and i != "form_template.py":
                self.formselection.addItem(str(i).replace('.py', ''))

        # Double-click an item to open the form
        self.formselection.doubleClicked.connect(lambda: self.open_form(self.formselection.currentItem().text()))
        layout.addWidget(self.formselection)

        # Button to select and open a form
        selectButton = QPushButton("Select Form")
        # On clicking the select form button, send the selected text to open_form to handle opening the new tab
        selectButton.clicked.connect(lambda: self.open_form(self.formselection.currentItem().text()))
        layout.addWidget(selectButton)

        self.tabs.formsTab.setLayout(layout)

    def open_form(self, name):
        ui_name = name.lower() + "UI"
        form_call = mapping.get(str(ui_name))
        try:
            if form_call:
                # Store the instance in a list
                form_instance = form_call(self)
                self.current_form_instances.append(form_instance)
        except Exception as e:
            print(f"There was an error opening the form: {e}")

    def show_tab_context_menu(self, point):
        try:
            # Find the index of the tab at the right-clicked position
            index = self.tabs.tabBar().tabAt(point)

            # Only show the context menu if the right-clicked tab is not the 'Tools' tab
            if index > 0 and self.tabs.tabText(index) != "Tools":
                # Show a context menu when right-clicking on a tab
                context_menu = QMenu(self)
                close_tab_action = QAction("Close Tab", self)
                # Pass the index as data to the triggered signal
                close_tab_action.triggered.connect(lambda: self.close_tab(index))
                context_menu.addAction(close_tab_action)

                context_menu.exec(self.tabs.mapToGlobal(point))

        except Exception as e:
            print(f"Error showing tab context menu: {e}")

    def close_tab(self, index):
        try:
            # If index is not provided, get the currently selected tab index
            if index is None:
                index = self.tabs.currentIndex()

            if index >= 1:
                # Get the widget associated with the tab index
                widget = self.tabs.widget(index)
                if widget in self.current_form_instances:
                    # Remove the widget from the list
                    self.current_form_instances.remove(widget)

                # Remove the tab at the specified index
                self.tabs.removeTab(index)
        except Exception as e:
            print(f"Error when closing tab: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_app = MainWindow()
    main_app.show()

    sys.exit(app.exec())
