from playwright.sync_api import sync_playwright
import csv

URL = "https://www.tcgplayer.com/search/magic/universes-beyond-assassin-s-creed?view=grid&productLineName=magic&setName=universes-beyond-assassin-s-creed"
CSV_FILE = "cards_data.csv"

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Set", "Lowest Price", "Market Price"])
        for row in data:
            writer.writerow(row)

def scrape_tcgplayer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL)
        
        card_data = []

        while True:
            # Wait for the card elements to load
            page.wait_for_selector('div.search-result__content')
            
            cards = page.query_selector_all('div.search-result__content')

            for card in cards:
                name_element = card.query_selector('span.product-card__title')
                set_element = card.query_selector('div.product-card__set-name__variant')
                lowest_price_element = card.query_selector('span.inventory__price-with-shipping')
                market_price_element = card.query_selector('span.product-card__market-price--value')

                if name_element and set_element and lowest_price_element and market_price_element:
                    name = name_element.inner_text()
                    set_name = set_element.inner_text()
                    lowest_price = lowest_price_element.inner_text().replace('$', '')
                    market_price = market_price_element.inner_text().replace('$', '')
                    
                    card_data.append([name, set_name, lowest_price, market_price])

            # Check if the "Next page" button is enabled
            next_button = page.query_selector('a[aria-label="Next page"]')
            if next_button and next_button.get_attribute('aria-disabled') == 'false':
                next_button.click()
                page.wait_for_timeout(3000)  # Wait for the next page to load
            else:
                break
        
        save_to_csv(card_data, CSV_FILE)
        browser.close()

if __name__ == "__main__":
    scrape_tcgplayer()
    print("Scraping completed. Data saved to", CSV_FILE)
