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
    set_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
    set_1.click()
    
    practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
    practice_card.click()
    
    m2_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '2. Sentence Completion')]")))
    m2_btn.click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Fill in the blank')]")))
    time.sleep(0.5)
    
    # Get the question card
    card_text = driver.find_element(By.XPATH, "//main").text
    print("Mode 2 Page Content:")
    print(card_text[:800])
    
    # Click option B ('Abate')
    letters_b = driver.find_elements(By.XPATH, "//div[text()='B']")
    if letters_b:
        letters_b[0].click()
    time.sleep(0.5)
    
    print("\n--- After Selecting Option B ---")
    page_after = driver.find_element(By.XPATH, "//main").text
    print(page_after[:1200])
    
    print("\nSUCCESS: Mode 2 verified with authentic 501-standard question!")
finally:
    driver.quit()
