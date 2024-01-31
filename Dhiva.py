import requests 

from bs4 import BeautifulSoup 

import nltk 

from nltk.sentiment.vader import SentimentIntensityAnalyzer 

from selenium import webdriver 

from selenium.webdriver.support.ui import WebDriverWait 

from selenium.webdriver.support import expected_conditions as EC 

from selenium.webdriver.common.by import By 

 

def detect_subscription_trickery(website_url): 

    # Send a GET request to the website URL 

    response = requests.get(website_url) 

    if response.status_code == 200: 

        # Parse the HTML content 

        soup = BeautifulSoup(response.content, 'html.parser') 

        # Look for elements indicating subscription trickery 

        subscription_keywords = ["cancel subscription", "unsubscribe", "manage subscription", "billing information"] 

        for keyword in subscription_keywords: 

            if soup.find(text=keyword): 

                return True 

    return False 

 

def evaluate_user_choice_limitation(website_url): 

    try: 

        # Send a GET request to the website URL 

        response = requests.get(website_url) 

        response.raise_for_status()  # Raise an exception for non-200 status codes 

        # Parse the HTML content 

        soup = BeautifulSoup(response.content, 'html.parser') 

        # Extract relevant elements 

        product_recommendations = soup.find_all(class_="product-recommendation")  # Example class for product recommendations 

        search_bar = soup.find(id="search-bar")  # Example ID for search bar 

        checkout_button = soup.find(class_="checkout-button")  # Example class for checkout button 

        # Evaluate user choice limitation based on the presence of specific elements 

        user_choice_limitation_score = 0 

        if product_recommendations: 

            user_choice_limitation_score += 1 

        if search_bar: 

            user_choice_limitation_score += 1 

        if checkout_button: 

            user_choice_limitation_score += 1 

        return user_choice_limitation_score 

    except requests.exceptions.RequestException as e: 

        print("Failed to retrieve website content for evaluation:", e) 

        return None 

 

def detect_subscription_trap(product_url): 

    try: 

        # Send a GET request to the product URL 

        response = requests.get(product_url) 

        response.raise_for_status()  # Raise an exception for non-200 status codes 

        # Parse the HTML content 

        soup = BeautifulSoup(response.content, 'html.parser') 

        # Look for subscription-related element 

        subscription_keywords = ["subscription", "premium", "recurring payment", "cancel anytime"] 

        for keyword in subscription_keywords: 

            if keyword in soup.get_text().lower(): 

                return True 

        return False 

    except requests.exceptions.RequestException as e: 

        print("Failed to retrieve product content for evaluation:", e) 

        return None 

 

def detect_forced_account_creation(website_url): 

    # Send a GET request to the website URL 

    response = requests.get(website_url) 

    if response.status_code == 200: 

        # Parse the HTML content 

        soup = BeautifulSoup(response.content, 'html.parser') 

        # Look for elements indicating forced account creation 

        account_creation_keywords = ["create account", "register", "sign up"] 

        for keyword in account_creation_keywords: 

            if soup.find(text=keyword): 

                return True 

    return False 

 

def detect_dark_patterns_in_reviews(website_url): 

    # Send a GET request to the website URL 

    response = requests.get(website_url) 

    if response.status_code == 200: 

        # Parse the HTML content 

        soup = BeautifulSoup(response.content, 'html.parser') 

        # Extract user reviews from the webpage 

        user_reviews = soup.find_all(class_="user-review") 

        if not user_reviews: 

            return False  # No user reviews found 

        # Initialize sentiment analyzer 

        nltk.download('vader_lexicon') 

        sid = SentimentIntensityAnalyzer() 

        # Analyze each user review for potential dark patterns 

        for review in user_reviews: 

            review_text = review.get_text() 

            # Perform sentiment analysis on the review text 

            sentiment_score = sid.polarity_scores(review_text)['compound'] 

            # Check if sentiment score is significantly positive or negative 

            if sentiment_score > 0.5 or sentiment_score < -0.5: 

                return True  # Suspicious review detected 

        return False  # No suspicious reviews found 

    return False  # Failed to retrieve webpage content 

 

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

            current_price = float(soup.find('span', class_='current-price').get_text().replace('₹', '').replace(',', ''))  # Replace 'current-price' with the actual class/id of the current price element 

        except (AttributeError, ValueError): 

            current_price = None 

        try: 

            previous_price = float(soup.find('span', class_='previous-price').get_text().replace('₹', '').replace(',', ''))  # Replace 'previous-price' with the actual class/id of the previous price element 

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

 

 
