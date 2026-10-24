# -*- coding: utf-8 -*-
"""
Live headless Chrome Selenium verification for Mode 2 (Sentence Completion) across Sets 11 to 17.
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

def test_set_mode2(set_num, expected_count):
    print(f"\n--- Testing Set {set_num} (Mode 2) ---")
    driver.get('http://localhost:4173/')
    
    # Click set
    set_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='Set {set_num}']")))
    set_btn.click()
    
    # Click Practice
    practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
    practice_card.click()
    
    # Click Sentence Completion
    m2_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '2. Sentence Completion')]")))
    m2_btn.click()
    
    # Wait for question card
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Fill in the blank')]")))
    
    # Wait for option A to be visible
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text()='A']")))
    
    # Verify counter
    counter_el = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 1 of')]")))
    print(f"Header Counter: {counter_el.text}")
    assert f"Q 1 of {expected_count}" in counter_el.text, f"Expected Q 1 of {expected_count}, got {counter_el.text}"
    
    # Check 5 option elements (A, B, C, D, E)
    option_letters = driver.find_elements(By.XPATH, "//div[text()='A' or text()='B' or text()='C' or text()='D' or text()='E']")
    assert len(option_letters) == 5, f"Expected 5 option letters, found {len(option_letters)}"
    print(f"Found {len(option_letters)} option badges (A-E)")
    
    # Click first option badge/row
    option_letters[0].click()
    time.sleep(0.5)
    
    # Verify feedback section rendered
    main_text = driver.find_element(By.XPATH, "//main").text
    assert ("Correct" in main_text or "Incorrect" in main_text), "Feedback banner not displayed"
    assert "ব্যাখ্যা" in main_text, "Option meanings breakdown (ব্যাখ্যা) not displayed"
    assert "Definition:" in main_text, "Definition not displayed"
    assert "বঙ্গানুবাদ:" in main_text, "Sentence translation (বঙ্গানুবাদ) not displayed"
    print("Feedback, option breakdown, definition, and বঙ্গানুবাদ verified!")
    
    # Verify Next button works
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next') or contains(., 'Finish')]")))
    next_btn.click()
    time.sleep(0.5)
    
    # Verify progressed to Q 2
    counter_el2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 2 of')]")))
    print(f"Progressed to: {counter_el2.text}")
    print(f"Set {set_num} verified successfully!")

try:
    # Test sample sets: 11, 14, 15, 17
    test_set_mode2(11, 20)
    test_set_mode2(14, 20)
    test_set_mode2(15, 20)
    test_set_mode2(17, 13)
    
    # Console error check
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"\nBrowser console errors count: {len(severe_errors)}")
    for e in severe_errors:
        print("  Console Error:", e['message'])
    assert len(severe_errors) == 0, "Found severe browser console errors!"
    
    print("\nALL LIVE BROWSER TESTS PASSED FLAWLESSLY FOR MODE 2!")

finally:
    driver.quit()
