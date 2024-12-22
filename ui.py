import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer


class RecipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('FoodFusion')
        self.setGeometry(100, 100, 600, 450)
        self.setWindowIcon(QIcon('icon.png'))

        main_layout = QVBoxLayout()

        title_label = QLabel('What can I cook today?')
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('color: #4CAF50;')
        main_layout.addWidget(title_label)

        input_layout = QVBoxLayout()

        input_label = QLabel('Available Products:')
        input_label.setFont(QFont('Arial', 16))
        input_label.setStyleSheet('color: #333;')
        input_layout.addWidget(input_label)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText('Enter your products, one per line...')
        self.text_area.setFont(QFont('Arial', 14))
        self.text_area.setStyleSheet('border: 2px solid #4CAF50; padding: 10px; background-color: #f9f9f9;')
        input_layout.addWidget(self.text_area)

        main_layout.addLayout(input_layout)

        self.submit_button = QPushButton('Find Recipe')
        self.submit_button.setFont(QFont('Arial', 16))
        self.submit_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        ''')
        self.submit_button.clicked.connect(self.send_products)
        main_layout.addWidget(self.submit_button)

        self.recipe_label = QLabel('Recipe:')
        self.recipe_label.setFont(QFont('Arial', 18))
        self.recipe_label.setAlignment(Qt.AlignCenter)
        self.recipe_label.setStyleSheet('color: #4CAF50;')
        main_layout.addWidget(self.recipe_label)

        self.recipe_text = QTextEdit()
        self.recipe_text.setFont(QFont('Arial', 14))
        self.recipe_text.setReadOnly(True)
        self.recipe_text.setStyleSheet('border: 2px solid #4CAF50; padding: 10px; background-color: #f9f9f9;')
        main_layout.addWidget(self.recipe_text)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)

    def send_products(self):
        self.submit_button.setText('Searching...')
        self.submit_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.submit_button.setText('Find Recipe'))
        QTimer.singleShot(2000, lambda: self.submit_button.setEnabled(True))

        products = self.text_area.toPlainText()

        try:
            response = requests.post('http://127.0.0.1:5000/submit', data={'products': products})
            if response.status_code == 200:
                recipe = response.json().get('recipe', '')
                self.display_recipe(recipe)
            else:
                QMessageBox.warning(self, 'Error', f'Server error: {response.status_code}')
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self, 'Error', 'Could not connect to the server')

    def display_recipe(self, recipe):
        self.recipe_text.clear()

        self.recipe_label.setText('Recipe: ' + recipe.split("\n")[0])

        self.recipe_text.setText('\n'.join(recipe.split("\n")[1:]))


def run_ui():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(245, 245, 245))
    palette.setColor(QPalette.AlternateBase, QColor(235, 235, 235))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = RecipeApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_ui()
