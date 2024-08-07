from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver
browser = webdriver.Chrome()

try:
    # Open the BuzzBox login page
    browser.get("http://127.0.0.1:8000/login/")  # Ensure your server is running locally

    wait = WebDriverWait(browser, 15)

    # Login
    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username.send_keys("your_username")  # Replace with your test username

    password = browser.find_element(By.NAME, "password")
    password.send_keys("your_password")  # Replace with your test password
    password.send_keys(Keys.RETURN)

    # Wait for the redirection to the home page
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'BuzzBox')]")))

    print("Login test passed and redirected to the home page.")

finally:
    # Close the browser after some time
    time.sleep(5)
    browser.quit()
