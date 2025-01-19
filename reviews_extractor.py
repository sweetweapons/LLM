import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_reviews(url):
    
    # Set up headless chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open the URL
    driver.get(url)
    time.sleep(3)  # Allow some time for the page to load

    reviews = []
    try:
        # Wait until the page loads
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # # Search for elements containing "review", "rating", "feedback" etc.
        # possible_review_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'review') or contains(@class, 'rating') or contains(@class, 'feedback')]")
        
        # for review_element in possible_review_elements:
        #     review_text = review_element.text  # or review_element.get_attribute('textContent')
        #     reviews.append(review_text)
        #     print(reviews)



        # # If no elements found, print a message
        # if not possible_review_elements:
        #     print("No review-related elements found. Trying different methods...")
        #     possible_review_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'review') or contains(text(), 'rating') or contains(text(), 'feedback')]")
        
#new code 
        reviews_data = {
        "reviews_count": 0,
        "reviews": []
        }
        possible_review_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'star') or contains(text(), 'rating') or contains(text(), 'review') or contains(text(), 'out of')]")

        if not possible_review_elements:
            possible_review_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'review') or contains(@class, 'comment') or contains(@class, 'feedback') or contains(@class, 'content')]")

        if not possible_review_elements:
            possible_review_elements = driver.find_elements(By.XPATH, "//div | //span | //p | //article")
        
        reviews_data["reviews_count"] = len(possible_review_elements)




        # Iterate through possible review elements
        for element in possible_review_elements:
            try:
                # Extract review details dynamically (modify based on actual structure)
                title = element.find_element(By.XPATH, ".//h3").text if element.find_elements(By.XPATH, ".//h3") else "No title"
                body = element.text  # Can extract specific parts if necessary
                reviews.append({
                    'title': title,
                    'body': body
                })
            except Exception as e:
                print(f"Error while extracting review: {e}")
                
    except Exception as e:
        print(f"Error while loading the page: {e}")
    finally:
        driver.quit()

    return reviews

# Example usage
if __name__ == "__main__":
    url = input("Enter product page URL: ")
    reviews = extract_reviews(url)
    
    if reviews:
        print("Reviews extracted:")
        for review in reviews:
            print(review)
    else:
        print("No reviews found.")
