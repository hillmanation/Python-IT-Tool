import datetime, secrets, time, string
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator, QIcon, QCursor
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QLineEdit, QCheckBox, QPushButton, QApplication, QToolTip
from User_Management.functions.ps import PSquery


class newuserformUI(QWidget):  # Inherit from QWidget
    def __init__(self, main_app):
        super(newuserformUI, self).__init__(main_app)  # Pass main_app as the parent
        self.reveal_checkbox = None
        self.temp_password = None
        self.roulette_button = None
        self.edit_account_names = None
        self.account_names = None
        self.ISSO_check = None
        self.DTA_check = None
        self.AUD_check = None
        self.ADM_check = None
        self.zz_check = None
        self.User_check = None
        self.SSO_input = None
        self.edit_full_name = None
        self.full_name = None
        self.last_name = None
        self.first_name = None
        self.main_app = main_app
        self.setup_ui()

    def setup_ui(self):
        try:
            title = "New User"

            newuser_layout = QGridLayout(self)  # Set layout for self (which is a QWidget)

            newuser_label = QLabel("Create New User")
            font = newuser_label.font()
            font.setPointSize(15)
            newuser_label.setFont(font)
            newuser_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            newuser_layout.addWidget(newuser_label, 0, 0, 1, 1) # Row 0, Column 0, Span 1 row, 1 column

            # User entered name values
            self.first_name = QLineEdit()
            self.first_name.setPlaceholderText("Enter User First Name")
            self.first_name.textChanged.connect(self.set_full_name)  # Connect to the full_name generator
            newuser_layout.addWidget(self.first_name, 1, 0, 1, 1)

            self.last_name = QLineEdit()
            self.last_name.setPlaceholderText("Enter User Last Name")
            self.last_name.textChanged.connect(self.set_full_name)  # Connect to the full_name generator
            newuser_layout.addWidget(self.last_name, 1, 1, 1, 5)

            # Full name field generated by the above boxes by default
            self.full_name = QLineEdit()
            self.full_name.setReadOnly(True)
            self.full_name.setPlaceholderText("Full Name will autogenerate here")
            newuser_layout.addWidget(self.full_name, 2, 0, 1, 4)

            # Give user the ability to adjust the full name value (i.e. Smith1, Jr., III, etc.)
            self.edit_full_name = QCheckBox("Edit Full Name")
            edit_fn_tooltip = "Check to toggle ability to edit the Full Name field. (i.e. for Smith1, Jr., III, etc.)"
            self.edit_full_name.setToolTip(edit_fn_tooltip)
            # On toggle make the full_name box editable
            self.edit_full_name.stateChanged.connect(self.toggle_full_name_edit)
            newuser_layout.addWidget(self.edit_full_name, 2, 4, 1, 2)

            # Enter SSO for username selection
            self.SSO_input = QLineEdit()
            self.SSO_input.setPlaceholderText("Enter user SSO")
            self.SSO_input.setValidator(QIntValidator())
            self.SSO_input.setMaxLength(9)
            self.SSO_input.textChanged.connect(self.generate_account_names)
            newuser_layout.addWidget(self.SSO_input, 3, 0, 1, 1)

            # Define tooltip text for checkboxes
            account_type_tooltip = "If this box is checked, add this account type to account creation."
            self.User_check = QCheckBox("User")
            self.User_check.setChecked(True)
            self.User_check.stateChanged.connect(self.generate_account_names)
            self.User_check.setToolTip(account_type_tooltip)
            newuser_layout.addWidget(self.User_check, 3, 1, 1, 1)

            # Display the appropriate SSO checkbox for the environment found above
            if "evav" not in self.main_app.DOMAIN_NAME:
                self.ADM_check = QCheckBox(".ADM")
                self.ADM_check.stateChanged.connect(self.generate_account_names)
                self.ADM_check.setToolTip(account_type_tooltip)
                newuser_layout.addWidget(self.ADM_check, 3, 2, 1, 1)
            else:
                self.zz_check = QCheckBox("zz")
                self.zz_check.stateChanged.connect(self.generate_account_names)
                self.zz_check.setToolTip(account_type_tooltip)
                newuser_layout.addWidget(self.zz_check, 3, 2, 1, 1)

            self.AUD_check = QCheckBox(".AUD")
            self.AUD_check.stateChanged.connect(self.generate_account_names)
            self.AUD_check.setToolTip(account_type_tooltip)
            newuser_layout.addWidget(self.AUD_check, 3, 3, 1, 1)

            self.DTA_check = QCheckBox(".DTA")
            self.DTA_check.stateChanged.connect(self.generate_account_names)
            self.DTA_check.setToolTip(account_type_tooltip)
            newuser_layout.addWidget(self.DTA_check, 3, 4, 1, 1)

            self.ISSO_check = QCheckBox(".ISSO")
            self.ISSO_check.stateChanged.connect(self.generate_account_names)
            self.ISSO_check.setToolTip(account_type_tooltip)
            newuser_layout.addWidget(self.ISSO_check, 3, 5, 1, 1)

            self.account_names = QLineEdit()
            self.account_names.setReadOnly(True)
            self.account_names.setPlaceholderText("SamAccountNames to be created will be listed here")
            newuser_layout.addWidget(self.account_names, 4, 0, 1, 4)

            self.edit_account_names = QCheckBox("Edit Accounts")
            # On toggle make the account names box editable
            self.edit_account_names.stateChanged.connect(self.toggle_account_edit)
            newuser_layout.addWidget(self.edit_account_names, 4, 4, 1, 2)

            # Display a temporary password field generated with today's date and last 4 of SSO
            self.temp_password = QLineEdit()
            self.temp_password.setReadOnly(True)
            self.temp_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.temp_password.setPlaceholderText("Temporary Password")
            newuser_layout.addWidget(self.temp_password, 5, 0, 1, 2)

            self.reveal_checkbox = QCheckBox("Show Password")
            self.reveal_checkbox.stateChanged.connect(self.reveal_password)
            newuser_layout.addWidget(self.reveal_checkbox, 5, 2, 1, 2)

            self.roulette_button = QPushButton("Password Roulette")
            self.roulette_button.clicked.connect(self.password_roulette)
            newuser_layout.addWidget(self.roulette_button, 5, 4, 1, 2)

            newuser_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            tab_index = self.main_app.tabs.addTab(self, title)  # Add self to tabs instead of newuser_tab
            self.main_app.tabs.setTabIcon(tab_index, QIcon('assets/material-icons/user_add_icon.png'))
            self.main_app.tabs.setCurrentIndex(tab_index)

            self.temp_password.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.temp_password.customContextMenuRequested.connect(self.copy_password_to_clipboard)
        except Exception as e:
            print(f"The following error occurred: {e}")

    def set_full_name(self):
        # Update the full name based on the values in the first and last name fields
        if not self.edit_full_name.isChecked():  # If edit_full_name is not checked then change the value of full_name
            first = self.first_name.text()
            last = self.last_name.text()
            full = ""
            # Generate the full_name using the values entered in first_name and last_name
            if first == "" and last =="":
                full = ""
            elif first != "" and last != "":
                full = f"{last}, {first}"
            elif first != "":
                full = f"{first}"
            elif last != "":
                full = f"{last}"

            self.full_name.setText(full)

    def toggle_full_name_edit(self):
        if self.edit_full_name.isChecked(): # Toggle the ability to edit the full_name box
            self.full_name.setReadOnly(False)
        else:
            self.full_name.setReadOnly(True)

    def toggle_account_edit(self):
        if self.edit_account_names.isChecked():
            self.account_names.setReadOnly(False)
        else:
            self.account_names.setReadOnly(True)

    def generate_account_names(self):
        try:
            if not self.edit_account_names.isChecked():  # Only do this if editing on the account_names box is not enabled
                if self.SSO_input.text() == "":  # If text is fully removed from SSO input, set account_names box to ""
                    self.account_names.setText("")
                    self.temp_password.setText("")
                else:
                    account_list = []  # Define list for account names
                    # Evaluate which boxes are checked and need included in the list
                    if self.User_check.isChecked():
                        account_list.append(self.SSO_input.text())
                    if self.ADM_check is not None and self.ADM_check.isChecked():
                        account_list.append(f"{self.SSO_input.text()}.ADM")
                    if self.zz_check is not None and self.zz_check.isChecked():
                        account_list.append(f"zz{self.SSO_input.text()}")
                    if self.AUD_check.isChecked():
                        account_list.append(f"{self.SSO_input.text()}.AUD")
                    if self.DTA_check.isChecked():
                        account_list.append(f"{self.SSO_input.text()}.DTA")
                    if self.ISSO_check.isChecked():
                        account_list.append(f"{self.SSO_input.text()}.ISSO")
                    # Set the account_names box to the list content
                    self.account_names.setText(str(', '.join(account_list)))
                    self.generate_temp_password()
        except Exception as e:
            print(f"Error generating account names: {e}")

    def generate_temp_password(self):
        today = datetime.date.today()
        ftoday = today.strftime("%Y%m%d")

        last4 = str(self.SSO_input.text()[-4:])  # Grab last 4 of the SSO_input
        temp_pass = f"P@ssword_{ftoday}_{last4}"
        self.temp_password.setText(temp_pass)

    def reveal_password(self): # Toggle the Password blips
        if self.reveal_checkbox.isChecked():
            self.temp_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.temp_password.setEchoMode(QLineEdit.EchoMode.Password)

    def password_roulette(self):
        self.temp_password.setEchoMode(QLineEdit.EchoMode.Normal)
        if self.temp_password.text() != "":
            seed = self.temp_password.text()
        else:
            seed = "Rolling Password..."
            self.temp_password.setText("")
            QTimer.singleShot(4000, lambda: self.temp_password.setText(seed))

        # Toss the text from the above seed into a character array
        # then define our possible password characters
        char_list = [char for char in seed]
        key = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"

        for i in range(len(char_list)):
            start_time = time.time()
            while time.time() - start_time < 0.25:  # Continue for 1/4 second
                char_list[i] = secrets.choice(key)  # Select a random character from the key
                self.temp_password.setText(''.join(char_list))  # Update the temp_password text box
                QCoreApplication.processEvents()  # Allow the GUI to update
                #QTimer.singleShot(1000, lambda: None)

        if not self.password_meets_requirements(''.join(char_list)):
            self.password_roulette()  # If the password does not meet the requirements, re-roll it

        if not self.reveal_checkbox.isChecked():
            self.temp_password.setEchoMode(QLineEdit.EchoMode.Password)

    def password_meets_requirements(self, password):
        # Check if the password meets the specified requirements
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in password)

        return has_upper and has_lower and has_digit and has_special

    def copy_password_to_clipboard(self, event):
        if self.temp_password.text() != "":
            clipboard = QApplication.clipboard()
            clipboard.setText(self.temp_password.text())

            # Display a tooltip near the mouse cursor
            mouse_pos = QCursor.pos()
            QToolTip.showText(mouse_pos, "Password Copied!", self.temp_password)
