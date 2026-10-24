# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import sys

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # Go to app
    page.goto("http://localhost:4173")
    page.wait_for_selector("text=GRE 333")
    
    # Click Set 1
    page.click("text=Set 1")
    page.wait_for_selector("text=Practice This Set")
    
    # Click Practice This Set
    page.click("text=Practice This Set")
    page.wait_for_selector("text=Sentence Completion")
    
    # Click Sentence Completion
    page.click("text=Sentence Completion")
    page.wait_for_selector("button:has-text('Check Answer')")
    
    # Get sentence text
    sentence = page.locator(".font-serif").first.inner_text()
    print("Mode 2 Sentence (Set 1 Word 1):")
    print(sentence)
    
    # Get options
    options = page.locator("button[role='radio']").all_inner_texts()
    print("Options:", options)
    
    # Click correct option 'Abate'
    page.click("button:has-text('Abate')")
    page.click("button:has-text('Check Answer')")
    
    # Verify post-answer explanation and translation
    page.wait_for_selector("text=Sentence Translation")
    translation = page.locator("text=Sentence Translation").locator("..").inner_text()
    print("\nPost-Answer Translation Box:")
    print(translation)
    
    browser.close()
    print("\nVisual verification test completed successfully!")
