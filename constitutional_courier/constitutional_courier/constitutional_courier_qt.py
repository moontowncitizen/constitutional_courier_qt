import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QTextEdit, QLineEdit, QPushButton,
    QSplitter, QScrollArea, QMenuBar, QAction, QMenu, QStatusBar
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor

class ConstitutionalCourier(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Constitutional Courier")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize articles dictionary
        self.articles = {}

        # UI setup
        self.init_ui()

        # Load content
        self.load_constitution()
        self.populate_sidebar()

        # Apply Patriotic Dark Mode theme
        self.apply_patriotic_dark_mode()

    def init_ui(self):
        # Central widget layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Menu bar
        menu_bar = QMenuBar(self)
        about_menu = QMenu("&About", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)
        menu_bar.addMenu(about_menu)
        self.setMenuBar(menu_bar)

        # Splitter for sidebar and main content
        splitter = QSplitter(Qt.Horizontal)
        self.sidebar = QListWidget()
        self.sidebar.itemClicked.connect(self.sidebar_selection_changed)
        splitter.addWidget(self.sidebar)

        # Main content area
        main_content = QWidget()
        main_content_layout = QVBoxLayout(main_content)

        # Search box
        search_layout = QHBoxLayout()
        self.search_entry = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_text)
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(search_button)
        main_content_layout.addLayout(search_layout)

        # Text viewer
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        main_content_layout.addWidget(self.text_view)

        splitter.addWidget(main_content)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def apply_patriotic_dark_mode(self):
        # Patriotic Dark Mode color scheme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                selection-background-color: #ff0000;  /* Red for selected items */
                selection-color: #ffffff;               /* White for selected text */
            }
            QPushButton {
                background-color: #0044cc;              /* Blue for buttons */
                color: #ffffff;                          /* White for button text */
                border: 1px solid #ffffff;              /* Optional: white border */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0033aa;              /* Darker blue on hover */
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 5px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 5px;
            }
            QMenuBar {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QStatusBar {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 10px;
                margin: 22px 0 22px 0;
            }
            QScrollBar::handle:vertical {
                background: #ff0000; /* Red handle */
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

    def populate_sidebar(self):
        # Clear the sidebar
        self.sidebar.clear()

        # Add a general item for the whole constitution text
        all_text_item = QListWidgetItem("The U.S. Constitution")
        self.sidebar.addItem(all_text_item)

        # Add items for each article or amendment found in the constitution text
        for title in self.articles.keys():
            item = QListWidgetItem(title)
            self.sidebar.addItem(item)

    def load_constitution(self):
        # Load text file content
        file_path = os.path.join(os.path.dirname(__file__), "constitution.txt")
        try:
            with open(file_path, "r") as file:
                self.constitution_text = file.read()
        except FileNotFoundError:
            self.constitution_text = "Error: Constitution file not found."

        self.text_view.setPlainText(self.constitution_text)
        self.extract_articles()

    def extract_articles(self):
        # Extract articles and amendments from text
        lines = self.constitution_text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("Article") or "Amendment" in line:
                self.articles[line] = i
                self.sidebar.addItem(line)

    def show_about(self):
        # Display about information
        self.status_bar.showMessage("Constitutional Courier - United States Constitution Reader")

    def sidebar_selection_changed(self, item):
        selected_title = item.text()  # Get the title of the selected item
        if selected_title == "The U.S. Constitution":
            # If the user selects the entire constitution, display the full text
            self.text_view.setPlainText(self.constitution_text)
        else:
            # For articles or amendments, get the start index from self.articles
            start_index = self.articles[selected_title]
            snippet = self.get_snippet(start_index)
            self.text_view.setPlainText(snippet)

    def get_snippet(self, start_index):
        # Get snippet for selected article or amendment
        lines = self.constitution_text.splitlines()
        end_index = len(lines)
        for i in range(start_index + 1, len(lines)):
            if "Article" in lines[i] or "Amendment" in lines[i]:
                end_index = i
                break
        return "\n".join(lines[start_index:end_index])

    def search_text(self):
        search_text = self.search_entry.text()
        if search_text:
            self.highlight_search_results(search_text)

    def highlight_search_results(self, search_text):
        # Clear previous highlights
        cursor = self.text_view.textCursor()
        format = QTextCharFormat()
        format.setBackground(Qt.white)
        cursor.setPosition(0)
        cursor.mergeCharFormat(format)

        # Set highlight format
        format.setBackground(QColor("yellow"))
        regex = QRegExp(search_text, Qt.CaseInsensitive)

        matches = 0
        cursor.setPosition(0)
        while not cursor.isNull() and not cursor.atEnd():
            cursor = self.text_view.document().find(regex, cursor)
            if cursor.isNull():
                break
            cursor.mergeCharFormat(format)
            matches += 1

        # Update status bar with match count
        if matches > 0:
            self.status_bar.showMessage(f"{matches} results found for '{search_text}'")
        else:
            self.status_bar.showMessage("No results found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConstitutionalCourier()
    window.show()
    sys.exit(app.exec_())
