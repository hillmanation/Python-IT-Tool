from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6 import QtGui


class PSStyleOutput(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: white; background-color: MidnightBlue")
    def appendPlainTextNoScroll(self, text):
        # Save the current scrollbar value
        scrollbar = self.verticalScrollBar()
        scroll_position = scrollbar.value()

        # Append the text
        self.appendPlainText(text)

        # Restore the scrollbar value
        scrollbar.setValue(scroll_position)


class PowershellStylePrompt(QPlainTextEdit):
    enterKeyPressed = pyqtSignal()

    def keyPressEvent(self, event):
        try:
            if event.key() in {Qt.Key.Key_Return, Qt.Key.Key_Enter}:
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    cursor = self.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfBlock)
                    cursor.insertBlock()
                else:
                    self.enterKeyPressed.emit()
            else:
                super().keyPressEvent(event)
        except Exception as e:
            print(f"Key press error: {e}")

    def setPlainText(self, text):
        self.clear()
        self.insertPlainText(text)