from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel


class ImageRotateDialog(QDialog):
    def __init__(self, image_path, rotation_speed=50, parent=None):
        super(ImageRotateDialog, self).__init__(parent)
        self.loading_label = None
        self.original_image_reader = None
        self.timer = None
        self.image_label = None
        self.original_image = None
        self.image_path = image_path
        self.rotation_speed = rotation_speed
        self.angle = 0
        self.setFixedSize(200, 75)

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.loading_label)

        # Create QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(64, 64)
        layout.addWidget(self.image_label)

        # Load the image from file
        self.load_image()

        # Set up QTimer to continuously rotate the image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_image)
        self.timer.start(self.rotation_speed)

        self.setLayout(layout)
        self.setWindowTitle("Rotating Image Dialog")

    def load_image(self):
        # Load image from file as a QPixmap
        self.original_image = QPixmap(self.image_path)

        # Set the original image as the pixmap
        self.image_label.setPixmap(self.original_image.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def rotate_image(self):
        try:
            # Rotate the image by a certain angle on each timer timeout
            self.angle += 10

            # Ensure angle stays within [0, 360] range
            self.angle %= 360

            # Create a transformation with rotation
            transform = QTransform().rotate(self.angle)

            # Apply the rotation transformation to get the rotated image
            rotated_pixmap = self.original_image.transformed(transform, Qt.TransformationMode.SmoothTransformation)

            self.image_label.setPixmap(rotated_pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(f"Error: {e}")