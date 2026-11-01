import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.makedirs('docs/screenshots', exist_ok=True)

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1200,820')
opts.add_argument('--force-device-scale-factor=1.5')

driver = webdriver.Chrome(options=opts)

def wait_and_click(xpath, delay=1.2):
    el = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", el)
    time.sleep(delay)

try:
    # 1. Home Dashboard (GRE 333)
    print("1. Capturing 01-home-dashboard.png...")
    driver.get('http://localhost:5173')
    time.sleep(2)
    driver.save_screenshot('docs/screenshots/01-home-dashboard.png')

    # 2. Word Smart 1 Corpus
    print("2. Capturing 02-word-smart-corpus.png...")
    wait_and_click("//button[contains(., 'Word Smart 1')]")
    driver.save_screenshot('docs/screenshots/02-word-smart-corpus.png')

    # 3. Click Set 1 of Word Smart 1
    print("3. Capturing 03-set-hub.png...")
    set_card = driver.find_elements(By.XPATH, "//div[contains(., 'Words 1–25') and contains(., 'Set 1')]")[-1]
    driver.execute_script("arguments[0].click();", set_card)
    time.sleep(1.5)
    driver.save_screenshot('docs/screenshots/03-set-hub.png')

    # 4. Enter Study Flashcard Mode
    print("4. Capturing 04-study-flashcard.png...")
    wait_and_click("//*[contains(text(), '1. Study')]/ancestor::div[contains(@style, 'cursor')][1]")
    driver.save_screenshot('docs/screenshots/04-study-flashcard.png')

    # Go back to Set Hub
    print("Navigating back to Set Hub...")
    wait_and_click("//button[contains(., 'Back to Set')]")

    # 5. Enter Practice Hub
    print("5. Capturing 05-practice-hub.png...")
    wait_and_click("//*[contains(text(), '2. Practice')]/ancestor::div[contains(@style, 'cursor')][1]")
    driver.save_screenshot('docs/screenshots/05-practice-hub.png')

    # 6. Sentence Completion Mode
    print("6. Capturing 06-sentence-completion.png...")
    wait_and_click("//*[contains(text(), 'Sentence Completion')]/ancestor::div[contains(@style, 'cursor')][1]")
    opt_btn = driver.find_elements(By.XPATH, "//button[contains(@style, 'text-align: left') or contains(@style, 'textAlign: left')]")
    if opt_btn:
        driver.execute_script("arguments[0].click();", opt_btn[0])
        time.sleep(1)
    driver.save_screenshot('docs/screenshots/06-sentence-completion.png')

    # Back to Practice Hub
    wait_and_click("//button[contains(., 'Practice Modes')]")

    # 7. Multi-Synonyms Mode
    print("7. Capturing 07-multi-synonyms.png...")
    wait_and_click("//*[contains(text(), 'Synonyms Finding (Multiple Options)')]/ancestor::div[contains(@style, 'cursor')][1]")
    cboxes = driver.find_elements(By.XPATH, "//div[contains(@style, 'cursor: pointer') and contains(@style, 'border')]")
    if len(cboxes) >= 2:
        driver.execute_script("arguments[0].click();", cboxes[0])
        driver.execute_script("arguments[0].click();", cboxes[1])
        time.sleep(0.5)
    driver.save_screenshot('docs/screenshots/07-multi-synonyms.png')

    # Back to Practice Hub
    wait_and_click("//button[contains(., 'Practice Modes')]")

    # 8. Find Meaning Mode
    print("8. Capturing 08-find-meaning.png...")
    wait_and_click("//*[contains(text(), 'Find the Meaning')]/ancestor::div[contains(@style, 'cursor')][1]")
    fm_btns = driver.find_elements(By.XPATH, "//button[contains(@style, 'text-align: left') or contains(@style, 'textAlign: left')]")
    if fm_btns:
        driver.execute_script("arguments[0].click();", fm_btns[0])
        time.sleep(1)
    driver.save_screenshot('docs/screenshots/08-find-meaning.png')

    # Back to Practice Hub
    wait_and_click("//button[contains(., 'Practice Modes')]")

    # 9. Antonym Finding Mode
    print("9. Capturing 09-antonym-drill.png...")
    wait_and_click("//*[contains(text(), 'Antonym Finding')]/ancestor::div[contains(@style, 'cursor')][1]")
    ant_btns = driver.find_elements(By.XPATH, "//button[contains(@style, 'text-align: left') or contains(@style, 'textAlign: left')]")
    if ant_btns:
        driver.execute_script("arguments[0].click();", ant_btns[0])
        time.sleep(1)
    driver.save_screenshot('docs/screenshots/09-antonym-drill.png')

    print("ALL 9 SCREENSHOTS CAPTURED WITH 100% SUCCESS!")

finally:
    driver.quit()
