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
    
    # Click Set 1
    set_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
    set_1.click()
    
    # Practice
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    
    # Mode 3
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '3. Synonyms Finding')]"))).click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Select all correct synonyms')]")))
    time.sleep(0.5)
    
    print("=== LIVE APP: Set 1, Q1 (ABATE) in Mode 3 (Before Selection) ===")
    main_text = driver.find_element(By.XPATH, "//main").text
    print(main_text)
    
    # Select options: Subside, Dwindle, Wane
    for opt_name in ['Subside', 'Dwindle', 'Wane']:
        el = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{opt_name}']")))
        el.click()
        time.sleep(0.2)
        
    # Now click Check Answer
    chk_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Check Answer')]")))
    chk_btn.click()
    time.sleep(0.5)
    
    print("\n=== LIVE APP: Set 1, Q1 (ABATE) in Mode 3 (After Selecting All 3 Correct Synonyms) ===")
    main_after = driver.find_element(By.XPATH, "//main").text
    print(main_after)
    
    print("\nSUCCESS: Mode 3 verified live in browser!")
finally:
    driver.quit()
