import sys, os, json
from PyQt6.QtCore import *
from PyQt6.QtCore import QEvent
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QLabel, QListWidget, \
    QVBoxLayout, QWidget, QTabWidget, QFormLayout, QDialog, QToolTip

## Individual Form imports
from forms.New_User import newuserformUI
from forms.User_Search import usersearchformUI
from forms.PS_Prompt import psformUI
from forms.User_Account import useraccountUI
from functions.ps import PSquery
from dialogs.about_popup import AboutPopupWindow