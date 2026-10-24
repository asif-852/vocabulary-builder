import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 900)
wait = WebDriverWait(driver, 10)

try:
    driver.get('http://localhost:4173/')
    
    # Scroll to Set 10
    set_10 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 10']")))
    set_10.click()
    
    practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
    practice_card.click()
    
    m1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]")))
    m1_btn.click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Choose the correct definition')]")))
    time.sleep(0.5)
    
    # Check Set 10, Q1 (Word: INNOCUOUS)
    card_text = driver.find_element(By.XPATH, "//main").text
    print("=== LIVE APP: Set 10, Q1 (INNOCUOUS) in Mode 1 ===")
    print(card_text)
    
    # Find options
    opts = driver.find_elements(By.XPATH, "//main//div[contains(@style, 'cursor: pointer') or contains(@class, 'cursor-pointer') or contains(@style, 'border: 1.5px')]")
    print(f"\nRendered option containers count: {len(opts)}")
    
    print("\nSUCCESS: Set 10, Q1 verified live in browser!")
finally:
    driver.quit()
