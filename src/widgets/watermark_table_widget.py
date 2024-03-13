import PyQt6
import src.assets.resources
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt


class WatermarkTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(WatermarkTableWidget, self).__init__(parent)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setEditTriggers(PyQt6.QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setColumnCount(2)
        self.horizontalHeader().setSectionResizeMode(0, PyQt6.QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, PyQt6.QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(PyQt6.QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionBehavior(PyQt6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(PyQt6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Set column headers
        self.setHorizontalHeaderLabels(["Name", "Value"])

    def paintEvent(self, event):
        # Call the base class paintEvent to draw the text content
        super().paintEvent(event)

        # Draw the watermark image with adjusted aspect ratio
        painter = QPainter(self.viewport())
        watermark_image = QPixmap(':/images/image.ico')

        widget_height = self.rect().height()
        widget_width = self.rect().width()

        # Calculate aspect ratio of the widget
        widget_aspect_ratio = widget_width / widget_height

        # Calculate target width and height
        target_height = min(widget_height, watermark_image.height())
        target_width = min(widget_width, watermark_image.width())

        # Scale the pixmap with the adjusted aspect ratio
        scaled_pixmap = watermark_image.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)

        # Calculate the position to center the image
        x_pos = (widget_width - target_width) // 2
        y_pos = (widget_height - target_height) // 2

        # Set opacity and draw the pixmap
        painter.setOpacity(0.2)  # Adjust the opacity as needed
        painter.drawPixmap(x_pos, y_pos, scaled_pixmap)
