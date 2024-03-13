import os, sys
# Add the top-level package directory (src) to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/src")
import src.assets.resources
import json
## Conditional Imports
import platform
if platform.system() == 'posix':
    import pwd
    import grp

from datetime import datetime
import PyQt6.QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent, Qt, QThread, QEventLoop, QTimer
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QLabel, QListWidget, QTableWidget, \
    QVBoxLayout, QWidget, QTabWidget, QFormLayout, QDialog, QToolTip, QBoxLayout, QHBoxLayout, QGridLayout, \
    QTableWidgetItem

## Individual Form imports
from src.forms.New_User import newuserform_ui
from src.forms.User_Search import usersearchform_ui
from src.forms.PS_Prompt import psform_ui
from src.forms.User_Account import useraccount_ui
from src.functions.ps import PSquery
from src.dialogs.about_popup import AboutPopupWindow
from src.widgets.watermark_table_widget import WatermarkTableWidget
from src.dialogs.app_loading import AppLoadingDialog

mapping = {  # Map plain text to match a function we will call as a new tab
    "New User": {"function": newuserform_ui, "description": "Create a New User"},
    "User Search": {"function": usersearchform_ui, "description": "Search for a User in AD"},
    "User Account": {"function": useraccount_ui, "description": "Test Page to Display User Information"},
    "Powershell Console": {"function": psform_ui, "description": "Simple Powershell Query Tool"}
}
