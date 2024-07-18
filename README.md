# TCGPlayer Price Scraper

This application is a GUI tool for scraping card prices from TCGPlayer using Python and the Playwright library. The tool allows users to input a search term for a card, select its condition from a dropdown menu, and then retrieve the lowest price and shipping cost from TCGPlayer.

## Features

- **Search Term Input**: Users can enter the card name and set they want to search for.
- **Condition Selection**: Users can select the card's condition from a dropdown menu (Lightly Played, Near Mint, Moderately Played, Damaged, Heavily Played).
- **Price and Shipping Information**: The tool retrieves and displays the lowest price, shipping cost, and total price of the card.
- **Graphical User Interface (GUI)**: The application provides a simple and intuitive GUI for easy interaction.

## Prerequisites

- **Python 3.x**: Ensure you have Python 3 installed on your machine.
- **Playwright**: The Playwright library for web scraping.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd tcgplayer-price-scraper
    ```

2. **Install the required Python packages**:
    ```sh
    pip install playwright tkinter
    playwright install
    ```

## Usage

1. **Run the application**:
    ```sh
    python tcgplayer_scraper.py
    ```

2. **Enter the search term**:
    - In the GUI, enter the card name and set you want to search for in the "Enter search term" input box.

3. **Select the card condition**:
    - Use the dropdown menu to select the condition of the card (Lightly Played, Near Mint, Moderately Played, Damaged, Heavily Played).

4. **Submit and retrieve prices**:
    - Click the "Submit" button to initiate the scraping process. The lowest price, shipping cost, and total price will be displayed in the text box below.

## Code Overview

### Main Components

1. **GUI Setup**: The Tkinter library is used to create the GUI components such as labels, entry boxes, buttons, and a dropdown menu.
2. **Web Scraping**: The Playwright library is used to automate browser interactions and scrape data from the TCGPlayer website.
3. **Event Handling**: The `store_data` and `execute_event` methods handle the input data and trigger the scraping process.

### Key Files

- **tcgplayer_scraper.py**: The main script containing the GUI and scraping logic.

## Troubleshooting

- **Element Not Found**: If the script cannot find a specific element, ensure the TCGPlayer page structure has not changed. Adjust the selectors in the script if necessary.
- **Dependencies**: Ensure all required Python packages are installed. If you encounter issues with Playwright, try reinstalling it and running `playwright install` again.

## Example Output

```
Results for 542925 (Condition: Lightly Played):
Price: $0.16
Shipping: $1.27
Total Price: $1.43
```

---