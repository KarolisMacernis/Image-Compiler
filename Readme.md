# Image Compiler Application

This application is a GUI-based tool for compiling multiple series of images together. It is built using Python, PyQt6, and the Pillow library.

## Features
- Allows the user to select multiple directories containing images.
- User can specify the name, opacity, and order of the images.
- User can select the output directory where the compiled images will be saved.
- User can select the output image type (PNG, JPG, BMP, TIF).
- The application compiles the images together, taking into account the specified opacity and order.

## Dependencies
- Python
- PyQt6
- Pillow (PIL)

## How to Run
1. Ensure that Python, PyQt6, and Pillow are installed on your system.
2. Run the `main.py` script to start the application.

## How to Use
1. Run the application. A window titled "Image Compiler" will appear.
2. At the top of the window, you'll see a spinner labeled "Choose number of slots". This spinner allows you to select the number of image directories you want to compile. Adjust the number and click the "Apply" button to create the corresponding number of slots.
3. Each slot consists of a "Directory" button, a "Name" text field, an "Opacity" spinner, and "Up" and "Down" buttons. Click the "Directory" button to select a directory containing images. In the "Name" field, enter a name to filter the images in the directory by including only those that contain the entered string in their file name. For example, if you enter "Chair", only images with "Chair" in their file name (like "Chair_001.png", "Chair_002.png",) will be used. If no name is entered, all the images in the directory will be used for that slot. The "Opacity" spinner allows you to set the opacity of the images from the corresponding directory. The "Up" and "Down" buttons allow you to adjust the order of the slots, which determines the order in which the images are compiled. This way the image slots act as layers which can be rearranged in order.
4. After setting up the slots, select the output directory by clicking the "Select output directory" button.
5. Choose the output image type from the combo box below the output directory button. You can choose between .png, .jpg, .bmp, and .tif.
6. Initiate the compilation process by clicking on the "Compile" button. The software will then merge the images from the chosen directories into a unified image for each group. These merged images will be stored in the designated output directory. They will be named in the format "Combined_{index}.{outputType}", where {index} represents the sequence number of the image group and {outputType} indicates the chosen output image format. For instance, the name of the first merged image could be "Combined_0.png".
7. A message box will appear when the compiling process is completed.

## Code Structure
The `MainWindow` class is the main application window for the Image Compiler tool. It contains methods for setting up the user interface, creating image slots, moving image slots, updating image slots, getting user inputs, selecting the output directory, updating the output image type, and compiling the images.

The `app` object is an instance of `QApplication`, and `window` is an instance of `MainWindow`. The window is shown and the application is executed with `app.exec()`.

## Use Case
An example use case for this can be having multiple render images of an object called "Chair_001.png", "Chair_002.png", "Chair_003.png" etc. and needing to combine them with another series of images containing its shadow called "Shadow_001.png", "Shadow_002.png", "Shadow_003.png"... The application can be used to specify the main object images containing the string "Chair" in one slot and the shadow images in the slot under it. Therefore, the "Chair_001.png" image will be combined with "Shadow_001.png", "Chair_002.png" will be combined with "Shadow_002.png" and so on. Keep in mind that the images must have an alpha channel in order for the objects under it to be visible.

## Limitations
- All images to be compiled together must have the same resolution.
- The output image type can only be PNG, JPG, BMP, or TIF.