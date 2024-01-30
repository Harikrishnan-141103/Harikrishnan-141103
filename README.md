import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_product_page(url):
    try:
        # Send a GET request to the provided link
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for urgency indicators (e.g., words like "hurry", "limited time", etc.)
        urgency_indicators = ["hurry", "limited time", "last chance", "bought in past month", "Order within"]
        urgency_flag = any(indicator in soup.get_text().lower() for indicator in urgency_indicators)
        
        # Check for price drop (e.g., comparing current price with previous price)
        try:
            current_price = float(soup.find('span', class_='current-price').get_text().replace('₹', '').replace(',', ''))  # Replace 'current-price' with the actual class/id of the current price element
        except (AttributeError, ValueError):
            current_price = None
        try:
            previous_price = float(soup.find('span', class_='previous-price').get_text().replace('₹', '').replace(',', ''))  # Replace 'previous-price' with the actual class/id of the previous price element
        except (AttributeError, ValueError):
            previous_price = None
        price_drop_flag = current_price is not None and previous_price is not None and current_price < previous_price
        
        # Check for elements indicative of a sneaky basket
        sneaky_basket_patterns = ['basket-sneak', 'hidden-basket', 'stealth-basket']
        sneaky_basket_flag = any(pattern in soup.get_text().lower() for pattern in sneaky_basket_patterns)
        
        # Check for misleading product information (e.g., false claims)
        misleading_info_patterns = ['limited stock', 'Top Brand', 'exclusive offer', 'best deal ever']
        misleading_info_flag = any(pattern in soup.get_text().lower() for pattern in misleading_info_patterns)

        return urgency_flag, price_drop_flag, sneaky_basket_flag, misleading_info_flag
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return False, False, False, False

# Example usage:
product_url = "https://www.amazon.in/Rajah-Ayurveda-Neelibhringadi-Keram-Growth/dp/B078HSLFHV/ref=sr_1_4?crid=38VZO0NBT9LMX&keywords=no+free+delivery+products&qid=1706593168&sprefix=no+free+delevery+products+%2Caps%2C231&sr=8-4"
urgency, price_drop, sneaky_basket, misleading_info = check_product_page(product_url)

print("Urgency:", urgency)
print("Price Drop:", price_drop)
print("Sneaky Basket:", sneaky_basket)
print("Misleading Product Info:", misleading_info)

