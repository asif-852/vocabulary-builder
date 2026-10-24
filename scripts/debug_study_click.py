import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get('http://localhost:4173/')
set_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Set 1']")))
set_1.click()
time.sleep(0.5)

study_cards = driver.find_elements(By.XPATH, "//*[text()='1. Study']")
if study_cards:
    study_cards[0].click()
    time.sleep(1)
    print("Page text in Study View:\n", driver.find_element(By.TAG_NAME, 'body').text[:400])
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    print("\nButtons found in Study View:")
    for b in buttons:
        print("btn:", repr(b.text))

driver.quit()
