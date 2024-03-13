import src.assets.resources
from PyQt6 import QtGui
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QCoreApplication


class AppLoadingDialog(QDialog):
    def __init__(self, parent=None):
        super(AppLoadingDialog, self).__init__(parent)
        self.setWindowTitle("Loading Tool...")
        self.setWindowIcon(QtGui.QIcon(':/images/GE-Monogram.ico'))
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        layout = QHBoxLayout(self)
        self.label = QLabel("Loading, please wait...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.label)

        # Create a QLabel to display the buffering symbol
        self.buffering_label = QLabel(self)
        self.buffering_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.buffering_label.setFixedSize(32, 32)
        ##layout.addWidget(self.buffering_label)

        # Set up the buffering symbol
        self.movie = QMovie(':/gifs/loading.gif')
        self.movie.setScaledSize(self.buffering_label.size())
        ##self.buffering_label.setMovie(self.movie)

        # Set up QTimer to update label text every 1/3 second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label_text)
        self.timer.start(333)  # 333 milliseconds (1/3 second)

        ##self.movie.start()

    def update_label_text(self):
        current_text = self.label.text()
        if current_text == "Loading, please wait...":
            self.label.setText("Loading, please wait")
        else:
            new_text = current_text + "."
            self.label.setText(new_text)
