from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Initialize the WebDriver with headless mode
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

try:
    # Open the BuzzBox login page
    browser.get("http://127.0.0.1:8000/login/")  # Ensure your server is running locally

    wait = WebDriverWait(browser, 30)  # Increase wait time to 30 seconds

    # Login
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username.send_keys("yashvin")  # Replace with your test username

    password = browser.find_element(By.NAME, "password")
    password.send_keys("8618776558")  # Replace with your test password
    password.send_keys(Keys.RETURN)

    # Wait for the redirection to the home page and check for a specific element
    try:
        home_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'BuzzBox')]")))
        print("Login test passed and redirected to the home page.")
        
        # Check for the correct title
        if browser.title == "Home":
            print("Page title after login is correct: Home")
        else:
            print(f"Page title after login is incorrect: {browser.title}")

    except EC.NoSuchElementException:
        print("Error: Home page element not found. Please check the XPath or page structure.")
    except AssertionError:
        print("Error: Page title did not match 'Home'.")

    # Debugging output
    print("Page title after login:", browser.title)
    print("Current URL after login:", browser.current_url)

finally:
    # Close the browser after some time
    time.sleep(15)
    browser.quit()
