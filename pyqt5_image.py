from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PIL import Image
from io import BytesIO

def save_image_as_binary(image_path, binary_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    with open(binary_path, 'wb') as binary_file:
        binary_file.write(image_data)

def load_image_from_binary(binary_path):
    with open(binary_path, 'rb') as binary_file:
        image_data = binary_file.read()
    image = Image.open(BytesIO(image_data))
    return image

def pil_image_to_pixmap(pil_image):
    with BytesIO() as buffer:
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        qpixmap = QPixmap()
        qpixmap.loadFromData(buffer.getvalue())
    return qpixmap

class ImageViewer(QMainWindow):
    def __init__(self, original_image, converted_image):
        super().__init__()
        self.setWindowTitle('Original and Converted Images')

        # convert PIL image to QPixmap
        original_pixmap = pil_image_to_pixmap(original_image)
        converted_pixmap = pil_image_to_pixmap(converted_image)

        # create label to display image
        original_label = QLabel()
        original_label.setPixmap(original_pixmap)

        converted_label = QLabel()
        converted_label.setPixmap(converted_pixmap)

        # layout to arrange image side by side
        layout = QVBoxLayout()
        layout.addWidget(original_label)
        layout.addWidget(converted_label)

        # set up the main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    import sys

    # file paths
    image_path = 'example_image.png'
    binary_path = 'image_binary.bin'
    converted_image_path = 'converted_image.png'

    save_image_as_binary(image_path, binary_path)

    converted_image = load_image_from_binary(binary_path)
    converted_image.save(converted_image_path)

    original_image = Image.open(image_path)
    converted_image = Image.open(converted_image_path)

    # set up application window
    app = QApplication(sys.argv)
    viewer = ImageViewer(original_image, converted_image)
    viewer.show()
    sys.exit(app.exec_())
