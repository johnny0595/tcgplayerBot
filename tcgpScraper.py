import tkinter as tk
from playwright.sync_api import sync_playwright
import re

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCGPlayer Price Scraper")

        self.label = tk.Label(root, text="Enter search term:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.condition_label = tk.Label(root, text="Select condition:")
        self.condition_label.pack(pady=5)

        self.condition_var = tk.StringVar(root)
        self.condition_var.set("Lightly Played")  # default value

        self.conditions = {
            "Lightly Played": "Condition-LightlyPlayed-filter",
            "Near Mint": "Condition-NearMint-filter",
            "Moderately Played": "Condition-ModeratelyPlayed-filter",
            "Damaged": "Condition-Damaged-filter",
            "Heavily Played": "Condition-HeavilyPlayed-filter"
        }

        self.condition_dropdown = tk.OptionMenu(root, self.condition_var, *self.conditions.keys())
        self.condition_dropdown.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit", command=self.store_data)
        self.submit_button.pack(pady=5)

        self.result_label = tk.Label(root, text="Stored data will appear here:")
        self.result_label.pack(pady=5)

        self.result_box = tk.Text(root, height=10, width=50)
        self.result_box.pack(pady=5)

        self.stored_data = ""

    def store_data(self):
        self.stored_data = self.entry.get()
        self.selected_condition = self.condition_var.get()
        self.result_label.config(text=f"Stored data: {self.stored_data} (Condition: {self.selected_condition})")
        self.execute_event()

    def execute_event(self):
        if self.stored_data:
            condition_filter = self.conditions[self.selected_condition]
            result = self.scrape_tcgplayer(self.stored_data, condition_filter)
            self.result_box.insert(tk.END, f"Results for {self.stored_data} (Condition: {self.selected_condition}):\n{result}\n\n")
        else:
            self.result_box.insert(tk.END, "No data to execute event.\n")

    def scrape_tcgplayer(self, search_term, condition_filter):
        START_URL = "https://www.tcgplayer.com/"

        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()

            # Load the TCGPlayer homepage
            page.goto(START_URL)
            
            # Enter the search term in the search box
            page.wait_for_selector('#autocomplete-input')
            search_box = page.query_selector('#autocomplete-input')
            search_box.fill(search_term)
            page.keyboard.press("Enter")
            
            # Click on the first search result
            page.wait_for_selector('[data-testid="product-card__image--0"]')
            page.click('[data-testid="product-card__image--0"]')
            
            # Wait for the card page to load
            page.wait_for_timeout(1000)  # 1 second
            
            if page.query_selector('#showFilters'):
                page.click('#showFilters')
                
                # Apply necessary filters by clicking on labels
                page.wait_for_selector('label[for="verified-seller-filter"]')
                page.click('label[for="verified-seller-filter"]')
                
                # Debugging: Check if the condition filter is present
                print(f"Checking condition filter: {condition_filter}")
                condition_element = page.query_selector(f'label[for="{condition_filter}"]')
                if condition_element:
                    print("Condition filter found, executing JavaScript to click...")
                    page.evaluate(f'document.querySelector("label[for=\'{condition_filter}\']").click()')
                    page.wait_for_timeout(500)  # Wait for 0.5 seconds to ensure click registers
                else:
                    print("Condition filter not found.")
                
                page.wait_for_selector('label[for="ListingType-ListingsWithoutPhotos-filter"]')
                page.click('label[for="ListingType-ListingsWithoutPhotos-filter"]')
                
                # Click the save button to apply filters
                page.wait_for_selector('.filter-drawer-footer__button-save')
                page.click('.filter-drawer-footer__button-save')
            else:
                # Apply necessary filters directly
                page.wait_for_selector('label[for="verified-seller-filter"]')
                page.click('label[for="verified-seller-filter"]')
                
                # Debugging: Check if the condition filter is present
                print(f"Checking condition filter: {condition_filter}")
                condition_element = page.query_selector(f'label[for="{condition_filter}"]')
                if condition_element:
                    print("Condition filter found, executing JavaScript to click...")
                    page.evaluate(f'document.querySelector("label[for=\'{condition_filter}\']").click()')
                    page.wait_for_timeout(500)  # Wait for 0.5 seconds to ensure click registers
                else:
                    print("Condition filter not found.")
                
                page.wait_for_selector('label[for="ListingType-ListingsWithoutPhotos-filter"]')
                page.click('label[for="ListingType-ListingsWithoutPhotos-filter"]')
            
            # Retrieve the price and shipping cost
            page.wait_for_selector('section.spotlight__listing')
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
                result = f"Price: ${price:.2f}\nShipping: ${shipping:.2f}\nTotal Price: ${total_price:.2f}"
            else:
                result = "Price or shipping information not found."

            browser.close()
        
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
