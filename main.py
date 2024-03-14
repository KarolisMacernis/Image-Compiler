# Image Compiler Application
# This module defines the main window and functionality for an image compilation tool.
# Dependencies: PyQt6, Pillow (PIL)

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSpinBox, QLabel, QPushButton, QHBoxLayout, QFileDialog, QLineEdit, QComboBox, QGroupBox
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PIL import Image, ImageEnhance
import os
import glob
import imghdr

class MainWindow(QWidget):
    """Main application window for the Image Compiler tool."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Image Compiler")
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Define the fixed widths and heights
        self.directoryWidth = 200
        self.nameWidth = 150
        self.opacityWidth = 50
        self.orderWidth = 150
        self.outputButtonHeight = 30
        self.compileButtonHeight = 35

        self.layout = QVBoxLayout()

        self.create_top_layout()
        self.layout.addSpacing(5)  # Add some space between the top layout and the group box
        self.create_group_box()
        self.layout.addSpacing(5)  # Add some space between the group box and the output directory button
        self.create_output_directory_button()
        self.create_output_type_combo_box()
        self.create_compile_button()

        self.outputDirectory = None

        self.setLayout(self.layout)

        # Lists to store the slot widgets
        self.directoryButtons = []
        self.lineEdits = []
        self.spinBoxes = []

        self.create_slots(self.spinner.value()) # Create the initial slots based on the initial spinner value

    def create_top_layout(self):
        """Create the top layout containing the spinner and apply button."""
        self.topLayout = QHBoxLayout()

        self.spinner = QSpinBox()
        self.spinner.setRange(2, 8)
        self.spinner.setValue(5)  # Set the initial value to 5
        self.topLayout.addWidget(QLabel("Choose number of slots: "))
        self.topLayout.addWidget(self.spinner)

        self.applyButton = QPushButton("Apply")
        self.applyButton.clicked.connect(self.update_slots) # Update the slots when the apply button is clicked
        self.topLayout.addWidget(self.applyButton)

        self.layout.addLayout(self.topLayout)

    def create_group_box(self):
        """Create the group box to contain the image slots."""
        self.groupBox = QGroupBox("Image Slots")
        self.groupBoxLayout = QVBoxLayout()
        self.groupBox.setLayout(self.groupBoxLayout)

        self.labels = ["Directory", "Name", "Opacity", "Order"] # Labels for the image slots
        self.labelsLayout = QHBoxLayout()
        for label in self.labels:
            labelWidget = QLabel(label)
            width = getattr(self, label.lower() + "Width", 0) # Get the width from the variable with the same name as the label
            labelWidget.setFixedWidth(width)
            if label == "Order":
                labelWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.labelsLayout.addWidget(labelWidget)

        self.groupBoxLayout.addLayout(self.labelsLayout)
        self.slotsContainerLayout = QVBoxLayout()
        self.groupBoxLayout.addLayout(self.slotsContainerLayout)
        self.layout.addWidget(self.groupBox)

    def create_output_directory_button(self):
        """Create the button to select the output directory."""
        self.outputDirectoryButton = QPushButton("Select output directory")
        self.outputDirectoryButton.setFixedHeight(self.outputButtonHeight)
        self.outputDirectoryButton.clicked.connect(self.select_output_directory)
        self.layout.addWidget(self.outputDirectoryButton)

    def create_output_type_combo_box(self):
        """Create the combo box to select the output image type."""
        self.outputTypeComboBox = QComboBox()
        self.outputTypeComboBox.addItems([".png", ".jpg", ".bmp", ".tif"])
        self.layout.addWidget(QLabel("Select output type: "))
        self.layout.addWidget(self.outputTypeComboBox)
        self.outputType = ".png"
        self.outputTypeComboBox.currentTextChanged.connect(self.update_output_type)

    def create_compile_button(self):
        """Create the button to initiate the compilation process."""
        self.compileButton = QPushButton("Compile")
        self.compileButton.setFixedHeight(self.compileButtonHeight)
        self.compileButton.clicked.connect(self.compile)
        self.layout.addWidget(self.compileButton)

    def choose_directory(self):
        """Open a dialog to choose a directory."""
        directory = QFileDialog.getExistingDirectory()
        return directory if directory else "Choose Directory"

    def create_directory_slot(self, button):
        """Create a slot for selecting a directory."""
        return lambda: button.setText(self.choose_directory())

    def create_slots(self, num_widgets):
        """Create the image slots."""
        for i in range(num_widgets):
            slotLayout = QHBoxLayout()
            slotLayout.index = i
            for j, label in enumerate(self.labels):
                if label == "Directory":
                    directoryButton = QPushButton("Choose Directory")
                    directoryButton.setFixedWidth(self.directoryWidth)  # Use the variable for the fixed width
                    directoryButton.clicked.connect(self.create_directory_slot(directoryButton))
                    slotLayout.addWidget(directoryButton)
                    self.directoryButtons.append(directoryButton)
                elif label == "Name":
                    lineEdit = QLineEdit()
                    lineEdit.setFixedWidth(self.nameWidth)  # Use the variable for the fixed width
                    slotLayout.addWidget(lineEdit)
                    self.lineEdits.append(lineEdit)
                elif label == "Opacity":
                    opacitySpinner = QSpinBox()
                    opacitySpinner.setFixedWidth(self.opacityWidth)  # Use the variable for the fixed width
                    opacitySpinner.setRange(0, 100)
                    opacitySpinner.setValue(100)  # Set the initial value to 100
                    slotLayout.addWidget(opacitySpinner)
                    self.spinBoxes.append(opacitySpinner)

            # Create Up/Down buttons
            upButton = QPushButton("Up")
            upButton.setFixedWidth(int(self.orderWidth / 2))  # Set the button width to half the Order label width
            upButton.clicked.connect(lambda _, layout=slotLayout: self.move_line(layout.index, -1))
            slotLayout.addWidget(upButton)

            downButton = QPushButton("Down")
            downButton.setFixedWidth(int(self.orderWidth / 2))  # Set the button width to half the Order label width
            downButton.clicked.connect(lambda _, layout=slotLayout: self.move_line(layout.index, 1))
            slotLayout.addWidget(downButton)

            self.slotsContainerLayout.insertLayout(i, slotLayout)  # Add the layout to the slotsContainerLayout

            # Adjust the window size to fit the widgets
            self.adjustSize()

            # Set the window size to fixed
            self.setFixedSize(self.size())

    def move_line(self, index, direction):
        """Move an image slot up or down."""
        if index + direction < 0 or index + direction >= self.slotsContainerLayout.count():
            return  # Out of bounds

        # Remove the widgets at the current index from the lists
        directoryButton = self.directoryButtons.pop(index)
        lineEdit = self.lineEdits.pop(index)
        spinBox = self.spinBoxes.pop(index)

        # Remove the line at index and insert it at index + direction
        line = self.slotsContainerLayout.takeAt(index)
        self.slotsContainerLayout.insertLayout(index + direction, line)

        # Update the indices of the moved line and the line that was in its new position
        line.index += direction
        if index + direction < self.slotsContainerLayout.count():
            self.slotsContainerLayout.itemAt(index).layout().index -= direction

        # Insert the widgets at the new index into the lists
        self.directoryButtons.insert(index + direction, directoryButton)
        self.lineEdits.insert(index + direction, lineEdit)
        self.spinBoxes.insert(index + direction, spinBox)

    def update_slots(self):
        """Update the image slots based on the spinner value."""
        for _ in range(self.slotsContainerLayout.count()):
            # Remove all lines from the layout
            line = self.slotsContainerLayout.takeAt(0)
            for i in reversed(range(line.count())):
                widget = line.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

        # Clear the lists of widgets
        self.directoryButtons.clear()
        self.lineEdits.clear()
        self.spinBoxes.clear()

        # Create new widgets
        self.create_slots(self.spinner.value())

        # Adjust the size of the window to fit the new widgets
        QTimer.singleShot(0, self.adjustSize)

    def get_user_inputs(self):
        """Get user inputs from the image slots."""
        directories = [button.text() for button in self.directoryButtons]
        name = [lineEdit.text() for lineEdit in self.lineEdits]
        opacities = [spinBox.value() for spinBox in self.spinBoxes]

        return directories, name, opacities
    
    def select_output_directory(self):
        """Select the output directory."""
        # Open a directory selection dialog and store the selected directory
        self.outputDirectory = QFileDialog.getExistingDirectory()
        # Update the button text to show the selected directory
        if self.outputDirectory:
            self.outputDirectoryButton.setText(self.outputDirectory)

    def update_output_type(self, text):
        """Update the selected output image type."""
        self.outputType = text
    
    def compile(self):
        """Compile the images."""
        # Get user inputs
        directories, names, opacities = self.get_user_inputs()

        # Get all images from each directory and sort them
        all_images = [[file for file in sorted(glob.glob(os.path.join(directory, f"*{name}*"))) if os.path.isfile(file) and imghdr.what(file)] for directory, name in zip(directories, names)]

        # Check if there are no images
        if not any(images for images in all_images):
            QMessageBox.information(self, "Error", "No images found.")
            return

        # Check if output directory is not selected
        if not self.outputDirectory:
            QMessageBox.information(self, "Error", "Please select an output directory.")
            return
        
        # Check if the resolutions of images match
        resolutions = set()
        for images in all_images:
            for image_path in images:
                with Image.open(image_path) as img:
                    resolutions.add(img.size)
        
        if len(resolutions) != 1:
            QMessageBox.information(self, "Error", "The resolutions of the images do not match.")
            return

        # Iterate over the images in parallel
        for j in range(max(len(images) for images in all_images)):

            # Initialize combined before the loop
            combined = None

            # Start with the last directory if it exists
            for i in range(len(all_images)-1, -1, -1):
                # Skip if there is no image at the current index
                if j >= len(all_images[i]):
                    continue

                # Open the image
                image = Image.open(all_images[i][j])

                # Adjust the alpha channel of the image according to the opacity value
                enhancer = ImageEnhance.Brightness(image.convert("RGBA").split()[3])
                alpha = enhancer.enhance(opacities[i] / 100)
                image.putalpha(alpha)

                # Combine the images
                if combined is None:
                    combined = image
                else:
                    combined = Image.alpha_composite(combined.convert("RGBA"), image)

            # If the output type is JPEG or BMP, blend the combined image with a white background
            if self.outputType in [".jpg", ".bmp"]:
                background = Image.new("RGB", combined.size, (255, 255, 255))
                background = background.convert("RGBA")  # Convert the background to RGBA mode
                combined = Image.alpha_composite(background, combined.convert("RGBA"))
                combined = combined.convert("RGB")  # Convert the combined image back to RGB mode

            # Save the combined image in the selected output directory
            combined.save(os.path.join(self.outputDirectory, f"Combined_{j}{self.outputType}"))

        # Show a message box when the compiling process is completed
        QMessageBox.information(self, "Compiling Complete", "The compiling process has been completed successfully.")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
