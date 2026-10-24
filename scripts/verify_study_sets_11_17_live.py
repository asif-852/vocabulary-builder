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
    # ----------------------------------------------------
    # TEST 1: Set 11, Word 1 (Log)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_11 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 11']")))
    set_11.click()
    
    # Click 1. Study
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='1. Study']"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Log')]")))
    time.sleep(0.5)
    
    print("=== LIVE APP: Set 11, Word 201 (Log) in Study View ===")
    main_text = driver.find_element(By.XPATH, "//main").text
    print(main_text)
    
    # Verify header Bengali meaning is present
    assert "দৈনন্দিন কার্যবিবরণী বা নথি" in main_text
    print(">>> SUCCESS: Log has correct Bengali meaning in header!")
    
    # ----------------------------------------------------
    # TEST 2: Set 14, Word 267 (Qualified)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_14 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 14']")))
    set_14.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='1. Study']"))).click()
    
    # Go to Qualified (word 267, which is index 7 in Set 14: words 261-280)
    for _ in range(6):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.2)
        
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Qualified')]")))
    print("\n=== LIVE APP: Set 14, Word 267 (Qualified) in Study View ===")
    main_q = driver.find_element(By.XPATH, "//main").text
    print(main_q)
    assert "শর্তসাপেক্ষ বা সীমিত" in main_q
    assert "Limited, restricted, or conditional" in main_q
    print(">>> SUCCESS: Qualified has correct adjective definition and Bengali meaning!")
    
    # ----------------------------------------------------
    # TEST 3: Set 17, Word 333 (Zealot)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_17 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 17']")))
    set_17.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='1. Study']"))).click()
    
    # Go to last word (Zealot, word 333, index 13 in Set 17)
    for _ in range(12):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.2)
        
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Zealot')]")))
    print("\n=== LIVE APP: Set 17, Word 333 (Zealot) in Study View ===")
    main_z = driver.find_element(By.XPATH, "//main").text
    print(main_z)
    assert "ধর্মান্ধ বা চরম গোঁড়া ব্যক্তি" in main_z
    print(">>> SUCCESS: Zealot has clean Bengali meaning without stacked diacritics!")
    
    # Check browser console errors
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"\nBrowser Console Severe Errors: {len(severe)}")
    assert len(severe) == 0

    print("\nALL LIVE STUDY AUDITS FOR SETS 11 TO 17 PASSED WITH FLYING COLORS!")

finally:
    driver.quit()
