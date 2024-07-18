# TCGPlayer Price Scraper

  

This Python script automates the process of scraping card prices from TCGPlayer.com based on input from a CSV file. It's designed to be faster and more efficient than previous GUI-based versions.

  
## Features

  

- Reads card information from a CSV file

- Automatically builds URLs with appropriate filters

- Scrapes prices, shipping costs, and total costs from TCGPlayer

- Updates the CSV file with the scraped information

- Handles various card conditions and printing types

- Applies the "Verified Seller" filter automatically

  

## Requirements

  

- Python 3.6+

- pandas

- playwright

  

## Installation

  

1. Ensure you have Python 3.6 or higher installed on your system.

2. Install the required libraries:

  

```

pip install pandas playwright

```

  

3. Install the Playwright browsers:

  

```

playwright install

```

  
## CSV File Format

The input CSV file should be formatted as follows:

| Product ID | Listing Type | Condition | Printing | Price | Shipping | Total |
|------------|--------------|-----------|----------|-------|----------|-------|
| 123456     | Without Photos | Near Mint | 1st Edition Holofoil |  |  |  |
| 234567     | With Photos | Lightly Played | Unlimited Holofoil |  |  |  |
### Column Details:

1. **Product ID**: 
   - Must be a 5 or 6-digit number
   - Example: 123456

2. **Listing Type**: 
   - Use exactly one of these two options:
     - "Without Photos"
     - "With Photos"

3. **Condition**: 
   - Use exactly one of these options:
     - "Near Mint"
     - "Lightly Played"
     - "Moderately Played"
     - "Heavily Played"
     - "Damaged"

4. **Printing**: 
   - Common options include:
     - "1st Edition Holofoil"
     - "Unlimited Holofoil"
     - "Normal"
     - "Foil"
     - "Holofoil"
   - For other printing types, use the exact term from TCGPlayer, with each word capitalized and separated by spaces
   - Example: "Reverse Holofoil"

5. **Price**, **Shipping**, **Total**: 
   - They will be filled by the script and overridden if not blank.


## Usage

1. Prepare your input CSV file as described above.

2. Update the `csv_file` variable in the script with the path to your CSV file (line 7):

```python

csv_file = '/path/to/your/cards.csv'

```
An example cards.csv file is included. I recommend using that.
  

3. Run the script:

  

```

python tcgplayer_scraper.py

```

  

4. The script will process each card in the CSV file, scrape the pricing information, and update the CSV with the results.

  

## Notes

- The script uses headless browsing for faster performance. Setting headless=False (on line 69) allows you to see what the the bot is doing in the browser.

- It automatically handles the "Verified Seller" filter.

- If a product ID is not 5-6 digits, the script will skip that card and leave the price fields blank.

- If no listings are available for a card, the script will fill in "N/A" for the price fields.

- The script prints the URL and scraped information for each card, allowing you to verify the applied filters.

- Ensure there are no typos in the column names or data entries

- On my computer it processes each card/product in around 3 seconds.

- Verify that "Listing Type", "Condition", and "Printing" match the options exactly as listed above

- If a specific filter doesn't apply to a card, you can leave that cell blank