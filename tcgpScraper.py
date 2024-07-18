from playwright.sync_api import sync_playwright
import csv
import re

SEARCH_TERM = "Frogmite - Duel Decks: Elspeth vs. Tezzeret"
START_URL = "https://www.tcgplayer.com/"
CSV_FILE = "cards_data.csv"

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Set", "Lowest Price", "Market Price"])
        for row in data:
            writer.writerow(row)

def scrape_tcgplayer():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        
        # 1. Load the TCGPlayer homepage
        print("Navigating to TCGPlayer homepage...")
        page.goto(START_URL)
        
        # 2. Enter the search term in the search box
        print(f"Entering search term: {SEARCH_TERM}...")
        page.wait_for_selector('#autocomplete-input')
        search_box = page.query_selector('#autocomplete-input')
        search_box.fill(SEARCH_TERM)
        page.keyboard.press("Enter")
        
        # 3. Click on the first search result
        print("Waiting for search results...")
        page.wait_for_selector('[data-testid="product-card__image--0"]')
        print("Clicking on the first search result...")
        page.click('[data-testid="product-card__image--0"]')
        
        # 4. Check for the "Show Filters" button
        print("Waiting for card page to load...")
        page.wait_for_timeout(1000)  # 1 second
        
        if page.query_selector('#showFilters'):
            print("Clicking to show filters...")
            page.click('#showFilters')
            
            # Apply necessary filters by clicking on labels
            print("Applying filters...")
            page.click('label[for="verified-seller-filter"]')
            page.click('label[for="Condition-LightlyPlayed-filter"]')
            page.click('label[for="ListingType-ListingsWithoutPhotos-filter"]')
            
            # Click the save button to apply filters
            print("Saving filters...")
            page.click('.filter-drawer-footer__button-save')
        else:
            # Apply necessary filters directly
            print("Applying filters directly...")
            page.click('label[for="verified-seller-filter"]')
            page.click('label[for="Condition-LightlyPlayed-filter"]')
            page.click('label[for="ListingType-ListingsWithoutPhotos-filter"]')
        
        # 5. Retrieve the price and shipping cost
        print("Waiting for filtered results...")
        page.wait_for_selector('section.spotlight__listing')
        
        print("Extracting price and shipping cost...")
        price_element = page.query_selector('section.spotlight__listing .spotlight__price')
        shipping_element = page.query_selector('section.spotlight__listing .spotlight__shipping')

        if price_element:
            price = float(price_element.inner_text().replace('$', ''))

            if "shipping:" in shipping_element.inner_text():
                shipping = 0.0
            else:
                shipping_text = shipping_element.inner_text().strip()
                shipping = float(re.sub(r'[^\d.]', '', shipping_text)) if shipping_text else 0.0
                
            total_price = price + shipping
            
            print(f"Price: ${price:.2f}")
            print(f"Shipping: ${shipping:.2f}")
            print(f"Total Price: ${total_price:.2f}")
        else:
            print("Price or shipping information not found.")

        page.wait_for_timeout(20000)  # 20 seconds
        browser.close()

if __name__ == "__main__":
    scrape_tcgplayer()
    print("Scraping completed.")
