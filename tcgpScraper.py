import re
import pandas as pd
from math import floor
from playwright.sync_api import sync_playwright

# Read the CSV file
csv_file = '/Users/jonathanduran-ortiz/Developer/Scripts/tcgplayerBot/cards.csv'
df = pd.read_csv(csv_file, delimiter=',')

# Function to build the URL based on the CSV row data
def build_url(row):
    base_url = f"https://www.tcgplayer.com/product/{row['Product ID']}?Language=English&page=1"
    filters = []
    if row['Listing Type'] == "Without Photos":
        filters.append("ListingType=standard")
    elif row['Listing Type'] == "With Photos":
        filters.append("ListingType=custom")
    
    condition_mapping = {
        "Lightly Played": "Lightly+Played",
        "Near Mint": "Near+Mint",
        "Moderately Played": "Moderately+Played",
        "Damaged": "Damaged",
        "Heavily Played": "Heavily+Played"
    }
    
    if row['Condition'] in condition_mapping:
        filters.append(f"Condition={condition_mapping[row['Condition']]}")

    if row['Printing']:
        filters.append(f"Printing={row['Printing'].replace(' ', '+')}")

    url = base_url + "&" + "&".join(filters)
    return url

# Function to extract price and shipping cost from the page
def extract_price_and_shipping(page, row):
    try:
        if page.query_selector('text="No Listings Available"'):
            print(f"No listings available for Product ID {row['Product ID']}")
            return "N/A", "N/A", "N/A"

        # Extract price
        price_element = page.query_selector('section.spotlight__listing .spotlight__price')
        price_text = price_element.inner_text().strip()
        # Remove commas from price string
        price_text = re.sub(',', '', price_text)
        price = float(price_text.replace('$', ''))

        # Extract shipping cost
        shipping_element = page.query_selector('section.spotlight__listing .spotlight__shipping')
        shipping_text = shipping_element.inner_text().strip()
        if "$50" in shipping_text or "shipping:" in shipping_text:
            shipping = 0.0
        else:
            shipping_text = re.sub(r'[^\d.]', '', shipping_text)
            shipping = float(f"{float(shipping_text):.2f}") if shipping_text else 0.0
        
        # Round down the shipping cost before adding

        total_price = price + shipping

        return f"{price:.2f}", f"{shipping:.2f}", f"{total_price:.2f}"
    except Exception as e:
        print(f"Error extracting price and shipping: {e}")
        return None, None, None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for index, row in df.iterrows():
        if len(str(row['Product ID'])) < 5 or len(str(row['Product ID'])) > 6:
            print(f"Skipping row {index} due to invalid Product ID: {row['Product ID']}")
            df.at[index, 'Price'] = ""
            df.at[index, 'Shipping'] = ""
            df.at[index, 'Total'] = ""
            continue
        
        url = build_url(row)
        page.goto(url)
        print(f"Navigating to: {url}")

        # Wait for the card page to load
        page.wait_for_selector('body')

        # Check if the verified seller filter is already applied
        verified_seller_checked = page.is_checked('label[for="verified-seller-filter"] input[type="checkbox"]')
        if not verified_seller_checked:
            if page.query_selector('#showFilters'):
                page.click('#showFilters')
                page.wait_for_selector('label[for="verified-seller-filter"]')
                page.click('label[for="verified-seller-filter"]')
                page.wait_for_selector('.filter-drawer-footer__button-save')
                page.click('.filter-drawer-footer__button-save')
            else:
                if page.query_selector('label[for="verified-seller-filter"]'):
                    page.click('label[for="verified-seller-filter"]')

        page.wait_for_timeout(1000)

        price, shipping, total = extract_price_and_shipping(page, row)
        
        df.at[index, 'Price'] = price if price is not None else "N/A"
        df.at[index, 'Shipping'] = shipping if shipping is not None else "N/A"
        df.at[index, 'Total'] = total if total is not None else "N/A"
        
        print(f"Price: {price}, Shipping: {shipping}, Total: {total}")
    
    browser.close()

# Save the updated DataFrame back to CSV
df.to_csv(csv_file, index=False)
