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
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 900)
wait = WebDriverWait(driver, 10)

def check_console_errors(stage_name):
    logs = driver.get_log('browser')
    severe_errors = [log for log in logs if log['level'] == 'SEVERE']
    if severe_errors:
        print(f"!!! SEVERE Console Errors at {stage_name}:")
        for err in severe_errors:
            print(f"    {err['message']}")
        raise AssertionError(f"Console errors detected at {stage_name}")
    else:
        print(f"[{stage_name}] Zero browser console errors (Clean).")

try:
    print("================================================================================")
    print("STARTING LIVE HEADLESS SELENIUM AUDIT: MODULE 1 (SETS 11 TO 17)")
    print("================================================================================")

    sets_to_test = [11, 12, 13, 14, 15, 16, 17]

    for s in sets_to_test:
        expected_total = 13 if s == 17 else 20
        print(f"\n>>> TESTING SET {s} (Expected {expected_total} words)...")

        driver.get('http://localhost:4173/')
        
        # Click on Set card
        set_elem = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='Set {s}']")))
        set_elem.click()
        
        # Click 2. Practice
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
        
        # Click 1. Find the Meaning
        wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]"))).click()
        
        # Verify Question 1 header
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Choose the correct definition')]")))
        header_text = driver.find_element(By.XPATH, "//main").text
        
        assert f"Set {s}: Find the Meaning" in header_text, f"Missing Set {s} title"
        assert f"Q 1 of {expected_total}" in header_text, f"Expected Q 1 of {expected_total}"
        assert "Score: 0" in header_text, "Expected initial Score: 0"
        
        # Verify exactly 4 options rendered
        opt_letters = ['A', 'B', 'C', 'D']
        for l in opt_letters:
            assert driver.find_elements(By.XPATH, f"//main//*[text()='{l}']"), f"Option letter {l} not found"
            
        check_console_errors(f"Set {s} Q1 Initial Load")
        
        # Click option A
        opt_a = driver.find_element(By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]")
        opt_a.click()
        time.sleep(0.3)
        
        # Verify feedback card appeared
        feedback = driver.find_elements(By.XPATH, "//*[contains(., 'Correct!') or contains(., 'Incorrect.')]")
        assert len(feedback) > 0, f"Feedback card did not appear for Set {s} Q1"
        assert "বাংলা অর্থ:" in driver.find_element(By.XPATH, "//main").text, f"Missing Bangla meaning in feedback for Set {s} Q1"
        
        # Click Next
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
        next_btn.click()
        time.sleep(0.3)
        
        assert f"Q 2 of {expected_total}" in driver.find_element(By.XPATH, "//main").text, f"Failed to advance to Q 2 in Set {s}"
        print(f"Set {s}: Successfully verified Q1 -> Answer -> Feedback -> Q2 navigation.")

    # -------------------------------------------------------------------------
    # DEEP VERIFICATION OF TARGETED WORDS
    # -------------------------------------------------------------------------
    print("\n--------------------------------------------------------------------------------")
    print("TARGETED DEEP VERIFICATIONS: WORDS 201, 245, 250, 288, 333")
    print("--------------------------------------------------------------------------------")

    # TEST A: Set 11, Word 201 (Log)
    driver.get('http://localhost:4173/')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 11']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='LOG']")))
    main_text = driver.find_element(By.XPATH, "//main").text
    assert "LOG" in main_text
    print("\n[Word 201: Log] Loaded correctly:")
    print("Prompt text preview:\n", main_text[:200])

    # TEST B: Set 13, Word 245 (Plethora) -> Q5 of Set 13
    driver.get('http://localhost:4173/')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 13']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]"))).click()
    
    # Advance to Q5 (Plethora is word 245 = index 4 in set 13)
    for q in range(4):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
        time.sleep(0.1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.1)
        
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='PLETHORA']")))
    print("\n[Word 245: Plethora] Reached question card. Answering...")
    # Click option
    wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
    time.sleep(0.3)
    plethora_text = driver.find_element(By.XPATH, "//main").text
    assert "অতিপ্রাচুর্য" in plethora_text, f"Expected clean 'অতিপ্রাচুর্য' in Plethora feedback, got:\n{plethora_text}"
    print(">>> SUCCESS: Word 245 (Plethora) displays pristine 'অতিপ্রাচুর্য' in feedback!")

    # TEST C: Set 13, Word 250 (Precarious) -> Q10 of Set 13
    for q in range(5):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
        time.sleep(0.1)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='PRECARIOUS']")))
    print("\n[Word 250: Precarious] Reached question card. Feedback text:")
    precarious_text = driver.find_element(By.XPATH, "//main").text
    assert "অনির্ভরযোগ্য" in precarious_text, f"Expected clean 'অনির্ভরযোগ্য' in Precarious feedback, got:\n{precarious_text}"
    print(">>> SUCCESS: Word 250 (Precarious) displays pristine 'অনির্ভরযোগ্য' in feedback!")

    # TEST D: Set 15, Word 288 (Sanction) -> Q8 of Set 15
    driver.get('http://localhost:4173/')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 15']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]"))).click()
    
    # Sanction is word 288 = index 7 in set 15 (words 281-300)
    for q in range(7):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
        time.sleep(0.1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.1)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='SANCTION']")))
    print("\n[Word 288: Sanction] Reached question card. Inspecting options:")
    sanction_card = driver.find_element(By.XPATH, "//main")
    card_lines = [line for line in sanction_card.text.split('\n') if line.strip()]
    print("Sanction Card Text:\n", "\n".join(card_lines))
    
    # Find options texts
    opt_divs = driver.find_elements(By.XPATH, "//main//div[contains(@style, 'border: 1.5px solid')]")
    assert len(opt_divs) == 4, f"Expected 4 options for Sanction, got {len(opt_divs)}"
    
    # Check that all options are VERB definitions (start with 'To ')
    for i, opt_div in enumerate(opt_divs):
        letter = ['A', 'B', 'C', 'D'][i]
        text_content = opt_div.text
        # Split letter from definition
        def_text = text_content.replace(letter, '').strip()
        print(f"  Option {letter}: {def_text}")
        assert def_text.startswith("To "), f"Option {letter} for verb Sanction does not start with 'To ': '{def_text}'"

    # Click the correct option for Sanction
    correct_opt = driver.find_element(By.XPATH, "//main//*[contains(text(), 'To give official permission or approval')]")
    correct_opt.click()
    time.sleep(0.3)
    
    sanction_after = driver.find_element(By.XPATH, "//main").text
    assert "Correct!" in sanction_after, "Failed to mark Sanction correct answer"
    assert "Score:" in sanction_after, f"Expected Score present, got {sanction_after}"
    print(">>> SUCCESS: Word 288 (Sanction) has 4 perfectly matched verb options and evaluates cleanly!")

    # TEST E: Set 17, Word 333 (Zealot) -> Final word of GRE 333!
    driver.get('http://localhost:4173/')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 17']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]"))).click()
    
    # Zealot is word 333 = index 12 in set 17 (words 321-333 = 13 words)
    for q in range(12):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
        time.sleep(0.1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))).click()
        time.sleep(0.1)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='ZEALOT']")))
    zealot_text = driver.find_element(By.XPATH, "//main").text
    assert "Q 13 of 13" in zealot_text, f"Expected Q 13 of 13 for Zealot, got {zealot_text}"
    print("\n[Word 333: Zealot] Final question in GRE 333 reached successfully:")
    print("Zealot card preview:\n", zealot_text[:200])

    # Answer Zealot
    wait.until(EC.element_to_be_clickable((By.XPATH, "//main//*[text()='A']/ancestor::div[contains(@style, 'border')]"))).click()
    time.sleep(0.2)
    # Check that Next button now says "Finish Drill"
    finish_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finish Drill')]")))
    finish_btn.click()
    time.sleep(0.5)

    # Check completion view
    completion_text = driver.find_element(By.XPATH, "//main").text
    assert "Find the Meaning Complete!" in completion_text, f"Expected completion view, got:\n{completion_text}"
    print(">>> SUCCESS: Final Set 17 drill completion view rendered flawlessly!")

    # Check browser logs at end of full run
    check_console_errors("End of Full Test Run")

    print("\n================================================================================")
    print("ALL 7 SETS (11 TO 17) & TARGET CHECKS PASSED LIVE IN HEADLESS CHROME WITH 0 ERRORS!")
    print("================================================================================")

finally:
    driver.quit()
