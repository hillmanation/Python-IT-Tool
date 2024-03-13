from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit

about_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About SDS User Management Tool</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
        }

        h1, h2 {
            color: white;
        }

        h2 {
            margin-top: 10px;
        }

        p {
            line-height: 1.5;
            color: white;
        }

        ul {
            margin-bottom: 20px;
        }

        li {
            margin-bottom: 5px;
        }

        strong {
            color: white;
        }

        footer {
            margin-top: 20px;
            color: white;
        }
    </style>
</head>
<body>
    <h1>SDS User Management Tool</h1>

    <h2>About the Tool</h2>
    <p>
        The SDS User Management Tool is a powerful and user-friendly application designed to streamline user management 
        tasks within your organization.
    </p>

    <h2>Features</h2>
    <ul>
        <li><strong>Intuitive Interface:</strong> Our tool boasts a user-friendly interface, making it accessible for 
        both novice and experienced administrators.</li>
        <li><strong>Versatile Functionality:</strong> From creating new user accounts to running PowerShell commands, 
        the tool covers a wide array of functionalities to meet your user management needs.</li>
        <li><strong>Tabbed Navigation:</strong> Organize your tasks effortlessly with tabbed navigation, allowing you 
        to work on multiple tasks simultaneously.</li>
        <li><strong>Modular Forms:</strong> Each Tab is based on a form from a unique python file, utilizing the 
        template included in the repository, anyone can create new forms for use with the tool. See documentation for 
        how to add or request features within the tool.</li>
    </ul>

    <h2>Disclaimer</h2>
    <p>
        <strong>Important: Use at Your Own Risk</strong><br>
        While we strive to provide a robust and reliable user management tool, it is crucial to understand the 
        implications of system administration. The creator of this tool is not responsible for any unintended 
        consequences, errors, or issues that may arise during its usage.
        <br><br>
        Always exercise caution and ensure that you have appropriate backups and permissions before making significant 
        changes to user accounts or system settings.
    </p>

    <h2>Support</h2>
    <p>
        For inquiries, support, or feedback, please contact our support team at 
        <a href="mailto:support@example.com">support@example.com</a>.
    </p>

    <footer>
        Thank you for choosing the SDS User Management Tool. We hope it enhances your user administration experience.
    </footer>
</body>
</html>
"""


class WatermarkTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(WatermarkTextEdit, self).__init__(parent)
        self.setReadOnly(True)
        self.document().setHtml(about_html)

    def paintEvent(self, event):
        # Call the base class paintEvent to draw the text content
        super().paintEvent(event)

        # Draw the watermark image
        painter = QPainter(self.viewport())
        watermark_image = QPixmap(':/images/jake-head.png')
        painter.setOpacity(0.1)  # Adjust the opacity as needed
        painter.drawPixmap(self.rect(), watermark_image)

    def showEvent(self, event):
        # Call the base class showEvent
        super().showEvent(event)
        # Scroll to the top after the widget is shown
        self.verticalScrollBar().setValue(0)


# noinspection PyUnresolvedReferences
class AboutPopupWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutPopupWindow, self).__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(550, 500)

        # Create a layout for the popup window
        layout = QVBoxLayout()

        # Create a WatermarkTextEdit widget
        about_text = WatermarkTextEdit()

        # Add the WatermarkTextEdit to the layout
        layout.addWidget(about_text)

        # Add a "Close" button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)  # Close the popup when the button is clicked
        layout.addWidget(close_button)

        # Set the layout for the popup window
        self.setLayout(layout)
