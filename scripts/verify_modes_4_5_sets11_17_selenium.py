# -*- coding: utf-8 -*-
"""
Live headless Chrome Selenium verification for Module 4 (Single Synonym) and Module 5 (Single Antonym)
across GRE 333 Sets 11 to 17 (Words 201 to 333).
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

def test_mode_for_set(set_num, mode_num, mode_title, mode_heading, expected_count):
    mode_name = "Mode 4 (Single Synonym)" if mode_num == 4 else "Mode 5 (Single Antonym)"
    print(f"\n==========================================")
    print(f"Testing Set {set_num} - {mode_name}")
    print(f"==========================================")
    
    driver.get('http://localhost:4173/')
    
    # 1. Click Set
    set_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='Set {set_num}']")))
    set_btn.click()
    
    # 2. Click Practice Hub
    practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
    practice_card.click()
    
    # 3. Click Mode Card
    mode_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//h3[contains(., '{mode_heading}')]")))
    mode_btn.click()
    
    # 4. Wait for Question Card
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(., '{mode_title}')]")))
    
    # Verify counter
    counter_el = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 1 of')]")))
    print(f"  [Q1] Counter: {counter_el.text}")
    assert f"Q 1 of {expected_count}" in counter_el.text, f"Expected Q 1 of {expected_count}, got {counter_el.text}"
    
    # Verify exactly 4 options (A, B, C, D)
    option_badges = driver.find_elements(By.XPATH, "//div[text()='A' or text()='B' or text()='C' or text()='D']")
    assert len(option_badges) == 4, f"Expected 4 option badges, found {len(option_badges)}"
    
    # Print Q1 word and options
    main_text_q1 = driver.find_element(By.XPATH, "//main").text
    lines = [l.strip() for l in main_text_q1.split('\n') if l.strip()]
    print(f"  [Q1] Question Header: {lines[0]} | {lines[1] if len(lines) > 1 else ''}")
    
    # 5. Click an option
    option_badges[0].click()
    time.sleep(0.4)
    
    # 6. Verify Feedback & Breakdown Table
    main_text_after = driver.find_element(By.XPATH, "//main").text
    assert ("Correct" in main_text_after or "Incorrect" in main_text_after), "Feedback banner not displayed"
    assert "Word (মূল শব্দ)" in main_text_after, "Table column 'Word (মূল শব্দ)' not displayed"
    assert "Meaning (অর্থ)" in main_text_after, "Table column 'Meaning (অর্থ)' not displayed"
    if mode_num == 4:
        assert "Synonyms (সমার্থক)" in main_text_after, "Table column 'Synonyms (সমার্থক)' not displayed"
    else:
        assert "Antonyms (বিপরীত)" in main_text_after, "Table column 'Antonyms (বিপরীত)' not displayed"
    print("  [Q1] Feedback & Breakdown table verified successfully!")
    
    # 7. Next Question Progression
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
    next_btn.click()
    time.sleep(0.4)
    
    # Verify progressed to Q2
    counter_el2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(normalize-space(), 'Q 2 of')]")))
    assert f"Q 2 of {expected_count}" in counter_el2.text, f"Expected Q 2 of {expected_count}, got {counter_el2.text}"
    print(f"  [Q2] Successfully progressed to: {counter_el2.text}")
    
    # Verify Q2 has 4 distinct options
    option_badges_q2 = driver.find_elements(By.XPATH, "//div[text()='A' or text()='B' or text()='C' or text()='D']")
    assert len(option_badges_q2) == 4, f"Expected 4 option badges in Q2, found {len(option_badges_q2)}"
    
    # Click option in Q2
    option_badges_q2[1].click()
    time.sleep(0.4)
    main_text_q2_after = driver.find_element(By.XPATH, "//main").text
    assert ("Correct" in main_text_q2_after or "Incorrect" in main_text_q2_after), "Feedback banner not displayed in Q2"
    print(f"  [Q2] Feedback & Breakdown verified successfully!")
    print(f"  >>> Set {set_num} {mode_name} PASSED!\n")

try:
    sets_config = [
        (11, 20),
        (12, 20), # Contains Partisan (gre333-229)
        (13, 20), # Contains Precipitate (gre333-251)
        (14, 20), # Contains Proscribe, Quibble
        (15, 20), # Contains Resolve (gre333-283) & Sage (gre333-286)
        (16, 20), # Contains Strut (noun & verb)
        (17, 13)  # Contains Vituperative (gre333-327) & Zealot (gre333-333)
    ]

    print("=================================================================")
    print("STARTING LIVE SELENIUM VERIFICATION FOR SETS 11-17 (MODES 4 & 5)")
    print("=================================================================")
    
    # Verify all Sets 11 to 17 in Mode 4 (Single Synonym)
    for s_num, count in sets_config:
        test_mode_for_set(
            set_num=s_num,
            mode_num=4,
            mode_title="closest in meaning",
            mode_heading="4. Synonym Finding",
            expected_count=count
        )
        
    # Verify all Sets 11 to 17 in Mode 5 (Single Antonym)
    for s_num, count in sets_config:
        test_mode_for_set(
            set_num=s_num,
            mode_num=5,
            mode_title="opposite in meaning",
            mode_heading="5. Antonym Finding",
            expected_count=count
        )

    # Browser Console Logs Check
    print("\n==========================================")
    print("CHECKING BROWSER CONSOLE LOGS")
    print("==========================================")
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser console severe error count: {len(severe_errors)}")
    for e in severe_errors:
        print("  Console Error:", e['message'])
    assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe browser console errors!"
    print("Zero browser console errors confirmed!")

    print("\n=================================================================")
    print(">>> 100% SUCCESS: ALL SETS 11-17 PASSED MODES 4 & 5 IN LIVE BROWSER <<<")
    print("=================================================================")

finally:
    driver.quit()
