# Creating a New Form using `form_template.py`

The Python IT Management Tool allows users to create custom forms that can be added as tabs to the main interface. This guide will walk you through the process of creating a new form using the `form_template.py` file provided in the `forms` folder.

## Step 1: Understanding the `form_template.py` File

The `form_template.py` file serves as a template for creating new forms. It contains a basic form class named `templateUI`. This class inherits from `QWidget` and includes a simple user interface with a label.

```python
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class templateUI(QWidget):
    def __init__(self, main_app):
        super(templateUI, self).__init__(main_app)  # Pass main_app as the parent
        self.main_app = main_app
        self.setup_ui()

    def setup_ui(self):
        title = "Template"

        template_layout = QVBoxLayout(self)

        template_label = QLabel("Template")
        font = template_label.font()
        font.setPointSize(15)
        template_label.setFont(font)
        template_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        template_layout.addWidget(template_label)

        tab_index = self.main_app.tabs.addTab(self, title)
        self.main_app.tabs.setCurrentIndex(tab_index)
```
This template includes a label and sets up a basic user interface. You can modify this class to create a custom form based on your specific requirements.  

## Step 2: Creating Your Custom Form
To create a custom form, follow these steps:

1. **Duplicate the `form_template.py` file**: Create a copy of the `form_template.py` file and rename it to match your new form.

2. **Modify the form class**: Open the duplicated file and modify the `templateUI` class to suit your needs. Add or remove widgets, set up layouts, and define the behavior of your form.

3. **Adjust the title**: Change the `title` variable in the `setup_ui` method to set the title of your form's tab.

4. **Import the form in `import_modules.py`**: Open the `import_modules.py` file located in the project directory. Add an import statement for your new form at the beginning of the file, like this:
```python
from forms.your_new_form_file import YourNewFormUI
```
Make sure to replace `your_new_form_file` with the actual filename of your new form.

5. **Update the `mapping` variable in `import_modules.py`**: Open the `import_modules.py` file and locate the `mapping` variable. Add an entry for your new form, associating it with its corresponding class. For example:
```python
mapping = {
    # ... other mappings
    "your new form": {"function": YourNewFormUI, "description": "Description of your form"}
}
```
Replace `"your new form"` with a unique identifier for your form and `YourNewFormUI` with the actual class name.

## Step 3: Run the Application
After completing these steps, run the Python IT Management Tool application. You should see your new form in the Tools tab list. Opening this form will display the user interface you defined in your custom form class.

Feel free to customize your form further and add additional functionalities based on your requirements.    
