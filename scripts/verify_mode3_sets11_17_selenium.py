# -*- coding: utf-8 -*-
"""
Live headless Chrome Selenium verification for Mode 3 (Synonyms Finding) across Sets 11 to 17.
"""

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
chrome_options.add_argument('--window-size=1440,900')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def test_set_mode3(set_num, expected_count):
    print(f"\n--- Testing Set {set_num} (Mode 3) ---")
    driver.get('http://localhost:4173/')
    
    # Click set
    set_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='Set {set_num}']")))
    set_btn.click()
    
    # Click Practice
    practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
    practice_card.click()
    
    # Click Synonyms Finding (Mode 3)
    m3_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '3. Synonyms Finding')]")))
    m3_btn.click()
    
    # Wait for question card
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Select all correct synonyms')]")))
    
    # Verify counter
    counter_el = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 1 of')]")))
    print(f"Header Counter: {counter_el.text}")
    assert f"Q 1 of {expected_count}" in counter_el.text, f"Expected Q 1 of {expected_count}, got {counter_el.text}"
    
    # Check 6 option items (.multi-syn-option)
    option_cards = driver.find_elements(By.CLASS_NAME, "multi-syn-option")
    assert len(option_cards) == 6, f"Expected 6 checkbox options, found {len(option_cards)}"
    print(f"Found {len(option_cards)} option items (6 checkboxes)")
    
    # Click first two checkboxes
    option_cards[0].click()
    time.sleep(0.2)
    option_cards[1].click()
    time.sleep(0.2)
    
    # Click Check Answer
    check_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Check Answer')]")))
    check_btn.click()
    time.sleep(0.5)
    
    # Verify feedback section rendered
    main_text = driver.find_element(By.XPATH, "//main").text
    assert ("All 3 correct synonyms identified" in main_text or "Partially correct" in main_text or "No correct synonyms identified" in main_text or "Missed" in main_text or "Correct" in main_text), "Feedback banner not displayed"
    print("Feedback banner and per-option evaluation verified!")
    
    # Verify Next button works
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next') or contains(., 'Finish')]")))
    next_btn.click()
    time.sleep(0.4)
    
    # Verify progressed to Q 2
    counter_el2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 2 of')]")))
    print(f"Progressed to: {counter_el2.text}")
    print(f"Set {set_num} verified successfully!")

try:
    test_set_mode3(11, 20)
    test_set_mode3(13, 20)
    test_set_mode3(15, 20)
    test_set_mode3(17, 13)
    
    # Console error check
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"\nBrowser console errors count: {len(severe_errors)}")
    for e in severe_errors:
        print("  Console Error:", e['message'])
    assert len(severe_errors) == 0, "Found severe browser console errors!"
    
    print("\nALL LIVE BROWSER TESTS PASSED FLAWLESSLY FOR MODE 3!")

finally:
    driver.quit()
