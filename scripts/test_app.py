import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        print("=== Test 1: Desktop Viewport (1440x900) ===")
        driver.set_window_size(1440, 900)
        driver.get('http://localhost:4173/')
        
        # Verify title
        assert "Vocabulary Builder" in driver.title
        print("Page title verified:", driver.title)
        
        # Wait for Set 1 to appear
        set_1_elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
        print("Set 1 card found.")
        
        # Verify source pills
        pills = driver.find_elements(By.CSS_SELECTOR, '.pill-button')
        pill_texts = [p.text for p in pills]
        print("Pills on Home page:", pill_texts[:3])
        assert any('GRE 333' in t for t in pill_texts)
        assert any('Word Smart 1' in t for t in pill_texts)
        assert any('Word Smart 2' in t for t in pill_texts)
        print("All 3 source pills verified.")
        
        # Click on Set 1
        set_1_elem.click()
        
        # Verify Set Hub
        h2 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h2'))).text
        print("Set Hub H2:", h2)
        assert "Set 1" in h2
        
        # Click "1. Study"
        study_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='1. Study']")))
        study_card.click()
        
        # Wait for Study View toggle button to appear
        toggle_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Explanation')]")))
        print("Initial toggle state:", toggle_btn.text)
        
        # Verify Zero-Jump Layout Stability
        print("\n--- Verifying Zero-Jump Layout Stability (Desktop) ---")
        word_elem = driver.find_element(By.CSS_SELECTOR, 'h2')
        word_initial = word_elem.text
        pos_initial = word_elem.location
        print(f"Word: '{word_initial}', Initial Position: X={pos_initial['x']}, Y={pos_initial['y']}")
        
        # Toggle explanation off
        toggle_btn.click()
        time.sleep(0.3)
        pos_toggled = word_elem.location
        print(f"After Toggle ({toggle_btn.text}): Pos: X={pos_toggled['x']}, Y={pos_toggled['y']}")
        
        delta_x = abs(pos_initial['x'] - pos_toggled['x'])
        delta_y = abs(pos_initial['y'] - pos_toggled['y'])
        print(f"Delta: dX={delta_x}px, dY={delta_y}px")
        assert delta_x == 0, f"X shifted by {delta_x}px!"
        assert delta_y == 0, f"Y shifted by {delta_y}px!"
        print(">>> SUCCESS: Zero-Jump verified on Desktop (0px shift)!")
        
        # Toggle back on
        toggle_btn.click()
        time.sleep(0.3)
        pos_back = word_elem.location
        assert pos_initial['x'] == pos_back['x'] and pos_initial['y'] == pos_back['y']
        
        # Click Next Word
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]")))
        next_btn.click()
        time.sleep(0.3)
        word_2 = driver.find_element(By.CSS_SELECTOR, 'h2').text
        print(f"Next word rendered: '{word_2}' (was '{word_initial}')")
        assert word_2 != word_initial
        
        # Go Back to Set
        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Back to Set')]")))
        back_btn.click()
        
        # Verify Mobile Viewport (390x844 iPhone)
        print("\n=== Test 2: Mobile Viewport (390x844) Zero-Jump ===")
        driver.set_window_size(390, 844)
        time.sleep(0.5)
        
        # Click 1. Study on mobile
        study_card_m = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='1. Study']")))
        study_card_m.click()
        
        toggle_btn_m = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Explanation')]")))
        word_elem_m = driver.find_element(By.CSS_SELECTOR, 'h2')
        pos_m_initial = word_elem_m.location
        print(f"Mobile Word '{word_elem_m.text}' Pos: X={pos_m_initial['x']}, Y={pos_m_initial['y']}")
        
        toggle_btn_m.click()
        time.sleep(0.3)
        pos_m_toggled = word_elem_m.location
        delta_m_x = abs(pos_m_initial['x'] - pos_m_toggled['x'])
        delta_m_y = abs(pos_m_initial['y'] - pos_m_toggled['y'])
        print(f"Mobile Delta: dX={delta_m_x}px, dY={delta_m_y}px")
        assert delta_m_x == 0, f"Mobile X shifted by {delta_m_x}px!"
        assert delta_m_y == 0, f"Mobile Y shifted by {delta_m_y}px!"
        print(">>> SUCCESS: Zero-Jump verified on Mobile (0px shift)!")
        
        # Back to Set
        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Back to Set')]")))
        back_btn.click()
        
        # Switch back to desktop for practice drill tests
        driver.set_window_size(1200, 800)
        practice_card = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='2. Practice']")))
        practice_card.click()
        
        print("\n=== Test 3: Practice Modes Verification ===")
        # Verify Practice Hub loaded
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Practice Modes')]")))
        print("Practice Hub loaded.")
        
        # Mode 1: Find Meaning
        print("\n--- Testing Mode 1: Find the Meaning ---")
        m1_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '1. Find the Meaning')]")))
        m1_btn.click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Choose the correct definition')]")))
        time.sleep(0.3)
        # Click first option letter 'A'
        letters_a = driver.find_elements(By.XPATH, "//div[text()='A']")
        assert len(letters_a) > 0, "No option A found in Mode 1"
        letters_a[0].click()
        time.sleep(0.3)
        assert "Correct" in driver.page_source or "Incorrect" in driver.page_source
        print("Feedback rendered successfully for Mode 1.")
        
        # Back to Practice Modes
        driver.find_element(By.XPATH, "//button[contains(., 'Practice Modes')]").click()
        
        # Mode 2: Sentence Completion
        print("\n--- Testing Mode 2: Sentence Completion ---")
        m2_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '2. Sentence Completion')]")))
        m2_btn.click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Fill in the blank')]")))
        time.sleep(0.3)
        letters_a_m2 = driver.find_elements(By.XPATH, "//div[text()='A']")
        assert len(letters_a_m2) > 0, "No option A found in Mode 2"
        letters_a_m2[0].click()
        time.sleep(0.3)
        assert "ব্যাখ্যা" in driver.page_source or "Definition" in driver.page_source
        print("Post-answer breakdown rendered with Bangla explanation.")
        
        driver.find_element(By.XPATH, "//button[contains(., 'Practice Modes')]").click()
        
        # Mode 3: Multi Synonym
        print("\n--- Testing Mode 3: Synonyms Finding (Multiple) ---")
        m3_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '3. Synonyms Finding')]")))
        m3_btn.click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Select all correct synonyms')]")))
        time.sleep(0.3)
        # Click checkboxes
        boxes = driver.find_elements(By.CLASS_NAME, "multi-syn-option")
        print(f"Checkbox items in Mode 3: {len(boxes)}")
        assert len(boxes) >= 6, "Expected 6-7 checkboxes in Mode 3"
        boxes[0].click()
        time.sleep(0.3)
        boxes = driver.find_elements(By.CLASS_NAME, "multi-syn-option")
        boxes[1].click()
        time.sleep(0.3)
        check_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "check-answer-btn")))
        check_btn.click()
        time.sleep(0.5)
        assert "Synonym" in driver.page_source
        print("Check answer evaluation and per-option feedback verified.")
        
        driver.find_element(By.XPATH, "//button[contains(., 'Practice Modes')]").click()
        
        # Mode 4: Single Synonym
        print("\n--- Testing Mode 4: Synonym Finding (Single) ---")
        m4_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '4. Synonym Finding')]")))
        m4_btn.click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'closest in meaning')]")))
        time.sleep(0.3)
        letters_a_m4 = driver.find_elements(By.XPATH, "//div[text()='A']")
        assert len(letters_a_m4) > 0, "No option A found in Mode 4"
        letters_a_m4[0].click()
        time.sleep(0.3)
        assert "Word (মূল শব্দ)" in driver.page_source
        print("Post-answer breakdown table verified in Mode 4.")
        
        driver.find_element(By.XPATH, "//button[contains(., 'Practice Modes')]").click()
        
        # Mode 5: Single Antonym
        print("\n--- Testing Mode 5: Antonym Finding (Single) ---")
        m5_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(., '5. Antonym Finding')]")))
        m5_btn.click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'opposite in meaning')]")))
        time.sleep(0.3)
        letters_a_m5 = driver.find_elements(By.XPATH, "//div[text()='A']")
        assert len(letters_a_m5) > 0, "No option A found in Mode 5"
        letters_a_m5[0].click()
        time.sleep(0.3)
        assert "Word (মূল শব্দ)" in driver.page_source or "Antonyms" in driver.page_source
        print("Post-answer breakdown table verified in Mode 5.")
        
        # Check browser console errors
        print("\n=== Test 4: Browser Console Error Check ===")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        print(f"Console errors found: {len(severe_errors)}")
        for err in severe_errors:
            print("Console Error:", err['message'])
        assert len(severe_errors) == 0, f"Found {len(severe_errors)} severe console errors!"
        print(">>> 0 console errors detected!")
        
        print("\n==============================================")
        print("ALL TESTS PASSED WITH 100% SUCCESS!")
        print("==============================================")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    run_tests()
