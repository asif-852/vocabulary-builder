from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:4173/')

e1 = driver.find_elements(By.XPATH, "//span[normalize-space()='Set 1']")
e2 = driver.find_elements(By.XPATH, "//*[contains(text(), 'Set 1')]")
print('normalize-space count:', len(e1))
print('contains count:', len(e2))
for e in e2:
    print('tag:', e.tag_name, 'text:', repr(e.text))
driver.quit()
