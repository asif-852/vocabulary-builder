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
    # 1. Test Set 10 Q1 (Innocuous)
    driver.get('http://localhost:4173/')
    set_10 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 10']")))
    set_10.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '3. Synonyms Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Select all correct synonyms')]")))
    time.sleep(0.5)
    
    print("=== LIVE APP: Set 10, Q1 (INNOCUOUS) in Mode 3 ===")
    main_text = driver.find_element(By.XPATH, "//main").text
    print(main_text)
    
    # Click 3 options to inspect explanation
    for opt_name in ['Harmless', 'Safe', 'Inoffensive']:
        el = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{opt_name}']")))
        el.click()
        time.sleep(0.2)
        
    chk_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Check Answer')]")))
    chk_btn.click()
    time.sleep(0.5)
    
    print("\n=== LIVE APP: Set 10, Q1 (INNOCUOUS) After Check Answer ===")
    print(driver.find_element(By.XPATH, "//main").text)

    # 2. Test Set 2 Q2 (Appease)
    driver.get('http://localhost:4173/')
    set_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 2']")))
    set_2.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '3. Synonyms Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Select all correct synonyms')]")))
    
    # Go to Q2 (Appease)
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
    next_btn.click()
    time.sleep(0.5)
    
    print("\n=== LIVE APP: Set 2, Q2 (APPEASE) in Mode 3 ===")
    print(driver.find_element(By.XPATH, "//main").text)
    
    for opt_name in ['Pacify', 'Placate', 'Propitiate']:
        el = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{opt_name}']")))
        el.click()
        time.sleep(0.2)
        
    chk_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Check Answer')]")))
    chk_btn.click()
    time.sleep(0.5)
    
    print("\n=== LIVE APP: Set 2, Q2 (APPEASE) After Check Answer ===")
    print(driver.find_element(By.XPATH, "//main").text)

finally:
    driver.quit()
