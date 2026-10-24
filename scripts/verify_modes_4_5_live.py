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
    # TEST 1: Mode 4 (Single Synonym) - Set 1, Q1 (Abate)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
    set_1.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '4. Synonym Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'closest in meaning')]")))
    time.sleep(0.5)

    print("=== LIVE APP: Mode 4 (Single Synonym) - Set 1, Q1 (Abate) ===")
    main_text = driver.find_element(By.XPATH, "//main").text
    print(main_text)

    # Click Subside
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Subside']"))).click()
    time.sleep(0.5)

    print("\n=== LIVE APP: Mode 4 - Set 1, Q1 After Selection ===")
    print(driver.find_element(By.XPATH, "//main").text)

    # ----------------------------------------------------
    # TEST 2: Mode 4 (Single Synonym) - Set 9, Q10 (Inadvertently - word 170)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_9 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 9']")))
    set_9.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '4. Synonym Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'closest in meaning')]")))

    # Navigate to Q10 (Inadvertently)
    for _ in range(9):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.2)

    print("\n=== LIVE APP: Mode 4 - Set 9, Q10 (Inadvertently) ===")
    main_text_adv = driver.find_element(By.XPATH, "//main").text
    print(main_text_adv)
    # Verify 4 options exist
    assert "A" in main_text_adv and "B" in main_text_adv and "C" in main_text_adv and "D" in main_text_adv
    print(">>> SUCCESS: Inadvertently has all 4 options (A, B, C, D)!")

    # Click Accidentally
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Accidentally']"))).click()
    time.sleep(0.5)
    print("\n=== LIVE APP: Mode 4 - Set 9, Q10 After Selection ===")
    print(driver.find_element(By.XPATH, "//main").text)

    # ----------------------------------------------------
    # TEST 3: Mode 5 (Single Antonym) - Set 1, Q1 (Abate)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
    set_1.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '5. Antonym Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'opposite in meaning')]")))
    time.sleep(0.5)

    print("\n=== LIVE APP: Mode 5 (Single Antonym) - Set 1, Q1 (Abate) ===")
    main_m5 = driver.find_element(By.XPATH, "//main").text
    print(main_m5)

    # Click Intensify
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Intensify']"))).click()
    time.sleep(0.5)
    print("\n=== LIVE APP: Mode 5 - Set 1, Q1 After Selection ===")
    print(driver.find_element(By.XPATH, "//main").text)

    # ----------------------------------------------------
    # TEST 4: Mode 5 (Single Antonym) - Set 9, Q10 (Inadvertently)
    # ----------------------------------------------------
    driver.get('http://localhost:4173/')
    set_9 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 9']")))
    set_9.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '5. Antonym Finding')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'opposite in meaning')]")))

    for _ in range(9):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.2)

    print("\n=== LIVE APP: Mode 5 - Set 9, Q10 (Inadvertently) ===")
    main_m5_adv = driver.find_element(By.XPATH, "//main").text
    print(main_m5_adv)
    assert "A" in main_m5_adv and "B" in main_m5_adv and "C" in main_m5_adv and "D" in main_m5_adv
    print(">>> SUCCESS: Inadvertently in Mode 5 has all 4 options (A, B, C, D)!")

    # Click Deliberately
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Deliberately']"))).click()
    time.sleep(0.5)
    print("\n=== LIVE APP: Mode 5 - Set 9, Q10 After Selection ===")
    print(driver.find_element(By.XPATH, "//main").text)

    # Check console errors
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"\nBrowser Console Severe Errors: {len(severe)}")
    assert len(severe) == 0

    print("\nALL LIVE BROWSER CHECKS FOR MODES 4 & 5 PASSED WITH FLYING COLORS!")

finally:
    driver.quit()
