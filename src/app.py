import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCompleter, QLabel, QHBoxLayout, QPushButton, QComboBox, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Ticker Selector")
        self.setGeometry(100, 100, 960, 580)

        self.ticker_list = []       # List to store selected tickers
        self.ticker_widgets = []    # List to store the ticker widgets for removal
        self.mediary = "default"
        self.mediary_list = ["Simulated", "Unsimulated"] # could add mediaries that require keys and other shit

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()  # Vertical layout for the overall window
        main_layout.setContentsMargins(20, 20, 20, 20)  # Padding around the layout
        main_layout.setSpacing(15)  # Space that is between widgets

        # THIS GUI ELEMENT IS FOR MANAGING TICKERS
        self.ticker_manager = QHBoxLayout() # Horizontal layout for search bar and stock label
        self.ticker_manager.setSpacing(10)  # Space between the search bar and the stock label
        self.ticker_manager.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)
        # Search bar for finding tickers
        self.ticker_search_bar = QLineEdit(self)
        self.ticker_search_bar.setPlaceholderText("Search Tickers...")
        self.ticker_search_bar.setMaximumWidth(300)
        # Search icon to the left of the ticker 
        search_icon = QIcon("src/assets/search-icon.svg")
        self.ticker_search_bar.addAction(search_icon, QLineEdit.LeadingPosition)
        # Add the search bar to the ticker manager layout
        # NOTE the ticker icons are added to the GUI in the add_ticker_to_list function
        self.ticker_manager.addWidget(self.ticker_search_bar)


        # GUI ELEMENT FOR MANAGING MEDIARIES
        self.mediary_manager = QHBoxLayout()
        self.mediary_manager.setSpacing(10)  # Space between the search bar and the stock label
        self.mediary_manager.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)
        # SEARCH for selecting the mediary
        self.mediary_search_bar = QLineEdit(self)
        self.mediary_search_bar.setPlaceholderText("Select Mediary...")
        self.mediary_search_bar.setMaximumWidth(300)
        # COMPLETER for selecting mediary
        completer = QCompleter(self.mediary_list, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)  # Show all items when the search bar is empty
        self.mediary_search_bar.setCompleter(completer)
        # ICON for selecting mediary
        search_icon = QIcon("src/assets/mediary-icon.svg")
        self.mediary_search_bar.addAction(search_icon, QLineEdit.LeadingPosition)
        self.mediary_manager.addWidget(self.mediary_search_bar)
        # INPUT for key depending on whether you use an actual honest to god mediary (you will lose money)
        self.mediary_key_input = QLineEdit(self)
        self.mediary_key_input.setPlaceholderText("Key...")
        self.mediary_key_input.setMaximumWidth(300)
        search_icon = QIcon("src/assets/key-icon.svg")
        self.mediary_key_input.addAction(search_icon, QLineEdit.LeadingPosition)
        self.mediary_manager.addWidget(self.mediary_key_input)

        # TODO GUI ELEMENT FOR MANAGING INTERVAL

        # TODO GUI ELEMENT FOR MANAGING DATES


        # Add each of the elements to the the windows main layout
        main_layout.addLayout(self.ticker_manager)
        main_layout.addLayout(self.mediary_manager)
        main_layout.addStretch()


        # Load stock data and set up the completer
        self.load_stock_data()

        # Set up the container widget
        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def load_stock_data(self):
        """Load stock data from a JSON file and set up the completer."""
        try:
            with open("src/stocks.json", "r") as file:
                data = json.load(file)

            # Extract tickers and set up completer
            tickers = [f"{stock['ticker']} : {stock['name']}" for stock in data]
            completer = QCompleter(tickers, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.ticker_search_bar.setCompleter(completer)

            self.ticker_search_bar.returnPressed.connect(self.add_ticker_to_list)

        except FileNotFoundError:
            self.ticker_search_bar.setPlaceholderText("stocks.json not found!")

    def add_ticker_to_list(self):
        """Add the selected ticker to the list and create a new stock shower."""
        ticker = self.ticker_search_bar.text()
        if ticker and ticker not in self.ticker_list:
            self.ticker_list.append(ticker)

            # Split the ticker from the full string (ticker: name)
            ticker_symbol = ticker.split()[0]  # Get the first part (ticker symbol)

            # Create a QWidget to hold both the label and the button
            stock_container = QWidget(self)
            stock_container.setFixedSize(QSize(60, 30))  # Set the container size

            # Create a new QLabel for the stock shower
            stock_shower = QLabel(ticker_symbol, stock_container, objectName="stockItem")
            stock_shower.setAlignment(Qt.AlignCenter)
            stock_shower.setGeometry(0, 0, 60, 30)  # Fill the container

            # Create a QPushButton and position it at the top-right of the container
            button = QPushButton("×", stock_container, objectName="stockItemDelete")
            button.setFixedSize(12, 12)  # Set button size
            button.move(48, 0)  # Position the button at top-right corner of the label (adjust as needed)

            # Connect the button click to remove the ticker
            button.clicked.connect(lambda: self.remove_ticker(stock_container, ticker))

            # Add the container (with label and button) to the layout
            self.ticker_manager.addWidget(stock_container)

            # Keep track of the widgets and tickers for removal
            self.ticker_widgets.append((stock_container, ticker))

        self.ticker_search_bar.clear()

    def remove_ticker(self, stock_container, ticker):
        """Remove the ticker from the list and the view."""
        if ticker in self.ticker_list:
            self.ticker_list.remove(ticker)

        # Remove the stock container widget from the layout
        stock_container.deleteLater()

        # Remove the ticker widget entry from the list of tracked widgets
        self.ticker_widgets = [widget for widget in self.ticker_widgets if widget[1] != ticker]


def load_stylesheet(file_path: str) -> str:
    """Load QSS stylesheet from the given file path."""
    with open(file_path, "r") as file:
        return file.read()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the stylesheet
    qss_path = "./src/style.qss"
    try:
        stylesheet = load_stylesheet(qss_path)
        app.setStyleSheet(stylesheet)
    except FileNotFoundError:
        print(f"Stylesheet file not found: {qss_path}")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
